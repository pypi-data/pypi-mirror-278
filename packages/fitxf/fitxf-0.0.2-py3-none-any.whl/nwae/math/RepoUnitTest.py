import warnings
import uuid
import os
import re
from nwae.math.utils import Logging, Profiling, EnvRepo
from nwae.math.utils.Env import Env
#----------------------------------------------------------------------------------
# IC Section
#----------------------------------------------------------------------------------
# Math
from nwae.math.fit.transform.FitXformPcaUnitTest import FitXformPcaUnitTest
from nwae.math.fit.utils.FitUtilsUnitTest import FitUtilsUt
from nwae.math.fit.utils.TensorUtils import TensorUtilsUnitTest
from nwae.math.fit.cluster.ClusterUnitTest import ClusterUnitTest
from nwae.math.fit.cluster.ClusterCosineUT import ClusterCosineUnitTest
# Utils
from nwae.math.utils.Lock import LockUnitTest
from nwae.math.utils.ObjPers import UnitTestObjectPersistence
from nwae.math.utils.Singleton import SingletonUnitTest
from nwae.math.utils.StringVar import StringVarUnitTest
# Algo
from nwae.math.algo.encoding.Base64 import Base64UnitTest


class RepoUnitTest:

    def __init__(
            self,
    ):
        self.repository_dir = EnvRepo(repo_dir=os.environ["REPO_DIR"])

        self.keys_dir = self.repository_dir.REPO_DIR + '/keys'
        self.regex_exceptions_path = self.repository_dir.CONFIG_UNITTEST_REGEX_EXCEPTIONS_FILEPATH
        self.presidio_yaml_path = self.repository_dir.CONFIG_UNITTEST_PRESIDIO_YAML_FILEPATH
        self.presidio_entities_path = self.repository_dir.CONFIG_UNITTEST_PRESIDIO_DEF_ENTITIES_JSON
        self.lm_cache_folder = self.repository_dir.MODELS_PRETRAINED_DIR
        self.document_folder = self.repository_dir.REPO_DIR + '/data/sample_docs'
        self.tmp_dir = os.environ["TEMP_DIR"]
        self.logger = Logging.get_logger_from_env_var()

        rand_str = re.sub(pattern=".*[\-]", repl="", string=str(uuid.uuid4()))
        self.db_test_table_or_index = 'nwae-math.repo-unit-test.' + str(rand_str)

        warnings.filterwarnings("ignore", message="Unverified HTTPS request")
        return

    def test(self):
        profiler = Profiling(logger=self.logger)
        test_record = {}

        t00 = profiler.start()

        for cls in [
            # Math
            FitXformPcaUnitTest, FitUtilsUt, TensorUtilsUnitTest, # HomomorphismUnitTest,
            ClusterUnitTest, ClusterCosineUnitTest,
            # Utils
            LockUnitTest, SingletonUnitTest, StringVarUnitTest,
            UnitTestObjectPersistence,
            # Datastore
            # This test can only run if you already set up Elasticsearch locally
            # MemoryCacheUnitTest, MySqlUnitTest, VecDbUnitTest, VecDbCcrcyTest, VecDbSingletonUnitTest,
            # Algo
            Base64UnitTest, # SortColumnsUnitTest, SortRangesAndOverlapsUnitTest,
            # Models
            # MultiTreeUnitTest,
            # Language
            # LangCharUnitTest, LangUnitTest,
            # Text
            # TextDiffUnitTest,
            # MaskTextSortedUnitTest, AnonymizerUnitTest, RegexPpUnitTest, TxtPreprocessorUnitTest,
            # Language Models
            # LangModelInterfaceTest, LangModelPtUnitTest,
            # Intent
            # ClassifyWrapperUnitTest,
            # InfoRetrievalUnitTest,
        ]:
            t0 = profiler.start()
            # if cls not in [VecDbCcrcyTest]:
            #     continue

            if cls == FitUtilsUt:
                self.logger.info('BEGIN TESTING ' + str(cls))
                ut = FitUtilsUt(logger=self.logger)
                ut.test_map_to_connbr()
                # TODO Uncomment these when we use them
                # ut.test_nn(epochs=5000, plot_graph=False, tol_dif=0.1)
                # ut.test_dist()
            elif cls == FitXformPcaUnitTest:
                self.logger.info('BEGIN TESTING ' + str(cls))
                ut = FitXformPcaUnitTest(
                    lm_cache_folder = self.lm_cache_folder,
                    logger = self.logger,
                )
                ut.test()
            elif cls == TensorUtilsUnitTest:
                self.logger.info('BEGIN TESTING ' + str(cls))
                ut = TensorUtilsUnitTest()
                ut.test_norm()
                ut.test_similarity_cosine_and_similarity_distance()
            else:
                self.logger.info('BEGIN TESTING ' + str(cls))
                cls(logger=self.logger).test()

            t1 = profiler.stop()
            secs_taken = profiler.get_time_dif_secs(start=t0, stop=t1, decimals=10)
            time_taken = str(round(secs_taken, 2))+'s' if secs_taken > 0.01 else \
                    str(round(secs_taken*1000000, 2))+'μs'
            test_record[cls] = {'secs_taken': time_taken}

        self.logger.info('------------------------------------------------------------------------------------')
        self.logger.info('OK DONE ' + str(len(test_record)) + ' TESTS SUCCESSFULLY')
        [
            self.logger.info(
                '   ' + str(i) + '. ' + str(k) + '\n      --> ' + str(v)
            )
            for i, (k, v) in enumerate(test_record.items())
        ]
        self.logger.info('Total secs taken ' + str(profiler.get_time_dif_secs(start=t00, stop=profiler.stop(), decimals=2)))


if __name__ == '__main__':
    env_repo = EnvRepo(repo_dir=os.environ.get('REPO_DIR', None))
    Env.set_env_vars_from_file(env_filepath=env_repo.REPO_DIR + '/.env.nwae.math.ut')

    RepoUnitTest().test()
    exit(0)
