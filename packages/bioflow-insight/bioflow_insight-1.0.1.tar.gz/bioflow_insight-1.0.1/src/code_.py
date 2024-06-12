from .outils import remove_comments
from .bioflowinsighterror import BioFlowInsightError
import re
from . import constant

class Code:
    def __init__(self, code, origin):
        self.code = code
        self.code_wo_comments = ""
        self.origin = origin
        self.initialise()
        #self.check_its_nextflow()

    
    def initialise(self):
        #I do this just to avoid out of file problems later on
        self.code = '\n'+self.code+'\n'
        self.code_wo_comments = remove_comments(self.code)
        self.code_wo_comments = re.sub(constant.BACKSLAPSH_JUMP, ' ', self.code_wo_comments)
        self.code_wo_comments = self.code_wo_comments.replace("||", "$OR$")


    def check_its_nextflow(self):
        for illegal in constant.ILLEGAL_IMPORTS:
            for match in re.finditer(constant.START_IMPORT+illegal, self.get_code()):
                bit_of_code = match.group(0)
                raise BioFlowInsightError(f"The presence of '{bit_of_code}' is detected{self.get_string_line(bit_of_code)}.", num = 1,origin=self)
            
   
    def get_line(self, bit_of_code):
        code = remove_comments(self.code)
        index = code.find(bit_of_code)
        if(index!=-1):
            line = code[:index].count('\n')
            if(line==0):
                return 1
            return line
        return -1
    
    def get_string_line(self, bit_of_code):
        line = self.get_line(bit_of_code)
        line_error = ''
        if(line!=-1):
            line_error = f", possibly at line {line}"
        return line_error


    #Returns the code witout comments
    def get_code(self, get_OG =False):
        if(get_OG):
            return self.code.strip()
        else:
            return self.code_wo_comments.strip()
    
    def get_file_address(self):
        return self.origin.get_file_address()
    