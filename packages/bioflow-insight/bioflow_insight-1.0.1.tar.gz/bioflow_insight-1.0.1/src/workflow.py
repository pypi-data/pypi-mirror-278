#Import dependencies
#Local
from .nextflow_file import Nextflow_File
from .ro_crate import RO_Crate
from . import constant
from .outils_graph import flatten_dico, initia_link_dico_rec, get_number_cycles
from .bioflowinsighterror import BioFlowInsightError

#Outside packages
import os
import re
import json
from pathlib import Path
import glob
import ctypes



class Workflow:
    """
    This is the main workflow class, from this class, workflow analysis can be done.
    After analysis, workflow structure reconstruction can be done.

    Attributes:
        file: A string indicating the address to the workflow main or the directory containing the workflow
        duplicate: A boolean indicating if processes are to be duplicated in the structure
        display_info: A boolean indicating if the analysis information should be printed
        output_dir: A string indicating where the results will be saved
        name: A string indicating the name of the workflow
        datePublished: A string indicating the date of publication of the workflow
        description: A string indicating the description of the workflow
        license: A string indicating the license of the workflow
        creativeWorkStatus: A string indicating the creative work statuts of the workflow
        authors: A string inidcating the authors of the workflow
        version: A string indicating the version of the workflow
        keywords: A string indicating the keywords of the workflow
        producer: A string indicating the producer of the workflow
        publisher: A string indicating the publisher of the workflow
        processes_2_remove: A string indicating the processes to remove from the workflow
        processes_annotation: A dictionnary containing processes 2 annotations
    """

    def __init__(self, file, duplicate=False, display_info=True, output_dir = './results',
                 name = None, datePublished=None, description=None,
                 license = None, creativeWorkStatus = None, authors = None, 
                 version = None, keywords = None, producer = None,
                 publisher = None, processes_2_remove = None,
                 processes_annotation = None):

        if(not os.path.isfile(file)):
            nextflow_files = glob.glob(f'{file}/*.nf')
            if(len(nextflow_files)==0):
                raise BioFlowInsightError("No Nextflow files ('.nf') are in the directory!", num = -1)
            try:
                file = '/'.join(nextflow_files[0].split('/')[:-1])+"/main.nf"
                with open(file, 'r') as f:
                        txt= f.read()
            except:
                file =nextflow_files[0]

        self.processes_annotation = processes_annotation

        self.nextflow_file = Nextflow_File(
            file,
            duplicate=duplicate,
            display_info=display_info,
            output_dir=output_dir,
            workflow = self
        )
        self.output_dir = Path(output_dir)
        self.rocrate = None
        self.name = name
        self.datePublished = datePublished
        self.description = description
        self.license = license
        self.creativeWorkStatus = creativeWorkStatus
        self.authors = authors
        self.version = version
        self.keywords = keywords
        self.producer = producer
        self.publisher = publisher
        if(processes_2_remove==""):
            processes_2_remove = None
        self.processes_2_remove = processes_2_remove
        self.log = ""
        self.fill_log()
        self.address = ""
        self.set_address()
        self.dico = {}
        self.get_dico()

    def get_repo_adress(self):
        """Method that returns the adress of the workflow repository 

        Keyword arguments:
        
        """
        current_directory = os.getcwd()
        repo = "/".join(self.nextflow_file.get_file_address().split("/")[:-1])
        if(repo==''):
            repo = current_directory
        return repo

    def get_processes_annotation(self):
        """Method the dictionnary of the process annotations

        Keyword arguments:
        
        """
        return self.processes_annotation

    def fill_log(self):
        """Method that reads the git log and saves it

        Keyword arguments:
        
        """
        current_directory = os.getcwd()
        os.chdir(self.get_repo_adress())
        try:
            os.system(f"git log --reverse > temp_{id(self)}.txt")
            with open(f'temp_{id(self)}.txt') as f:
                self.log = f.read()
            os.system(f"rm temp_{id(self)}.txt")
        except:
            None
        os.chdir(current_directory)

    def get_address(self):
        """Method that returns the adress of the workflow main

        Keyword arguments:
        
        """
        return self.address

    def set_address(self):
        """Method that sets the adress of the workflow main

        Keyword arguments:
        
        """
        current_directory = os.getcwd()
        os.chdir(self.get_repo_adress())
        try:
            os.system(f"git ls-remote --get-url origin > temp_address_{id(self)}.txt")
            with open(f'temp_address_{id(self)}.txt') as f:
                self.address = f.read()
            os.system(f"rm temp_address_{id(self)}.txt")
        except:
            None
        os.chdir(current_directory)
        for match in re.finditer(r"https:\/\/github\.com\/([^\.]+)\.git", self.address):
            self.address = match.group(1)

    def get_dico(self):
        """Method that returns a dictionnary containg information regarding the github repository

        Keyword arguments:
        
        """
        current_directory = os.getcwd()
        os.chdir(self.get_repo_adress())
        try:
            _ = os.system(f"wget -qO - https://api.github.com/repos/{self.address} > temp_dico_{id(self)}.json")
            with open(f'temp_dico_{id(self)}.json') as json_file:
                self.dico = json.load(json_file)
            os.system(f"rm temp_dico_{id(self)}.json")
            
        except:
            _ = os.system(f"rm temp_dico_{id(self)}.json")
        os.chdir(current_directory)
    


    def get_name(self):
        """Method that returns the name of the workflow

        Keyword arguments:
        
        """
        if(self.name==None):
            return self.nextflow_file.get_file_address().split("/")[-2]
        else:
            return self.name

    #Format yyyy-mm-dd
    #Here i return the first commit date
    def get_datePublished(self):
        """Method that returns the date of publication

        Keyword arguments:
        
        """
        if(self.datePublished==None):
            for match in re.finditer(r"Date: +\w+ +(\w+) +(\d+) +\d+:\d+:\d+ +(\d+)",self.log):
                month = constant.month_mapping[match.group(1)]
                day = match.group(2)
                year = match.group(3)
                return f"{year}-{month}-{day}"
        else:
            return self.datePublished
        

    def get_description(self):
        """Method that returns the description

        Keyword arguments:
        
        """
        if(self.description==None):
            try:
                res = self.dico["description"]
            except:
                res = None
            return res
        else:
            return self.description
        
    

    def get_main_file(self):
        """Method that returns the name of the main file

        Keyword arguments:
        
        """
        return self.nextflow_file.get_file_address().split("/")[-1]


    def get_license(self):
        """Method that returns the license

        Keyword arguments:
        
        """
        if(self.license==None):
            try:
                res = self.dico["license"]["key"]
            except:
                res = None
            return res
        else:
            return self.license
        
    
    #TODO
    def get_creativeWorkStatus(self):
        return "TODO"
    
    #TODO
    def get_version(self):
        return "TODO"


    def get_authors(self):
        """Method that returns a list of the authors

        Keyword arguments:
        
        """
        if(self.authors==None):
            authors = {}
            for match in re.finditer(r"Author: ([^>]+)<([^>]+)>",self.log):
                authors[match.group(2)] = match.group(1).strip()
            tab = []
            for author in authors:
                #tab.append({"@id":author, "name":authors[author]})
                tab.append({"@id":authors[author], "email":author})
            return tab
        else:
            authors = self.authors.split(',')
            tab = []
            for a in authors:
                tab.append({"@id":a.strip()})
            return tab
    

    #Need to follow this format : "rna-seq, nextflow, bioinformatics, reproducibility, workflow, reproducible-research, bioinformatics-pipeline"
    def get_keywords(self):
        """Method that returns the keywords

        Keyword arguments:
        
        """
        if(self.keywords==None):
            try:
                res = ", ".join(self.dico["topics"])
            except:
                res = None
            return res
        else:
            return self.keywords

    

    def get_producer(self):
        """Method that returns the producer

        Keyword arguments:
        
        """
        if(self.producer==None):
            try:
                res = {"@id": self.dico["owner"]["login"]}
            except:
                res = None
            return res
        else:
            return self.producer
    

    def get_publisher(self):
        """Method that returns the publisher

        Keyword arguments:
        
        """
        if(self.dico!={}):
            return "https://github.com/"
        else:
            return None
    
    def get_output_dir(self):
        """Method that returns the output directory

        Keyword arguments:
        
        """
        return self.nextflow_file.get_output_dir()

    def get_file_address(self):
        """Method that returns the adress of the workflow main

        Keyword arguments:
        
        """
        return self.nextflow_file.get_file_address()

    def add_2_rocrate(self, dico):
        """TODO
        """
        self.nextflow_file.add_2_rocrate(dico)

    def get_processes_defined(self):
        """Method that returns a list of the processes defined 

        Keyword arguments:
        
        """
        processes = self.nextflow_file.get_processes_defined(dict={}).keys()
        return list(processes)
    
    def get_processes_called(self):
        """Method that returns a list of the processes called/used during the workflow execution

        Keyword arguments:
        
        """
        return self.nextflow_file.get_processes_called()

    def get_tools(self):
        """Method that returns a list of the tools used by the workflow

        Keyword arguments:
        
        """
        processes = self.get_processes_called()
        tab = []
        for p in processes:
            tab+=p.get_tools()
        return list(set(tab))
    
    def get_commands(self):
        """Method that returns a list of the commands used by the workflow

        Keyword arguments:
        
        """
        processes = self.get_processes_called()
        tab = []
        for p in processes:
            tab+=p.get_commands()
        return list(set(tab))
    
    def get_modules(self):
        """Method that returns a list of the modules used by the workflow

        Keyword arguments:
        
        """
        processes = self.get_processes_called()
        tab = []
        for p in processes:
            tab+=p.get_modules()
        return list(set(tab))

    def initialise_rocrate(self):
        """Method that initialises the RO-Crate file

        Keyword arguments:
        
        """
        self.rocrate = RO_Crate(self)
        self.rocrate.initialise()

    def get_layers(self):
        """TODO
        """
        graph = self.nextflow_file.get_graph()
        if(not graph.is_initialised()):
            graph.initialise()
        process_dependency_graph = graph.get_process_dependency_graph_dico()
        dico_flattened = {"nodes": [], "edges": [], "subworkflows":[]}

        def get_node(dico, id):
            for n in dico['nodes']:
                if(n['id']==id):
                    return n
            return None

        def remove_node(dico, id):
            node = None
            for n in dico['nodes']:
                if(n['id']==id):
                    node = n.copy()
                    break
            try:
                dico['nodes'].remove(node)
            except:
                print("prob1")

        def remove_edge_if_A(dico, id_A):
            edges = []
            for edge in dico['edges']:
                if(edge['A']==id_A):
                    edges.append(edge)
            for edge in edges:
                try:
                    dico['edges'].remove(edge)
                except:
                    print("prob2")
            
        flatten_dico(process_dependency_graph, dico_flattened)
        links = initia_link_dico_rec(dico_flattened)
        _, edges_create_cycles = get_number_cycles(links)
        #If the graph isn't a dag -> we remoce the edges which make it cyclic
        for A, B in edges_create_cycles:
            #print({"A":A, "B":B})
            #print(dico_flattened["edges"])
            dico_flattened["edges"].remove({"A":A, "B":B, "label":''})

        layers = []
        while(dico_flattened["nodes"]!=[]):
          
            layer = dico_flattened["nodes"].copy()
            
            for edge in dico_flattened["edges"]:
                removed = False
                node = get_node(dico_flattened, edge['B'])
                while(not removed):
                    try:
                        layer.remove(node)
                    except:
                        removed = True
            
            
            for node in layer:
                dico_flattened['nodes'].remove(node)
                remove_edge_if_A(dico_flattened, node['id'])
            layers.append(layer)
            
        layers_object = []
        for layer in layers:
            tab = []
            for element in layer:
                address = int(re.findall(r"\dx\w+", element['id'])[0], base=16)
                tab.append(ctypes.cast(address, ctypes.py_object).value)
            layers_object.append(tab)
        return layers_object
                

    def initialise(self, create_rocrate = True):
        """Method that initialises the analysis of the worflow

        Keyword arguments:
        
        """
        self.nextflow_file.initialise()
        if(create_rocrate):
            self.initialise_rocrate()

    def generate_all_graphs(self, render_graphs = True):
        """Method that generates all graphs representing the workflow

        Keyword arguments:
        
        """
        tab_processes_2_remove = []
        if(self.processes_2_remove!=None):
            temp = self.processes_2_remove.split(",")
            for t in temp:
                tab_processes_2_remove.append(t.strip())
        self.nextflow_file.generate_all_graphs(render_graphs = render_graphs, processes_2_remove = tab_processes_2_remove)
