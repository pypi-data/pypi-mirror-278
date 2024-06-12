
import re 
import os
import copy

from . import constant

from .code_ import Code
from .nextflow_building_blocks import Nextflow_Building_Blocks
from .bioflowinsighterror import BioFlowInsightError





#Remove ' and " from a given string
def clean_string(txt):
    txt = txt.replace("'", "")
    txt = txt.replace('"', "")
    return txt

class Include(Nextflow_Building_Blocks):
    def __init__(self, code, file, importing, origin, duplicate):
        self.origin = origin
        self.importing = importing
        self.duplicate = duplicate
        self.code = Code(code = code, origin = self)
        self.file = None
        self.address = file
        self.define_file(file)
        self.aliases = {}
        self.defines = []
        #self.initialise()
    

    def get_aliases(self):
        return self.aliases

    def get_defines(self):
        return self.defines
    
    def get_file(self):
        return self.file
    
    def get_address(self):
        return self.address
    
    def get_root_directory(self):
        return self.origin.get_root_directory()


    def get_list_name_includes(self):
        if(self.duplicate):
            names = []
            for ele in self.defines:
                names.append(ele.get_alias())
            return names
        else:
            return list(self.aliases.keys())
        
    def define_file(self, file):
        from .nextflow_file import Nextflow_File
        address = clean_string(file)
        root = self.origin.get_file_address()
        root = '/'.join(root.split('/')[:-1])
        found_file = False

        if(os.path.isfile(address)):
            found_file = True
        
        if(not found_file):
            if(address[-1]in [';']):
                address = address[:-1]

            if(address.split('/')[0] in ["$projectDir", "${projectDir}", "${baseDir}", "$baseDir"]):
                address = '/'.join(address.split('/')[1:])
                root = self.get_root_directory()
            address = root+'/'+address
            if(os.path.isfile(address)):
                found_file = True
        
        if(not found_file):
            if(address[-3:]!=".nf"):
                address+=".nf"
            if(os.path.isfile(address)):
                found_file = True

        if(not found_file and os.path.isfile(address[:-3]+"/main.nf")):
            self.file = Nextflow_File(address[:-3]+"/main.nf", origin=self, duplicate=self.duplicate, DSL="DSL2")
        
        #TODO -> check if the nextflow_file is defined somewhere else? 
        #In the cas the nextflow file is imported multiple times

        else:
            if(os.path.isfile(address)):
                self.file = Nextflow_File(address, origin=self, duplicate=self.duplicate, DSL="DSL2")
            else:
                address = os.path.normpath(address)
                raise BioFlowInsightError(f"Something went wrong in an include{self.get_string_line(self.get_code())}. No such file: '{address}'.", num = 10,origin=self)

        
        #If not duplicate -> we need to see if there is another include which has already defined the file
        #TODO -> if you wanna generalise this to all include (inbetween files -> you just need to update get_include() )
        if(not self.duplicate):
            #other_includes = self.origin.get_all_includes()
            other_includes = self.origin.get_includes()
            for other in other_includes:
                if(self.get_address()==other.get_address()):
                    self.file = other.get_file()

    def initialise(self):
        self.file.initialise()

        for include in self.importing:
            include = include.strip()
            found = False
            if(include!=''):
                if(re.fullmatch(constant.WORD, include)):
                    if(self.duplicate):
                        self.defines.append(self.file.get_element_from_name(include))
                    else:
                        self.aliases[include] = self.file.get_element_from_name(include)
                    found = True
                else:
                    pattern_as = constant.INCLUDE_AS
                    for match in re.finditer(pattern_as, include):
                        found = True
                        if(self.duplicate):
                            #TODO -> try shallow copy too
                            #thing_as = copy.copy(self.file.get_element_from_name(match.group(1)))
                            thing_as = copy.deepcopy(self.file.get_element_from_name(match.group(1)))
                            thing_as.set_alias(match.group(3))
                            self.defines.append(thing_as)
                        else:
                            #other_includes = self.origin.get_includes()
                            #added_from_other = False
                            #for other in other_includes:
                            #    if(self.get_address()==other.get_address()):
                            #        self.aliases[match.group(3)] = other.file.get_element_from_name(match.group(1))
                            #        added_from_other = True
                            #if(not added_from_other):
                            self.aliases[match.group(3)] = self.file.get_element_from_name(match.group(1))
                
                if(not found):
                    raise Exception(f"I was not able to import '{include}' from {self.file.get_file_address()}")



    
    


