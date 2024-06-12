

import warnings

#TODO
#- uniform eveything here
#- add a list of words illegal for channel eg. [true, process, workflow...]

import re
from .outils import get_end_operator, get_end_call
from .code_ import Code
from .executor import Executor
from .bioflowinsighterror import BioFlowInsightError
from . import constant


class Operation(Executor):
    def __init__(self, code, origin, OG_code = ''):
        self.origin = origin
        self.code = Code(code, origin = self)
        self.origins = []
        self.gives = []
        self.label = ""
        self.calls = {}
        self.OG_code = OG_code
        self.show_in_structure = True
        self.operation_type = None

    def change_code(self, code):
        self.code = Code(code, origin = self)



    def add_element_gives(self, ele):
        self.gives.append(ele)

    def add_element_origins(self, ele):
        self.origins.append(ele)


    def is_defined_in_process(self, process):
        if(len(self.gives)!=0):
            raise Exception(f"This operation is defined in {process.get_name()} shoudn't be able to give a channel")
        #Don't need to remove it from the list of operations cause it was never added (that's done outside of the operation)
        for c in self.origins:
            c.remove_element_from_sink(self)
            c.add_sink(process)

    def get_name(self):
        return str(self)

    
    def get_gives(self):
        return self.gives
    
    def get_type(self):
        return "Operation"
    
    def check_in_channels(self, channel):
        return self.origin.check_in_channels(channel)   

    def add_channel(self, channel):
        self.origin.add_channel(channel)   

    def get_elements_called(self, tab = []):
        for o in self.origins:
            if(o.get_type()=="Call"):
                tab+=o.get_elements_called()
        return tab


    def add_origin_channel(self, name):
        from .channel import Channel
        #Check that the name is not the list of illegal words
        #and Check that the thing extarcted is not WorkflowNameFile like 'WorkflowHgtseq' in nf-core/hgtseq
        if(name not in constant.ERROR_WORDS_ORIGINS and name.lower()!=f"workflow{self.get_name_file().lower()}"):
            channel = Channel(name=name, origin=self.origin)
            #TODO -> this needs to be checked
            if(not self.origin.check_in_channels(channel)):
                    self.origin.add_channel(channel)
            else:
                channel = self.origin.get_channel_from_name(name)
            self.origins.append(channel)
            #channel.initialise()
            channel.add_sink(self)
        


    #I don't need to define the equivalent gives -> cause it's not possible:)
    def add_origin_emits(self, full_code, name_called, name_emitted):
        from .emitted import Emitted
        #Check that it not already been added
        added = False
        for o in self.origins:
            if(full_code==o.get_code()):
                added = True

        if(not added):
            #full_code, name_called, name_emitted = match.group(1), match.group(2), match.group(3)
            IGNORE_NAMES = ['params']
            #In the cas an operator is extracted at the end of the emit
            if(full_code.count('.')>=2):
                splited = full_code.split('.')
                if( splited[-1] in constant.LIST_OPERATORS):
                    full_code = '.'.join(splited[:-1])
            if(name_called not in IGNORE_NAMES):
                process = self.origin.get_process_from_name(name_called)
                subworkflow = self.origin.get_subworkflow_from_name(name_called)

                if(process!=None and subworkflow!=None):
                    raise Exception(f"Problem in get_element -> {name_called} exists as process and subworkflow")
                #Case subworkflow
                if(process==None and subworkflow!=None):
                    emitted = Emitted(name=full_code, origin=self.origin, emitted_by=subworkflow)
                    emitted.set_emits(name_emitted)
                #Case Process
                if(process!=None and subworkflow==None):
                    emitted = Emitted(name=full_code, origin=self.origin, emitted_by=process)
                    #TODO -> analyse the outputs of the process

                if(process==None and subworkflow==None):
                    if(name_called[:5]=="Call_"):
                        name_called = self.calls[name_called].get_code()
                    raise BioFlowInsightError(f"The call for '{name_called}' coudn't be found, before its use in the operation '{self.get_code(get_OG=True)}'{self.get_string_line(self.get_code(get_OG=True))}. Either because the call wasn't made before the operation or that the element it is calling doesn't exist.", num =8, origin=self)

                emitted.add_sink(self)
                self.origins.append(emitted)

    #This methods checks if the input is an emit and adds it if it's the case, it also returns T/F if it's an emit
    def check_is_emit(self, name):
        pattern_emit_tab = constant.EMIT_TAB
        pattern_emit_name = constant.EMIT_NAME
        patterns = [pattern_emit_tab, pattern_emit_name]
        found_an_emit = False
        for pattern in patterns:
            for match in re.finditer(pattern, name):
                found_an_emit = True
                full_code, name_called, name_emitted = match.group(0), match.group(1), match.group(3)
                if(name_emitted not in constant.LIST_OPERATORS):
                    self.add_origin_emits(full_code, name_called, name_emitted)
                else:
                    self.add_origin_emits(full_code, name_called, "")

        if(not found_an_emit):
            for match in re.finditer(constant.EMIT_ALONE, name+' '):
                found_an_emit = True
                full_code, name_called = match.group(0).strip(), match.group(1)
                self.add_origin_emits(full_code, name_called, "")

        return found_an_emit

    #Function that returns if an operation is a create or a branch
    def get_operation_type(self):
        if(self.operation_type==None):
            if(len(self.origins)!=0 and len(self.gives)!=0):
                return 'Branch'
            else:
                return 'Create'
        return self.operation_type
        
    def set_operation_type(self, type):
        self.operation_type = type


    #Here since the operation "gives" a channel -> we don't check 
    #if it's a global channel since we are defining a new one
    def add_gives(self, name):
        from .channel import Channel
        #Case it's a call and it's been replaced
        if(re.fullmatch(constant.CALL_ID, name)):
            self.gives.append(self.calls[name])
            raise Exception("This shoudn't happen! -> a call is taking a value")
        
        else:
            channel = Channel(name=name, origin=self.origin)
            if(not self.origin.check_in_channels(channel)):
                self.origin.add_channel(channel)
            else:
                channel = self.origin.get_channel_from_name(name)

            self.gives.append(channel)
            #channel.initialise()
            channel.add_source(self)

    def add_origin(self, name):
        #Check that it's not already been added
        added = False
        for o in self.origins:
            if(name==o.get_code()):
                added = True

        if(not added):
            if(self.origin.get_DSL()=="DSL2"):
                #Case it's a call and it's been replaced
                if(re.fullmatch(constant.CALL_ID, name)):
                    self.origins.append(self.calls[name])
                else:
                    ##Case it's a subworkflow
                    #subworkflow = self.origin.get_subworkflow_from_name(name)
                    #process = self.origin.get_process_from_name(name)
                    #if(subworkflow!=None):
                    #    print("George it's a subworkflow")
                    #    #Case suborkflow
                    #    self.origins.append(subworkflow)
                    ##Case process
                    #elif(process!=None):
                    #    print("George it's a process")
                    #    #Case process
                    #    self.origins.append(process)
                    ##In this case it's a channel
                    #else:
                    self.add_origin_channel(name)
            else:
                self.add_origin_channel(name)
                

    #Function that from an operation gives the origin ('input') channels
    #For every case i have checked by compilying the nextflow code for each operator
    def initialise_origins(self):
        operation = self.get_code(clean_pipe = True)+" "
        ERROR_WORDS = constant.ERROR_WORDS_ORIGINS

        #Replace the channels written like "ch[0]" to "ch" -> since in anycase it's just a 
        #subpart of the channel (we can't analyse what's in the channel)
        replacing_tab = True
        while(replacing_tab):
            replacing_tab = False
            pattern_channel_tab = constant.CHANNEL_TAB
            for match in re.finditer(pattern_channel_tab, operation):
                if(match.group(1) not in ["out", "output"]):
                    operation = operation.replace(match.group(0), match.group(1))
                    replacing_tab = True
                    break

        #pattern= r'([^\=\n]+)\s*=\s*([^\?\n]+)\s*\?([^\n]+)'
        #if(bool(re.fullmatch(pattern, operation))):
        #     for match in re.finditer(pattern, operation):
        #          origin_temp = match.group(3).split(":")
        #          for o in origin_temp:
        #               origin.append(o.strip())
                    

        #else:
                
        #If the first word after an '=' is not the channel key word than it is an actual channel
        #TODO -> check if this condition actually works!!
        #temp = operation.split('.')[0].split('=')[-1].strip()
        #if(get_first_word(temp)!='Channel' and get_first_word(temp)!='channel'):
        #    origin.append(get_first_word(temp)) 

        #TODO -> does this case ever exist?
        #================================
        #Case channel1
        #================================
        if(bool(re.fullmatch(constant.WORD, operation.strip()))):
            self.add_origin(operation)


        #Case tupel with call -> this is not supported by BioFlow-Insight -> try calling first then using the emits
        if(bool(re.fullmatch(r"\( *\w+ *(\, *\w+)+ *\) *= *Call_\d+", operation.strip()))):
            raise BioFlowInsightError(f"A tuple is associated with an call{self.get_string_line(self.get_code(get_OG= True))}. BioFlow-Insight doesn't support this (see specification list), try defining the operation in a different way.", num=9, origin=self)


        case_operation_starts_with_emit = False
        #---------------------------
        #Check emits
        #---------------------------
        #================================
        #Case call.out[num]
        #================================
        #TODO -> here i assume that the [] is a decimal not necessary the case
        pattern_emit_tab = constant.EMIT_TAB
        #================================
        #Case channel1 = call.out.something
        #================================
        pattern_emit_name = constant.EMIT_NAME
        patterns = [pattern_emit_tab, pattern_emit_name]
        first_call = True
        for pattern in patterns:
            #================================
            #Case channel1 = emits
            #================================
            pattern_equals = r"\w+\s*=\s*\(?\s*("+pattern+r")"
            for match in re.finditer(pattern_equals, operation):
                full_code, name_called, name_emitted = match.group(1), match.group(2), match.group(4)
                if(name_emitted in constant.LIST_OPERATORS):
                    self.add_origin_emits(full_code, name_called, "")
                else:
                    self.add_origin_emits(full_code, name_called, name_emitted)
                case_operation_starts_with_emit = True
        
            #================================
            #Case call.out[].something().. or call.out.channel.something().. -> we want to extract that emits
            #================================
            for match in re.finditer(pattern, operation):
                if(first_call):
                    full_code, name_called, name_emitted = match.group(0), match.group(1), match.group(3)
                    
                    #Check that it's a the begining of the operation
                    code = operation
                    operation_until_out = code[:code.find("out")]
                    if(operation_until_out==full_code[:full_code.find("out")]):
                        code_wo_spaces = code.replace(' ', '')
                        #We check that the term after the out is an operator or a channel
                        is_operator = True
                        try:
                            if(code_wo_spaces[len(match.group(0).replace(' ', ''))] in ['(', '{']):
                                is_operator=True
                            else:
                                is_operator=False
                        except:
                            is_operator=False
                        if(is_operator):
                            
                            self.add_origin_emits(full_code, name_called, "")
                        else:
                            self.add_origin_emits(full_code, name_called, name_emitted)
                        case_operation_starts_with_emit = True
                    first_call = False

       
        #Here i the case where we assume the emit looks like "call.out"
        if(not case_operation_starts_with_emit):
            #================================
            #Case channel1 = emits
            #================================
            pattern_equals = constant.EMIT_EQUALS
            for match in re.finditer(pattern_equals, operation):
                full_code, name_called = match.group(1), match.group(2)
                self.add_origin_emits(full_code, name_called, "")
                case_operation_starts_with_emit = True

            #================================
            #Case call.out.something().. we want to extract that emits
            #================================
            #for match in re.finditer(r"(\w+)\s*\.\s*out", operation):
            #TODO -> check this 
            #I've changed this to avoid problems like this : "ch_svdb_dbs.out_occs.toList()"
            for match in re.finditer(constant.EMIT_OPERATION, operation+" "):
                    full_code, name_called = match.group(0), match.group(1)
                    #Check that it's a the begining of the operation
                    operation_until_out = operation[:operation.find("out")]
                    if(operation_until_out==full_code[:full_code.find("out")]):
                        self.add_origin_emits(full_code, name_called, "")
                        case_operation_starts_with_emit = True
     



        if(not case_operation_starts_with_emit):
            
            #================================
            #Case channel1 = channel2.something
            #================================
            pattern= constant.CHANNEL_EQUALS_OPERATION
            for match in re.finditer(pattern, operation):
                if(match.group(1) not in ERROR_WORDS):
                    #Here we create the channel from the name -> checks if it already exists in the workflow
                    name = match.group(1)
                    if(bool(re.fullmatch(constant.WORD, name))):
                        self.add_origin(name)

            #================================
            #Case channel1 = [.., ..]
            #================================
            pattern= constant.CHANNEL_EQUALS_LIST
            if(bool(re.fullmatch(pattern, operation.strip()))):
                for match in re.finditer(pattern, operation):
                    origin_possibilities = match.group(1).split(",")
                    for o in origin_possibilities:
                        name = o.strip()
                        if(name not in ERROR_WORDS):
                            #Here we create the channel from the name -> checks if it already exists in the workflow
                            if(bool(re.fullmatch(constant.WORD, name))):
                                self.add_origin(name)

            #================================
            #Case (ch1, ch2, ...) = emit.out
            #================================
            pattern= constant.TUPLE_EMIT
            for match in re.finditer(pattern, operation):
                raise BioFlowInsightError(f"A tuple is associated with an emit{self.get_string_line(self.get_code(clean_pipe = False))}. BioFlow-Insight doesn't support this (see specification list), try defining the operation in a different way.", num=7, origin=self)



            #================================
            #Case (ch1, ch2, ...) = channel.something
            #================================
            pattern= constant.TUPLE_EQUALS
            for match in re.finditer(pattern, operation):
                if(match.group(2) not in ERROR_WORDS):
                    #Here we create the channel from the name -> checks if it already exists in the workflow
                    name = match.group(2)
                    if(bool(re.fullmatch(constant.WORD, name))):
                        self.add_origin(name)
            
            #================================
            #Case channel1 = channel2
            #================================
            if(bool(re.fullmatch(constant.CHANNEL_EQUALS, operation.strip()))):
                temp = operation.split('=')[-1].strip()
                if(temp not in ERROR_WORDS and bool(re.fullmatch(constant.WORD, temp))):
                    #Here we create the channel from the name -> checks if it already exists in the workflow
                    self.add_origin(temp)


            #================================
            #Case (ch1, ch2, ...) = (ch1_1, ch2_1, ...)
            #================================
            #Nextflow doesn't allow this 
            #TODO -> double check

            #================================
            #Case channel.something().. -> we want to extract that channel
            #================================
            index_dot = operation.find(".")
            if(index_dot!=-1):
                if(bool(re.fullmatch(constant.WORD_DOT, operation[:index_dot+1].strip()))):
                    temp = operation[:index_dot].strip()
                    if(temp not in ERROR_WORDS and bool(re.fullmatch(constant.WORD, temp))):
                        #Here we create the channel from the name -> checks if it already exists in the workflow
                        name = temp
                        if(bool(re.fullmatch(constant.WORD, name))):
                            self.add_origin(name)

       
        ##================================
        ##join/ phase/ cross/ combine
        ##================================
        #pattern= r'\.\s*(join|phase|cross|combine)\s*\(([^\)]+)\)'
        #for match in re.finditer(pattern, operation):
        #    name = match.group(2).strip()
        #    #Case channel
        #    if(bool(re.fullmatch(r'\w+', name))):
        #        self.add_origin(name)
        #    else:
        #        #check and add if it's an emitted value
        #        emited = self.check_is_emit(name)
        #        if(not emited):
        #            raise Exception(f"I don't know what i'm looking at {name} in {self.get_code()}")

        
        #================================
        #merge/ mix/ concat/ spread/ join/ phase/ cross/ combine
        #================================
        pattern= constant.MERGE_OPERATIONS
        for match in re.finditer(pattern, operation):
            start, end, beginning_character= match.span(1)[0], match.span(1)[1], match.group(3)
            operator_call, operator_params = get_end_operator(operation, start, end, beginning_character)
            spliting_param = ''
            if(beginning_character=="("):
                spliting_param=","
            if(beginning_character=="{"):
                spliting_param=";"
            temp= operator_params.split(spliting_param)
            for t in temp:
                name = t.strip()
                #Case channel
                if(bool(re.fullmatch(constant.WORD, name))):
                    self.add_origin(name)
                else:
                    #check and add if it's an emitted value
                    emited = self.check_is_emit(name)
                    if(not emited):
                        #TODO -> check at what extend this is used
                        channels = self.get_channels()
                        for c in channels:
                            if(c.get_name() in name):
                                pos = [m.start() for m in re.finditer(c.get_name(), operation)]
                                to_add = True
                                for p in pos:
                                    if(p>0):
                                        #Check it is actually the channel and not a different channel
                                        if(bool(re.fullmatch(constant.ILLEGAL_CHARCTER_BEFORE_POTENTIAL_CHANNELS, operation[p-1]))):
                                            to_add = False
                                        if(bool(re.fullmatch(constant.ILLEGAL_CHARCTER_AFTER_POTENTIAL_CHANNELS, operation[p+len(c.get_name())]))):
                                            to_add = False
                                if(to_add):
                                    self.add_origin(c.get_name())
                        #TODO update this -> it's an operation itselfs
                        warnings.warn(f"I don't know what i'm looking at '{name}' in '{self.get_code()}'\n")
        
        ##================================
        ##merge/ mix/ concat
        ##================================
        #pattern= r'\.\s*(merge|mix|concat)\s*\((\s*\w+\s*\,\s*(\w+\s*\,\s*)*\w+\s*|\s*(\w+)\s*)\)'
        #for match in re.finditer(pattern, operation):
        #    temp=match.group(2)
        #    temp= temp.split(',')
        #    for t in temp:
        #        t= t.strip()
        #        #Here we create the channel from the name -> checks if it already exists in the workflow
        #        name = t
        #        if(bool(re.fullmatch(r'\w+', name))):
        #            self.add_origin(name)
        #
        ##================================
        ##spread
        ##================================
        #pattern= r'\.\s*spread\s*\(([\s\w\.(),\"\'\{\}\[\]+-]+)\)'
        #for match in re.finditer(pattern, operation):
        #    #Here we create the channel from the name -> checks if it already exists in the workflow
        #    name = match.group(1).strip()
        #    if(bool(re.fullmatch(r'\w+', name))):
        #        self.add_origin(name)

        #print(self.origin)
        #self.origins = list(set(origin))
        



    #Method that intialises the gives (the outputs) of an opeartion
    def initialise_gives(self):
        code = self.get_code(clean_pipe = True)
        #Case channel1 = something -> then channel1 is added to the gives
        if(bool(re.fullmatch(constant.CHANNEL_EQUALS_SOMETHING, code))):
            first_gives = code.split("=")[0].strip()
            if(bool(re.fullmatch(constant.WORD, first_gives))):
                self.add_gives(first_gives)
        
        #Case (ch1, ch2, ...) = something -> then ch1, ch2, ... is added to the gives
        elif(bool(re.fullmatch(constant.TUPLE_EQUALS_SOMETHING, code))):
            for match in re.finditer(constant.TUPLE_EQUALS_SOMETHING, code):
                to_give = match.group(1)[1:-1]#Removing the parentheses
                to_give = to_give.split(",")
                for g in to_give:
                    g = g.strip()
                    if(bool(re.fullmatch(constant.WORD, g))):
                        self.add_gives(g)
                    else:
                        raise Exception("Something unexpected")

        #else:
        #    print(self.get_code())
        #    raise Exception("Something unexpected!")
                
       
        #Cases we use the "set" operators
        set_operators = constant.SET_OPERATORS
        start_end = [["(", ")"], ["{", "}"]]
        for operator in set_operators:
            for start, end in start_end:
                pattern = f"{operator}\s*\{start}([^\{end}]+)\{end}"
                for match in re.finditer(pattern, code):
                    channels = match.group(1)
                    #Add channel
                    gives = re.split(';|,|\n', channels)
                    for g in gives:
                        c = g.strip()
                        if(c!=""):
                            if(bool(re.fullmatch(constant.WORD, c))):
                                if(not bool(re.fullmatch(constant.NUMBER, c))):
                                    self.add_gives(c)
                            else:
                                #check and add if it's an emitted value
                                emited = self.check_is_emit(c)
                                #TODO -> do i not need to add it in the gives?
                                if(not emited):
                                    raise Exception(f"I don't know what i'm looking at '{c}' in '{self.get_code()}'")
                            
                    
                #print(operator, s, start, end)
    
    

    def get_origins(self):
        return self.origins
    
    #def get_origins(self):
    #    tab = []
    #    for o in self.origins:
    #        #tab.append(o.get_name())
    #        tab.append(o)
    #    return tab

    def get_gives(self):
        tab = []
        for g in self.gives:
            #tab.append(g.get_name())
            tab.append(g)
        return tab
    
    def print_operation(self):
        print(self.get_code())

    #TODO -> put this somewhere
    def check_loop(self):
        for g in self.gives:
            for o in self.origins:
                if(g==o):
                    print(f"Loop here:\n- {self.get_code()}\n- For the {o.get_name()} channel")

    #This method checks if an operation is just a full emited 
    #This is in the case of a parameter in a call
    def check_if_operation_is_an_full_emitted(self):
        #george_here
        pattern_emit_tab  = constant.EMIT_TAB
        pattern_emit_name = constant.EMIT_NAME
        pattern_emit_full = constant.EMIT_ALONE_2
        patterns = [pattern_emit_tab, pattern_emit_name, pattern_emit_full]
        for pattern in patterns:
            if(bool(re.fullmatch(pattern, self.get_code(clean_pipe = True)))):
                return True
        return False

    
    #def print_summary(self, tab = 0, print_code=False):
    #    print("  "*tab+f"{self}")
    #    if(print_code):
    #        print("  "*(tab+1)+"* Code :", self.get_code())
    #    print("  "*(tab+1)+"* Origins")
    #    for o in self.get_origins():
    #        print("  "*(tab+1+2)+o.get_code(), f"'{o.get_type()}'")
    #    print("  "*(tab+1)+"* Gives")
    #    for g in self.get_gives():
    #        print("  "*(tab+1+2)+g.get_code(), f"'{g.get_type()}'")
        
    def write_summary(self, address, tab = 0):
        file = open(address, "a") 
        file.write("  "*tab+f"{self}\n") 
        file.write("  "*(tab+1)+"* Code : "+str(self.get_code())+ "\n")
        file.write("  "*(tab+1)+"* Origins"+ "\n")
        for o in self.get_origins():
            file.write("  "*(tab+1+2)+o.get_code()+ f" '{o.get_type()}'\n")
        file.write("  "*(tab+1)+"* Gives\n")
        for g in self.get_gives():
            file.write("  "*(tab+1+2)+g.get_code()+ f" '{g.get_type()}'\n")
        
        file.write("\n")
        
        # Closing the opened file 
        file.close()


    def get_code(self, replace_calls = True, clean_pipe = False, get_OG=False):
        code = self.code.get_code()
        if(get_OG):
            if(self.OG_code!=""):
                return self.OG_code
            else:
                return code

        

        if(clean_pipe):
            code = self.clean_pipe_operator(code)
  
        if(replace_calls):
            for call in self.calls:
                code = code.replace(self.calls[call].get_code(), str(call))
            
        return code
    
    def initialise_double_dot(self):
        self.extract_calls(clean_pipe=False)
        code = self.get_code(clean_pipe = False)
        pattern = constant.DOUBLE_DOT
        for match in re.finditer(pattern, code):
            double_dot = match.group(0).strip()
        
            c = double_dot.split("=")[0].strip()
            self.add_gives(c)
            
            possibilities = double_dot[double_dot.rfind('?')+1:].split(":")
            for p in possibilities:
                p = p.strip()
                if(p!=""):
                    name = p
                    #print(name)
                    if(bool(re.fullmatch(constant.WORD, name))):
                        self.add_origin(name)
                    elif(self.check_is_emit(name)):
                        None
                    #else:
                    #    raise Exception(f"Don't know what i'm looking at '{name}' in operation '{self.get_code()}', in file '{self.get_file_address()}'!")
                

    

    def extract_calls(self, clean_pipe = True):
        from .call import Call
        to_call = self.get_name_processes_subworkflows()
        pattern_call = constant.BEGINNING_CALL
        searching = True
        while(searching):
            searching= False
            text = self.get_code(clean_pipe = clean_pipe)
            
            for c in self.calls:
                text = text.replace(self.calls[c].get_code(), "")
            for match in re.finditer(pattern_call, text):
                if(match.group(1) in to_call):
                    searching=True
                    start, end = match.span(0)
                    call = Call(code =get_end_call(text, start, end), origin =self)
                    call.initialise()
                    self.calls[str(call)] = call
                    break

        #pattern_call_pipe = r"\|\s*(\w+)"
        #searching = True
        #while(searching):
        #    searching= False
        #    text = self.get_code(clean_pipe = clean_pipe)
        #    
        #    for c in self.calls:
        #        text = text.replace(self.calls[c].get_code(), "")
        #    for match in re.finditer(pattern_call_pipe, text):
        #        if(match.group(1) in to_call):
        #            print(match.group(1), text)
        #            start, end = match.span(0)
        #            from .outils import checks_in_condition_if, checks_in_string, extract_inside_parentheses
        #            if(not checks_in_condition_if(text, match.group(1)) and not checks_in_string(text, match.group(1))):
        #                searching=True
        #                call = Call(code =extract_inside_parentheses(text, match.group(1)), origin =self)
        #                call.initialise()
        #                self.calls[str(call)] = call
        #                break
  
    

    def initialise(self):
        pattern = constant.DOUBLE_DOT
        #If the operation is a double dot consition thing
        if(bool(re.fullmatch(pattern, self.get_code(clean_pipe = False)))):
            self.initialise_double_dot()
        elif(bool(re.fullmatch(constant.DOUBLE_DOT_TUPLE, self.get_code(clean_pipe = False)))):
            raise BioFlowInsightError(f"A ternary conditional operator was used with an tuple{self.get_string_line(self.get_code(clean_pipe = False))}. BioFlow-Insight doesn't support this yet (see specification list), try defining the operation in a different way.", num=5, origin=self)
        else:
            self.extract_calls()
            self.initialise_origins()
            self.initialise_gives()



        self.write_summary(self.get_output_dir() / "debug/operations.nf")
        
    def check_if_empty_call(self):
        return self.get_code()==""
    


    def initialise_from_call(self):
        if(self.get_code()!="" and self.get_code()[0]=="[" and self.get_code()[-1]=="]"):
            #print("in list", self.get_code())
            None
            #TODO
            #basically in this code -> i want to do the same thing for analye_parameters for a call
            #But instead of adding them to the params, adding them to the gives..
            #Cause in the list you can put anything really
            
        #Working here
        if(self.get_code()!=""):
            self.extract_calls()
            self.initialise_gives()
            self.initialise_origins()
            self.gives+=self.origins
            self.gives = list(set(self.gives))
            #TODO -> this was originally uncommented, check it doesn't add any other bugs
            #self.origins = []
            warnings.warn(f"TO CHECK !! From this : '{self.get_code()}'. I extracted to give (for a call) '{self.gives}' (in file '{self.get_file_address()}')\n")
            #TODO
            #We check that the operation is an actuel operation and not just a string for example
            #if(len(self.get_origins())==0 and len(self.get_gives())==0):
            #    self.show_in_structure = False

        self.write_summary(self.get_output_dir() / "debug/operations_in_call.nf")

    def get_structure(self, dico, to_remove = False):
        if(self.show_in_structure):
            code = self.get_code(replace_calls=False)
            #Need to replace /* and */ by /\* and *\/ so graphivz doesn't think it's a comment
            #Same for // -> replace it by /\/\
            code = code.replace("/*", "/\*").replace("*/", "*\/").replace("//", "/\/\\")
            code = code.replace('"', "'")
            if(self.get_operation_type()=="Branch"):
                fillcolor = "white"
            else:
                fillcolor = ""

            #TODO check this -> IMPORTANT
            if(not to_remove):
                dico['nodes'].append({'id':str(self), 'name':"", "shape":"point", 'xlabel': code, 'fillcolor':fillcolor})
            else:
                #The ones which have the 'to_remove' name is because they are used in as takes and emits in subworkflow (they will be removed in post)
                dico['nodes'].append({'id':str(self), 'name':"to_remove", "shape":"point", 'xlabel': code, 'fillcolor':fillcolor})


            for o in self.origins:
                #Case origins is a channel
                if(o.get_type()=="Channel"):
                    channel = o
                    channel.get_structure(dico, B=self)
                
                #Case origins is a call
                elif(o.get_type()=="Call"):
                    call = o
                    call.get_structure(dico)
                    #Case the first call is a process
                    if(call.get_first_element_called().get_type()=="Process"):
                        dico["edges"].append({'A':str(call.get_first_element_called()), 'B':str(self), "label":""})#TODO check name of channel
                    #Case the first call is a subworkflow
                    elif(call.get_first_element_called().get_type()=="Subworkflow"):
                        sub = call.get_first_element_called()
                        if(sub.get_nb_emit()==0):
                            raise BioFlowInsightError(f"The subworkflow '{sub.get_name()}' doesn't emit anything. It is given to an operation{self.get_string_line(call.get_code())}.", num=20, origin=self)
                        elif(sub.get_nb_emit()>1):
                            raise BioFlowInsightError(f"To much to unpack : The subworkflow '{sub.get_name()}' emits over one channel in a operation{self.get_string_line(call.get_code())}.", num=20, origin=self)
                            #TODO recommendation -> try using an emit subworkflow.out
                        else:
                            emit = sub.get_emit()[0]
                            dico["edges"].append({'A':str(emit), 'B':str(self), "label":emit.get_code()})
                        #for out in sub.get_emit():
                        #    print(out, out.get_code())
                        #    #These are channels
                        #    #TODO check this -> it was the one line 644 before
                        #    #out.get_structure(dico, B=self)
                        #    out.get_structure(dico)

                    elif(call.get_first_element_called().get_type()=="Function"):
                        #TODO check if this is actually the cas
                        None
                    else:
                        raise Exception("This souldn't happen!")
                    
                
                #Case origins is a Emmited
                elif(o.get_type()=="Emitted"):
                    emitted = o
                    emitted.get_structure(dico, B=self)

                else:
                    print(self.get_code())
                    print(self.get_file_address())
                    raise Exception(f"This souldn't happen! The origin of an operation is of type '{o.get_type()}'. It's code is '{o.get_code()}'")
                

