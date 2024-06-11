import abc
from typing import Dict, Tuple, List, Optional

from .tool import Tool, TextLike

class ToolWrapper(Tool):

    def __init__(self, base_tool:Tool) -> None:
        assert isinstance(base_tool, Tool)

        super().__init__(base_tool.description, None)

        self._base_tool = base_tool

    def _execute(self, query:Optional[Dict[str, str]], 
                context:Optional[str]) -> Tuple[Dict[str, TextLike], Dict[str, str]]:
        
        query, context = self._before_execution(query, context)
        result, description = self._base_tool._execute()
        result, description = self._after_execution(result, description)

        return result, description
    
    def _before_execution(self, query:Optional[Dict[str, str]], 
                context:Optional[str]) -> Tuple[Dict[str, str], str]:
        
        return query, context
    
    def _after_execution(self, result:Dict[str, TextLike], 
                         description:Dict[str, str]) -> Tuple[Dict[str, TextLike], Dict[str, str]]:
        
        return result, description