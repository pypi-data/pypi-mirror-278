import re
from .channel import Channel
from .bioflowinsighterror import BioFlowInsightError
from . import constant


class Emitted(Channel):

    def __init__(self, name, origin, emitted_by):
        Channel.__init__(self, name=name, origin=origin)

        self.emitted_by = emitted_by
        if(not emitted_by.is_initialised()):
            emitted_by.initialise()
        
        self.source.append(emitted_by)
        self.emits = None #->this is the channel it's emits -> in the case of a subworkflow

    def get_emitted_by(self):
        return self.emitted_by
    
    def get_emits(self):
        return self.emits

    def get_type(self):
        return "Emitted"

    def set_emits_decimal(self, decimal):
        self.emits = self.emitted_by.get_emit()[decimal]

    def set_emits_name(self, name):
        emitted  = self.emitted_by.get_emit()
        
        for o in emitted:
            code = o.get_code()
            if(code[:len("emit:")]=="emit:"):
                code =code[len("emit:"):].strip()
            if(name==code):
                self.emits = o
            else:
                for match in re.finditer(constant.WORD_EQUALS, code):
                    if(name==match.group(1)):
                        self.emits = o
        
        if(self.emits==None):
            print(self.get_code())
            raise Exception(f"No emitted matched with '{name}' (in file '{self.get_file_address()}'). Should match with emittes from '{self.emitted_by.get_name()}' (in file '{self.emitted_by.get_file_address()}'")

    def set_emits(self, input):
        if(input!=""):
            try:
                input = int(input)
                self.set_emits_decimal(decimal=input)
            except:
                self.set_emits_name(name=input)
        else:
            #TODO -> check this
            if(self.emitted_by.get_type()=='Process'):
                #self.emits = self.emitted_by
                None
            elif(self.emitted_by.get_type()=='Subworkflow'):
                if(len(self.emitted_by.emit)!=1):
                    raise BioFlowInsightError(f"One channel was expected in the emit '{self.get_code()}'. Even though multiple emits are defined for the workflow '{self.emitted_by.get_name()}'", num=6, origin=self)
                self.emits = self.emitted_by.emit[0]
            else:
                raise Exception("This shoudn't happen!")

    def get_structure(self, dico, B):
        emits = self.get_emitted_by()
        if(not emits.is_called(self)):
            end = "in the file"
            if(self.origin.get_type()=="Subworkflow"):
                end = f"in the subworkflow '{self.origin.get_name()}'"
            raise BioFlowInsightError(f"Tried to access the emit '{self.get_code()}' but the {emits.get_type()} '{emits.get_name()}' has not been called {end}.", num = 8, origin=self)
            

        #Case if the emit emits a process
        if(emits.get_type()=="Process"):
            if(self.emits==None):
                #for i in range(emits.get_nb_outputs()):
                #    print("here")
                #    #I don't need to add the process (node) to the structure -> cause it's either there or will be added later on
                dico["edges"].append({'A':str(emits), 'B':str(B), "label":self.get_code()})
            else:
                dico["edges"].append({'A':str(self.emits), 'B':str(B), "label":self.get_code()})
        #Case if the emit emits a subworkflow
        elif(emits.get_type()=="Subworkflow"):
            if(self.emits==None):
                raise Exception("Just a check")
                for ope in emits.get_emit():
                    dico["edges"].append({'A':str(ope), 'B':str(B), "label":self.get_code()})
            else:
                dico["edges"].append({'A':str(self.emits), 'B':str(B), "label":self.get_name()})
                    

