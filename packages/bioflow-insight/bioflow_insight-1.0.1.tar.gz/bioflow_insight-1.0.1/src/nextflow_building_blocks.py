import os
import re
from pathlib import Path

from . import constant

from .outils import extract_curly, extract_end_operation, extract_executor_from_middle, get_end_call, expand_call_to_operation, get_curly_count, get_parenthese_count, expand_pipe_operator, checks_in_condition_if, checks_in_string
from .code_ import Code
from .bioflowinsighterror import BioFlowInsightError



class Nextflow_Building_Blocks:
    def __init__(self, code):
        self.code = Code(code = code, origin = self)

        self.processes = []
        self.channels = []
        self.DSL = ""
        #DSL2
        self.includes = []
        self.main = None
        self.executors = []
        self.subworkflows = []
        self.functions=[]
        
        

    #---------------------------------
    #AUXILIARY METHODS FOR ALL CLASSES
    #---------------------------------
    def get_code(self, get_OG = False):
        return self.code.get_code(get_OG = get_OG)
    
    def get_output_dir(self):
        return self.origin.get_output_dir()
    
    def get_DSL(self):
        return self.origin.get_DSL()
    
    def get_processes_annotation(self):
        return self.origin.get_processes_annotation()
    
    def get_file_address(self):
        return self.origin.get_file_address()

    def get_display_info(self):
        return self.origin.get_display_info()
    
    def get_name_processes_subworkflows(self):
        return self.origin.get_list_name_subworkflows()+self.origin.get_list_name_includes()+ self.origin.get_list_name_processes()
    
    #Only used by the process or subworkflow
    def is_called(self, called_from):
        if(self.get_type() in ["Process", "Subworkflow"]):

            executors = called_from.origin.get_executors()
            for exe in executors:
                if(exe.get_type()=="Call"):
                    if(self in exe.get_elements_called()):
                        return True
                #Case operation
                else:
                    for o in exe.get_origins():
                        if(o.get_type()=="Call"):
                            if(self in o.get_elements_called()):
                                return True
            return False
        raise Exception("You can't do this!")
    
    def get_line(self, bit_of_code):
        return self.origin.get_line(bit_of_code)
    
    def get_string_line(self, bit_of_code):
        return self.origin.get_string_line(bit_of_code)
    
    def get_name_file(self):
        return self.origin.get_name_file()
    
    def get_rocrate_key(self, dico):
        return f"{self.get_file_address()[len(dico['temp_directory'])+1:]}#{self.get_name()}"


    

    #----------------------
    #PROCESSES
    #----------------------
    def extract_processes(self):
        from .process import Process
        code = self.get_code()
        #Find pattern
        for match in re.finditer(constant.PROCESS_HEADER, code):
            start = match.span(0)[0]
            end = extract_curly(code, match.span(0)[1])#This function is defined in the functions file
            p = Process(code=code[start:end], origin=self)
            self.processes.append(p)

    def get_list_name_processes(self):
        tab = []
        for p in self.get_processes():
            tab.append(p.get_name())
        return tab
    
    def get_process_from_name(self, name):
        for p in self.get_processes():
            if(p.get_name()==name):
                return p
        return None
    
    def get_channels(self):
        return self.origin.get_channels()

    def get_processes(self):
        return self.processes

    #----------------------
    #CHANNELS
    #----------------------

    #Check if a channel given in parameters is already in channels
    def check_in_channels(self, channel):
        for c in self.channels:
            if(c.equal(channel)):
                return True
        return False

    def get_channel_from_name(self, name):
        for c in self.channels:
            if(name == c.get_name()):
                return c
        #raise Exception(f"{name} is not in the list of channels")
        return None

    #Method that adds channel into the lists of channels
    def add_channel(self, channel):
        if(not self.check_in_channels(channel)):
            self.channels.append(channel)
        else:
            raise Exception("This shoudn't happen!")


    """def add_channels_structure_temp(self, dico, added_operations):
        for c in self.get_channels():
            for source in c.get_source():
                for sink in c.get_sink():
                    if(not(isinstance(source, Operation)) or not(isinstance(sink, Operation))):
                        raise Exception("NOt operations!!")
                    
                    if(source not in added_operations):
                        #dot.node(str(source), "", shape="point", xlabel= source.get_code())
                        dico["nodes"].append({"id":str(source), "name":'', "shape":"point", "xlabel": source.get_code()})
                        added_operations.append(source)
                    if(sink not in added_operations):
                        #dot.node(str(sink), "", shape="point", xlabel= sink.get_code())
                        dico["nodes"].append({"id":str(sink), "name":'', "shape":"point", "xlabel": sink.get_code()})
                        added_operations.append(sink)

                    #dot.edge(str(source), str(sink), label= c.get_name())
                    dico["edges"].append({"A":str(source), "B":str(sink), "label": c.get_name()})
        return dico"""


    #----------------------
    #EXECUTORS
    #----------------------
    


    def get_executors(self):
        return self.executors
    
    def extract_executors(self):
        from .operation import Operation
        from .call import Call

        #https://github.com/nextflow-io/nextflow/blob/45ceadbdba90b0b7a42a542a9fc241fb04e3719d/docs/operator.rst
        #TODO This list needs to be checked if it's exhaustive

        if(self.get_type()=="Subworkflow"):
            code = self.get_work()
        elif(self.get_type()=="Main DSL2"):
            code = self.get_code()
            code = re.sub(constant.WORKFLOW_HEADER, "", code)
            if(code[-1]!='}'):
                raise Exception("This shoudn't happen")
            code = code[:-1]

        else:
            code = self.get_code()

        things_to_remove = []
        things_to_remove+= self.processes+self.includes+self.subworkflows+self.functions
        if(self.main!=None):
            things_to_remove+=[self.main]
        
        for to_remove in things_to_remove:
            code = code.replace(to_remove.get_code(get_OG = True), "", 1)

        #We add this to simplify the search of the executors 
        code = "start\n"+code+"\nend"

        #This function takes an executor (already found and expandes it to the pipe operators)
        def expand_to_pipe_operators(text, executor):
            #If the executor ends with the pipe operator -> we remove it so that it can be detected by the pattern
            if(executor[-1]=="|"):
                executor = executor[:-1].strip()
            start = text.find(executor)+len(executor)
            for match in re.finditer(constant.END_PIPE_OPERATOR, text[start:]):
                begining, end = match.span(0)
                if(begining==0):
                    return expand_pipe_operator(text, executor+match.group(0))
                break
            return executor

        

        #---------------------------------------------------------------
        #STEP1 - Extract equal operations eg. 
        # *Case "channel = something"
        # *Case "(channel1, channel2) = something"
        #--------------------------------------------------------------- 
        pattern_equal = constant.LIST_EQUALS
    
        searching = True
        while(searching):
            searching= False
            text = code
            for e in self.executors:
                text = text.replace(e.get_code(), "", 1)
            
            for pattern in pattern_equal:
                for match in re.finditer(pattern, text):
                    
                    start, end = match.span(2)
                    ope = extract_end_operation(text, start, end)
                    ope = expand_to_pipe_operators(text, ope)
                 
                    #If the thing which is extracted is not in the conditon of an if 
                    if(not checks_in_condition_if(text, ope) and not checks_in_string(text, ope)):
                        operation = Operation(ope, self)
                        self.executors.append(operation)
                        searching= True
                        break

        #I switched step 2 and step 3 -> cause there were cases where there was operations in the paramters of a call -> they were extracted and removed
        #-----------------------------------
        #STEP3 - Extract the remaining calls
        #-----------------------------------
        #These are the processes and subworkflows we need to check are called
        if(self.get_DSL()=="DSL2"):
            to_call = self.get_list_name_processes()+self.get_list_name_subworkflows()+self.get_list_name_includes()
            pattern_call = constant.BEGINNING_CALL
            searching = True
            while(searching):
                searching= False
                text = code
                for e in self.executors:
                    text = text.replace(e.get_code(), "", 1)
        
                for match in re.finditer(pattern_call, text):
                    if(match.group(1) in to_call):
                        
                        start, end = match.span(0)
                        txt_call = get_end_call(text, start, end)
                        txt_call = expand_to_pipe_operators(text, txt_call)
                        #If the thing which is extracted is not in the conditon of an if 
                        if(not checks_in_condition_if(text, txt_call) and not checks_in_string(text, txt_call)):
                            if(txt_call.find("|")!=-1 and txt_call[txt_call.find("|")-1]!="|" and txt_call[txt_call.find("|")+1]!="|"):
                                first_thing_called = txt_call.split('|')[-1].strip()
                                if(first_thing_called in to_call):
                                    call = Call(code =txt_call, origin =self)
                                    self.executors.append(call)
                                else:
                                    added = True
                                    if(first_thing_called in constant.LIST_OPERATORS):
                                        added = True
                                    if(not added):
                                        for operator in constant.LIST_OPERATORS:
                                            for match in re.finditer(operator+constant.END_OPERATOR, txt_call.split('|')[-1].strip()):
                                                start, end = match.span(0)
                                                if(start==0):
                                                    added = True
                                    if(not added):
                                        raise BioFlowInsightError(f"In the executor '{txt_call}', '{first_thing_called}' is neither a process, subworkflow or an operator{self.get_string_line(txt_call)}", num = 14, origin=self)
                                    else:
                                        ope = Operation(code =txt_call, origin =self)
                                        self.executors.append(ope)
                            else:
                                #We need to see if we can expand the call to a operation perhaps process().set{ch}
                                expanded = expand_call_to_operation(text, txt_call)#TODO update this
                                if(txt_call==expanded):
                                    call = Call(code =txt_call, origin =self)
                                    self.executors.append(call)
                                else:
                                    ope = Operation(code =expanded, origin =self)
                                    self.executors.append(ope)
                            
                            searching = True
                            break


        #-------------------------------------------------
        #STEP2 - Extract the terms which use the operators
        #-------------------------------------------------
        pattern_dot = constant.DOT_OPERATOR
        searching = True
        searched = []


        while(searching):
            searching= False
            text = code
            for e in self.executors:
                text = text.replace(e.get_code(), "", 1)
            
            for match in re.finditer(pattern_dot, text):
                start, end = match.span(1)
                
                if(match.group(1) not in constant.ERROR_WORDS):
                    if(match.group(1) in constant.LIST_OPERATORS):
                        #TODO -> the function below might not work perfectly but i don't have any other ideas
                        
                        
                        #Use if there is an operator called right before opening the curlies/parenthse
                        #curly_left, curly_right = get_curly_count(text[:start]), get_curly_count(text[end:])
                        parenthese_left, parenthese_right = get_parenthese_count(text[:start]), get_parenthese_count(text[end:])
                        
                        #if(curly_left==0 and curly_right==0 and parenthese_left==0 and parenthese_right==0 and (start, end) not in searched):
                        if(parenthese_left==0 and parenthese_right==0 and (start, end) not in searched):
                            searched.append((start, end))
                        
                            try:
                                pot = extract_executor_from_middle(text, start, end) 
                            except:
                                try:
                                    temp = text[start-10:end+10]
                                except:
                                    temp = text[start:end]
                                raise BioFlowInsightError(f"Failed to extract the operation or call{self.get_string_line(temp)}. Try rewriting it in a simplified version.", num = 11, origin=self)
                            
                            pot = expand_to_pipe_operators(text, pot)
                            
                            #If the thing which is extracted is not in the conditon of an if 
                            if(not checks_in_condition_if(text, pot) and not checks_in_string(text, pot)):
                                if(self.get_DSL()=="DSL2"):
                                    to_call = self.get_list_name_processes()+self.get_list_name_subworkflows()+self.get_list_name_includes()
                                    if(pot.find("|")!=-1):
                                        if(not checks_in_condition_if(pot, '|') and not checks_in_string(pot, '|')):#TODO checks_in_string is the first occurance
                                            first_thing_called = pot.split('|')[-1].strip()
                                            if(first_thing_called in to_call):
                                                call = Call(code =pot, origin =self)
                                                self.executors.append(call)
                                            elif(first_thing_called in constant.LIST_OPERATORS):
                                                ope = Operation(code =pot, origin =self)
                                                self.executors.append(ope)
                                            else:
                                                raise BioFlowInsightError(f"'{first_thing_called}' is neither a process, subworkflow or an operator. In the executor '{pot}'{self.get_string_line(pot)}.", num=14,origin=self)#TODO -> try rewriting the operation using the standard syntaxe
                                        
                                        else:
                                            from .executor import Executor
                                            executor = Executor(pot, self)
                                            self.executors.append(executor.return_type())
                                    
                                    else:
                                        from .executor import Executor
                                        executor = Executor(pot, self)
                                        self.executors.append(executor.return_type())
                                else:
                                    ope = Operation(pot, self)
                                    self.executors.append(ope)
                                searching = True
                                break
                        

        #---------------------------------------------------------------
        #STEP4 - Extract the Executors which only use the pipe operators (which start with a channel)
        #---------------------------------------------------------------
        to_call = self.get_list_name_processes()+self.get_list_name_subworkflows()+self.get_list_name_includes()

        searching = True
        while(searching):
            searching= False
            text = code
            for e in self.executors:
                text = text.replace(e.get_code(get_OG=True), "", 1)
            pattern = constant.BEGINNING_PIPE_OPERATOR
            
            for match in re.finditer(pattern, text):
                txt_call = expand_pipe_operator(text, match.group(0))
                full_executor =  txt_call
                
                #start, end = match.span(0)
                ## Check to see if a parameter is given such as in the example 'splitLetters | flatten | convertToUpper | view { it.trim() }'
                #params, full_executor = check_if_parameter_is_given_pipe(text, start, end)
                #if(params!=''):
                #    tab_to_call = txt_call.split('|')
                #    start = f"{tab_to_call[0]}({params})"
                #    txt_call = start + '|' + '|'.join(tab_to_call[1:])
                #    print(start)
                #print(params, full_executor)
                
                #If the thing which is extracted is not in the conditon of an if 
                if(not checks_in_condition_if(text, full_executor) and not checks_in_string(text, full_executor)):
                    tab_to_call = txt_call.split('|')
                    if(tab_to_call[0].strip() in to_call):
                        start = f"{tab_to_call[0]}()"
                        txt_call = start + '|' + '|'.join(tab_to_call[1:])
                    first_thing_called = txt_call.split('|')[-1].strip()

                    if(first_thing_called in to_call):
                        call = Call(code =txt_call, origin =self, OG_code= full_executor)
                        self.executors.append(call)
                        searching = True
                        break
                    elif(first_thing_called in constant.LIST_OPERATORS):
                        ope = Operation(code =txt_call, origin =self, OG_code= full_executor)
                        self.executors.append(ope)
                        searching = True
                        break
                    else:
                        added = False
                        #This is in the case "channel | map {dfvfdvd}"
                        for ope in constant.LIST_OPERATORS:
                            if(first_thing_called[:len(ope)]==ope and not added):
                                ope = Operation(code =txt_call, origin =self, OG_code= full_executor)
                                self.executors.append(ope)
                                added = True
                                searching = True
                        if(added):
                            break
                        elif(not added):
                            raise BioFlowInsightError(f"In the executor '{txt_call}', '{first_thing_called}' is neither a process, subworkflow or an operator (in the file '{self.get_file_address()}')", num = 14,origin=self)
        
        #---------------------------------------------------------------------
        #STEP5 - We remove the things which were falsy extracted as executors
        #---------------------------------------------------------------------
        to_remove = []
        starting_by_to_remove = ["System.out"]
        for e in self.executors:
            for r in starting_by_to_remove:
                if(e.get_code()[:len(r)]==r):
                    to_remove.append(e)
        for e in to_remove:
            self.executors.remove(e)
        

    #----------------------
    #OPERATIONS
    #----------------------

    #Method that adds operation into the lists of operations
    def add_operation(self, operation):
        self.operations.append(operation)

    #----------------------
    #INCLUDES
    #----------------------
    def get_all_includes(self):
        return self.origin.get_all_includes()

    def add_include_to_all_includes(self, include):
        self.origin.add_include_to_all_includes(include)

