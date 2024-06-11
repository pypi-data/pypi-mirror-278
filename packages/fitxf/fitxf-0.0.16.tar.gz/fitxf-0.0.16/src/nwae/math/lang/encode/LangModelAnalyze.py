import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import re
from nwae.math.lang.encode.LangModelAnalyzeData import LmAnalyzeData
from nwae.math.lang import IntentCluster, LangModelPt
from nwae.math.lang.classify.TxtClassifyDense import TxtClassifyDense
from nwae.utils.Environ import Env
from nwae.math.utils.EnvironRepo import EnvRepo
import logging
from nwae.math.utils.Logging import Logging
from nwae.utils.Pandas import Pandas


#
# The accuracy of measurement depends on the language model, if it was trained to
#    - optimize cosine similarity (distance far away and k-means cluster gives bad results)
#    - optimize distance similarity (means k-means cluster gives good results)
#    - optimize via some other metric causing only very localized similarities, thus
#      cluster tests can never work
# For example "xlm-roberta-base" will give weaker results for clustering test, but better
# results when testing similarity by angle.
# However, the differences are usually small & it usually makes no difference which metric
# you use when doing intent detection.
#
class LmAnalyze:

    # Standardized labels [0, 1, 2, ...]
    COL_CLASS = LmAnalyzeData.COL_CLASS

    def __init__(
            self,
            lang_tgt,
            lang_data = 'en',
            # Train in target or original data language ('en')
            lang_train = None,
            # contains columns
            #    - "class" (standardized from 0 to n)
            #    - "label" (arbitrary human labeling)
            #    - "text"
            train_csvpath = None,
            validate_csvpath = None,
            csv_colmap = None,
            lm_model_name = None,
            lm_cache_dir = None,
            nlp_data_cache_dir = None,
            model_cache_dir = None,
            predict_via_model_compression = False,
            logger = None,
    ):
        self.lang_tgt = lang_tgt
        self.lang_data = lang_data
        self.lang_train = lang_train if lang_train is not None else self.lang_tgt
        assert self.lang_train in (self.lang_tgt, self.lang_data,), \
                'Language to be trained in "' + str(self.lang_train) + '" not valid'
        self.train_csvpath = train_csvpath
        self.validate_csvpath = validate_csvpath
        self.csv_colmap = csv_colmap if csv_colmap is not None else {}
        self.lm_model_name = lm_model_name
        self.lm_cache_dir = lm_cache_dir if lm_cache_dir is not None else Env.get_home_download_dir()
        self.nlp_data_cache_dir = nlp_data_cache_dir if nlp_data_cache_dir is not None else Env.get_home_download_dir()
        self.model_cache_dir = model_cache_dir if model_cache_dir is not None else Env.get_home_download_dir()
        self.predict_via_model_compression = predict_via_model_compression
        self.logger = logger if logger is not None else logging.getLogger()

        # To train we have option to use either the translated text or original text
        self.csvcol_text_train = LmAnalyzeData.COL_TEXT_ORIGINAL if self.lang_train in (self.lang_data,) \
            else LmAnalyzeData.COL_TEXT_TRANSLATED
        # Valuation always uses the translated column
        self.csvcol_text_val = LmAnalyzeData.COL_TEXT_TRANSLATED
        self.csvcol_label = self.csv_colmap.get(LmAnalyzeData.COL_LABEL, LmAnalyzeData.COL_LABEL)

        self.logger.info(
            'Data lang "' + str(self.lang_data) + '", target lang "' + str(self.lang_tgt)
            + '", text train column "' + str(self.csvcol_text_train)
            + '", text valuation column "' + str(self.csvcol_text_val) + '"'
        )

        self.df_train = LmAnalyzeData(
            lang_data = self.lang_data,
            lang_tgt = self.lang_tgt,
            label_text_csvpath = self.train_csvpath,
            cache_dir = self.nlp_data_cache_dir,
            match_phrase = {LmAnalyzeData.COL_TYPE: 'trn'},
            csv_colmap = self.csv_colmap,
            logger = self.logger,
        ).get_data()

        self.df_val = LmAnalyzeData(
            lang_data = self.lang_data,
            lang_tgt = self.lang_tgt,
            label_text_csvpath = self.validate_csvpath,
            cache_dir = self.nlp_data_cache_dir,
            match_phrase = {LmAnalyzeData.COL_TYPE: 'val'},
            csv_colmap = self.csv_colmap,
            logger = self.logger,
        ).get_data()

        self.lm = LangModelPt.get_singleton(
            LmClass      = LangModelPt,
            lang         = self.lang_tgt,
            model_name   = self.lm_model_name,
            cache_folder = self.lm_cache_dir,
            logger       = self.logger,
        )
        # Lang model inside TxtClassifyCluster must be same as self.lm model or make sure to
        # pass in "custom_text_encoding" in params_other during train()
        self.intent_cluster = IntentCluster(
            lang               = self.lang_tgt,
            model_name         = str(self.__class__.__name__) + '-' + str(IntentCluster.__name__),
            lm_cache_folder    = self.lm_cache_dir,
            lm_model_name      = self.lm_model_name,
            logger             = self.logger,
        )
        self.intent_simple = TxtClassifyDense(
            lang               = self.lang_tgt,
            model_name         = str(self.__class__.__name__) + '-' + str(TxtClassifyDense.__name__),
            lm_cache_folder    = self.lm_cache_dir,
            lm_model_name      = self.lm_model_name,
            logger             = self.logger,
            params_other       = {},
        )
        return

    def sample_dataframe_rows(
            self,
            df,
            retain_ratio,
    ):
        len_df = len(df)
        self.logger.debug('Original len = ' + str(len_df))
        keep_ratio = np.random.uniform(low=0., high=1., size=len_df) < retain_ratio
        df_sampled = df[keep_ratio].reset_index(drop=True)
        self.logger.debug('After sampling len = ' + str(len(df_sampled)))
        return df_sampled

    def format_text(
            self,
            text,
            pat_repl_list = (
                    ("[\n\r]", "<br>"),
                    ("[ ]", "&nbsp"),
            )
    ):
        text_proc = str(text).strip()
        for pat, repl in pat_repl_list:
            text_proc = re.sub(pattern=pat, repl=repl, string=text_proc)
        return text_proc

    """
    Study the effectiveness of Bert Embedding (hidden states), by clustering text embeddings
    """
    def analyze_embedding(
            self,
            # "cluster", "randomforest", "nn", "nb"
            method = 'cluster',
            params_other = {},
            # permitted values: None, "json", "string"
            return_type = None,
    ):
        texts_train = self.df_train[self.csvcol_text_train].values
        texts_val = self.df_val[self.csvcol_text_val].values

        max_cluster_turning_points = params_other.get('max_turning_points', 1)
        max_clusters = params_other.get('max_clusters', None)
        return_compact_desc = params_other.get('return_compact_desc', False)

        self.logger.info(
            'Analyze embedding method "' + str(method) + '", train texts using column "'
            + str(self.csvcol_text_train) + '", valuation texts using column "' + str(self.csvcol_text_val)
            + '", max cluster turning point ' + str(max_cluster_turning_points)
        )

        emb_trn = self.lm.encode(
            text_list = texts_train,
            return_tensors = 'np',
        )
        emb_val = self.lm.encode(
            text_list = texts_val,
            return_tensors = 'np',
        )

        if method == 'cluster':
            res = self.analyze_by_cluster(
                df_train = self.df_train,
                df_val = self.df_val,
                vect_embeddings = emb_trn,
                max_cluster_turning_points = max_cluster_turning_points,
                return_compact_desc = return_compact_desc,
            )
        elif method == 'simple':
            res = self.analyze_by_simple(
                df_train = self.df_train,
                df_val   = self.df_val,
                vect_embeddings_train = emb_trn,
                vect_embeddings_val   = emb_val,
            )
        elif method == 'nb':
            res = self.analyze_by_naive_bayes(
                df_train = self.df_train,
                df_val   = self.df_val,
                vect_embeddings_train = emb_trn,
                vect_embeddings_val   = emb_val,
            )
        elif method == 'randomforest':
            res = self.analyze_by_randomforest(
                df_train = self.df_train,
                df_val   = self.df_val,
                vect_embeddings_train = emb_trn,
                vect_embeddings_val   = emb_val,
            )
        elif method == 'nn':
            res = self.analyze_by_nn(
                df_train = self.df_train,
                df_val   = self.df_val,
                vect_embeddings_train = emb_trn,
                vect_embeddings_val   = emb_val,
            )
        else:
            raise Exception('No such method "' + str(method) + '"')

        if return_type in ['json']:
            res['analysis'] = str(res['analysis'])
            res['result'] = res['result'].to_dict('records')
        elif return_type in ['string']:
            res_txt = ''
            for k, v in res.items():
                tp_v = type(v)
                if tp_v is dict:
                    res_txt = res_txt + '<h3>' + str(k) + '</h3>'
                    for kk, vv in v.items():
                        res_txt = res_txt + '  <b>' + str(kk) + '</b>: ' + str(vv) + '\n'
                elif tp_v is pd.DataFrame:
                    res_txt = res_txt + '<h3>' + str(k) + '</h3>' + str(v) + '\n'
                else:
                    res_txt = res_txt + '<h3>' + str(k) + '</h3>' + str(v) + '\n'

            res = self.format_text(text=res_txt)
        return res

    def __return_result(
            self,
            method,
            lang_model,
            accuracy,
            df_prediction,
            score = None,
            analysis = None,
    ):
        score = accuracy if score is None else score
        return {
            'method': method,
            'lang_model': lang_model,
            'accuracy': np.round(accuracy, 2),
            'score': np.round(score, 2),
            'analysis': analysis,
            'result': df_prediction,
        }

    def analyze_by_cluster(
            self,
            df_train,
            df_val,
            vect_embeddings,
            max_cluster_turning_points = 1,
            return_compact_desc = False,
    ):
        df_lang = df_train.copy()

        col_text = self.csvcol_text_val

        cluster_text_list = df_lang[col_text].values
        train_label_list = df_lang[self.csvcol_label].values
        # max_clusters = min(20, int(len(text_list) / 3)) if max_clusters is None else max_clusters
        max_clusters = len(np.unique(df_lang[self.csvcol_label].values))
        min_clusters = max_clusters

        enc_txt, model_labels, _, _ = self.intent_cluster.train(
            text_list = cluster_text_list,
            labels    = None,
            params_other = {
                'min_clusters': min_clusters,
                'max_clusters': max_clusters,
                'custom_text_encoding': vect_embeddings,
                'max_turning_points': max_cluster_turning_points,
            },
        )
        df_lang['ModelLabel'] = model_labels
        cols_keep = ['ModelLabel', self.csvcol_label, col_text]
        df_lang = df_lang[cols_keep]
        df_lang = df_lang.sort_values(
            by = cols_keep
        ).reset_index(drop=True)

        model_lbl_desc = self.intent_cluster.map_model_labels_to_ref_labels(
            # text_list = df_lang['Body_pp'].tolist(),
            model_labels = df_lang['ModelLabel'].values,
            ref_labels_or_data_csv = df_lang[self.csvcol_label].values,
            text_list = df_lang[col_text].values,
            return_compact_desc = return_compact_desc,
        )
        accuracy = 0.
        for mdl_lbl, ana_1 in model_lbl_desc.items():
            label_map = ana_1['label_map']
            label_stats = ana_1['label_stats']
            pop_prop = label_stats['_PopulationProp']
            max_acc = 0.
            for lbl, ana_2 in label_map.items():
                max_acc = ana_2['_LocalProp'] if ana_2['_LocalProp']>max_acc else max_acc
            accuracy += max_acc * pop_prop

        return self.__return_result(
            method = 'cluster',
            df_prediction = df_lang,
            accuracy = accuracy,
            lang_model = self.intent_cluster.get_lang_model_name(),
            score = np.round((accuracy - 0.5) * 2, decimals=2),
            analysis = model_lbl_desc,
        )

    def analyze_by_simple(
            self,
            df_train,
            df_val,
            vect_embeddings_train,
            vect_embeddings_val,
    ):
        train_text_list = df_train[self.csvcol_text_train].values
        train_label_list = df_train[self.csvcol_label].values

        self.intent_simple.update_model_add_records(
            records = [{TxtClassifyDense.IN_MEMORY_COL_LABEL_USER: lbl, TxtClassifyDense.IN_MEMORY_COL_TEXT: txt}
                       for lbl, txt in list(zip(train_label_list, train_text_list))]
        )

        texts_val = df_val[self.csvcol_text_val].values
        labels_val = df_val[self.csvcol_label].values
        # labels_pred, probs_pred = self.intent_cluster.predict(text_list=texts_val, use_centers=True)
        labels_pred, probs_pred = self.intent_simple.predict(
            text_list = texts_val,
            params_other = {
                TxtClassifyDense.KEY_PREDICT_SIMILARITY_TYPE: 'cosine',
                'PCA': self.predict_via_model_compression,
            },
        )
        # print(list(zip(labels_pred, texts_val)))
        # raise Exception('asdf')

        df_result = pd.DataFrame({
            'text': texts_val,
            'label': labels_val,
            'pred': [r[0] for r in labels_pred],
            'prob': [r[0] for r in probs_pred],
        })
        df_result['correct'] = 1 * (df_result['label'] == df_result['pred'])
        accuracy = np.sum(df_result['correct']) / len(df_result)

        return self.__return_result(
            method = 'simple',
            df_prediction = df_result,
            accuracy = accuracy,
            lang_model = self.lm.model_name,
        )

    def analyze_by_randomforest(
            self,
            df_train,
            df_val,
            vect_embeddings_train,
            vect_embeddings_val,
    ):
        # can use arbitray human labelled category
        labels_train = df_train[self.csvcol_label].values

        clf = RandomForestClassifier()
        clf.fit(vect_embeddings_train, labels_train)
        joblib.dump(clf, "model_rf.joblib")

        """
        Evaluate against validation set
        """
        texts_val = df_val[self.csvcol_text_val].values
        labels_val = df_val[self.csvcol_label].values
        clf_loaded = joblib.load("model_rf.joblib")
        preds = clf_loaded.predict(vect_embeddings_val)

        df_result = pd.DataFrame({'text': texts_val, 'label': labels_val, 'pred': preds})
        df_result['correct'] = 1 * (df_result['label'] == df_result['pred'])
        accuracy = np.sum(df_result['correct']) / len(df_result)

        return self.__return_result(
            method = 'random forest',
            df_prediction = df_result,
            accuracy = accuracy,
            lang_model = self.lm.model_name,
        )

    def analyze_by_naive_bayes(
            self,
            df_train,
            df_val,
            vect_embeddings_train,
            vect_embeddings_val,
    ):
        # can use arbitray human labelled category
        labels_train = df_train[self.csvcol_label].values

        clf = GaussianNB()
        clf.fit(X=vect_embeddings_train, y=labels_train)
        joblib.dump(clf, "model_nb.joblib")

        """
        Evaluate against validation set
        """
        texts_val = df_val[self.csvcol_text_val].values
        labels_val = df_val[self.csvcol_label].values
        clf_loaded = joblib.load("model_nb.joblib")
        preds = clf_loaded.predict(vect_embeddings_val)

        df_result = pd.DataFrame({'text': texts_val, 'label': labels_val, 'pred': preds})
        df_result['correct'] = 1 * (df_result['label'] == df_result['pred'])
        accuracy = np.sum(df_result['correct']) / len(df_result)

        return self.__return_result(
            method = 'naive bayes',
            df_prediction = df_result,
            accuracy = accuracy,
            lang_model = self.lm.model_name,
        )

    def analyze_by_nn(
            self,
            df_train,
            df_val,
            vect_embeddings_train,
            vect_embeddings_val,
    ):
        import tensorflow as tf

        textlabels_train = df_train[self.csvcol_label].values
        # Convert to numbers
        unique_textlabels = np.unique(textlabels_train)
        map_lbl_txt = {i: txtlbl for i, txtlbl in enumerate(unique_textlabels)}
        map_txt_lbl = {txtlbl: i for i, txtlbl in map_lbl_txt.items()}
        labels_train = [map_txt_lbl[txtlbl] for txtlbl in textlabels_train]

        labels_train_categorical = tf.keras.utils.to_categorical(labels_train)
        n_labels_train = len(np.unique(labels_train))

        textlabels_val = df_val[self.csvcol_label].values
        texts_val = df_val[self.csvcol_text_val].values

        model = tf.keras.Sequential()
        ly_in = tf.keras.layers.Input(shape=(vect_embeddings_train.shape[-1],))
        model.add(ly_in)
        ly_dropout = tf.keras.layers.Dropout(rate=0.1)
        model.add(ly_dropout)
        ly_dense = tf.keras.layers.Dense(units=100, activation='relu')
        model.add(ly_dense)
        ly_dense2 = tf.keras.layers.Dense(units=n_labels_train, activation='softmax')
        model.add(ly_dense2)

        model.summary()

        model.compile(
            optimizer = 'adam',
            loss      = 'categorical_crossentropy',
            metrics   = ['accuracy'],
        )

        model.fit(x=vect_embeddings_train, y=labels_train_categorical, epochs=100, batch_size=16)
        model.save('model_nn.joblib')
        model_loaded = tf.keras.models.load_model('model_nn.joblib')

        """
        Evaluate against validation set
        """
        pred = model_loaded.predict(vect_embeddings_val)
        pred = np.argmax(pred, axis=1)
        pred_txtlbl = [map_lbl_txt[nolbl] for nolbl in pred]

        df_result = pd.DataFrame({'text': texts_val, 'label': textlabels_val, 'pred': pred_txtlbl})
        df_result['correct'] = 1 * (df_result['label'] == df_result['pred'])
        accuracy = np.sum(df_result['correct']) / len(df_result)
        self.logger.info('Accuracy NN = ' + str(accuracy * 100) + '%')

        return self.__return_result(
            method = 'network dense',
            df_prediction = df_result,
            accuracy = accuracy,
            lang_model = self.lm.model_name,
        )

    def get_sample_data(
            self,
            n_samples = 100,
            # download from https://www.kaggle.com/datasets/hgultekin/bbcnewsarchive?resource=download
            csvpath = 'bbc-news-data.csv',
    ):
        df = pd.read_csv(csvpath, sep='\t')
        labels_unique = pd.unique(df['category']).tolist()
        labels_unique.sort()
        # print('labels: ' + str(labels_unique))

        df[self.COL_CLASS] = -1
        for i in range(len(labels_unique)):
            df.loc[df[self.csvcol_label] == labels_unique[i], self.COL_CLASS] = i

        if n_samples < len(df):
            # Pick random n_samples
            rand_indexes = np.random.choice(len(df), n_samples, replace=False)
            # print(rand_indexes)
            df = df.loc[rand_indexes]

        return df


if __name__ == '__main__':
    Pandas.increase_display()

    er = EnvRepo(
        repo_dir = os.environ['REPO_DIR'],
    )

    # en, de, fr, nl, tr, pt, pt-br, es, vi (hi, bn, cy)
    # "--" for random translation
    lang_tgt = 'ko'
    lang_train = 'en'
    lm_model_name_custom = 'intfloat/multilingual-e5-base'
    train_csvpath = er.NLP_DATASET_DIR + '/lang-model-test/data.csv'
    # train_csvpath = er.NLP_DATASET_DIR + '/bbc-news.en.csv'
    csv_colmap = None
    # train_csvpath = er.NLP_DATASET_DIR + '/kaggle/google_news_202309_trnval.csv'
    # csv_colmap = {LmAnalyzeData.COL_TEXT: 'Title', LmAnalyzeData.COL_LABEL: 'Category'}
    predict_via_model_compression = False

    """
    Analyze embedding accuracy
    """
    ana = LmAnalyze(
        lang_tgt = lang_tgt,
        lang_data = 'en',
        lang_train = lang_train,
        train_csvpath = train_csvpath,
        validate_csvpath = train_csvpath,
        csv_colmap = csv_colmap,
        lm_model_name = lm_model_name_custom,
        lm_cache_dir = er.MODELS_PRETRAINED_DIR,
        nlp_data_cache_dir = er.NLP_DATASET_DIR,
        model_cache_dir = er.MODELS_TRAINING_DIR,
        predict_via_model_compression = predict_via_model_compression,
        logger = Logging.get_default_logger(log_level=logging.INFO, propagate=False)
    )

    for method in [
        'simple',
        # 'cluster',
        # 'randomforest',
        # 'nb',
        # 'nn',
    ]:
        res = ana.analyze_embedding(
            method = method,
            params_other = {
                'max_turning_points':  1,
                'return_compact_desc': False,
            },
            return_type = None,
        )
        print('----------------------------------------------------------------------')
        print('Analyze Method "' + str(method) + '"')
        df = res['result']
        df.to_csv('result.' + str(method) + '.csv')
        print(str(df))
        [print(str(k) + ': ' + str(v)) for k, v in res.items() if k not in('result',)]

        if method == 'simple':
            ana.intent_simple.stop_threads()

    exit(0)
