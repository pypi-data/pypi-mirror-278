import re
import json


from .code_ import Code
from .outils import get_next_param
from .executor import Executor
from .bioflowinsighterror import BioFlowInsightError
from . import constant


class Call(Executor):
    def __init__(self, code, origin, OG_code = ''):
        self.code = Code(code = code, origin = self)
        self.origin = origin
        self.called = []
        self.first_element_called = None
        self.parameters = []#These are in the order
        self.OG_code = OG_code
        
    def __str__(self):
     return f"Call_{id(self)}"
    
    

    def get_code(self, clean_pipe = False, get_OG=False):
        if(get_OG):
            if(self.OG_code==''):
                return self.code.get_code()
            return self.OG_code
        if(clean_pipe):
            return self.clean_pipe_operator(self.code.get_code())
        else:
            return self.code.get_code()
        
    
    def get_type(self):
        return "Call"

    
    def get_first_element_called(self):
        return self.first_element_called
    
    def get_elements_called(self, tab_input = [], first_call = True):
        tab = tab_input.copy()
        #if(first_call):
        #    print(tab)
        #    if(tab!=[]):
        #        raise Exception("herer")
        #    tab = []
      
        tab += [self.first_element_called]
        for para in self.parameters:
            if(para.get_type()=="Call"):
                tab = para.get_elements_called(tab_input = tab.copy(), first_call = False)
            elif(para.get_type()=="Operation"):
                tab = para.get_elements_called(tab = tab.copy())

        temp = list(set(tab))
        #del tab
        return temp

        
    def get_code_split_space(self, code):
        to_add_spaces = ['(', ')', '}', '{']
        for character in to_add_spaces:
            code = code.replace(f'{character}', f' {character} ')
        return code.split()

    def analye_parameters(self, param):

        #Step 1 -> get parameters
        tab_params, start, next_param = [], 0, None
        temp_param = param
        while(start!=-1):
            temp_param = temp_param[start:]
            next_param, start = get_next_param(temp_param)
            tab_params.append(next_param.strip())

        #Step 2 -> analyse paramters
        for param in tab_params:
            analysed_param = False
    
            if param!='':
                #Case it's a channel
                if(re.fullmatch(constant.WORD, param) and not analysed_param):
                #if(re.fullmatch(constant.WORD, param) and not analysed_param or param in ['[]'] or param[:7]=="params."):
                    from .channel import Channel
                    channel = Channel(name=param, origin=self.origin)
                    if(not self.origin.check_in_channels(channel)):
                        self.origin.add_channel(channel)
                    else:
                        channel = self.origin.get_channel_from_name(param)
                    #TODO -> check this
                    channel.add_sink(self)
                    self.parameters.append(channel)
                    analysed_param = True
                else:
                    from .executor import Executor
                    executor = Executor(param, self)
                    executor = executor.return_type()
                    if(executor.get_type()=="Call"):
                        temp_call = executor
                        temp_call.initialise()
                        self.parameters.append(temp_call)
                    elif(executor.get_type()=="Operation"):
                        ope = executor
                        ope.initialise_from_call()
                        #Case is an Emitted -> there's only one value given and it's an emitted
                        if(ope.check_if_operation_is_an_full_emitted() and len(ope.get_gives())==1 and ope.get_gives()[0].get_type()=="Emitted"):
                            emit = ope.get_gives()[0]
                            self.parameters.append(emit)
                        else:
                            self.parameters.append(ope)
                    else: 
                        raise Exception(f"I don't know what type '{param}' is!")
    
    
    def get_nb_outputs(self):
        first=self.get_first_element_called()
        if(first.get_type()=="Process"):
            return first.get_nb_outputs()
        elif(first.get_type()=="Subworkflow"):
            return first.get_nb_emit()
        raise Exception("This soudn't happen!")
    

    def get_structure(self, dico):
        if(self.get_first_element_called().get_type()=="Process"):
            process = self.get_first_element_called()
            dico['nodes'].append({'id':str(process), 'name':process.get_alias(), "shape":"ellipse", 'xlabel':"", "fillcolor":""})
            
            def add_parameter(p):
                #Case parameter is a channel
                if(p.get_type()=="Channel"):
                    channel = p
                    channel.get_structure(dico, B=process)

                #Case parameter is a Emitted 
                elif(p.get_type()=="Emitted"):
                    emitted = p
                    emitted.get_structure(dico, B=process)

                #Case parameter is a Operation 
                elif(p.get_type()=="Operation"):
                    operation = p
                    if(operation.show_in_structure):
                        operation.get_structure(dico)
                        dico["edges"].append({'A':str(operation), 'B':str(process), "label":""})
                
                #Case parameter is a Call
                elif(p.get_type()=="Call"):
                    call = p
                    call.get_structure(dico)
                    #Case the first call is a process
                    if(call.get_first_element_called().get_type()=="Process"):
                        for output in call.get_first_element_called().get_outputs():
                            dico["edges"].append({'A':str(call.get_first_element_called()), 'B':str(process), "label":""})#TODO check name of channel
                    #Case the first call is a subworkflow
                    elif(call.get_first_element_called().get_type()=="Subworkflow"):
                        for emit in call.get_first_element_called().get_emit():
                            dico["edges"].append({'A':str(emit), 'B':str(process), "label":""})#TODO check name of channel
        
                else:
                    raise Exception(f"Type '{p.get_type()}' was given as a parameter -> I don't know how to handle this!")
            
            #If the name number of parameters are given
            if(len(self.parameters)==process.get_nb_inputs()):
                for p in self.parameters:
                    add_parameter(p)
            #If they are not -> we check that the right number isn't implied
            else:
                num_inputs = 0
                for p in self.parameters:
                    if(p.get_type()=="Call"):
                        num_inputs+= p.get_nb_outputs()
                    elif(p.get_type()=="Emitted"):
                        emitted = p
                        if(emitted.get_emitted_by().get_type()=="Subworkflow"):
                            if(emitted.get_emits()==None):
                                num_inputs+= emitted.get_emitted_by().get_nb_emit()
                            else:
                                num_inputs+=1
                        elif(emitted.get_emitted_by().get_type()=="Process"):
                            if(emitted.get_emits()==None):
                                num_inputs+= emitted.get_emitted_by().get_nb_outputs()
                            else:
                                num_inputs+=1
                        else:
                            raise Exception("This shoudn't happen")
                    else:
                        #Cause in case channel, operation or emit, it is only one channel given
                        num_inputs+=1
                if(num_inputs==process.get_nb_inputs()):
                    for p in self.parameters:
                        add_parameter(p)
                    
                else:
                    raise BioFlowInsightError(f"Not the same number of parameters given as input for the process '{process.get_alias()}'{self.get_string_line(self.get_code(get_OG=True))}.", num=2, origin=self)
        
        elif(self.get_first_element_called().get_type()=="Subworkflow"):
            sub = self.get_first_element_called()
            
            temp_dico = {}
            temp_dico['nodes'] = []
            temp_dico['edges'] = []
            temp_dico['subworkflows'] = {}
            sub.get_structure(temp_dico)
            dico['subworkflows'][sub.get_alias()] = temp_dico
            param_index = 0

            def add_parameter(p, param_index):
                sub_input = sub.get_takes()[param_index]
                #Case parameter is a channel
                if(p.get_type()=="Channel"):
                    channel = p
                    channel.get_structure(dico, B=sub_input)

                #Case parameter is a Emitted 
                elif(p.get_type()=="Emitted"):
                    emitted = p
                    emitted.get_structure(dico, B=sub_input)

                #Case parameter is a Operation 
                elif(p.get_type()=="Operation"):
                    operation = p
                    if(operation.show_in_structure):
                        operation.get_structure(dico)
                        dico["edges"].append({'A':str(operation), 'B':str(sub_input), "label":""})
                
                #Case parameter is a Call
                elif(p.get_type()=="Call"):
                    call = p
                    call.get_structure(dico)
                    #Case the first call is a process
                    if(call.get_first_element_called().get_type()=="Process"):
                        for output in call.get_first_element_called().get_outputs():
                            dico["edges"].append({'A':str(call.get_first_element_called()), 'B':str(sub_input), "label":""})#TODO check name of channel
                    #Case the first call is a subworkflow
                    elif(call.get_first_element_called().get_type()=="Subworkflow"):
                        for emit in call.get_first_element_called().get_emit():
                            dico["edges"].append({'A':str(emit), 'B':str(sub_input), "label":""})#TODO check name of channel
        
                else:
                    raise Exception(f"Type '{p.get_type()}' was given as a parameter -> I don't know how to handle this!")
                param_index+=1
                return param_index 
            
            #If the name number of parameters are given
            if(len(self.parameters)==sub.get_nb_takes()):
                for p in self.parameters:
                    param_index  = add_parameter(p, param_index )
            #If they are not -> we check that the right number isn't implied
            else:
                num_inputs = 0
                for p in self.parameters:
                    if(p.get_type()=="Call"):
                        num_inputs+= p.get_nb_outputs()
                    else:
                        #Cause in case channel, operation or emit, it is only one channel given
                        num_inputs+=1
                if(num_inputs==sub.get_nb_takes()):
                    for p in self.parameters:
                        param_index  = add_parameter(p, param_index )
                    
                else:
                    raise BioFlowInsightError(f"Not the same number of parameters given as input for the subworklfow '{sub.get_alias()}' in the call{self.get_string_line(self.get_code())}.", num = 2, origin=self)


        elif(self.get_first_element_called().get_type()=="Function"):
            None

        else:
            raise Exception(f"This shoudn't happen! is type")

    #This function synthaxes the one above -> needs to be rechecked
    def get_structure_2(self, dico):

        def add_parameter(p, to_link):

            #Case parameter is a channel
            if(p.get_type()=="Channel"):
                channel = p
                channel.get_structure(dico, B=to_link)
            
            #Case parameter is a Emitted 
            elif(p.get_type()=="Emitted"):
                emitted = p
                emitted.get_structure(dico, B=to_link)
            
            #Case parameter is a Operation 
            elif(p.get_type()=="Operation"):
                operation = p
                operation.get_structure(dico)
                dico["edges"].append({'A':str(operation), 'B':str(to_link), "label":""})
        
            #Case parameter is a Call
            elif(p.get_type()=="Call"):
                call = p
                call.get_structure(dico)
                #Case the first call is a process
                if(call.get_first_element_called().get_type()=="Process"):
                    for output in call.get_first_element_called().get_outputs():
                        dico["edges"].append({'A':str(call.get_first_element_called()), 'B':str(to_link), "label":""})#TODO check name of channel
                #Case the first call is a subworkflow
                elif(call.get_first_element_called().get_type()=="Subworkflow"):
                    for emit in call.get_first_element_called().get_emit():
                        dico["edges"].append({'A':str(emit), 'B':str(to_link), "label":""})#TODO check name of channel
           
            else:
                    raise Exception(f"Type '{p.get_type()}' was given as a parameter -> I don't know how to handle this!")
                
            
        first_call = self.get_first_element_called()
        param_index = 0
        if(first_call.get_type()=="Process" or first_call.get_type()=="Subworkflow"):
            if(first_call.get_type()=="Process"):
                dico['nodes'].append({'id':str(first_call), 'name':first_call.get_alias(), "shape":"ellipse", 'xlabel':"", 'fillcolor':''})
            else:  
                temp_dico = {}
                temp_dico['nodes'] = []
                temp_dico['edges'] = []
                temp_dico['subworkflows'] = {}
                first_call.get_structure(temp_dico)
                dico['subworkflows'][first_call.get_alias()] = temp_dico
            
            #If the name number of parameters are given
            if(len(self.parameters)==first_call.get_nb_inputs()):
                for p in self.parameters:
                    if(first_call.get_type()=="Subworklow"):
                        sub_input = first_call.get_takes()[param_index]
                        add_parameter(p, sub_input)
                        param_index+=1
                    else:
                        add_parameter(p, first_call)
            #If they are not -> we check that the right number isn't implied
            else:
                num_inputs = 0
                for p in self.parameters:
                    if(p.get_type()=="Call"):
                        num_inputs+= p.get_nb_outputs()
                    else:
                        #Cause in case channel, operation or emit, it is only one channel given
                        num_inputs+=1
                if(num_inputs==first_call.get_nb_inputs()):
                    for p in self.parameters:
                        if(first_call.get_type()=="Subworklow"):
                            sub_input = first_call.get_takes()[param_index]
                            add_parameter(p, sub_input)
                            param_index+=1
                        else:
                            add_parameter(p, first_call)
                    
                else:
                    raise Exception(f"Not the same number of parameters given as input for the process '{first_call.get_alias()}' in the call ('{self.get_code()}')")
                


    def analyse_call(self, call):
        tab_call = self.get_code_split_space(call)
        if(re.fullmatch(constant.WORD, tab_call[0]) and tab_call[1]=='('):
            #params1 = ' '.join(tab_call[2:-1])
            start = re.findall(tab_call[0]+constant.END_CALL, call)[0]
            params = call.replace(start, "")
            if(params[-1]==')'):
                params = params[:-1]
            else:
                print(self.get_code())
                raise Exception("This shouldn't happens")
            
            self.analye_parameters(params)
            process = self.get_process_from_name(tab_call[0])
            subworkflow = self.get_subworkflow_from_name(tab_call[0])
            fun = self.get_function_from_name(tab_call[0])
            if(process!=None and subworkflow==None and fun==None):
                self.first_element_called = process
            if(process==None and subworkflow!=None and fun==None):
                self.first_element_called = subworkflow
            if(process==None and subworkflow==None and fun!=None):
                self.first_element_called = fun
            if(process==None and subworkflow==None and fun==None):
                raise Exception("No first call found!!")
            self.called.append(self.first_element_called)
        else:
            print(self.get_file_address())
            raise Exception(f"Call didn't match pattern '{call}'")
    
    
    def get_called(self):
        tab = self.called
        for params in self.parameters:
            if(isinstance(params, Call)):
                tab += params.get_called()
        #TODO -> check this 
        tab = list(set(tab))
        return tab


    def write_summary(self, tab=0):
        file = open(f"{self.get_output_dir()}/debug/calls.nf", "a")
        file.write("  "*tab+f"{self}"+"\n")
        file.write("  "*(tab+1)+"* Called "+str(self.get_called())+"\n")
        file.write("  "*(tab+1)+"* Code : "+ str(self.get_code())+"\n")
        file.write("  "*(tab+1)+"* Parameters"+"\n")
        for p in  self.parameters:
            file.write("  "*(tab+3)+p.get_code()+f" '{p.get_type()}'"+"\n")
        file.write("\n")

    def add_call_count(self):
        if(self.get_first_element_called().get_type()=="Process"):
            process = self.get_first_element_called()
            with open(f"{self.get_output_dir()}/debug/processes_used.json") as json_file:
                dict = json.load(json_file)
            try:
                a = dict[process.get_file_address()]
            except:
                dict[process.get_file_address()] = []
            dict[process.get_file_address()].append(process.get_code())
            with open(f"{self.get_output_dir()}/debug/processes_used.json", "w") as outfile:
                    json.dump(dict, outfile, indent=4)
        elif(self.get_first_element_called().get_type()=="Subworkflow"):
            None
            #TODO  
        elif(self.get_first_element_called().get_type()=="Function"):
            None
            #TODO  
        else:
            raise Exception(f"I don't know what to do with '{self.get_first_element_called().get_type()}' in the call '{self.get_code()}' (in file ''{self.get_file_address()}'')")
        
    def initialise(self):
        self.analyse_call(self.get_code(clean_pipe = True))
        self.write_summary()
        #self.add_call_count()
        



