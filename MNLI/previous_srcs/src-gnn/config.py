import os
from pathlib import Path

######################################
# must change save_model_folder to designate save param path
# statistics will go to the save_model_folder too
#####################################

# whether log when executing
DEBUG = True
LOG = True
#log file path is below

######################################
# Paths 
######################################
SRC_ROOT = Path(os.path.dirname(os.path.realpath(__file__)))
PROJ_ROOT = SRC_ROOT.parent #care if multi source under src

DATA_ROOT = PROJ_ROOT / "data" / "multinli_1.0"
PARAM_PATH = PROJ_ROOT / "param"

PDATA_ROOT = PROJ_ROOT / "data" / "MNLI_Stanza"

# GLOVE path
GLOVE_ROOT = PROJ_ROOT / "data" / "glove_embedding"
GLOVE_NAME = "glove.42B.300d.txt"
GLOVE = GLOVE_ROOT / GLOVE_NAME
GLOVE_VOCAB = GLOVE_ROOT / "glove.42B.300d.vocab.pkl"
GLOVE_WORD2ID = GLOVE_ROOT / "glove.42B.300d.word2id.pkl"
GLOVE_SAVED_TENSOR = GLOVE_ROOT / "glove.42B.300d.tensor.pkl"
GLOVE_DIMENSION = 300
GLOVE_VOCAB_SIZE = 1917496

# data path
DEV_MMA_FILE = DATA_ROOT / "multinli_1.0_dev_mismatched.jsonl"
DEV_MA_FILE = DATA_ROOT / "multinli_1.0_dev_matched.jsonl"
TRAIN_FILE = DATA_ROOT / "multinli_1.0_train.jsonl"

# processed data
PDEV_MMA_FILE = PDATA_ROOT / "pre_multinli_1.0_dev_mismatched.jsonl"
PDEV_MA_FILE = PDATA_ROOT / "pre_multinli_1.0_dev_matched.jsonl"
PTRAIN_FILE = PDATA_ROOT / "pre_multinli_1.0_train.jsonl"

# save model
SAVE_MODEL_FOLDER = "SynNLIv0.1_glove_GAT3_test_before_migration"
LOG_FILE_PATH =  PARAM_PATH / SAVE_MODEL_FOLDER / "train_log.txt"
PURE_TRAIN_STAT_PATH = PARAM_PATH / SAVE_MODEL_FOLDER / "stat.jsonl"

######################################
# Preprocssing Config / Data related
######################################
label_to_id = {
    "contradiction" : 0,
    "neutral" : 1,
    "entailment" : 2,
}
id_to_label = label_to_id.keys()

h_field = "sentence2"
p_field = "sentence1"
label_field = "gold_label"
# alias
hf = "sentence2"
pf = "sentence1"
lf = "gold_label"
idf = "pairID"

######################################
# MODEL
######################################
#CROSS_ATTENTION_HIDDEN_SIZE = 392
NUM_CLASSES = 3
EMBEDDING_D = 300
HIDDEN_SIZE = 300

# Bert Enbedding
BERT_EMBEDDING = "bert-base-uncased" #cased?
BERT_MAX_INPUT_LEN = 512

# NLI Model config class and instance

# for conv encoder
NUM_CONV_LAYERS = 3
NUM_CONV_ATT_HEADS = 3

# for big model
class Model_Config():
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
        return

nli_config_dict = {
    "hidden_size" : 300,
    "embedding" : "glove300d",
    "encoder" : "gat",
    "cross_att" : "scaled_dot",
    "aggregation" : "max",
    "prediction" : "2-layer-FNN",
    "activation" : "relu"
}

nli_config = Model_Config(nli_config_dict)

######################################
# Trainning
######################################
"""
reference for bert fine-tuning
BATCH_SIZE = # 32 / 16 / 8
NUM_EPOCHS = # 2 / 3 / 4
LR = # 5/3/2 1e-5
WEIGHT_DECAY = 0.01

reference for KAGNet
BATCH_SIZE = 64
NUM_EPOCHS = 10
LR = 1e-3
"""
BATCH_SIZE = 32 # 32 / 16 / 8
NUM_EPOCHS = 5 # 2 / 3 / 4
LR = 5*1e-4 # 5/3/2 1e-5 for finetuning, 1e-3/4 for training?
WEIGHT_DECAY = 0.01
MAX_GRAD_NORM = 1.0
NUM_WARMUP = 100
DROUP_OUT_PROB = 0.1

follow_batch = ["x_p", "x_h", "label"]
tensor_attr_list = ["edge_index_p", "edge_index_h", "x_p", "x_h", "label"]