import logging
import os
from io import StringIO
import numpy as np
import pandas as pd
from nwae.math.algo.encoding.Base64 import Base64
from nwae.math.data.ut.LabelTextEmbed01 import DATA_LABEL_TEXT_EMBEDDING_01_TRAIN, DATA_LABEL_TEXT_EMBEDDING_01_EVAL
from nwae.math.fit.transform.FitXformPca import FitXformPca
from nwae.math.lang.encode.LangModelPt import LangModelPt as LmPt
from nwae.math.utils.EnvironRepo import EnvRepo
from nwae.math.utils.Logging import Logging


class FitXformPcaUnitTest:

    def __init__(
            self,
            lm_cache_folder = None,
            logger = None,
    ):
        self.logger = logger if logger is not None else logging.getLogger()
        self.lm_cache_folder = lm_cache_folder
        self.base64 = Base64(logger=self.logger)
        return

    def test(self):
        fitter = FitXformPca(logger=self.logger)

        # texts_train = [
        #     "Let's have coffee", "Free for a drink?", "How about Starbucks?",
        #     "I am busy", "Go away", "Don't disturb me",
        #     "Monetary policies", "Interest rates", "Deposit rates",
        # ]
        # labels_train = ['drink', 'drink', 'drink', 'busy', 'busy', 'busy', 'finance', 'finance', 'finance']
        # texts_test = ["How about a cup of coffee?", "Not now", "Financial policies"]

        def get_data(
                s,
        ):
            df = pd.read_csv(
                filepath_or_buffer = StringIO(s),
                sep = ',',
                index_col = False,
            )
            columns_keep = ['label', 'text', 'embedding']
            for c in columns_keep: assert c in df.columns
            df = df[columns_keep]
            df.dropna(inplace=True)
            # _, _, df[self.col_label_std] = FitUtils().map_labels_to_consecutive_numbers(lbl_list=list(df[self.col_label]))
            self.logger.info('Successfully read data of shape ' + str(df.shape))
            return df

        df_train = get_data(s=DATA_LABEL_TEXT_EMBEDDING_01_TRAIN)
        df_eval = get_data(s=DATA_LABEL_TEXT_EMBEDDING_01_EVAL)

        texts_train, labels_train = df_train['text'].tolist(), df_train['label'].tolist()
        texts_eval, labels_eval = df_eval['text'].tolist(), df_eval['label'].tolist()

        def get_lm() -> LmPt:
            return LmPt.get_singleton(
                LmClass = LmPt,
                lang = 'en',
                cache_folder = self.lm_cache_folder,
                logger = self.logger,
            )

        try:
            raise Exception('Force to use pre-calculated embeddings.')
            emb_train = get_lm().encode(text_list=texts_train, return_tensors='np')
            emb_eval = get_lm().encode(text_list=texts_test, return_tensors='np')
        except Exception as ex:
            self.logger.info('Failed to calculate embeddings: ' + str(ex) + ', using precalculated embeddings instead.')
            emb_train = np.array([
                self.base64.decode_base64_string_to_numpy_array(s64=s, data_type=np.float64)
                for s in df_train['embedding'].tolist()
            ])
            emb_eval = np.array([
                self.base64.decode_base64_string_to_numpy_array(s64=s, data_type=np.float64)
                for s in df_eval['embedding'].tolist()
            ])
        # x = np.array([
        #     [1, 1, 1, 1], [2, 2, 2, 2],
        #     [2, 1.5, -1, 0.3], [1, 2, -2, 1],
        #     [3, 0.5, 0, -1], [1, 1, 1, -2],
        # ])
        res = fitter.fit_optimal(
            X = emb_train,
            X_labels = labels_train,
            target_grid_density = 2.,
            measure = 'min',
            min_components = 3,
            max_components = 3,
        )
        self.logger.debug('PCA fit result ' + str(res))
        print('grid numbers', fitter.X_grid_numbers)
        print('distance error', fitter.distance_error)
        print('distance error %', fitter.distance_error_pct)
        print('distance error mean', fitter.distance_error_mean)
        print('angle error', fitter.angle_error)
        print('angle error mean', fitter.angle_error_mean)
        print('grid density', fitter.grid_density)
        print('grid density mean', fitter.grid_density_mean)

        x_pca = fitter.X_transform
        x_pca_check = fitter.X_transform_check
        x_estimate = fitter.X_inverse_transform

        # Check if estimation of actual value is correct
        diff = x_estimate - emb_train
        sq_err_per_vect = np.sum(diff*diff) / len(diff)
        x_dim = emb_train.shape[-1]
        sq_err_per_vect_thr = 0.1 * x_dim
        assert sq_err_per_vect < sq_err_per_vect_thr, \
            'Estimate back using PCA, per vector sq err ' + str(sq_err_per_vect) \
            + '>=' + str(sq_err_per_vect_thr) + ', details: ' + str(diff)

        # Check if our manual calculation of the principal component values are correct
        diff = x_pca_check - x_pca
        sq_err_sum = np.sum(diff*diff)
        assert sq_err_sum < 0.000000001, \
            'Manual calculate PCA component values, sq err ' + str(sq_err_sum) + ', diff ' + str(diff)

        for use_grid in (False, True,):
            pred_labels, pred_probs = fitter.predict(
                X = emb_eval,
                use_grid = use_grid,
                return_full_record = False,
            )
            print(
                'Use grid "' + str(use_grid) + '", predicted labels: ' + str(pred_labels)
            )
            expected_top_labels = df_eval['label'].tolist()
            scores = []
            for i, exp_lbl in enumerate(expected_top_labels):
                # 1.0 for being 1st, 0.5 for appearing 2nd
                score_i = 1*(pred_labels[i][0] == exp_lbl) + 0.5*(pred_labels[i][1] == exp_lbl)
                score_i = min(score_i, 1.0)
                scores.append(score_i)
                # Check only top prediction
                if pred_labels[i][0] != exp_lbl:
                    self.logger.warning(
                        '#' + str(i) + ' Use grid "' + str(use_grid) + '". Predicted top label ' + str(pred_labels[i])
                        + ' not expected ' + str(exp_lbl)
                    )
            score_avg = np.mean(np.array(scores))
            self.logger.info(
                'Use grid "' + str(use_grid) + '". Mean score ' + str(score_avg) + ', scores' + str(scores)
            )
            assert score_avg > 0.9, \
                'Use grid "' + str(use_grid) + '". Mean score fail ' + str(score_avg) + ' < 0.9. Scores ' + str(scores)

        print('ALL TESTS PASSED OK')
        return


if __name__ == '__main__':
    FitXformPcaUnitTest(
        lm_cache_folder = EnvRepo(repo_dir=os.environ.get("REPO_DIR", None)).MODELS_PRETRAINED_DIR,
        logger = Logging.get_default_logger(log_level=logging.INFO, propagate=False),
    ).test()
    exit(0)
