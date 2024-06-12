#
# Created on Tue Apr 16 2024
# Copyright (c) 2024 Huy Truong
# ------------------------------
# Purpose: Evaluator is for supervised, semi-superved, linear prob, fine-tune evaluations
# ------------------------------
#
from typing import Union
from torch.nn.modules import Module
from gentraframe.trainer import Trainer, SingleTrainer
from gentraframe.gen_random_mask_v8 import generate_batch_mask
from gentraframe.utils import *
from gentraframe.config import TrainConfig
from torch_geometric.loader import DataLoader
import torch
from datetime import datetime
import wandb
import time
import numpy as np


class DefaultEvaluator(Trainer):
    def run(self, input_dict: dict[str,Any],  output_keys: list[str], config: TrainConfig) -> Union[dict[str,Any], tuple, Any]:
        task = input_dict['task']
        models = input_dict['models']
        datasets = input_dict['datasets']
        model_path = input_dict['model_paths'][0]
        """perform training or testing"""
        train_args = config

        do_load = config.do_load

        #check conditions
        assert models is not None and len(models) > 0
        assert datasets is not None and len(datasets) >= 1

        #setup some configs
        edge_attrs = train_args.use_data_edge_attrs.split(',') if train_args.use_data_edge_attrs is not None else None
        
        test_loader = DataLoader(datasets[-1], batch_size=train_args.batch_size, shuffle=False) #type:ignore

        device = train_args.device if train_args.device == 'cuda' and torch.cuda.is_available() else 'cpu'
        model_names = [ model.name if hasattr(model,'name') else type(model).__name__ for model in models] #type:ignore
        setattr(train_args, 'model_name', '+'.join(model_names) )
        run_name, postfix = self.start_profiler(task, train_args)
        models = self.load(models, model_path= model_path, device=device, do_load= do_load)
        print('#'*80)
        print(self.as_dict(train_args))
        print('#'*80)
        if task == 'semi':
            print(f'gen-mask version: {generate_batch_mask.__module__}')

        # get loss fn
        criterion = get_criterion(train_args.criterion, device= device)
        
        # gather metrics
        test_metric_fn_dict=  get_metric_fn_collection(prefix='test', task = task) 
       
        #intial records
        best_loss = np.inf
        best_error = np.inf
        best_acc = 0
        best_epoch = 0
        
        start_time = time.time()
        dt1 = datetime.fromtimestamp(start_time)
        print('Start time:', dt1)
        print("*" * 80)

        #############
        #TODO: norm configs should be defined here
        ############
        
        test_loss, test_metric_dict = self.test_one_epoch(models=models,
                                                    loader= test_loader,
                                                    criterion= criterion, 
                                                    metric_fn_dict = test_metric_fn_dict,
                                                    config=train_args,
                                                    task=task,
                                                    )
        
        print_single_metrics(epoch= 0,
                             test_loss=test_loss,
                             test_metric_dict= test_metric_dict)

        if train_args.log_method == 'wandb':
            log_metrics_on_wandb(epoch=0,
                            commit=True,
                            test_loss=test_loss,
                            best_loss=best_loss,
                            best_epoch=best_epoch,
                            test_metric_dict=test_metric_dict,
                            )
                
        end_time = time.time()
        dt2 = datetime.fromtimestamp(end_time) 
        print("*" * 80)
        print('End time:', dt2)
        print('Training time:', dt2 - dt1)

        if train_args.log_method == 'wandb':
            wandb.finish()
        
        return []
    
class SingleEvaluator(DefaultEvaluator, SingleTrainer):
    
    def test_one_epoch(self, models: list[torch.nn.Module],
                        loader: DataLoader,
                        criterion : Callable, 
                        metric_fn_dict: dict[str, Callable],
                        config: TrainConfig,
                        task: str,
                        **kwargs) -> tuple[float, dict]:  
        return DefaultEvaluator.test_one_epoch(self, models, loader, criterion, metric_fn_dict, config, task,  **kwargs)

    def forward_fn(self, models: list[Module], data: Data, batch_mask: Optional[torch.Tensor] = None) -> Any:
        return SingleTrainer.forward_fn(self, models, data, batch_mask)

# class LinearProbingEvaluator(Trainer):

#     @abstractmethod
#     def forward_fn(self, models: list[torch.nn.Module], data: Data, batch_mask: Optional[torch.Tensor] = None) -> Any:
#         pass

#     def get_linear_model(self, in_dim: int, out_dim:int) -> torch.nn.Module:
#         pl: IterPipeline = getattr(self,'pl')
#         pl.pl_config.in_dim = in_dim
#         pl.pl_config.out_dim = out_dim

#         new_model_config = ModelConfig().parse_args()
#         new_model_config.name = 'linear'
#         new_model_config.nc = 1
#         new_model_config.act = None #type:ignore

#         linear_model = pl.model_builder.get_single_model(new_model_config)
#         return linear_model

#     def fit(self, models: list[torch.nn.Module], datasets: list[Dataset], prev_paths: list[str] = []) -> list[str]: 
#         """perform training or testing"""
#         pl_args = self.pl_config
#         args = self.args
#         encoders = models

#         model_path = prev_paths[0]  if len(prev_paths) > 0 else pl_args.model_path 
        
#         task = pl_args.task
#         do_load = True #pl_args.do_load
#         #check conditions
#         assert encoders is not None and len(encoders) > 0
#         assert datasets is not None and (len(datasets) == 2 or len(datasets) ==3)

#         #setup some configs
#         #edge_attrs = args.use_data_edge_attrs.split(',') if args.use_data_edge_attrs is not None else None
#         #use_data_batch = args.use_data_batch
#         device = args.device if args.device == 'cuda' and torch.cuda.is_available() else 'cpu'
#         encoders = self.load(encoders, model_path= model_path, device=device, do_load= do_load)
        
#         [m.eval() for m in encoders]
#         #create embeddings
#         data_dict = {'train': [], 'val': []} if len(datasets) == 2 else  {'train': [], 'val': [], 'test':[]}
#         with torch.no_grad():
#             for key, dataset in zip(list(data_dict.keys()), datasets) :
#                 loader = DataLoader(dataset, batch_size=args.batch_size, shuffle= (key == 'train') ) 
#                 for data in loader:
#                     data.x = data.x.to(device)
#                     data.y = data.y.to(device)
#                     data.edge_index = data.edge_index.to(device)
#                     emb = self.forward_fn(models=encoders, data=data, batch_mask= None)
#                     data.x = emb
#                     if task == 'semi':
#                         data.y = deepcopy(data.x) #data.x.clone()

#                     data_dict[key].append(data)
        
#         #create linear probing loaders
#         in_dim =  data_dict['train'][0].x.shape[-1]
#         out_dim = data_dict['train'][0].y.shape[-1]

#         model = self.get_linear_model(in_dim, out_dim)
#         model.to(device)
        
#         lp_datasets = [data_dict['train'], data_dict['val']] if 'test' not in data_dict else [data_dict['train'], data_dict['val'], data_dict['test']] 

#         self.pl_config.do_load = False
#         return super().fit(models=[model], datasets=lp_datasets) #type:ignore


# class LinearProbingSingleEvaluator(LinearProbingEvaluator, SingleTrainer):
    
#     def forward_fn(self, models: list[Module], data: Data, batch_mask: Optional[torch.Tensor] = None) -> Any:
#         return SingleTrainer.forward_fn(self, models, data, batch_mask)