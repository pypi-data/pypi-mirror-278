from typing import Dict, Tuple, Optional

from .tool import Tool, TextLike
from .wrapper import ToolWrapper

class FixedInputWrapper(ToolWrapper):
    def __init__(self, base_tool: Tool, fixed_inputs:Dict[str, TextLike]) -> None:
        super().__init__(base_tool)

        self._fixed_inputs = fixed_inputs

    def _before_execution(self, query: Optional[Dict[str, str]], context: Optional[str]) -> Tuple[Dict[str, str], str]:
        query.update(self._fixed_inputs)
        
        return query, context
    
class MapInputWrapper(ToolWrapper):
    def __init__(self, base_tool: Tool, input_mapping:Dict[str, str]) -> None:
        super().__init__(base_tool)

        self._input_mapping = input_mapping
    
    def _before_execution(self, query: Optional[Dict[str, str]], context: str | None) -> Tuple[Dict[str, str], str]:
        new_query = {}

        for name in query:
            if name in self._input_mapping:
                name = self._input_mapping[name]
            
            new_query[name] = query[name]

        return new_query, context