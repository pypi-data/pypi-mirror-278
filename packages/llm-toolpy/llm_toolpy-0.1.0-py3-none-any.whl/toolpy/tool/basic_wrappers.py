from typing import Dict, Tuple, Optional

from .tool import Tool, TextLike
from .wrapper import ToolWrapper

class FixedParameterWrapper(ToolWrapper):
    def __init__(self, base_tool: Tool, fixed_parameters:Dict[str, TextLike]) -> None:
        super().__init__(base_tool)

        self._fixed_parameters = fixed_parameters

    def _before_execution(self, query: Optional[Dict[str, str]], context: Optional[str]) -> Tuple[Dict[str, str], str]:
        query.update(self._fixed_parameters)
        
        return query, context