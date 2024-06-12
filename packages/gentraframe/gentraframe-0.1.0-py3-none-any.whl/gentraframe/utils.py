#
# Created on Sun Mar 31 2024
# Copyright (c) 2024 Huy Truong
# ------------------------------
# Purpose: Store general functions
# ------------------------------

import numpy as np
from copy import deepcopy
import torch
from functools import partial
import torch.nn.functional as F
from typing import Any, Callable, Literal, Optional, Union, Protocol, Type
import torch_geometric
from torch_geometric.data import Data
import wandb
import math
import networkx as nx
import torch_geometric.utils as pgu
import timeit
from functools import wraps
from gentraframe.config import GTConfig

class RunFn(Protocol):
    def __call__(self, inpout: Any, outputs : list[str], **kwargs) -> Union[dict[str,Any], tuple, Any]:
        pass

def scale(data: Any, norm_type: str="minmax", mean: Any=None, std: Any=None, min: Any=None, max: Any=None, eps: float=1e-8)->Any:
    """scale function supports normalization

    Args:
        data (Any): unnormed data
        norm_type (str, optional): minmax or znorm . Defaults to "minmax".
        mean (Any, optional): mean values. Defaults to None.
        std (Any, optional): std values. Defaults to None.
        min (Any, optional): min values. Defaults to None.
        max (Any, optional): max values. Defaults to None.
        eps (float, optional): a very small number to avoid zero division. Defaults to 1e-8.

    Returns:
        Any: normed data
    """
    assert norm_type in ['minmax', "znorm"]
    if norm_type == "minmax":
        assert min is not None  and max is not None , "min and max values are missing"
        return (data - min) / (max - min)
    elif norm_type == "znorm":
        assert mean is not None and std is not None , "mean and std values are missing"
        return (data - mean) / (std + eps)
    

def descale(scaled_data: Any, norm_type:str="minmax", mean:Any=None, std:Any=None, min:Any=None, max:Any=None)->Any:
    """Descale function supports denormalization

    Args:
        scaled_data (Any): normed data
        norm_type (str, optional): znorm or minmax. Defaults to "minmax".
        mean (Any, optional): mean values. Defaults to None.
        std (Any, optional): std values. Defaults to None.
        min (Any, optional): min values. Defaults to None.
        max (Any, optional): max values. Defaults to None.

    Returns:
        Any: unnormed data
    """
    if norm_type == 'minmax':
        assert min  is not None and max is not None, "min and max values are missing"
        data = (scaled_data * (max-min)) + min
    elif norm_type == 'znorm':
        assert mean is not None and std is not None, "mean and std values are missing"
        data = (scaled_data * std) + mean
    else:
        data = scaled_data
    return data

    
def nx_to_pyg(data: Any, graph: Data)-> Data:
    """ load data import graph Data containing topology
    Args:
        data (Any): 
        graph (Data): Data converted from nx graph containing topology

    Returns:
        torch_geometric.data.Data: pyg data format
    """
    g_data = deepcopy(graph)
    y = data
    g_data.y = torch.Tensor(np.reshape(y, [-1, 1])) #type:ignore
    g_data.x = torch.Tensor(np.reshape(y, [-1, 1])) #type:ignore
    return g_data

def calculate_classified_accuracy(y_pred, y_true):
    y_true = y_true.max(1)[1].long()#.squeeze().long()
    preds = y_pred.max(1)[1].type_as(y_true)
    correct = preds.eq(y_true).double()
    correct = correct.sum().item()
    return correct / len(y_true) 

def calculate_nse(y_pred, y_true, exponent=2):
    raveled_y_pred = torch.ravel(y_pred) 
    raveled_y_true = torch.ravel(y_true) 
    return 1.0 - torch.div(torch.sum(torch.pow(raveled_y_pred - raveled_y_true, exponent)) , torch.sum(torch.pow(raveled_y_true - torch.mean(raveled_y_true), exponent)) + 1e-12) 

def calculate_rmse(y_pred, y_true):
    return torch.sqrt(torch.mean((y_pred-y_true)**2))

def calculate_rel_error(y_pred, y_true, epsilon: float =1e-6):
    err = torch.abs(torch.subtract(y_true, y_pred))
    mask = (torch.abs(y_true) > 0.01)
    rel_err = torch.abs(torch.divide(err[mask], y_true[mask] + epsilon))
    return torch.mean(rel_err)

def calculate_rel_error2(y_pred, y_true, epsilon: float =1e-4):
    flat_pred = y_pred.reshape([-1,1])
    flat_true = y_true.reshape([-1,1])
    err = torch.abs(torch.subtract(flat_true, flat_pred))
    mask = (torch.abs(flat_true) > 0.01)
    rel_err = torch.abs(torch.divide(err[mask], flat_true[mask] + epsilon))
    return torch.mean(rel_err)


def calculate_accuracy(y_pred, y_true, threshold=0.2):
    mae = torch.abs(torch.subtract(y_true, y_pred))
    acc = (mae <= (y_true * threshold)).float()
    return torch.mean(acc)


def calculate_correlation_coefficient(y_pred, y_true):
    vx = y_pred - torch.mean(y_pred)
    vy = y_true - torch.mean(y_true)

    cost = torch.sum(vx * vy) / (torch.sqrt(torch.sum(vx ** 2)) * torch.sqrt(torch.sum(vy ** 2)))
    #cov    = torch.mul(y_pred-y_pred.mean(), y_true-y_true.mean()).mean()
    #std   = torch.sqrt(torch.mul(torch.square(y_pred-y_pred.mean()), torch.square(y_true-y_true.mean()))).mean()
    
    return torch.clamp(cost, -1.0, 1.0)

def calculate_r2(y_pred, y_true):
    r = calculate_correlation_coefficient(y_pred, y_true)
    return r**2

def inverse_mask_tuple(mask_tuple : tuple) -> tuple:
    inverse_tuple = [~x for x in mask_tuple]
    return tuple(inverse_tuple)

def apply_masks(x: torch.Tensor, masks: list[torch.Tensor]):
    # x has shape (num_masks, batch_size * num_graphs, num_features)
    # masks has length = num_masks, masks's element has shape  (batch_size* num_graphs)

    num_masks = len(masks)
    if num_masks == 1:
        if len(x.size()) == 2:
            return x[masks[0]]
        else:
            return x.squeeze(0)[masks[0]]


    xs=[]
    for i in range(num_masks):
        mask = masks[i]
        xs.append(x[i][mask])

    # out has shape = (num_masks, batch_size * num_graphs, num_features)
    return torch.cat(xs,dim=0)


def get_metric_fn_collection(prefix:str, task: Literal['supervised','semi'] = 'semi')->dict:
    """util creating metric funtions

    Args:
        prefix (str): set a prefix name for tracking these experiment

    Returns:
        dict: contains functional name and callable functions
    """
    if task == 'semi':
        metric_fn_dict= {
            f'{prefix}_error': calculate_rel_error2,
            f'{prefix}_0.1': partial(calculate_accuracy,threshold=0.1),
            f'{prefix}_corr': calculate_correlation_coefficient,
            f'{prefix}_r2': calculate_r2,
            f'{prefix}_mae': F.l1_loss,
            f'{prefix}_rmse': calculate_rmse,
            f'{prefix}_mynse': partial(calculate_nse,exponent=2),
        }
    else:
        metric_fn_dict= {
            f'{prefix}_acc': calculate_classified_accuracy,
        }
    return metric_fn_dict

def get_linear_probing_metric_fn_collection(prefix:str, task: Literal['supervised','semi'] = 'semi')->dict:
    """util creating metric funtions

    Args:
        prefix (str): set a prefix name for tracking these experiment

    Returns:
        dict: contains functional name and callable functions
    """
    if task == 'semi':
        metric_fn_dict= {
            f'{prefix}_error': calculate_rel_error2,
            f'{prefix}_mae': F.l1_loss,
            f'{prefix}_rmse': calculate_rmse,
        }
    else:
        metric_fn_dict= {
            f'{prefix}_acc': calculate_classified_accuracy,
        }
    return metric_fn_dict

def load_checkpoint(path: str, model: torch.nn.Module, load_key:str ='model_state_dict') -> tuple[torch.nn.Module, dict]:
    """support load model and relevant data

    Args:
        path (str): checkpoint file
        model (torch.nn.Module): a model architecture to load weights into
        load_key (str): a key indicate the corresponding model weights

    Returns:
        tuple[torch.nn.Module, dict]: tuple of loaded model and relevant data as dict
    """
    models, cp_dict = load_custom_checkpoint(path, models= [model], load_keys=[load_key])
    return models[0], cp_dict

def load_custom_checkpoint(path: str, models: list[torch.nn.Module], load_keys: list[str]) -> tuple[list[torch.nn.Module], dict]:
    """support load multiple models and relevant data

    Args:
        path (str): checkpoint file
        models (list[torch.nn.Module]): model architectures to load weights into
        load_keys (list[str]): key list indicate the corresponding model weights

    Returns:
        tuple[list[torch.nn.Module], dict]: tuple of list of loaded model and relevant data as dict
    """
    assert path[-4:] == '.pth'
    assert models is not None
    assert len(load_keys) == len(models)
    cp_dict = torch.load(path)
    for i in range(len(models)):
        name = models[i].name if hasattr(models[i],'name') else type(models[i]).__name__
        if load_keys[i] in cp_dict:
            try:
                models[i].load_state_dict(cp_dict[load_keys[i]])
                print(f'Model at position {i}...loaded')
            except RuntimeError:
                print(f'Unable to load weights from {load_keys[i]} to model {name}! Use new model instead!')
        else:
            print(f'WARNING! models at position {i} has no state dict! Use new model instead!')
    return models, cp_dict

def save_checkpoint(path:str,**kwargs) ->str:
    """support save checkpoint. User can leverage kwargs to store model and relevant data

    Args:
        path (str): saved path

    Returns:
        str: saved path
    """
    torch.save(kwargs,path)
    return path

def print_single_metrics(epoch:int, **kwargs):
    formatter =f'Epoch: {epoch:03}, ' # f'Epoch: {epoch:0.3d}'
    for k, v in kwargs.items():
        if isinstance(v, dict):
            for sk, sv in v.items():
                formatter +=  f'{sk}: {sv:.4f}, '
        else:
            formatter += f'{k}: {v:.4f}, '
    print(formatter)

def print_metrics(epoch:int,tr_loss:float,val_loss:float, tr_metric_dict:dict, val_metric_dict:dict):
    """support pretty print string format

    Args:
        epoch (int): current epoch/ trial
        tr_loss (float): training loss
        val_loss (float): validation loss
        tr_metric_dict (dict): training metric dict including name, values
        val_metric_dict (dict): validation metric dict including name, values
    """
    metric_log = ''

    for k, v in tr_metric_dict.items():
        metric_log += f'{k}: {v:.4f}, '
    
    if val_metric_dict:
        for k, v in val_metric_dict.items():
            metric_log += f'{k}: {v:.4f}, '
    
    formatter =  f"Epoch: {epoch:03d}, train loss: {tr_loss:.4f},"
    formatter += f"val_loss: {val_loss:.4f}," if val_loss else ''
    formatter += f" {metric_log}"
    print(formatter)

def print_multitest_metrics(trials:int,mean_test_loss:float, std_test_loss:float,mean_test_sensor_loss:float,std_test_sensor_loss:float,out_test_metric_dict:dict, out_test_sensor_metric_dict:dict ):
    """support beautifying string format for multi-trial evaluation

    Args:
        trials (int): number of trials
        mean_test_loss (float): mean of test losses
        std_test_loss (float): std of test losses
        mean_test_sensor_loss (float): mean of test sensor losses
        std_test_sensor_loss (float): std of test sensor losses
        out_test_metric_dict (dict): metric dict contains mean, std and raw measurment values in trials runs
        out_test_sensor_metric_dict (dict): metric dict contains mean, std and raw measurment sensor values in trials runs
    """
    metric_log = ''
    for k, v in out_test_metric_dict.items():
        if 'mean' in k:
                name = k[:-5]
                std = out_test_metric_dict[f'{name}_std']
                metric_log += f'{name}: {v:.4f} +/- {std:.4f}, '

    for k, v in out_test_sensor_metric_dict.items():
        if 'mean' in k:
                name = k[:-5]
                std = out_test_sensor_metric_dict[f'{name}_std']
                metric_log += f'sensor_{name}: {v:.4f} +/- {std:.4f}, '

    print(f'\nThis TEST experiment reports the average result of {trials} runs.') 
    print(f"test_loss: {mean_test_loss:.4f} +/- {std_test_loss:.4f}, sensor_test_loss: {mean_test_sensor_loss:.4f} +/- {std_test_sensor_loss:.4f}, {metric_log}")
    
def get_gradient_norm(model: torch.nn.Module,norm_type = 2)-> tuple[torch.Tensor, list[torch.Tensor], list[str]]:
    """support get gradient norms from a model. Tracking modules whose names has 'block', 'mlp' or 'res' words

    Args:
        model (torch.nn.Module): any torch module 
        norm_type (int, optional): calculated type of norm. Defaults to 2.

    Returns:
        tuple[torch.Tensor, list[torch.Tensor], list[str]]: returned sum norms of all blocks, list of each norms, list of each name
    """
    block_norms = []
    block_names = []
    for name,param in model.named_parameters():
        # if 'block' in name or 'mlp' in name or 'res' in name :
        #     block_norms.append(torch.norm(param.grad.detach() , p=norm_type) ) 
        #     block_names.append(name)

        if (param.grad is not None) and not (name.endswith('.bias') or len(param.shape) == 1):
            block_norms.append(torch.norm(param.grad.data, p=norm_type))
            block_names.append(name)


    total_norm =  torch.norm(torch.stack(block_norms), norm_type)
    return total_norm, block_norms,block_names

def log_metrics_on_wandb(epoch:int,commit:bool=True, is_epoch_a_trial=False, **kwargs):
    """support function allowing to push log to wandb server

    Args:
        epoch (int): deterministic epoch
        commit (bool, optional): if it is one of non-last incremental logs, set it to True. Defaults to True.
    """
    for k,v in kwargs.items():
        if isinstance(v,dict):
            wandb.log(v,commit=False)
        else:
            wandb.log({k:v},commit=False)
    if is_epoch_a_trial:
        wandb.log({'trial': epoch},commit=commit)
    else:
        wandb.log({'epoch': epoch},commit=commit)

def create_random_graph(num_nodes:int, edge_form_prob:float = 0.5, include_pos:bool=True, radius= 10, graph_id = 0) -> Data: 
    G = nx.gnp_random_graph(num_nodes, edge_form_prob, directed=False) 
    test_features = {}
    pos_features = {}
    g_features = {}
    # sign = 1
    # for i, node_name in enumerate(G.nodes()): 
    #     test_features[node_name] = i
    #     pos_features[node_name] = (i, sign * i)
    #     sign = -1 * sign

    r = radius
    horizontal_distance_between_graphs = graph_id * 4*radius
    for i, node_name in enumerate(G.nodes()): 
        test_features[node_name] = i 
        pos_features[node_name] = (r * np.cos(i/num_nodes * 2* np.pi) + horizontal_distance_between_graphs, r * np.sin(i/num_nodes * 2* np.pi)) if i !=0 else (horizontal_distance_between_graphs,0)
        g_features[node_name] = graph_id

    nx.set_node_attributes(G, test_features, name='x')
    nx.set_node_attributes(G, g_features, name='graph_id')
    if include_pos:
        nx.set_node_attributes(G, pos_features, name='pos') 
    return pgu.from_networkx(G)

    
def measure(func, repeat=3, number=10000):
    """Include debug statement and timeit setup"""
    @wraps(func)
    def wrapper(*args,**kwargs):
        res = func(*args,**kwargs)
        times = timeit.repeat(
            stmt=lambda: func(*args,**kwargs),
            repeat=repeat, number=number)
        print(f'The function was run in {repeat} times. The mean execution time is {sum(times)/repeat} seconds.')
        return res

def load_secret(secret_path:str) -> Optional[dict]:
    if secret_path is None:
        return None 
    secret_extension = secret_path[-2:]
    if secret_extension == 'py':
        import importlib.util
        import sys
        spec = importlib.util.spec_from_file_location("mysecret", secret_path)
        module = importlib.util.module_from_spec(spec)#type:ignore
        sys.modules["mysecret"] = module 
        spec.loader.exec_module(module) #type:ignore
        return module.secrets
    else:
        raise NotImplementedError()
    
def get_criterion(loss_name: str, device: str) -> Callable:
    """ get loss by name """
    if loss_name == 'sce':
        def sce_loss(x, y, alpha = 3):
            x = F.normalize(x,p=2,dim=-1)
            y = F.normalize(y,p=2,dim=-1)
            loss = (1.0 - (x*y).sum(dim=-1)).pow_(alpha)
            return loss.mean()

        criterion = sce_loss
    elif loss_name == 'mse':
        criterion = torch.nn.MSELoss(reduction="mean").to(device)
    elif loss_name == 'mae':
        criterion = torch.nn.L1Loss(reduction="mean").to(device)
    elif loss_name == 'ce':
        criterion =torch.nn.CrossEntropyLoss(reduction="mean").to(device)
    else:
        raise KeyError(f'criterion {loss_name} is not supported')

    return criterion