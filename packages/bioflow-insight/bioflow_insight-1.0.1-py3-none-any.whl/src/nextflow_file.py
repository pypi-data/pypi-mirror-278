
import re 
import os
import json
import glob
from datetime import date

#TODO -> check this or either change the warnings to nothing 
import warnings
from pathlib import Path

from . import constant

warnings.filterwarnings("ignore")
from .nextflow_building_blocks import Nextflow_Building_Blocks
from .outils import extract_curly, get_curly_count, get_parenthese_count, get_dico_from_tab_from_id
from .bioflowinsighterror import BioFlowInsightError





class Nextflow_File(Nextflow_Building_Blocks):
    def __init__(self, address, duplicate = True, DSL="", author = None, name = None, origin=None, output_dir='./results', display_info = True,
                 workflow = None):
        self.file = address 
        if(self.get_file_address().find('/')==-1):
            raise BioFlowInsightError(f"BioFlow-Insight cannot directly analyse a workflow from its directory. Please analyse the workflow from the parent directory instead.", num = -1)
        
        self.output_dir = Path(output_dir)
        contents = ''
        try:
            with open(self.get_file_address(), 'r') as f:
                contents = f.read()
        except Exception:
            raise BioFlowInsightError(f"No such file: '{self.get_file_address()}'.", num = 10,origin=self)
        
        Nextflow_Building_Blocks.__init__(self, contents)
        self.workflow_name = name
        self.author = author
        self.duplicate = duplicate
        self.origin = origin
        self.DSL = ""
        self.workflow = workflow
        self.first_file = DSL==""
        self.graph = None
        self.display_info = display_info
        self.all_includes = []
        self.added_2_rocrate = False
        self.check_file_correctness()
        self.set_DSL(DSL=DSL)
        #self.extract_metadata()
        self.check_file_correctness_after_DSL()
        self.set_null()
        
    def get_name_file(self):
        name = self.get_file_address().split('/')[-1]
        return name[:-3]


    def check_file_correctness(self):
        code = self.get_code()
        if(code.count("{")!=code.count("}")):
            curly_count = get_curly_count(code)
            if(curly_count!=0):
                raise BioFlowInsightError(f"Not the same number of opening and closing curlies '{'{}'}' in the file.", num = 16,origin=self)
        if(code.count("(")!=code.count(")")):
            parenthese_count = get_parenthese_count(code)
            if(parenthese_count!=0):
                raise BioFlowInsightError(f"Not the same number of opening and closing parentheses '()' in the file.", num = 16, origin=self)
            
        if(code.count('"""')%2!=0):
            raise BioFlowInsightError(f"An odd number of '\"\"\"' was found in the code.", num = 16, origin=self)
        
            #if(code.count("'''")!=code.count("'''")):
            #    raise BioFlowInsightError(f"Not the same number of ''' in the file '{self.get_file_address()}'")
            #
            #if(code.count('"""')!=code.count('"""')):
            #    raise BioFlowInsightError(f'Not the same number of """ in the file "{self.get_file_address()}"')

    #TODO -> finish function
    def check_file_correctness_after_DSL(self):
        if(self.first_file):
            if(self.DSL=="DSL2"):
                code = "\n"+self.get_code()+"\n"
                found_main = False
                for match in re.finditer(constant.WORKFLOW_HEADER_2, code):
                    found_main = True
                if(not found_main):
                    raise BioFlowInsightError(f"No 'main' workflow was found.", num = 16, origin=self)

    def get_output_dir(self):
        if(self.first_file):
            return self.output_dir
        else:
            if(self.origin==None):
                return self.output_dir 
            else:
                return self.origin.get_output_dir()
            
    def get_processes_annotation(self):
        if(self.first_file):
            return self.workflow.get_processes_annotation()
        else:
            if(self.origin==None):
                return None
            else:
                return self.origin.get_processes_annotation()
        
    def get_display_info(self):
        if (self.first_file):
            return self.display_info
        else:
            if(self.origin==None):
                return self.display_info 
            else:
                return self.origin.get_display_info()
                


    def set_name(self):
        if self.first_file and self.workflow_name is None:
            address = self.get_file_address()
            self.workflow_name = address.split('/')[-2]   
    
    def set_author(self):
        if self.first_file and self.author is None:
            address = self.get_file_address()
            try:
                self.author = address.split('/')[-3]
            except:
                self.author="Unknown"

    def get_channels(self):
        return self.channels

    def set_null(self):
        self.processes = []
        self.channels = []
        self.functions = []
        #DSL2
        self.includes = []
        self.main = None
        self.executors = []
        self.subworkflows = []
        self.already_added_structure = False
        self.graph = None
        self.all_includes = []
        self.added_2_rocrate = False
    
    def extract_metadata(self):

        #When the start=="" it means it's the first analysis
        if(self.first_file):
            self.set_null()
            self.set_name()
            self.set_author()
            dico_wf = {}
            dico_wf["workflow name"] = self.workflow_name
            dico_wf["author"] = self.author
            dico_wf["date analysis"] = date.today().strftime("%m/%d/%y")#m/d/y
            dico_wf["DSL"] = self.DSL
            dico_wf["link"] = "TODO"
            dico_wf["publish date"] = "TODO"
            dico_wf["file given"] = self.get_file_address()
            #dico_wf["processes"] = {} 
            
            if(self.DSL=="DSL1"):
                #self.extract_processes()
                #dico_wf["processes"]["number defined"] = len(self.processes)
                #dico_wf["processes"]["number used"] = len(self.processes)
                None

            elif(self.DSL=="DSL2"):
                dico_wf["number nextflow files from root"] = "TODO"
                
                ##Number of process defined
                #root = '/'.join(self.get_file_address().split('/')[:-1])
                #nextflow_files = glob.glob(f'{root}/**/*.nf', recursive=True)
                #number_defined=0
                #
                #for file in nextflow_files:
                #    
                #    wf = Nextflow_File(file, DSL="DSL2")
                #    wf.extract_processes()
                #    number_defined+=wf.get_number_processes()
                #dico_wf["processes"]["number defined"] = number_defined
                #
                ##Number of process used
                processes_used = {}
                with open(self.output_dir / "debug" / "processes_used.json", "w") as outfile:
                    json.dump(processes_used, outfile, indent=4)

            else:
                raise Exception(f"The workflow's DSL is '{self.DSL}' -> I don't know what this is!")
            
            with open(self.output_dir / "general.json", "w") as outfile:
                json.dump(dico_wf, outfile, indent=4)

    def get_type(self):
        return "Nextflow File"
    

    def get_line(self, bit_of_code):
        return self.code.get_line(bit_of_code)
    
    def get_string_line(self, bit_of_code):
        return self.code.get_string_line(bit_of_code)
        
    def set_DSL(self, DSL=""):
        #Set the DSL
        if(DSL==""):

            
            os.makedirs(self.output_dir, exist_ok=True)
            os.makedirs(self.output_dir / 'debug', exist_ok=True)
            os.makedirs(self.output_dir / 'graphs', exist_ok=True)

            with open(self.output_dir / "debug" / "operations.nf",'w') as file:
                pass
            with open(self.output_dir / "debug" / "calls.nf",'w') as file:
                pass
            with open(self.output_dir / "debug" / "operations_in_call.nf",'w') as file:
                pass
            
            self.DSL = self.which_DSL()
            self.set_null()
            if(self.get_display_info()):
                print(f"The workflow is written in '{self.get_DSL()}'")
        else:
            self.DSL = DSL


    #----------------------
    #GENERAL
    #----------------------
    def get_file_address(self):
        return os.path.normpath(self.file)
    
    def get_root_directory(self):
        if(self.origin==None):
            return '/'.join(self.get_file_address().split('/')[:-1])
        else:
            return self.origin.get_root_directory()
    
    #Returns either a subworkflow or process from the name
    def get_element_from_name(self, name):
        for process in self.processes:
            if(name==process.get_name()):
                return process
        for subworkflow in self.subworkflows:
            if(name==subworkflow.get_name()):
                return subworkflow
        for fun in self.functions:
            if(name==fun.get_name()):
                return fun
        raise BioFlowInsightError(f"'{name}' is expected to be defined in the file, but it could not be found.", num = 18, origin=self)

    def get_DSL(self):
        return self.DSL
    
    #Method which returns the DSL of the workflow -> by default it's DSL2
    #I use the presence of include, subworkflows and into/from in processes as a proxy
    def which_DSL(self):
        DSL = "DSL2"
        #If there are include
        self.extract_includes()
        if(len(self.includes)>0):
            return DSL
        #If there are subworkflows
        self.extract_subworkflows()
        if(len(self.subworkflows)>0):
            return DSL
        #If there is the main
        self.extract_main()
        if(self.main!=None):
            return DSL
        #Analyse the processes
        self.extract_processes()
        for p in self.processes:
            DSL = p.which_DSL()
            if(DSL=="DSL1"):
                return DSL
        return DSL

    #----------------------
    #PROCESS
    #----------------------
    def get_process_from_name(self, name):
        for process in self.processes:
            if(process.get_name()==name):
                return process
        if(self.duplicate):
            for include in self.includes:
                defines = include.get_defines()
                for d in defines:
                    if(d.get_alias()==name and d.get_type()=="Process"):
                        return d
        else:
            for include in self.includes:
                aliases = include.get_aliases()
                for a in aliases:
                    if(a==name and aliases[a].get_type()=="Process"):
                        return aliases[a]

        return None
        raise Exception(f"Process '{name}' couldn't be found in '{self.get_file_address()}'")


    def get_processes_defined(self, dict = {}):
        processes = self.get_processes()
        for p in processes:
            dict[p] = []
        for include in self.includes:
            _ = include.get_file().get_processes_defined(dict = dict)
        return dict


    def get_processes_called(self):
        if(self.get_DSL()=="DSL1"):
            return self.get_processes()
        elif(self.get_DSL()=="DSL2"):
            return self.main.get_processes_called(defined={})
        else:
            raise Exception("This shouldn't happen!")




    #----------------------
    #MAIN WORKFLOW
    #----------------------
    #This method extracts the "main" workflow from the file 
    def extract_main(self):
        from .main_DSL2 import Main_DSL2
        #This returns the code without the comments
        code = "\n"+self.get_code()+"\n"
        #Find pattern
        twice = False
        for match in re.finditer(constant.WORKFLOW_HEADER_2, code):
            start = match.span(1)[0]
            end = extract_curly(code, match.span(1)[1])#This function is defined in the functions file
            self.main = Main_DSL2(code= code[start:end], origin=self)
            if(twice):
                raise Exception(f"Found multiple 'main workflows' in {self.get_file_address()}")
            twice = True

    #----------------------
    #SUBWORKFLOW (ones found in the file)
    #----------------------
    def extract_subworkflows(self):
        from .subworkflow import Subworkflow
        #Get code without comments
        code = self.get_code()
        #Find pattern
        for match in re.finditer(constant.SUBWORKFLOW_HEADER, code):
            start = match.span(0)[0]
            end = extract_curly(code, match.span(0)[1])#This function is defined in the functions file
            sub = Subworkflow(code=code[start:end], origin=self, name=match.group(1))
            self.subworkflows.append(sub)

    def get_list_name_subworkflows(self):
        names = []
        for sub in self.subworkflows:
            names.append(sub.get_name())
        return names
    
    def get_subworkflow_from_name(self, name):
        for sub in self.subworkflows:
            if(sub.get_name()==name):
                return sub
        if(self.duplicate):
            for include in self.includes:
                defines = include.get_defines()
                for d in defines:
                    if(d.get_alias()==name and d.get_type()=="Subworkflow"):
                        return d
        else:
            for include in self.includes:
                aliases = include.get_aliases()
                for a in aliases:
                    if(a==name and aliases[a].get_type()=="Subworkflow"):
                        return aliases[a]
        return None
        raise Exception(f"Subworkflow '{name}' couldn't be found in '{self.get_file_address()}'")


    #----------------------
    #INCLUDES
    #----------------------
    def extract_includes(self):
        from .include import Include

        code = self.get_code()

        #pattern = r"include +{([^\}]+)} +from +([^\n ]+)"
        #pattern = r"include +({([^\}]+)}|(\w+)) +from +([^\n ]+)"
        pattern = constant.FULL_INLCUDE_2
        
        for match in re.finditer(pattern, code):
            
            includes = match.group(1).replace('{', '').replace('}', '').strip()

            #We do this if there are multiple includes
            #TODO -> this in a nicer way
            #To take into account
            #include {
            #PAIRTOOLS_SELECT
            #    as PAIRTOOLS_SELECT_VP;
            #PAIRTOOLS_SELECT
            #    as PAIRTOOLS_SELECT_LONG
            found_semi, found_n = bool(includes.find(";")+1), bool(includes.find("\n")+1)
            if(found_semi and found_n):
                temp = includes.split(";")
                tab = []
                for temp_include in temp:
                    temp_include = temp_include.replace("\n", ' ').strip()
                    if(temp_include[:3] in constant.LIST_AS):
                        tab[-1] = tab[-1]+" "+temp_include
                    else:
                        tab.append(temp_include)
                includes = tab
            elif(found_semi):
                includes = includes.split(";")
            elif(found_n):
                temp = includes.split("\n")
                tab = []
                for temp_include in temp:
                    temp_include = temp_include.strip()
                    if(temp_include[:3]in constant.LIST_AS):
                        tab[-1] = tab[-1]+" "+temp_include
                    else:
                        tab.append(temp_include)
                includes = tab
            else:
                includes = [includes]
            
            
            #TODO -> check this
            #https://www.nextflow.io/docs/latest/plugins.html#plugins
            #https://github.com/nextflow-io/nf-validation
            #address = match.group(0).split('from')[1].strip()
            address = match.group(6).strip()
            if(address[1:].split('/')[0] not in ['plugin']):
                include = Include(code =match.group(0), file = address, importing = includes, origin=self, duplicate = self.duplicate)
                self.includes.append(include)
                self.add_include_to_all_includes(include)


    def get_list_name_includes(self):
        names = []
        for include in self.includes:
            names+=include.get_list_name_includes()
        return names
    
    #----------------------
    #FUNCTIONS
    #----------------------

    #Method that extracts the functions from a file -> we don't analyse them
    #since they don't structurally change the workflow
    def extract_functions(self):
        from .function import Function
        #pattern_function = r"(def|String|void|Void|byte|short|int|long|float|double|char|Boolean) *(\w+) *\([^,)]*(,[^,)]+)*\)\s*{"
        pattern_function = constant.HEADER_FUNCTION
        code = self.get_code()
        #Find pattern
        for match in re.finditer(pattern_function, code):
            start = match.span(0)[0]
            end = extract_curly(code, match.span(0)[1])#This function is defined in the functions file
            #f = Code(code=code[start:end], origin=self)
            f = Function(code = code[start:end], name = match.group(2), origin =self)
            self.functions.append(f)

    def get_function_from_name(self, name):
        for fun in self.functions:
            if(fun.get_name()==name):
                return fun
            
        if(self.duplicate):
            for include in self.includes:
                defines = include.get_defines()
                for d in defines:
                    if(d.get_alias()==name and d.get_type()=="Function"):
                        return d
        else:
            for include in self.includes:
                aliases = include.get_aliases()
                for a in aliases:
                    if(a==name and aliases[a].get_type()=="Function"):
                        return aliases[a]
        return None

    def get_includes(self):
        return self.includes
    
    def get_all_includes(self):
        if(self.first_file):
            return self.all_includes
        else:
            return self.origin.get_all_includes()

    def add_include_to_all_includes(self, include):
        if(self.first_file):
            self.all_includes.append(include)
        else:
            self.origin.add_include_to_all_includes(include)
    
    #----------------------
    #INITIALISE
    #----------------------

    #Method that initialises the nextflow file
    def initialise(self):

        
        if(self.get_DSL()=="DSL2"):
            if(self.get_display_info()):
                print(self.get_file_address())

            #Extarct Processes
            self.extract_processes()
            #print("Extract processes :", self.processes)

            #CODE without processes
            code = self.get_code()
            for proecess in self.processes:
                code = code.replace(proecess.get_code(), "")
            #for match in re.finditer(r"\\\s*\n\s*\|", code):
            #    #TODO add line
            #    print(code)
            #    raise BioFlowInsightError(f"The use of backslash '\\' and pipe operator '|' was found in the file '{self.get_file_address()}.' ", origin=self)


            #Analyse Processes
            #TODO analyse processes

            #Extarct includes
            self.extract_includes()
            #print("Extract includes :", self.includes)

            #Analyse Inludes
            for include in self.includes:
                include.initialise()

            #Extract subworkflows
            self.extract_subworkflows()
            #print("Extract subworkflows :", self.subworkflows)

            #Extract main
            self.extract_main()
            #print("Extract main :", self.main)

            #Extract functions
            self.extract_functions()

            #Extract Executors
            self.extract_executors()
            
            #Analyse Executors
            for e in self.executors:
                e.initialise()
                
            

            #Analyse Main
            if(self.main!=None and self.first_file):
                self.main.initialise()
            
            #Analyse subworkflows
            indice=1
            for sub in self.subworkflows:
                sub.initialise()
                indice+=1

            #if(self.first_file):
            #    number_process_used = 0
            #    with open(self.output_dir / 'debug/processes_used.json') as json_file:
            #        dict = json.load(json_file)
            #    for file in dict:
            #        number_process_used+=len(set(dict[file]))
            #
            #    with open(self.output_dir / "general.json") as json_file:
            #        dico_wf = json.load(json_file)
            #
            #    #dico_wf["processes"]["number used"] = number_process_used
            #
            #    with open(self.output_dir / "general.json", "w") as outfile:
            #        json.dump(dico_wf, outfile, indent=4)
                

        elif(self.get_DSL()=="DSL1"):
            if(self.get_display_info()):
                print(self.get_file_address())
            self.extract_processes()
            self.extract_functions()
            self.extract_executors()
            for e in self.executors:
                e.initialise()
        
        else:
            raise Exception(f"I don't know what to do with this:/ '{self.get_DSL()}'")
        
        if(self.first_file):
            self.initialise_graph()


    #The start parameter is for when we call 'get_structure_DSL2' for the first time
    def get_structure_DSL2(self, dico, start = False):
        if(not self.already_added_structure):
            self.already_added_structure = True
            #Add the operations found in the file (outside of main or subworkflow) to the structure
            for o in self.executors:
                if(o.get_type()=="Operation"):
                    o.get_structure(dico)
                else:
                    if(o.get_first_element_called().get_type()!="Function"):
                        raise Exception(f"Executor of type '{o.get_type()}' was extracted in a DSL2 workflow (outside of a subworkflow or main)! This shoudn't happen! The code is '{o.get_code()}' -> it was called in file '{o.get_file_address()}'")
                
            #for c in self.get_channels():
            #    for source in c.get_source():
            #        for sink in c.get_sink():
            #            dico["edges"].append({'A':str(source), 'B':str(sink), "label":c.get_name()})

            if(start):
                if(self.main!=None):
                    self.main.get_structure(dico)
            if(not start and self.main!=None):
                warnings.warn(f"Another main was detected in the file '{self.get_file_address()}' (it is not represented in the graph)")
                #raise Exception(f'There was a second main which was detected in the workflow in the file {self.get_file_address()}')
        return dico
    


    def get_structure_DSL1(self, dico):
        for p in self.get_processes():
            p.get_structure(dico)

        for o in self.get_executors():
            if(o.get_type()=="Operation"):
                o.get_structure(dico)
            else:
                raise Exception(f"Executor of type '{o.get_type()}' was extracted in a DSL1 workflow! This shoudn't happen! The code is '{o.get_code()}'")
    
        for c in self.get_channels():
            for source in c.get_source():
                for sink in c.get_sink():
                    #If the sink an operation then the edge has already been added in the get_structure method for the operation
                    if(sink.get_type()=="Process"):
                        dico["edges"].append({'A':str(source), 'B':str(sink), "label":c.get_name()})

        return dico
                    

    def get_structure(self):
        dico = {}
        dico['nodes'] = []
        dico['edges'] = []
        dico['subworkflows'] = {}

        if(self.DSL == "DSL1"):
            return self.get_structure_DSL1(dico=dico)
        elif(self.DSL == "DSL2"):
            return self.get_structure_DSL2(dico=dico, start = True)
        else:
            raise Exception(f"The workflow's DSL is '{self.DSL}' -> I don't know what this is!")
            
    
    def initialise_graph(self):
        from .graph import Graph
        if(self.graph==None):
            self.graph = Graph(self)

    def generate_all_graphs(self, render_graphs = True, processes_2_remove = []):
        #Initialisation (obligatory)
        self.graph.initialise(processes_2_remove = processes_2_remove)

        #Generate the different graphs
        self.graph.get_specification_graph(render_graphs = render_graphs)
        self.graph.get_specification_graph_wo_labels(render_graphs = render_graphs)
        self.graph.render_graph_wo_operations(render_graphs = render_graphs)
        self.graph.get_specification_graph_wo_orphan_operations(render_graphs = render_graphs)
        self.graph.get_specification_graph_wo_orphan_operations_wo_labels(render_graphs = render_graphs)
        self.graph.render_dependency_graph(render_graphs = render_graphs)
        self.graph.get_dependency_graph_wo_labels(render_graphs = render_graphs)
        self.graph.get_dependency_graph_wo_orphan_operations(render_graphs = render_graphs)
        self.graph.get_dependency_graph_wo_orphan_operations_wo_labels(render_graphs = render_graphs)

        
        #Generate the different metadata associated with the graphs
        self.graph.get_metadata_specification_graph()
        self.graph.get_metadata_dependency_graph()
        self.graph.get_metadata_process_dependency_graph()

    def get_graph(self):
        return self.graph
    #def get_metadata_graph_wo_operations(self):
    #    self.graph.get_metadata_graph_wo_operations()
    
    def add_main_DSL1_2_rocrate(self, dico, file_dico, file_name):
        main_key = f"{file_name}/main"
        file_dico["hasPart"].append(main_key)
        dico_main = {}
        dico_main["@id"] = main_key
        dico_main["name"] = "Main Workflow"
        dico_main["@type"] = ["SoftwareSourceCode", "ComputationalWorkflow"]
        #TODO -> check if this remains true
        #dico_main["conformsTo"] = {"@id": "https://bioschemas.org/profiles/ComputationalWorkflow/0.5-DRAFT-2020_07_21"}
        #dico_main["dct:conformsTo"]= "https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE/"
        dico_main["input"] = []
        dico_main["output"] = []
        dico_main["isPartOf"] = [{"@id": file_name}]
        dico_main["hasPart"] = []
        self.add_processes_2_rocrate(dico, dico_main, main_key)
        dico["@graph"].append(dico_main)

    def add_processes_2_rocrate(self, dico, file_dico, file_name):
        for p in self.processes:
            process_key = f"{file_name}/{p.get_name()}"
            file_dico["hasPart"].append(process_key)
            p.add_2_rocrate(dico, file_name)

    def add_includes_2_rocrate(self, dico, file_dico, file_name):
        for include in self.includes:
            included_key = include.get_file().get_file_address()[len(dico["temp_directory"])+1:]
            file_dico["hasPart"].append({"@id":included_key})
            included_dico = get_dico_from_tab_from_id(dico, included_key)
            included_dico["isPartOf"].append({"@id":file_name})
            include.get_file().add_2_rocrate(dico)

    def add_subworkflows_2_rocrate(self, dico, file_dico, file_name):
        for sub in self.subworkflows:
            sub_key = sub.get_rocrate_key(dico)
            file_dico["hasPart"].append({"@id":sub_key})
            sub.add_2_rocrate(dico, file_name)

    def add_2_rocrate(self, dico):
        if(not self.added_2_rocrate):
            self.added_2_rocrate = True
            file_name = self.get_file_address()[len(dico["temp_directory"])+1:]
            file_dico = get_dico_from_tab_from_id(dico, file_name)
            if(self.first_file):

                #Case DSL1
                if(self.get_DSL()=="DSL1"):
                    #file_dico["@type"].append("ComputationalWorkflow")
                    self.add_main_DSL1_2_rocrate(dico, file_dico, file_name)
                    self.add_processes_2_rocrate(dico, file_dico, file_name)
                
                #Case DSL2
                elif(self.get_DSL()=="DSL2"):
                    self.add_processes_2_rocrate(dico, file_dico, file_name)
                    self.add_includes_2_rocrate(dico, file_dico, file_name)
                    self.main.add_2_rocrate(dico, file_name)
                    self.add_subworkflows_2_rocrate(dico, file_dico, file_name)
                    
                else:
                    raise Exception("This shoudn't happen!")
            else:
                if(self.get_DSL()=="DSL2"):
                    self.add_processes_2_rocrate(dico, file_dico, file_name)
                    self.add_includes_2_rocrate(dico, file_dico, file_name)
                    self.add_subworkflows_2_rocrate(dico, file_dico, file_name)
                    
                    #TODO 
                else:
                    raise Exception("This shoudn't happen!")
            

