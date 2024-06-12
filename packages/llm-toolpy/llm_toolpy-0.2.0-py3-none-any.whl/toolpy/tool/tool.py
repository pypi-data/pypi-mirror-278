import abc
import json
from types import MappingProxyType
from typing import Dict, Union, List, final, Optional, Tuple

from toolpy.llm import LLMRegistry, QueryLike

TextLike = Union[str, List[str], Dict[str, "TextLike"]]

class Tool(abc.ABC):
    '''
    Base class for creating LLM tools.
    '''

    def __init__(self, description:str, input_description:Dict[str, str], model_name:Optional[str] = None) -> None:
        super().__init__()

        self._model_name = None
        self._description = description
        self._input_description = input_description

    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_description(self) -> MappingProxyType[str, str]:
        return MappingProxyType(self._input_description)

    @final
    def __call__(self, query:Optional[Dict[str, str]]=None, 
                 context:Optional[str]=None) -> Tuple[Dict[str, TextLike], Dict[str, str]]:
        '''
        Execute the tool.

        Args:
            query (str): query for the tool execution.
            context (str): context in the tool execution moment.

        Returns:
            Dict[str, TextLike]: tool result.
            Dict[str, str]: result keys description.
        '''
        return self._execute(query, context)

    @abc.abstractmethod
    def _execute(self, query:Optional[Dict[str, str]], 
                context:Optional[str]) -> Tuple[Dict[str, TextLike], Dict[str, str]]:
        '''
        Execute the tool.

        Args:
            query (str): query for the tool execution.
            context (str): context in the tool execution moment.

        Returns:
            Dict[str, str]: tool results.
        '''
        ...

    def _query(self, prompt:QueryLike, json_mode:bool=False) -> TextLike:
        registry = LLMRegistry()
        interface = registry.get_model(self._model_name)
        
        result = interface.query(prompt, json_mode)

        if json_mode:
            result = json.loads(result)

        return result