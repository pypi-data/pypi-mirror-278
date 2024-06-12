import re

from .code_ import Code
from .nextflow_building_blocks import Nextflow_Building_Blocks
from .outils import remove_jumps_inbetween_parentheses, remove_jumps_inbetween_curlies, sort_and_filter, get_dico_from_tab_from_id, check_if_element_in_tab_rocrate
from .bioflowinsighterror import BioFlowInsightError

from . import constant

class Process(Nextflow_Building_Blocks):
    def __init__(self, code, origin):
        self.origin = origin
        self.code = Code(code, origin = self)
        self.name = ""
        self.alias = ""
        self.inputs = []
        self.outputs = []
        self.input_code = ""
        self.output_code = ""
        self.when_code = ""
        self.script_code = ""
        self.tools = []
        self.modules = []
        self.commands = []
        self.initialise()
        self.initialised = True

    def set_alias(self, alias):
        self.alias = alias
    
    def get_alias(self):
        return self.alias
    
    def get_name(self):
        return self.name
    
    def get_tools(self, remove_script_calls = True):
        def remove_script_calls(tab_temp):
            tab = tab_temp.copy()
            if("python" in tab):
                tab.remove("python")
            if("R" in tab):
                tab.remove("R")
            if("perl" in tab):
                tab.remove("perl")
            return tab
        if(remove_script_calls):
            return remove_script_calls(self.tools)
        else:
            return self.tools
    

    #def get_source(self):
    #    return [self]
    
    #MEthod which returns the DSL type of a process, i use the presence 
    #of from and into as a proxy. By default it's DSL2
    def which_DSL(self):
        DSL = "DSL2"
        pattern = constant.FROM
        for match in re.finditer(pattern, self.code.get_code()):
            DSL = "DSL1"
        pattern = constant.INTO
        for match in re.finditer(pattern, self.code.get_code()):
            DSL = "DSL1"
        return DSL

    def is_initialised(self):
        return self.initialised

    #def get_sink(self):
    #    return [self]
    
    def get_type(self):
        return "Process"

    
    

    def get_inputs(self):
        return self.inputs
    
    def get_nb_inputs(self):
        return len(self.inputs)
    
    def get_outputs(self):
        return self.outputs
    
    def get_nb_outputs(self):
        return len(self.outputs)
    
    #TODO -> Have a much better way of doing this  
    def extract_tools(self):
        script = self.script_code.lower()
        for tool in constant.TOOLS:
            if tool in script:
                self.tools.append(tool)
    

    def initialise_parts(self):
        code = self.get_code()
        
        #Check to see if the process is empty
        temp_code = re.sub(constant.PROCESS_HEADER, "", code)
        temp_code = temp_code[:-1].strip()
        if(len(temp_code)==0):
            raise BioFlowInsightError(f"The process '{self.get_name()}' defined in the file '{self.get_file_address()}' is an empty process!", num = 22, origin=self)
        input_multiple, input_pos= False, (0, 0)
        for match in re.finditer(constant.INPUT, code):
            if(input_multiple):
                raise BioFlowInsightError(f"Multiple 'input:' were found in the process '{self.get_name()}'.", num = 22, origin=self)
            input_pos = match.span(0)
            input_multiple = True

        output_multiple, output_pos= False, (0, 0)
        for match in re.finditer(constant.OUTPUT, code):
            if(output_multiple):
                raise BioFlowInsightError(f"Multiple 'output:' were found in the process '{self.get_name()}'?", num = 22, origin=self)
            output_pos = match.span(0)
            output_multiple = True

        when_multiple, when_pos= False, (0, 0)
        for match in re.finditer(constant.WHEN, code):
            if(when_multiple):
                raise BioFlowInsightError(f"Multiple 'when:' were found in the process '{self.get_name()}'.", num = 22, origin=self)
            when_pos = match.span(0)
            when_multiple = True

        script_pos= (0, 0)
        for match in re.finditer(constant.SCRIPT, code):
            script_pos = match.span(0)
            break

        positions = [input_pos, output_pos, when_pos, script_pos]
        variables_index = ['input', 'output', 'when', 'script']
        positions, variables_index = sort_and_filter(positions, variables_index)
        

        for i in range(len(positions)):
            temp_code = ""
            if(i==len(positions)-1):
                temp_code =  code[positions[i][1]:code.rfind('}')].strip()
            else:
                temp_code =  code[positions[i][1]:positions[i+1][0]].strip()
            
            if(variables_index[i]=='input'):
                self.input_code = temp_code
            elif(variables_index[i]=='output'):
                self.output_code = temp_code
            elif(variables_index[i]=='when'):
                self.when_code = temp_code
            elif(variables_index[i]=='script'):
                self.script_code = temp_code
                self.extract_tools()
            else:
                raise Exception("This shoudn't happen!")


    #Method that returns the input part of the process code
    def get_input_code(self):
        return self.input_code


    #Function that extracts the inputs from a process 
    def initialise_inputs_DSL1(self):
        code = "\n"+self.get_input_code()+"\n"
        code = remove_jumps_inbetween_parentheses(code)
        code = remove_jumps_inbetween_curlies(code)
        #Simplying the inputs -> when there is a jump line '.' -> it turns it to '.'
        code = re.sub(constant.JUMP_DOT, '.', code)

        def add_channel(name):
            from .channel import Channel
            input = Channel(name=name, origin=self.origin)
            if(not self.origin.check_in_channels(input)):
                self.origin.add_channel(input)
                input.add_sink(self)
                self.inputs.append(input)
            else:
                input = self.origin.get_channel_from_name(name)
                self.inputs.append(input)
                input.add_sink(self)
        
        #Case there is a single channel as an input -> doesn't use from to import channel -> uses file (see https://github.com/nextflow-io/nextflow/blob/45ceadbdba90b0b7a42a542a9fc241fb04e3719d/docs/process.rst)
        pattern = constant.FILE
        for match in re.finditer(pattern, code):
            add_channel(match.group(1))
        
    
        #Case there are multiple channels as input (e.g. channel1.mix(channel2))
        pattern = constant.FROM
        for match in re.finditer(pattern, code):
            extracted = match.group(1).strip()
            if(bool(re.fullmatch(constant.WORD, extracted))):
                add_channel(extracted)
            else:
                from .operation import Operation
                operation = Operation(code=extracted, origin=self.origin)
                operation.initialise()
                operation.is_defined_in_process(self)
                self.inputs+=operation.get_origins()
        
        #self.inputs = list(set(self.inputs))#TODO Check this

    #Function that extracts the inputs from a process (for DSLS workflows)
    def initialise_inputs_DSL2(self):
        code = self.get_input_code()
        code = remove_jumps_inbetween_parentheses(code)
        code = remove_jumps_inbetween_curlies(code)
        for input in code.split("\n"):
            input = input.strip()
            if(input!=""):
                self.inputs.append(input)            


    #Method that returns the input part of the process code
    def get_output_code(self):
        return self.output_code
    
    def get_file_extensions_outputs(self):
        code = self.get_output_code()
        extensions = []
        for match in re.finditer(r"(\.\w+)+|\.\w+", code):
            extensions.append(match.group(0))
        return extensions
    
    def get_input_parameters(self):
        code = self.get_input_code()
        parameters = []
        for match in re.finditer(r"\w+", code):
            parameters.append(match.group(0))
        parameters = list(set(parameters))#Here we can a unique cause a parameter can only be given once in any case
        words_2_remove = ["path", "val", "tuple", "into", "stageAs", "emit"]
        for word in words_2_remove:
            try:
                parameters.remove(word)
            except:
                None
        return parameters

    def get_modules(self):
        return self.modules
    
    def get_commands(self):
        return self.commands



    #Function that extracts the outputs from a process (DSL1)
    def initialise_outputs_DSL1(self):
        code = self.get_output_code()
        code = remove_jumps_inbetween_parentheses(code)
        code = remove_jumps_inbetween_curlies(code)
        def add_channel(name):
            from .channel import Channel
            output = Channel(name=name, origin=self.origin)
            if(not self.origin.check_in_channels(output)):
                self.origin.add_channel(output)
                output.add_source(self)
                self.outputs.append(output)
            else:
                output = self.origin.get_channel_from_name(outputs[i].strip())
                self.outputs.append(output)
                output.add_source(self)


        pattern =constant.INTO_2
        for match in re.finditer(pattern, code):
            outputs = match.group(1).split(',')
            for i in range(len(outputs)):
                add_channel(outputs[i].strip())
        
        pattern = constant.FILE
        for match in re.finditer(pattern, code):
            add_channel(match.group(1))

    #Function that extracts the inputs from a process (for DSLS workflows)
    def initialise_outputs_DSL2(self):
        code = self.get_output_code()
        code = remove_jumps_inbetween_parentheses(code)
        code = remove_jumps_inbetween_curlies(code)
        for output in code.split("\n"):
            output = output.strip()
            if(output!=""):
                self.outputs.append(output) 


    def initialise_name(self):
        for match in re.finditer(constant.PROCESS_HEADER, self.code.get_code()):
            self.name = match.group(1)
            self.name = self.name.replace("'", "")
            self.name = self.name.replace('"', '')
            self.alias = self.name

    def get_structure(self, dico):
        dico['nodes'].append({'id':str(self), 'name':self.get_name(), "shape":"ellipse", 'xlabel':"", 'fillcolor':''})

    def initialise_inputs_outputs(self):
        DSL = self.origin.get_DSL()
        if(DSL=="DSL1"):
            self.initialise_inputs_DSL1()
            self.initialise_outputs_DSL1()
        elif(DSL=="DSL2"):
            self.initialise_inputs_DSL2()
            self.initialise_outputs_DSL2()
        #else:
        #    raise Exception("Workflow is neither written in DSL1 nor DSL2!")


    def initialise(self):
        self.initialise_name()
        self.initialise_parts()
        self.initialise_inputs_outputs()
        annotations = self.get_processes_annotation()
        if(annotations!=None):
            self.tools = annotations[self.get_code()]["tools"]
            self.commands = annotations[self.get_code()]["commands"]
            self.modules = annotations[self.get_code()]["modules"]

    def add_2_rocrate(self, dico, parent_key):
        process_key = self.get_rocrate_key(dico)
        dico_process = get_dico_from_tab_from_id(dico, process_key)
        if(dico_process==None):
            dico_process = {}
            dico_process["@id"] = process_key
            dico_process["name"] = "Process"
            dico_process["@type"] = ["SoftwareSourceCode", "Script"]
            #ADD INPUTS
            dico_process["input"] = []
            for input in self.get_inputs():
                if(type(input)==str):
                    name_input = input
                else:
                    name_input = input.get_code()
                dico_input = get_dico_from_tab_from_id(dico, name_input)
                if(dico_input==None):
                    dico_input = {"@id":name_input, "@type": "FormalParameter"}
                    dico["@graph"].append(dico_input)
                dico_process["input"].append({"@id":dico_input["@id"]})
            #ADD OUTPUTS
            dico_process["output"] = []
            for output in self.get_outputs():
                if(type(output)==str):
                    name_output = output
                else:
                    name_output = output.get_code()
                dico_output = get_dico_from_tab_from_id(dico, name_output)
                if(dico_output==None):
                    dico_output = {"@id":name_output, "@type": "FormalParameter"}
                    dico["@graph"].append(dico_output)
                dico_process["output"].append({"@id":dico_output["@id"]})
            #ADD isPartOf
            dico_process["isPartOf"] = []
            dico_process["isPartOf"].append({"@id":parent_key})
            #ADD hasPart
            dico_process["hasPart"] = []
            for tool in self.get_tools():
                dico_tool = get_dico_from_tab_from_id(dico, tool)
                if(dico_tool==None):
                    dico_tool = {"@id":tool, 
                                   "name": "Tool"
                                   #TODO in later versions
                                   #, "url": "https://some.link.com"
                                   #, "identifier": "tool_identifier"
                                   }
                    dico["@graph"].append(dico_tool)
                dico_process["hasPart"].append({"@id":dico_tool["@id"]})

            dico["@graph"].append(dico_process)
        else:
            if(not check_if_element_in_tab_rocrate(dico_process["isPartOf"], parent_key)):
                dico_process["isPartOf"].append({"@id":parent_key})

