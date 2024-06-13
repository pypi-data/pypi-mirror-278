from typing import Any, List, Optional

from .tool import Tool
from .adapter import Adapter

class Pipeline:
    def __init__(self, tools:List[Tool], adapter:Optional[Adapter]=None, global_memory:bool=False) -> None:
        self._tools = tools
        self._global_memory = True

        if adapter is None:
            adapter = Adapter()

        self._adapter = adapter

    def __call__(self, query, query_description, initial_context:str="", map_context:bool=False) -> Any:

        previous_outputs = dict(query)
        previous_outputs_description = dict(query_description)
        previous_description = "Collects user inputs"

        final_output = dict()
        final_output_description = ""

        for i in range(len(self._tools)):
            next_tool = self._tools[i]

            #Map
            next_query, next_context = self._adapter.map_tools(previous_tool_description=previous_description, 
                                previous_output=previous_outputs, 
                                previous_output_description=previous_outputs_description, 
                                next_tool=next_tool)
            
            if not map_context:
                next_context = ""

            if i == 0:
                next_context = initial_context +"\n"+next_context
            
            #Execute
            next_output, next_output_description = next_tool(next_query, next_context)

            #Grab results if last
            if i == len(self._tools) - 1:
                final_output = next_output
                final_output_description = next_output_description

            #Next to previous
            if self._global_memory:
                previous_outputs.update(next_output)
                previous_outputs_description.update(next_output_description)
            else:
                previous_outputs = next_output
                previous_outputs_description = next_output_description

            previous_description = next_tool.description

        return final_output, final_output_description