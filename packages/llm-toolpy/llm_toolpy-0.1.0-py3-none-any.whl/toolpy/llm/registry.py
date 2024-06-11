import abc
import enum
import threading
import warnings
from typing import List, Union, Dict, final, Optional

from .interface import LLMInterface

class LLMRegistry:
    _registry :Dict[str, LLMInterface] = dict()
    _default_model : Optional[str] = None

    def registry(self, model_name:str, interface:LLMInterface, 
                 default:bool=False) -> None:
        
        if model_name in self._registry:
            raise ValueError(f"Model with name {model_name} was already \
                            registred.")

        self._registry[model_name] = interface

        if default:
            self.set_default_model(model_name)

    def get_model(self, model_name:Optional[str]) -> LLMInterface:
        if (model_name is not None) and (model_name not in self._registry):
            raise ValueError(f"Model with name {model_name} is not \
                             registred.")
        
        elif model_name is None:
            if self._default_model is None:
                raise RuntimeError("No default model was defined.")

            model_name = self._default_model
        
        return self._registry[model_name]
    
    def set_default_model(self, model_name:str) -> None:
        if model_name not in self._registry:
            raise ValueError(f"Model with name {model_name} is not \
                             registred.")
        
        LLMRegistry._default_model = model_name