#
# Created on Fri May 31 2024
# Copyright (c) 2024 Huy Truong
# ------------------------------
# Purpose: 
# ------------------------------
#
from typing import Literal, Any
from tap import Tap
import yaml
import os

class GTConfig(Tap):
    
    """An abstract config for inheritance
    """
    def _from_yaml(self, yaml_path, skip_unsettable=False)->None:
        assert yaml_path[-4:] == 'yaml'
        assert os.path.isfile(yaml_path)

        with open(yaml_path, 'r') as yaml_in:
            yaml_object = yaml.unsafe_load(yaml_in) #yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
            
            self.from_dict(yaml_object,skip_unsettable=skip_unsettable)

    def _to_yaml(self, yaml_path)->dict:
        from collections import OrderedDict
        assert yaml_path[-4:] == 'yaml' 

        kv_dict = self.as_dict()
        yaml_object = OrderedDict()
        for cv in self.class_variables:
            assert cv in kv_dict, f'class_variables has a key {cv} is not found in kv_dict'
            yaml_object[cv] = kv_dict[cv]

        #Order reservation in YAML file# ref: https://stackoverflow.com/questions/45253643/order-preservation-in-yaml-via-python-script    
        def ordered_dict_representer(self, value): 
            return self.represent_mapping('tag:yaml.org,2002:map', value.items())
        
        yaml.add_representer(OrderedDict, ordered_dict_representer)
        with open(yaml_path,'w') as yaml_out:
            yaml.dump(yaml_object, yaml_out, indent = 4, sort_keys=False)

        return yaml_object
    

# class PipelineConfig(GTConfig):
#     task: Literal['semi','supervised'] # task we work with
#     node_in_dim: int = -1 # node in dim
#     edge_in_dim: int = -1 # edge in dim
#     out_dim: int = -1 # label out dim

class ModelConfig(GTConfig):
    name : Literal['gcn','gatres', 'gatres_encoder', 'gatres_predictor', 'ffn', 'gatres','linear'] = 'gcn' #name of the model
    num_layers: int = 2 #number of layers
    nc: int = 16 #number of hidden nc
    act: Literal['relu','gelu'] = 'relu' #activation
    has_final_linear: bool = False # if true, add a linear following the gnn layers
    weight_path: str # path storing the model weights
    do_load: bool # load weights of the model 

class TrainConfig(GTConfig):
    model_path: str = '' #temp
    do_load: bool = False # flag represents temporarily global setting for all mdoels
    model_configs: list[ModelConfig] = [] # involving DL models in this train
    lr: float= 0.01 #0.01 #Learning rate. Default is 0.0005
    weight_decay: float= 5e-4 #weight decay. Default is 0.000006
    epochs: int= 100 #number of epochs to train the model
    mask_rate: float=0.95 #masking ratio. Default is 0.95
    criterion: Literal["mse", "mae", "sce","ce"] ='ce' # criterion loss. Support mse|sce|mae
    batch_size: int= 64 #batch size
    use_data_batch: bool=False #pass pyg data batch as parameter into model. Set False to fasten training. Default is False
    use_data_edge_attrs: str= None # pass pyg data edge attributes. Eg: [diameter,length] for multi-use. Support: diameter| length| None #type:ignore
    device:str='cuda' #Training device. If gpu is unavailable, device is set to cpu. 
    norm_type: Literal["znorm", "minmax", "unused"]='unused' #normalization type. Support znorm| minmax|unused"
    use_gradient_clipping=False # flag indicating whether using gradient clipping.
    """###########################TRACKING EXPERIMENTS SETTINGS################################"""
    log_method: str = '' #log method! Support wandb or None
    #log_gradient: bool = False #flag indicates keeping track of gradient flow
    project_name: str ='dev-pretext-train' #name of tracking project"
    save_path: str = 'experiments_logs/test_args/fun_test' #Path to store model weights
    log_per_epoch: int = 1# log every log_per_epoch 
    """#########################################################################################"""
    
    def configure(self) -> None:
        def str_or_none(string: str) -> str:
            return string if string is not None else None # type:ignore
        self.add_argument('--use_data_edge_attrs',type=str_or_none)
    

