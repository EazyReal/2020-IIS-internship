//the file path should be relative to the path that call `allennlp train`
//usage: `allennlp train "./src_gmn/training_config.jsonnet" -s "./param/testv1"   --include-package "package_v1" --force`
//use amp

local bert_model = "bert-base-uncased";
local train_data_path = "./data/MNLI_Stanza/pre_multinli_1.0_dev_matched.jsonl";
local validation_data_path = "./data/MNLI_Stanza/pre_multinli_1.0_dev_mismatched.jsonl";
local BATCH_SIZE = 32;
local EPOCH = 10;

{
    "dataset_reader" : {
        "type": "nli-graph",
        "wordpiece_tokenizer": {
            "type" : "pretrained_transformer",
            "model_name" : bert_model
        }
    },
    "train_data_path": train_data_path,
    "validation_data_path": validation_data_path,
    "model": {
        "type": "simple_model",
        "embedder": {
            "type": "pretrained_transformer_mismatched",
            "model_name" : bert_model
        },
        "pooler": {
            "type": "boe", //bag_of_embeddings
            "embedding_dim": 768
        }
    },
    "data_loader": {
        "batch_size": BATCH_SIZE,
        "shuffle": true
    },
    "trainer": {
        "type": "gradient_descent",
        "optimizer": "huggingface_adamw",
        "patience": 5,
        "validation_metric": "-loss",
        "num_epochs": 10,
        "checkpointer": null, //use default
        "cuda_device": 0, // use cuda:0
        //"grad_norm": None, gradient norm rescaled to have max norm of this value
        "grad_clipping": 1.0, //gradient clipping
        "learning_rate_scheduler": {
            "type": "linear_with_warmup",
            //"num_epochs": EPOCH, this will be passed by **extras
            "warmup_steps": 100,
            //optimizer: torch.optim.Optimizer, (should this be passed after train command?)
            //num_steps_per_epoch: int = None,
            //last_epoch: int = -1,
        },
        "tensorboard_writer": {
            //"summary_interval" : 100, //default=100
            "histogram_interval": 1000, //default= No Log
            //"batch_size_interval": null, (bug?)
            "should_log_parameter_statistics": true,
            "should_log_learning_rate": true, //default if False
            //get_batch_num_total: Callable[[], int] = None, passed from Trainer
        },
        //moving_average: Optional[MovingAverage] = None,
        //batch_callbacks: List[BatchCallback] = None,
        //epoch_callbacks: List[EpochCallback] = None,
        //distributed: bool = False,
        //local_rank: int = 0,
        //world_size: int = 1,
        //num_gradient_accumulation_steps: int = 1, // this can be enable if want to use batchsize = 1 
        "use_amp": true,
    }
}
