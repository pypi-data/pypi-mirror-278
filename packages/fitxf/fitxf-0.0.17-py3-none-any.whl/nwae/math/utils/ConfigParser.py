import logging
import configparser
import numpy as np
import re
import os
import uuid
import unittest
from nwae.math.utils.StringVar import StringVar


#
# Enhanced Config Parser
#
#   1. Can specify value by local variable to any depth/recursion
#      If a variable name is not found, will default to look in environment variable.
#      If not found in environment variable, will throw error.
#
#      [CodeSection]
#        GIT_DIR = /usr/local/git
#        REPO_NAME = myrepo
#      [OtherSection]
#        # Can read variables in format ${<SECTION_NAME>::<VARIABLE_NAME>}, e.g.
#        REPO_DIR = ${CodeSection::GIT_DIR}/${CodeSection::REPO_NAME}/
#      [OtherOtherSection]
#        Comment = Repo Directory is ${OtherSection::REPO_DIR}
#      [OtherOtherOtherSection]
#        Comment = Other other section comment is ${OtherOtherSection::Comment}
#     ...
#
#   2. Can specify value by environment variable
#
#     # When there is no section name, will take from environment variable $MYSQL_PWD
#     MYSQL_PASSWORD = ${MYSQL_PWD}
#
#
class Config:

    SECTION_VARNAME_SPLIT_STR = r'::'
    VAR_NAME_PROPERTIES = {
        'front': '${',
        'back': '}',
    }
    # ENVVAR_NAME_PROPERTIES = {
    #     'front': '$ENV{',
    #     'back': '}',
    # }

    DEF_APP_DIRNAME = 'nlp-services'
    DEF_MASK_KEYS = ('password', 'passwd', 'secret')
    DEF_MASK_KEYS_STRICT = ('password', 'passwd', 'secret', 'port', 'path', 'folder', 'dir')

    TRUE_STRINGS_LOWER = ('1', 'yes', 'ok', 'true', 'on', 'activate',)

    def __init__(
            self,
            filepath,
            logger = None,
            log_to_screen = True,
            log_level = 'WARNING',
            # use environment variable if variable in value not found in config itself
            use_envvar_if_var_not_found = True,
            return_default_config = False,
    ):
        self.config = configparser.ConfigParser()
        self.logger = logger if logger is not None else logging.getLogger()
        self.log_to_screen = log_to_screen
        self.log_level = log_level
        self.filepath = filepath
        self.use_envvar_if_var_not_found = use_envvar_if_var_not_found
        self.is_config_from_file = False

        self.string_var = StringVar(logger=self.logger)

        try:
            self.config.read([self.filepath], encoding='utf-8')
            self.logger.info('Successfully read config from file path "' + str(self.filepath) + '"')
            self.is_config_from_file = True
        except Exception as ex:
            self.logger.error('Exception reading config file "' + str(self.filepath) + '": ' + str(ex))

        # configparser converts all keys to lower() by default
        # [[print(ks,kv,v) for kv,v in x.items()] for ks,x in self.config.items()]
        # raise Exception('asdf')

        if not self.is_config_from_file:
            if not return_default_config:
                raise Exception('Fatal error loading config file "' + str(self.filepath) + '"')
            else:
                self.set_default_config()
                self.logger.warning(
                    'Config filepath invalid "' + str(self.filepath) + '", using default config: '
                    + str(self.get_entire_config())
                )
        return

    def set_default_config(
            self,
    ):
        pass

    def get(
            self,
            section_name,
            var_name,
            use_regex_replace_var = False,
    ):
        # Read raw text value from config
        value = self.config[section_name][var_name].strip()
        self.logger.debug(
            'For section/var "' + str(section_name) + '/' + str(var_name) + '", value "' + str(value) + '"'
        )
        value_new = value

        var_str_front, var_str_back = self.VAR_NAME_PROPERTIES['front'], self.VAR_NAME_PROPERTIES['back']
        # Replace vars (from env var or another section/var) in raw text value recursively (calling back get())
        value_new =  self.replace_vars(
            value = value_new,
            var_string_front = var_str_front,
            var_string_back = var_str_back,
            replace_func = self.get_var_value_recursive,
            use_regex = use_regex_replace_var,
        )
        return value_new

    def get_var_value_recursive(
            self,
            var_name,
    ):
        try:
            # Assume is of the form "SECTION::VAR", means looking up another section variable
            sect, var = var_name.split(sep=self.SECTION_VARNAME_SPLIT_STR, maxsplit=2)
            # recursive call get()
            var_value = self.get(section_name=sect, var_name=var)
        except Exception as ex:
            self.logger.error('Exception for var name "' + str(var_name) + '": ' + str(ex))
            var_value = None

        if not var_value:
            # Not section var, thus possible env var
            if self.use_envvar_if_var_not_found:
                # Get from environment instead
                var_value = self.get_var_value_environ(var_name=var_name)
                self.logger.info(
                    'Got from environment variable instead for var name "' + str(var_name)
                    + '" as "' + str(var_value) + '"'
                )
            else:
                raise Exception(
                    'Could not find variable value for var name "' + str(var_name)
                    + '" from config file "' + str(self.filepath) + '"'
                )

        return var_value

    def get_var_value_environ(
            self,
            var_name,
    ):
        assert var_name in os.environ.keys(), 'Not in environment variable "' + str(var_name) + '"'
        var_value = os.environ[var_name]
        return var_value

    def replace_vars(
            self,
            value,
            var_string_front,
            var_string_back,
            replace_func,
            use_regex = False,
    ):
        value_new = self.string_var.replace_vars(
            value = value,
            var_string_start = var_string_front,
            var_string_end = var_string_back,
            get_var_value_func = replace_func,
            use_regex = use_regex,
            varname_pattern = StringVar.PAT_VARNAME if use_regex else None,
        )
        return value_new

    def get_entire_config(
            self,
            mask_keys = DEF_MASK_KEYS,
            # Mask 70% of text
            mask_pct  = 0.7,
    ):
        cf_dict = {}
        for section, section_config in self.config.items():
            cf_dict[section] = dict(self.config.items(section))
            for k,v in cf_dict[section].items():
                # Replace variables in values by calling get()
                cf_dict[section][k] = self.get(section_name=section, var_name=k)
                for mask_k in mask_keys:
                    if re.match(pattern=".*("+mask_k.lower()+").*", string=str(k).strip().lower()):
                        v = str(v)
                        mask = np.arange(len(v)) < len(v)*mask_pct
                        v_show = ''.join(np.array([c for c in v])[np.logical_not(mask)].tolist())
                        v_mask = '*'*len(mask[mask])
                        cf_dict[section][k] = v_mask + v_show
        return cf_dict

    def print_entire_config(
            self,
            mask_keys = DEF_MASK_KEYS,
    ):
        def_config = self.config.items('DEFAULT')
        def_config_keys = [k for k,_ in def_config]
        for sect, sect_config in self.get_entire_config(mask_keys=mask_keys).items():
            print('[' + str(sect) + ']')
            if sect == 'DEFAULT':
                [print('   ', k, ':', v) for k, v in sect_config.items()]
            else:
                [print('   ', k, ':', v) for k, v in sect_config.items() if k not in def_config_keys]


class ConfigParserUnitTest(unittest.TestCase):
    def test(self):
        test_config = \
"""
[DEFAULT]
TopDir = /usr/local/GIT
UnicodeText = 统一码文本

[X.Y]
PretrainedDir =      pT
# Will default to find from environmental variables instead since "NOSUCHVAR" is not from this file
NoSuchVar = ${NOSUCHVAR}
# In this case will also default to environmental variable, since has no section
UseEnvVar = ${UseEnvVar}

[NLP]
Lang = ru
LangModelDir = ${DEFAULT::TopDir}/data/models/${X.Y::PretrainedDir}/

[NLP2]
DoubleVariable = Double Var ${NLP::LangModelDir}
# Secret = This var $ENV{SECRET_ENV_PASSWORD} is from environment variable
"""
        filepath_tmp = str(uuid.uuid4()) + '.ini'
        print('Create temporary config file "' + str(filepath_tmp) + '"')
        with open(filepath_tmp, 'w', encoding='utf-8') as fh:
            fh.write(test_config)

        cf = Config(
            filepath = filepath_tmp,
            use_envvar_if_var_not_found = True,
        )
        os.environ['NOSUCHVAR'] = '해당 변수 없음'
        os.environ['UseEnvVar'] = '777'
        # os.environ['SECRET_ENV_PASSWORD'] = 'abc888'
        all_config = cf.get_entire_config(
            mask_keys = Config.DEF_MASK_KEYS,
            mask_pct = 0.6,
        )
        self.assertTrue(
            expr = len(all_config) == 4,
            msg = 'Length config sections not 4 but ' + str(len(all_config)) + ': ' + str(all_config)
        )

        for sect, var, expected_val in (
                ('DEFAULT', 'TopDir', '/usr/local/GIT'),
                ('DEFAULT', 'UnicodeText', '统一码文本'),
                ('X.Y', 'PreTrainedDir', 'pT'),
                # Default to environment variable
                ('X.Y', 'NoSuchVar', '해당 변수 없음'),
                ('X.Y', 'UseEnvVar', '777'),
                ('NLP', 'Lang', 'ru'),
                ('NLP', 'LangModelDir', '/usr/local/GIT/data/models/pT/'),
                ('NLP2', 'DoubleVariable', 'Double Var /usr/local/GIT/data/models/pT/'),
                # ('NLP2', 'Secret', 'This var ' + os.environ['SECRET_ENV_PASSWORD'] + ' is from environment variable'),
                # ('NoSuchSection', 'NoSuchVar', None),
        ):
            for use_re in (True, False,):
                val = cf.get(
                    section_name = sect,
                    var_name = var,
                    use_regex_replace_var = use_re,
                )
                self.assertTrue(
                    expr = val == expected_val,
                    msg = 'Use regex "' + str(use_re) + '". Value get "' + str(val) + '" not equal to expected value "'
                          + str(expected_val) + '"',
                )
        print(cf.print_entire_config(mask_keys=[]))
        os.remove(path=filepath_tmp)
        print('Deleted temporary config file "' + str(filepath_tmp) + '"')
        print('ALL TESTS PASSED OK')
        return


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    ConfigParserUnitTest().test()
    exit(0)
