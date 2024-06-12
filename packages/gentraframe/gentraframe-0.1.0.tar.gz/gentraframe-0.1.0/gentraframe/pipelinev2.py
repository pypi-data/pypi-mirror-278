#
# Created on Fri May 31 2024
# Copyright (c) 2024 Huy Truong
# ------------------------------
# Purpose: A generic pypeline
# ------------------------------
#

from typing import Protocol, Any, Optional
import networkx as nx
import matplotlib.pyplot as plt
from gentraframe.config import GTConfig 
from abc import abstractmethod
import inspect
from gentraframe.utils import RunFn


class ModuleV2(Protocol):
    @abstractmethod
    def get_inpout_config(self)-> Optional[GTConfig]: 
        """return the input output config"""
        pass
       
    
class ComponentV2():
    def __init__(self, name: str, inputs: list[str], outputs: list[str], module: ModuleV2) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.module = module
        

    def attach(self, parent: Any) -> tuple[str, list[str], list[str]]:
        self.parent = parent
        return self.name, self.inputs, self.outputs
    
    def run(self, input_dict: dict[str,Any], **kwargs) -> dict[str,Any]: #type:ignore
        """ execute the module
        """
        out_dict = {}
        #get current inpout config
        inpout_config = self.module.get_inpout_config()
        
        #perform module.run        
        #run_fn = self.module.get_run()
        
        assert hasattr(self.module, 'run')
        run_fn: RunFn = getattr(self.module,'run')

        parameters  =  inspect.signature(run_fn).parameters
        assert 'inpout' in parameters, f'inpout is not in the parameters of function {run_fn}'
        inpout_param : inspect.Parameter = parameters['inpout']
        annotation = inpout_param.annotation
        if annotation == inspect.Parameter.empty:
            print('WARNING! param: inpout has to be type defined! Type is unsafe!')
            casted_inpout_config = inpout_config
            out = run_fn(casted_inpout_config, self.outputs, **kwargs)  #type:ignore
        else:
            casted_inpout_config = None
            if inpout_config is not None:
                print(f'annotation = {annotation}')
                print(f'type(annotation) = {type(annotation)}')
                casted_inpout_config = annotation.__origin__(inpout_config)()
                #add values into inpout
                for k in self.inputs:
                    setattr(casted_inpout_config, k, input_dict[k])
            out = run_fn(casted_inpout_config, self.outputs, **kwargs)  
        

        #check attributes and assing values into output dict
        if isinstance(out, dict):
            assert set(self.outputs).intersection(out)
            out_dict = out
        elif isinstance(out, tuple):
            assert len(self.outputs) == len(out)
            out_dict = {o_key: out[i]  for i,o_key in enumerate(self.outputs)}
        else:
            if len(self.outputs) > 0:
                assert len(self.outputs) == 1
                out_dict = {self.outputs[0]: out}
            else:
                out_dict = {}
        #merge the existing values from input_dict
        out_dict.update(input_dict)
        return out_dict


class Pipeline(ComponentV2):
    def __init__(self, name: str, inputs: list[str]=[], outputs: list[str]=[], com_list : list[ComponentV2] = [], verbose: bool=True) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        ##
        self.verbose = verbose
        self.com_dict : dict[str, ComponentV2] = {}
        self.in_dict  = {}
        self.out_dict = {}
        self.name_roots : list[str] = []
        self.g = nx.DiGraph()
        for com in com_list:
            name, inputs, outputs = com.attach(self)
            assert name not in self.com_dict, f'error: name {name} is duplicated! In context of pipeline {self.name}, all names have to be unique!'
            self.com_dict[name] = com 
            self.in_dict[name] = inputs
            self.out_dict[name] = outputs
            self.g.add_node(name, visited=False)

            if len(inputs) == 0:
                self.name_roots.append(name)
        
        
        for i in range(len(com_list)-1):
            i_node  = com_list[i].name
            i_in_nodes = self.in_dict[i_node]
            i_out_nodes = self.out_dict[i_node]
            for j in range(i,len(com_list)):
                j_node  = com_list[j].name
                j_in_nodes = self.in_dict[j_node]
                j_out_nodes = self.out_dict[j_node]

                edge_label = set(i_out_nodes).intersection(j_in_nodes)
                if edge_label:
                    self.g.add_edge(i_node, j_node, edge_label=edge_label)
                
                
                edge_label =set(j_out_nodes).intersection(i_in_nodes)
                if edge_label:
                    self.g.add_edge(j_node, i_node, edge_label=edge_label)
        
        if len(self.name_roots) == 0:
            self.name_roots = [node_name for node_name in self.g.nodes if len(self.g.in_edges(node_name)) == 0]

        if self.verbose:
            nx.draw(self.g, with_labels=True)
            pos = nx.spring_layout(self.g)
            nx.draw_networkx_edge_labels(
                self.g, pos,
                font_color='red',
            )
            plt.show(block=True)
        

    def reset(self):
        for _, node_data in self.g.nodes(data=True): 
            node_data['visited'] = False

    def process_node(self, name: str, next_dict: dict, **kwargs) -> dict:
        if not self.g.nodes[name]['visited']:
            assert set(next_dict.keys()).issuperset(self.in_dict[name])
            next_dict = self.com_dict[name].run(next_dict,   **kwargs)
            assert isinstance(self, Pipeline) or set(next_dict.keys()).intersection(self.out_dict[name]), f'Expected output keys: {self.out_dict[name]}, but get output keys= {next_dict.keys()}'
            self.g.nodes[name]['visited'] = True
        return next_dict

    def run(self, input_dict: dict[str,Any], **kwargs) -> dict[str,Any]: #type:ignore
        next_dict = input_dict
        for root in self.name_roots:
            next_dict = self.process_node(root, next_dict,  **kwargs)
        
        for root in self.name_roots:
            nodes = nx.traversal.bfs_tree(self.g, source = root)
            for node in nodes:
                next_dict = self.process_node(node, next_dict, **kwargs)

        return next_dict
    


Component = ComponentV2
Module = ModuleV2