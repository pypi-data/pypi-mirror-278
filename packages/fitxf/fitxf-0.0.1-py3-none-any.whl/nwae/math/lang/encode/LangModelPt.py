import torch
import logging
import os
from nwae.math.lang.encode.LangModelInterface import LangModelInterface
from nwae.math.lang.encode.LangModelInterfaceX import LangModelInterfaceX as LmInterfaceX
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from nwae.math.utils.EnvironRepo import EnvRepo
from nwae.math.utils.Logging import Logging


#
# Leader Board: https://huggingface.co/spaces/mteb/leaderboard
#
class LangModelPt(LangModelInterface, LmInterfaceX):

    #
    # Names that follow HuggingFace convention
    # Can pre-cache the following models by git pull into your desired directory
    #   git lfs install
    #   git clone https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L6-v2
    #   git clone https://huggingface.co/deepset/sentence_bert
    #   git clone https://huggingface.co/bert-base-chinese
    #   git clone https://huggingface.co/monsoon-nlp/hindi-bert
    #   git clone https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
    #
    LM_MINILM_L6_V2 = 'sentence-transformers/paraphrase-MiniLM-L6-v2'
    LM_SENTENCE_BERT = 'deepset/sentence_bert'
    LM_BERT_BASE_ZH = 'bert-base-chinese'
    # Multi-lingual models
    LM_ST_MULTILINGUAL_MINILM_L12_V2 = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    LM_INTFL_MULTILINGUAL_E5_SMALL = 'intfloat/multilingual-e5-small'
    # Best performance for cy (Welsh)
    LM_BERT_BASE_MULTILINGUAL_UNCASED = 'bert-base-multilingual-uncased'
    LM_BERT_BASE_MULTILINGUAL_CASED = 'bert-base-multilingual-cased'
    LM_DISTILBERT_MULTILINGUAL_CASED = 'distilbert-base-multilingual-cased'
    # Supposed have Welsh/cy, but not the case in our tests
    LM_XLM_ROBERTA_BASE = 'xlm-roberta-base'
    LM_XLM_ROBERTA_LARGE = 'xlm-roberta-large'
    #
    # Can pre-cache the following models by git pull into your desired directory
    #   git lfs install
    #   git clone https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L6-v2
    #   git clone https://huggingface.co/deepset/sentence_bert
    #   git clone https://huggingface.co/bert-base-chinese
    #   git clone https://huggingface.co/monsoon-nlp/hindi-bert
    #   git clone https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
    #

    DEFAULT_MODEL_MAP = {
        # This model does much better in Bengali compared to paraphrase multilingual
        'bn': LM_INTFL_MULTILINGUAL_E5_SMALL,
        # All other languages sink here
        'multi': LM_ST_MULTILINGUAL_MINILM_L12_V2,
    }

    # Only if we need a different or particular directory name, otherwise will default to the same one as HF
    LM_PATH_INFO = {
        # LM_INTFL_MULTILINGUAL_E5_SMALL: 'intfloat--multilingual-e5-small',
    }

    def __init__(
            self,
            lang,
            model_name = None,
            cache_folder = None,
            include_tokenizer = False,
            params_other = None,
            logger = None,
    ):
        super().__init__(
            lang = lang,
            cache_folder = cache_folder,
            model_name = model_name,
            include_tokenizer = include_tokenizer,
            params_other = params_other,
            logger = logger,
        )
        LmInterfaceX.__init__(
            self = self,
            logger = logger,
        )

        assert self.lang, 'Language cannot be empty "' + str(self.lang) + '"'
        if self.lang not in self.DEFAULT_MODEL_MAP.keys():
            self.logger.warning('Lang not in default model map keys "' + str(self.lang) + '", default to "multi"')
            self.lang = 'multi'
        self.logger.info(
            'Lang "' + str(self.lang) + '", model name "' + str(self.model_name)
            + '", cache folder "' + str(self.cache_folder) + '"'
        )

        try:
            # User may pass in model downloaded path
            if os.path.isdir(str(self.model_name)):
                self.model_path = self.model_name
            # If user passes in only language, we derive the model and path
            else:
                self.model_name = self.DEFAULT_MODEL_MAP[self.lang] if self.model_name is None else self.model_name
                self.model_path = self.cache_folder + '/' + self.LM_PATH_INFO.get(self.model_name, self.model_name)

            assert os.path.isdir(self.model_path), 'Not a directory "' + str(self.model_path) + '"'
            self.logger.info('Model name "' + str(self.model_name) + '" path "' + str(self.model_path) + '"')

            self.logger.info(
                'Lang model "' + str(self.model_name) + '" with cache folder "' + str(self.cache_folder)
                + '", include tokenizer "' + str(self.include_tokenizer)
                + '", name_or_path "' + str(self.model_path) + '"'
            )
            if self.include_tokenizer:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    pretrained_model_name_or_path = self.model_path,
                    # cache_folder = self.cache_folder,
                )
                self.logger.info(
                    'OK Tokenizer for model "' + str(self.model_path) + '", cache folder "' + str(self.cache_folder) + '"'
                )
                self.model = AutoModel.from_pretrained(
                    # hugging face will know to use the cache folder above, without specifying here it seems
                    pretrained_model_name_or_path = self.model_path
                )
                self.logger.info(
                    'OK Model "' + str(self.model_path) + '", cache folder "' + str(self.cache_folder) + '"'
                )
            else:
                self.model = SentenceTransformer(
                    model_name_or_path = self.model_path,
                    cache_folder = self.cache_folder,
                )
        except Exception as ex:
            errmsg = 'Fail to instantiate language model for lang "' + str(lang)\
                     + '" model "' + str(self.model_name) + '", path "' + str(self.model_path) \
                     + '", cache folder "' + str(self.cache_folder) + '": ' + str(ex)
            self.logger.fatal(errmsg)
            raise Exception(errmsg)
        return

    # Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def encode(
            self,
            text_list,
            # max length has got no meaning
            maxlen = None,
            return_tensors = 'pt',
            # does not apply here since we can't see the tokenization
            return_attnmasks = False,
            params_other = None,
    ):
        if self.include_tokenizer:
            self.logger.debug('Calculating embedding using tokenizer')
            embeddings_tensor = None
            for txt in text_list:
                # Tokenize sentences
                encoded_input = self.tokenizer(txt, padding=True, truncation=True, return_tensors='pt')

                # Compute token embeddings
                with torch.no_grad():
                    model_output = self.model(**encoded_input)

                # Perform pooling. In this case, max pooling.
                attn_masks = encoded_input['attention_mask']
                embedding = self.mean_pooling(model_output=model_output, attention_mask=attn_masks)
                if embeddings_tensor is not None:
                    embeddings_tensor = torch.cat((embeddings_tensor, embedding), dim=0)
                else:
                    embeddings_tensor = embedding

            attn_masks = None
            if return_tensors == 'pt':
                return (embeddings_tensor, attn_masks) if return_attnmasks else embeddings_tensor
            else:
                embedding_np = embeddings_tensor.cpu().detach().numpy()
                return (embedding_np, attn_masks) if return_attnmasks else embedding_np
        else:
            self.logger.debug('Calculating embedding using single sentence transformer wrapper')
            embedding = self.model.encode(
                sentences = text_list,
            )
            # TODO
            #    How to get this? Since this depends on the tokenizer used by the language model,
            #    this means we cannot calculate on our own by tokenizing.
            attn_masks = None

            if return_tensors == 'pt':
                pt_array = torch.from_numpy(embedding)
                return (pt_array, attn_masks) if return_attnmasks else pt_array
            else:
                return (embedding, attn_masks) if return_attnmasks else embedding


if __name__ == '__main__':
    er = EnvRepo(repo_dir=os.environ['REPO_DIR'])
    lgr = Logging.get_default_logger(log_level=logging.INFO, propagate=False)

    for lg, txt in (
            ['en', 'Sentence to embedding'],
            ['cy', 'Dyfalwch fy iaith'],
            ['hi', 'मेरी भाषा का अनुमान लगाओ'],
            ['bn', 'আমি রুটি ভালোবাসি'],
            ['zh', '猜猜我的语言'],
    ):
        lm_1 = LangModelPt(
            lang = lg,
            cache_folder = er.MODELS_PRETRAINED_DIR,
            include_tokenizer = True,
            logger = lgr,
        )
        vec_1 = lm_1.encode(text_list=[txt])
        print(lg, lm_1.model_name, lm_1.model_path, txt)

    lm = LangModelPt(
        lang = 'ko',
        model_name = LangModelPt.LM_INTFL_MULTILINGUAL_E5_SMALL,
        cache_folder = er.MODELS_PRETRAINED_DIR,
        logger = lgr,
    )
    text_list = [
        '칠리 페퍼', '와사비', '머스타드',
        '케이크', '도넛', '아이스크림',
    ]
    labels = ['hot', 'hot', 'hot', 'sweet', 'sweet', 'sweet']
    lm.visualize_embedding(
        encoding_np = lm.encode(text_list=text_list, return_tensors='np'),
        labels_list = labels,
    )

    print('rps', lm.speed_test(sentences=text_list, min_rounds=200))
    exit(0)
