import re 
from . import constant
from .code_ import Code
from .main_DSL2 import Main_DSL2
from .bioflowinsighterror import BioFlowInsightError
from .outils import remove_jumps_inbetween_parentheses, get_dico_from_tab_from_id, check_if_element_in_tab_rocrate




class Subworkflow(Main_DSL2):
    def __init__(self, code, origin, name):
        Main_DSL2.__init__(self, code, origin)
        self.name = name.replace("'", "").replace('"', '')
        self.alias = self.name
        #These are the different parts of of a subworkflow -> work corresponds to the main 
        self.take = []
        self.work = None
        self.emit = []

        self.initialised = False

    def print_summary(self, tab = 0):
        print("  "*tab+f"* {self.name} ({self})")
        super().print_summary(tab)

    def set_alias(self, alias):
        self.alias = alias

    def get_alias(self):
        return self.alias

    def get_type(self):
        return "Subworkflow"

    def get_name(self):
        return self.name
    
    def get_work(self):
        return self.work.get_code()
    
    #TODO -> when return the code of a subworkflow -> i return evrything (not just the work) -> check if that is correct
    #Method which initiliases the different parts of a workflow (take/main/emit)
    def initialise_parts(self):
        code = self.get_code()
        take_multiple, take_pos= False, (0, 0)
        for match in re.finditer(constant.TAKE, code):
            if(take_multiple):
                raise BioFlowInsightError(f"Multiple 'take:' were found in the subworkflow '{self.get_name()}'.", num = 22, origin=self)
            take_pos = match.span(0)
            take_multiple = True

        main_multiple, main_pos= False, (0, 0)
        for match in re.finditer(constant.MAIN, code):
            if(main_multiple):
                raise BioFlowInsightError(f"Multiple 'main:' were found in the subworkflow '{self.get_name()}'.", num = 22, origin=self)
            main_pos = match.span(0)
            main_multiple = True

        emit_multiple, emit_pos= False, (0, 0)
        for match in re.finditer(constant.EMIT_SUBWORKFLOW, code):
            if(emit_multiple):
                raise BioFlowInsightError(f"Multiple 'emit:' were found in the subworkflow '{self.get_name()}'. ", num = 22, origin=self)
            emit_pos = match.span(0)
            emit_multiple = True

        #Case everything is there
        if(take_pos!=(0, 0) and main_pos!=(0, 0) and emit_pos!=(0, 0)):
            if(take_pos[0]<main_pos[0] and main_pos[0]<emit_pos[0]):
                self.take = Code(code[take_pos[1]:main_pos[0]].strip(), origin = self)
                self.work = Code(code[main_pos[1]:emit_pos[0]].strip(), origin = self)
                self.emit = Code(code[emit_pos[1]:code.rfind('}')].strip(), origin = self)
            elif(take_pos[0]<emit_pos[0] and emit_pos[0]<main_pos[0]):
                self.take = Code(code[take_pos[1]:emit_pos[0]].strip(), origin = self)
                self.emit = Code(code[emit_pos[1]:main_pos[0]].strip(), origin = self)
                self.work = Code(code[main_pos[1]:code.rfind('}')].strip(), origin = self)
            else:
                raise Exception('You need to add a case')
        #Case nothing is there
        if(take_pos==(0, 0) and main_pos==(0, 0) and emit_pos==(0, 0)):
            #raise Exception(f"Subworkflow {code} doesn't have anything defined")
            self.work = Code(code, origin = self)
        #Case there is an input but no output
        if(take_pos!=(0, 0) and main_pos!=(0, 0) and emit_pos==(0, 0)):
            if(take_pos[0]<main_pos[0]):
                self.take = Code(code[take_pos[1]:main_pos[0]].strip(), origin = self)
                self.work = Code(code[main_pos[1]:code.rfind('}')].strip(), origin = self)
            else:
                raise Exception('You need to add a case')
        #Case there is no input but an output
        if(take_pos==(0, 0) and main_pos!=(0, 0) and emit_pos!=(0, 0)):
            if(main_pos[0]<emit_pos[0]):
                self.work = Code(code[main_pos[1]:emit_pos[0]].strip(), origin = self)
                self.emit = Code(code[emit_pos[1]:code.rfind('}')].strip(), origin = self)
            else:
                raise Exception('You need to add a case')
        #Case there is a main but no input and no output
        if(take_pos==(0, 0) and main_pos!=(0, 0) and emit_pos==(0, 0)):
            self.work = Code(code[main_pos[1]:code.rfind('}')].strip(), origin = self)
        if( main_pos==(0, 0) and (take_pos!=(0, 0) or emit_pos!=(0, 0))):
            if(take_pos!=(0, 0) and emit_pos!=(0, 0)):
                raise Exception("TODO")
            elif(take_pos!=(0, 0) and emit_pos==(0, 0)):
                raise Exception("TODO")
            elif(take_pos==(0, 0) and emit_pos!=(0, 0)):
                self.emit = Code(code[emit_pos[1]:code.rfind('}')].strip(), origin = self)
                firt_curly  = code.find("{")
                self.work = Code(code[firt_curly+1:emit_pos[0]].strip(), origin = self)
            else:
                raise Exception("Not possible!")
    
    def get_channel_from_name_takes(self, name):
        for c in self.channels:
            if(name == c.get_name()):
                return c
        return None

    def initialise_takes(self):
        if(self.take!=[]):
            code = remove_jumps_inbetween_parentheses(self.take.get_code()).split('\n')
            tab = []
            for i in range(len(code)):
                code[i] = code[i].strip()
                if(code[i]!=''):
                    channel = self.get_channel_from_name_takes(code[i])
                    #In the case the channel doesn't exist
                    if(channel==None):
                        from .operation import Operation
                        ope = Operation(f"take: {code[i]}", self)
                        from .channel import Channel
                        channel = Channel(code[i], self)
                        ope.add_element_gives(channel)
                        channel.add_source(ope)
                        #ope.initialise_from_subworkflow_take()
                    else:
                        raise BioFlowInsightError(f"The channel '{code[i]}' is already defined somewhere else in the subworkflow ('{self.get_name()}') or in the file.", num=4, origin=self)
                    tab.append(ope)
                    for channel in ope.get_gives():
                        self.channels.append(channel)
                    
            self.take = tab

    #def initialise_emit(self):
    #    if(self.emit!=None):
    #        code = self.emit.get_code().split('\n')
    #        tab = []
    #        for i in range(len(code)):
    #            code[i] = code[i].strip()
    #            channel = self.get_channel_from_name(code[i])
    #            if(channel!=None):
    #                tab.append(channel)
    #                channel.add_sink(Operation(code=channel.get_name(), origin=self))
    #                
    #            else:
    #                #Case it's an operation 
    #                operation = Operation(code[i], self)
    #                operation.initialise()
    #                for gives in operation.get_gives():
    #                    tab.append(gives)
    #                    #TODO -> check not add origin too!
    #                    gives.add_sink(Operation(code=gives.get_name(), origin=self))
    #                #self.add_operation(operation)
    #                self.executors.append(operation)
    #        self.emit = tab

    def initialise_emit(self):
        from .operation import Operation
        if(self.emit!=[]):
            code = remove_jumps_inbetween_parentheses(self.emit.get_code()).split('\n')
            tab = []
            for i in range(len(code)):
                code[i] = code[i].strip()
                if(code[i]!=""):
                    channel = self.get_channel_from_name(code[i])
                    if(channel!=None):
                        ope = Operation(code=f"emit: {code[i]}", origin=self)
                        ope.add_element_origins(channel)
                        channel.add_sink(ope)
                        tab.append(ope)
                        
                    else:
                        #raise Exception(f"I don't know how to handle '{code[i]}'")
                        #Case it's an operation 
                        operation = Operation(code[i], self)
                        operation.initialise()
                        operation.change_code(f"emit: {code[i]}")
                        tab.append(operation)
                        #operation.add_gives(channel)
                        #for gives in operation.get_gives():
                        #    #TODO -> check not add origin too!
                        #    gives.add_sink(operation)
                        #tab.append(operation)
                        #print(operation)
                        ##self.add_operation(operation)
                        ##self.executors.append(operation)
            self.emit = tab
            
            

    

    def get_emit(self):
        return self.emit
    
    def get_nb_emit(self):
        return len(self.emit)

    def get_takes(self):
        return self.take
    
    def get_nb_takes(self):
        return len(self.take)
    
    def get_nb_inputs(self):
        return self.get_nb_takes()
            

    def initialise(self):
        if(not self.initialised):
            self.initialise_parts()
            self.initialise_takes()
            super().initialise()
            self.initialise_emit()
            self.initialised = True

    def get_structure(self, dico):
        super().get_structure(dico)

        for ope in self.get_takes():
            #ope.set_operation_type("Branch")
            ope.get_structure(dico, to_remove = True)
    
        for ope in self.get_emit():
            #ope.set_operation_type("Branch")
            ope.get_structure(dico, to_remove = True)

    def add_2_rocrate(self, dico, parent_key):
        sub_key = self.get_rocrate_key(dico)
        dico_sub = get_dico_from_tab_from_id(dico, sub_key)
        if(dico_sub==None):
            dico_sub = {}
            dico_sub["@id"] = sub_key
            dico_sub["name"] = "Subworkflow"
            dico_sub["@type"] = ["SoftwareSourceCode", "ComputationalWorkflow"]
            #TODO -> check if this remains true
            #dico_main["conformsTo"] = {"@id": "https://bioschemas.org/profiles/ComputationalWorkflow/0.5-DRAFT-2020_07_21"}
            #dico_main["dct:conformsTo"]= "https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE/"
            
            
            #ADD INPUTS
            dico_sub["input"] = []
            for input in self.get_takes():
                if(type(input)==str):
                    name_input = input
                else:
                    name_input = input.get_code()
                dico_input = get_dico_from_tab_from_id(dico, name_input)
                if(dico_input==None):
                    dico_input = {"@id":name_input, "@type": "FormalParameter"}
                    dico["@graph"].append(dico_input)
                dico_sub["input"].append({"@id":dico_input["@id"]})
            #ADD OUTPUTS
            dico_sub["output"] = []
            for output in self.get_emit():
                if(type(output)==str):
                    name_output = output
                else:
                    name_output = output.get_code()
                dico_output = get_dico_from_tab_from_id(dico, name_output)
                if(dico_output==None):
                    dico_output = {"@id":name_output, "@type": "FormalParameter"}
                    dico["@graph"].append(dico_output)
                dico_sub["output"].append({"@id":dico_output["@id"]})


            dico_sub["isPartOf"] = [{"@id": parent_key}]
            dico_sub["hasPart"] = []


            called = []
            for exe in self.get_executors():
         
                if(exe.get_type()=="Call"):
                    called+=exe.get_elements_called()
                else:
                    for o in exe.get_origins():
                        if(o.get_type()=="Call"):
                            called+=o.get_elements_called()

            for c in called:
                if(c==self):
                    raise Exception("This shoudn't happen!")
                c.add_2_rocrate(dico, sub_key)
                dico_sub["hasPart"].append({"@id":c.get_rocrate_key(dico)})

            dico["@graph"].append(dico_sub)
        else:
            if(not check_if_element_in_tab_rocrate(dico_sub["isPartOf"], parent_key)):
                dico_sub["isPartOf"].append({"@id":parent_key})
   


        

