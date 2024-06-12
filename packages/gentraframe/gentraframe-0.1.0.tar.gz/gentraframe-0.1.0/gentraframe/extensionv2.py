#
# Created on Fri Apr 26 2024
# Copyright (c) 2024 Huy Truong
# ------------------------------
# Purpose: create a module for pipeline
# ------------------------------
from copy import deepcopy
from typing import  Any, Literal, Optional, Union, Type
from torch import nn
from torch_geometric.data import Data, Dataset
from torch_geometric.datasets.planetoid import Planetoid
from torch_geometric.transforms import NormalizeFeatures
import torch_geometric.utils as pgu
import torch.nn.functional as F
import torch
from torch_geometric.nn import GCN, MLP, GCNConv
from gentraframe.config import ModelConfig, TrainConfig, GTConfig
from gentraframe.utils import RunFn



class CustomDataset(Dataset):
    def __init__(self, data_list):
        super(CustomDataset, self).__init__()
        self.data_list = data_list

    def len(self):
        return len(self.data_list)

    def get(self, idx):
        return self.data_list[idx]
    
class MyCora3(Planetoid):

    def __init__(self, 
                 do_scale:bool,
                 root:str, 
                 remove_isolated:bool,
                 ) -> None:
        
        norm_features_tf = NormalizeFeatures() if do_scale else None
        super().__init__(root=root, 
                         name='Cora',
                         #split='public', 
                         transform= norm_features_tf)
        self.remove_isolated = remove_isolated
        
    def get_set(self, from_set:Literal['train','val','test'], task: Literal['semi','super']) ->  Dataset:
        mask_name = f'{from_set}_mask'
        data = self.get(0)
        assert hasattr(data, mask_name)
        mask = getattr(data, mask_name)
        new_data = deepcopy(data)
        if task == 'semi':
            new_data.x = new_data.x[mask]
            new_data.y =  deepcopy(new_data.x)
        else:
            new_data.x = new_data.x 
            new_data.y = F.one_hot(new_data.y[mask], self.num_classes).to(torch.float32) # new_data.y[mask] # new_data.y[mask] #
            new_data.mask = mask
            
        if self.remove_isolated:
            keep_indices = pgu.mask_to_index(mask)
            new_data.edge_index, new_data.edge_attr=  pgu.subgraph(keep_indices,edge_index=new_data.edge_index, edge_attr= new_data.edge_attr, relabel_nodes=True, return_edge_mask=False) #type:ignore
            
        return CustomDataset([new_data])
      
class CoraProvider:
    class MyConfig(GTConfig):
        task: str
        from_sets: list[Literal['train','val','test']]


    def get_inpout_config(self)-> GTConfig: 
        return CoraProvider.MyConfig()

    def run(self, inpout : Type[MyConfig], outputs : list[str], **kwargs) -> Union[dict[str,Any], tuple, Any]: 
    #def run(self, input_dict: dict[str,Any], output_keys: list[str], **kwargs)-> Union[dict[str,Any], tuple, Any]:
        task = inpout.task
        from_sets = inpout.from_sets
        self.my_cora = MyCora3( do_scale=True, root= 'cora', remove_isolated= (task == 'semi')) 
        #communicate with pipeline config
        sample : Data =   self.my_cora.get_set(from_set=from_sets[0], task= task).get(0) #type:ignore
        in_dim = sample.x.shape[-1]  #type:ignore
        out_dim = sample.y.shape[-1] #type:ignore
        print(sample)

        output_dict = {}
        output_dict['in_dim'] = in_dim
        output_dict['out_dim'] = out_dim
        output_dict['datasets'] = [self.my_cora.get_set(from_set=from_set, task=task)  for from_set in from_sets ] #type:ignore

        return output_dict
    
    
class DefaultModelBuilder:
    class MyConfig(GTConfig):
        in_dim: int
        out_dim: int

    def get_inpout_config(self)-> GTConfig: 
        return CoraProvider.MyConfig()
    def _get_single_model(self, config : ModelConfig, in_dim: int, out_dim:int)->nn.Module:
        name = config.name
       
        assert in_dim >0 and out_dim >0
        
        if name == 'gcn':
            return GCN(hidden_channels=config.nc,
                       num_layers=config.num_layers,
                       in_channels=in_dim,
                       out_channels=out_dim,
                       act= config.act,
                       act_first=True,
                       )
        elif name in ['ffn','mlp']:
            return MLP(hidden_channels=config.nc,
                       num_layers=config.num_layers,
                       in_channels=in_dim,
                       out_channels=out_dim,
                       act= config.act,
                       norm = None,
                       )
        elif name =='linear':
            return MLP(hidden_channels=config.nc,
                       num_layers=1,
                       in_channels=in_dim,
                       out_channels=out_dim,
                       act= None,
                       norm = None,
                       )
        else:
            raise NotImplementedError(f'{name} is not supported.')

    def get_model_by_config(self, model_config: ModelConfig, in_dim : int, out_dim: int) -> nn.Module:
        model = self._get_single_model(model_config,in_dim= in_dim, out_dim= out_dim)
        setattr(model, 'name', model_config.name)
        return model
    
    def run(self, inpout: Type[MyConfig], outputs: list[str],config: TrainConfig , **kwargs)-> Union[dict[str,Any], tuple, Any]:
        in_dim = inpout.in_dim
        out_dim = inpout.out_dim

        models = [self.get_model_by_config(model_config, in_dim, out_dim)  for model_config in config.model_configs]
        
        return models
    
    
    
    