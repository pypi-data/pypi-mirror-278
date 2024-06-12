from .nextflow_building_blocks import Nextflow_Building_Blocks
from .bioflowinsighterror import BioFlowInsightError
import re
from .outils import get_dico_from_tab_from_id

from . import constant


class Main_DSL2(Nextflow_Building_Blocks):
    def __init__(self, code, origin):
        Nextflow_Building_Blocks.__init__(self, code)
        self.origin = origin
        self.calls = []
        self.initialised = False

    def get_channels(self):
        return self.channels

    def get_type(self):
        return "Main DSL2"

    def get_calls(self):
        return self.calls
    
    def is_initialised(self):
        return self.initialised

    def get_all_called(self):
        called = []
        for exe in self.get_executors():
            if(exe.get_type()=="Call"):
                called+=exe.get_elements_called()
            else:
                for o in exe.get_origins():
                    if(o.get_type()=="Call"):
                        called+=o.get_elements_called()
        return called

    def get_processes(self):
        return self.origin.get_processes()+super().get_processes()
    
    def get_process_from_name(self, name):
        return self.origin.get_process_from_name(name)
    
    def get_processes_called(self, defined = {}):

        for c in self.get_all_called():
            if(c.get_type()=="Process"):
                defined[c] = []
            elif(c.get_type()=="Subworkflow"):
                _ = c.get_processes_called(defined = defined)
        
        return list(defined.keys())


    def get_function_from_name(self, name):
        return self.origin.get_function_from_name(name) 
    
    def get_list_name_subworkflows(self):
        return self.origin.get_list_name_subworkflows()
    
    def get_list_name_includes(self):
        return self.origin.get_list_name_includes()
    
    
    def get_channel_from_name(self, name):
        channel_file = self.origin.get_channel_from_name(name)
        if(channel_file!=None):
            return channel_file
        return super().get_channel_from_name(name)

    
    """def get_added_operations_structure(self):
        return self.origin.get_added_operations_structure()"""

    def check_in_channels(self, channel):
        found = super().check_in_channels(channel)
        if(not found):
            if(self.origin.get_type()=="Nextflow File"):
                return self.origin.check_in_channels(channel)
            else:
                raise Exception(f"The origin is a '{self.origin.get_type()}' it should be a 'Nextflow File'")
        return found
        

    def get_subworkflow_from_name(self, name):
        return self.origin.get_subworkflow_from_name(name)
    
    def check_includes(self):
        code = self.get_code()

        pattern = constant.FULL_INCLUDE
        for match in re.finditer(pattern, code):
            if(self.get_type()=="Main DSL2"):
                raise BioFlowInsightError(f"An include ('{match.group(0)}') was found in the main in the file '{self.get_file_address()}'. FlowInsight does not support this -> see specification list.", num = 12,origin=self)
            elif(self.get_type()=="Subworkflow"):
                raise BioFlowInsightError(f"An include ('{match.group(0)}') was found in the subworkflow '{self.get_name()}' in the file '{self.get_file_address()}'. FlowInsight does not support this -> see specification list.", num = 12, origin=self)
            else:
                raise Exception("This shouldn't happen!")
            
        
    def initialise(self):
        if(not self.initialised):
            
            self.initialised=True

            #Check that includes are not defined in the main or subworkflows
            self.check_includes()

            #Extract Executors
            self.extract_executors()
            
        
            #Analyse Executors
            for e in self.executors:
                e.initialise()
            


    """def add_channels_structure(self, dot):
        return self.add_channels_structure_temp(dot, self.origin.get_added_operations_structure())
    """
    def get_origin(self):
        return self.origin

    def check_same_origin(self, sub):
        return self.get_origin()== sub.get_origin()

    #Add "global" channels and operation to the structure defined in the file
    def get_structure_DSL2(self, dico):
        self.origin.get_structure_DSL2(dico)

 
    def get_structure(self, dico):
        #Add "global" channels and operation to the structure defined in the file
        self.get_structure_DSL2(dico)


        for e in self.executors:
            if(e.get_type()=="Operation"):
                e.get_structure(dico)
            elif(e.get_type()=="Call"):
                e.get_structure(dico)
            else:
                raise Exception(f"Executor of type '{e.get_type()}' was extracted in a DSL2 workflow! I don't know what this is! The code is '{e.get_code()}'")


        #
        #nodes_added = []
        #
        ##Add operation
        #for o in self.get_operations():
        #    dico['nodes'].append({'id':str(o), 'name':"", "shape":"point", 'xlabel':o.get_code()})
        #    nodes_added.append(str(o))
        #    
        #    #Need to check for cases where the origin is a process or a subworkflow
        #    for origin in o.get_origins():
        #
        #        if(origin.get_type()=="Process"):
        #            #Here i'm not adding the node but an edge -> the node is add when the call happens
        #            dico["edges"].append({'A':str(origin), 'B':str(o), "label":""})
        #
        #        elif(origin.get_type()=="Subworkflow"):
        #            emits = origin.get_emit()
        #            #TODO -> i'm only doing one parameter for now
        #            if(len(emits)==1):
        #                for source in emits[0].get_source():
        #                    dico["edges"].append({'A':str(source), 'B':str(o), "label":""})
        #            else:
        #                raise Exception(f'TO much to unpack for "{o.get_code()}"')
        #        
        #        elif(origin.get_type()=="Emitted"):
        #            if(origin.get_emitted_by().get_type()=="Process"):
        #                dico["edges"].append({'A':str(origin.get_emitted_by()), 'B':str(o), "label":origin.get_name()})
        #            
        #            elif(origin.get_emitted_by().get_type()=="Subworkflow"):
        #                for source in origin.get_emits().get_source():
        #                    dico["edges"].append({'A':str(source), 'B':str(o), "label":origin.get_name()})
        #
        #            else:
        #                raise Exception(f"I don't know how to handle {origin.get_emitted_by()}")
        #            
        #       
        #        elif(origin.get_type()=="Channel"):
        #            None
        #            #Here we do nothing since the channels are gonna be added below
        #
        #        else:
        #            raise Exception(f"George I don't know if this should be an error or not -> i don't think it should be")
        #            #TODO check this -> it should be added by the channel here below
        #        
        #
        ##Adding channels
        #for c in self.get_channels():
        #    for source in c.get_source():
        #        for sink in c.get_sink():
        #            #Here we check that the operation exists (already added to the structure) -> it's to avoid showing the operation for the emited channel
        #            if(str(sink) in nodes_added):
        #                dico["edges"].append({'A':str(source), 'B':str(sink), "label":c.get_name()})
        #
        # 
        #for c in self.get_calls():
        #    c.get_structure(dico)
        #
        ##return dico
    
    def add_2_rocrate(self, dico, parent_key):
        main_key = f"{parent_key}/MAIN"
        dico_main = get_dico_from_tab_from_id(dico, main_key)
        if(dico_main==None):
            dico_main = {}
            dico_main["@id"] = main_key
            dico_main["name"] = "Main Workflow"
            dico_main["@type"] = ["SoftwareSourceCode", "ComputationalWorkflow"]
            #TODO -> check if this remains true
            #dico_main["conformsTo"] = {"@id": "https://bioschemas.org/profiles/ComputationalWorkflow/0.5-DRAFT-2020_07_21"}
            #dico_main["dct:conformsTo"]= "https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE/"
            dico_main["input"] = []
            dico_main["output"] = []
            dico_main["isPartOf"] = [{"@id": parent_key}]
            dico_main["hasPart"] = []
            called = self.get_all_called()
            for c in called:
                c.add_2_rocrate(dico, main_key)
                dico_main["hasPart"].append({"@id":c.get_rocrate_key(dico)})
                
            dico["@graph"].append(dico_main)