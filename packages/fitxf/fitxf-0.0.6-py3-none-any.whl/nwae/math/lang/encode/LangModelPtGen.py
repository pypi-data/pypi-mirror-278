import logging
import os
import torch
from nwae.math.lang.encode.LangModelInterface import LmInterface
from nwae.math.lang.encode.LangModelInterfaceX import LmInterfaceX
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from nwae.math.utils.EnvRepo import EnvRepo
from nwae.math.utils.Log import Logging


# https://blog.gopenai.com/bye-bye-llama-2-mistral-7b-is-taking-over-get-started-with-mistral-7b-instruct-1504ff5f373c
# https://medium.com/towards-artificial-intelligence/nsql-first-ever-fully-opensource-sql-foundation-model-f7b501d91ca4
class LmPtGen(LmInterface, LmInterfaceX):

    #
    # Names that follow HuggingFace convention
    # Can pre-cache the following models by git pull into your desired directory
    #   git lfs install
    #   git clone https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L6-v2
    # Generative Models
    LM_MISTRAL_7B_INSTRUCT_V0_1 = 'mistralai/Mistral-7B-Instruct-v0.1'
    # Text to SQL
    LM_NUMBERS_STATION_NSQL_350M = 'NumbersStation/nsql-350M'
    LM_NUMBERS_STATION_NSQL_2B = 'NumbersStation/nsql-2B'

    DEFAULT_MODEL_MAP = {
        'en': LM_MISTRAL_7B_INSTRUCT_V0_1,
        'sql': LM_NUMBERS_STATION_NSQL_350M,
    }

    # Only if we need a different or particular directory name
    LM_PATH_INFO = {
        LM_MISTRAL_7B_INSTRUCT_V0_1: 'mistralai_Mistral-7B-Instruct-v0.1',
        LM_NUMBERS_STATION_NSQL_350M: 'NumbersStation_nsql-350M',
        LM_NUMBERS_STATION_NSQL_2B: 'NumbersStation_nsql-2B',
    }

    def __init__(
            self,
            lang,
            model_name = None,
            cache_folder = None,
            include_tokenizer = True,
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

        self.lang = 'multi' if self.lang not in self.DEFAULT_MODEL_MAP.keys() else self.lang
        self.model_path = None

        self.model_name = self.DEFAULT_MODEL_MAP[self.lang] if self.model_name is None else self.model_name

        self.model_path = self.cache_folder + '/' + self.LM_PATH_INFO.get(self.model_name, self.model_name)
        self.model_path = self.model_path if os.path.isdir(self.model_path) else None
        self.logger.info('Model name "' + str(self.model_name) + '" path "' + str(self.model_path) + '"')

        name_or_path = self.model_name if self.model_path is None else self.model_path
        self.logger.info(
            'Lang model "' + str(self.model_name) + '" with cache folder "' + str(self.cache_folder)
            + '", include tokenizer "' + str(self.include_tokenizer)
            + '", name_or_path "' + str(name_or_path) + '"'
        )
        if self.include_tokenizer:
            self.tokenizer = AutoTokenizer.from_pretrained(
                pretrained_model_name_or_path = name_or_path,
                cache_folder = self.cache_folder,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                # hugging face will know to use the cache folder above, without specifying here it seems
                pretrained_model_name_or_path = name_or_path
            )
        else:
            raise Exception('not supported')
        # except Exception as ex:
        #     errmsg = 'Fail to instantiate SentenceTransformer() for lang "' + str(lang)\
        #              + '" model "' + str(self.model_name) + '", path "' + str(self.model_path) \
        #              + '", cache folder "' + str(self.cache_folder) + '": ' + str(ex)
        #     self.logger.fatal(errmsg)
        #     raise Exception(errmsg)

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        return

    # Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def gen(
            self,
            text_list,
            # max length has got no meaning
            maxlen = 1000,
            return_tensors = 'pt',
            # does not apply here since we can't see the tokenization
            return_attnmasks = False,
            params_other = None,
    ):
        encodeds = self.tokenizer.apply_chat_template(text_list, return_tensors=return_tensors)

        model_inputs = encodeds.to(self.device)
        self.model.to(self.device)

        generated_ids = self.model.generate(model_inputs, max_new_tokens=maxlen, do_sample=True)
        decoded = self.tokenizer.batch_decode(generated_ids)
        return decoded[0]

    def generate_sql(
            self,
            text,
            maxlen = 500,
            return_tensors = 'pt',
    ):
        input_ids = self.tokenizer(text, return_tensors=return_tensors).input_ids
        generated_ids = self.model.generate(input_ids, max_length=maxlen)
        return self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)


if __name__ == '__main__':
    er = EnvRepo()
    lgr = Logging.get_default_logger(log_level=logging.INFO, propagate=False)

    messages = [
        {"role": "user", "content": "What is your favourite condiment?"},
        {"role": "assistant",
         "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
        {"role": "user", "content": "Do you have mayonnaise recipes?"}
    ]

    q1 = """CREATE TABLE stadium (stadium_id number, location text, name text, capacity number)
-- Using valid SQLite, answer the following questions for the tables provided above.
-- how many stadiums in total?
SELECT"""

    q2 = """CREATE TABLE sms (sms_id number, sender number, content text)
CREATE TABLE sender (sender_id number, country text, provider text)
-- Using valid SQLite, answer the following questions for the tables provided above.
-- How many messages were sent by provider Beeline from Russia?
SELECT"""

    lm = LmPtGen(
        lang = 'sql',
        model_name = LmPtGen.LM_NUMBERS_STATION_NSQL_2B,
        cache_folder = er.MODELS_PRETRAINED_DIR,
        logger = lgr,
    )

    for text in [q1, q2]:
        print(lm.generate_sql(text=text))
    exit(0)
