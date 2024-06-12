from typing import Dict, Optional, Tuple

from .tool import Tool, TextLike
from .basic_tool import BasicTool

class Adapter(BasicTool):
    _system_message = '''You are a tool adapter that outputs in JSON. You should tell how to adapt one tool output to insert at the next tool input. 
The JSON object must use the schema: {'inputs_map':{'from_output':'to_input'}, ...], 'to_context':['str']}

Where:
    'inputs_map' show which previous output send to each next input, mapping previous name to next name.

    'to_context' show outputs names that do not correspond to any input, but will help the next tool. 
The order in the list will be the order in which these outputs will be concatenated to send the next tool. 
Cannot contain outputs already mapped to inputs in 'inputs_map'.

Observe that some previous outputs may not used either in the 'inputs_map' and in the 'to_context'.

Please use a valid JSON format.'''

    _base_prompt = '''Adapt the previous tool to the next tool:

Previous tool description: {from_description}
Previous tool outputs: {from_output_description}

Next tool description: {to_description}
Next tool inputs: {to_input_description}

'''

    _description = "Map tool outputs to next tool inputs"

    _input_description = {"from_description":"previous tool description",
                          "from_output_description":"previous tool output descriptions",
                          "to_description":"next tool description",
                          "to_input_description":"next tool input descriptions"}
    
    _return_description = {"inputs_map":"mapping from previous tool inputs to next tool outputs",
                           "to_context":"previous tool inputs that can be usefull for the next, but is not in it inputs."}

    _cache : Dict[str, str] = {}

    def __init__(self, model_name:Optional[str] = None) -> None:

        super().__init__(self._description, self._input_description, self._base_prompt, 
                         self._return_description, self._system_message,  model_name,
                         json_mode=True)
        
    
    def map_tools(self, 
                  previous_output:Dict[str,TextLike], previous_output_description:Dict[str, str], 
                  next_tool:Tool, 
                  additional_inputs:Optional[Dict[str, TextLike]]=None, 
                  additional_inputs_description:Optional[Dict[str,str]]=None,
                  previous_tool:Optional[Tool] = None,
                  previous_tool_description:Optional[str]=None):
        
        from_output_description = dict(previous_output_description)
        previous = dict(previous_output)

        if additional_inputs is not None and additional_inputs_description is not None:
            from_output_description.update(additional_inputs_description)
            previous.update(additional_inputs)

        query = {"from_description":"unavailable",
         "from_output_description":str(from_output_description),
         "to_description":next_tool.description,
         "to_input_description":str(next_tool.input_description)
         }
        
        if previous_tool is not None:
            query["from_description"] = previous_tool.description
        elif previous_tool_description is not None:
            query["from_description"] = previous_output_description
        
        query_text = str(query)
        if query_text in self._cache:
            result = self._cache[query_text]
        else:
            result, _ = self(query)
            self._cache[query_text] = result

        next_query = dict()
        for previous_key in result["inputs_map"]:
            next_key = result["inputs_map"][previous_key]
            
            next_query[next_key] = previous[previous_key]
            
        next_context = "Additional information:\n"
        for previous_key in result["to_context"]:
            next_context += previous_key+":\n"
            next_context += "description: "+from_output_description[previous_key]+"\n"
            next_context += str(previous[previous_key]) + "\n\n"

        return next_query, next_context
    
    @classmethod
    def clear_cache(cls):
        cls._cache.clear()