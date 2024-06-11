import logging
import torch
import os
from nwae.math.lang.encode.LangModelPt import LangModelPt
from nwae.math.utils import EnvRepo, Logging, Profiling
from nwae.math.lang.encode.LmIfTest import LangModelInterfaceTest


class LangModelPtUnitTest:

    def __init__(
            self,
            pt_cache_folder,
            logger = None,
    ):
        self.pt_cache_folder = pt_cache_folder
        self.logger = logger if logger is not None else logging.getLogger()

        assert os.path.isdir(self.pt_cache_folder), 'Not a directory "' + str(self.pt_cache_folder) + '"'
        return

    def test_discover_max_len(
            self,
            lang,
            random_txt,
    ):
        li = LangModelPt(
            lang = lang,
            cache_folder = self.pt_cache_folder,
            logger = self.logger,
        )
        res = li.self_discover_max_len(sample_text=random_txt)
        print(res)
        return

    def test_singleton(self):
        o = LangModelInterfaceTest()
        LM = LangModelPt
        o.test_singleton(
            ClassType = LM,
            uniq_models_names = (
                LM.LM_ST_MULTILINGUAL_MINILM_L12_V2,
                # LM.LM_INTFL_MULTILINGUAL_E5_SMALL,
            ),
            cache_folder = self.pt_cache_folder,
        )
        return

    def test_same_embedding_output(self):
        for lg, txt in (
                ['en', 'Sentence to embedding'],
                ['cy', 'Dyfalwch fy iaith'],
                ['hi', 'मेरी भाषा का अनुमान लगाओ'],
                ['zh', '猜猜我的语言'],
        ):
            lm_1 = LangModelPt(
                lang = lg,
                cache_folder = self.pt_cache_folder,
                include_tokenizer = True,
                logger = self.logger,
            )
            lm_2 = LangModelPt(
                lang = lg,
                cache_folder = self.pt_cache_folder,
                include_tokenizer = False,
                logger = self.logger,
            )
            vec_1 = lm_1.encode(text_list=[txt])
            vec_2 = lm_2.encode(text_list=[txt])
            diff = torch.sum((vec_1 - vec_2) ** 2).item()

            self.logger.debug(
                'Lang "' + str(lg) + '", model name "' + str(lm_1.model_name)
                + '", model path "' + str(lm_1.model_path) + '", text "' + str(txt) + '"'
            )
            self.logger.debug(str(vec_1)[0:200] + '...')
            self.logger.debug(str(vec_2)[0:200] + '...')
            self.logger.debug('Difference squared = ' + str(diff))

            assert diff < 0.000001, 'Embedding calculation differ:\n' + str(vec_1) + '\n' + str(vec_2)

        print('ALL TESTS PASSED')


if __name__ == '__main__':
    er = EnvRepo(repo_dir=os.environ['REPO_DIR'])
    t = LangModelPtUnitTest(
        pt_cache_folder = er.MODELS_PRETRAINED_DIR,
        logger = Logging.get_default_logger(log_level=logging.DEBUG, propagate=False),
    )
    print('--------------------------------------------------------------------------------')
    t.test_singleton()
    print('OK PASSED Singleton Test')
    print('--------------------------------------------------------------------------------')
    # t.test_discover_max_len(lang='en', random_txt=Lm)
    print('OK PASSED Discover Max Length Test')
    print('--------------------------------------------------------------------------------')
    t.test_same_embedding_output()
    print('OK PASSED Same Embedding Output Test')
    exit(0)
