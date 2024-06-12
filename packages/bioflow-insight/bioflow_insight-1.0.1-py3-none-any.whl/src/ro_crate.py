import json
import glob
import os
import re

from . import constant

class RO_Crate:
    def __init__(self, workflow):
        self.workflow = workflow
        self.directory = '/'.join(workflow.get_file_address().split('/')[:-1])
        self.files = []
        self.dico = {}
        self.dico["temp_directory"] = self.directory

    def get_files(self):
        self.files = glob.glob(f'{self.directory}/**/*.*', recursive=True)
        tab_files = []
        for file in self.files:
            tab_files.append({"@id":file[len(self.directory)+1:]})
        return tab_files

    def initialise_dico(self):
        self.dico["@context"] = "https://w3id.org/ro/crate/1.1/context"
        self.dico["@graph"] = []
        #GENERAL
        general = {}
        general["@id"] = f"ro-crate-metadata-{self.workflow.get_name()}.json"
        general["@type"] = "CreativeWork"
        general["about"] = {"@id":"./"}
        general["conformsTo"] = [{"@id":"https://w3id.org/ro/crate/1.1"}
                                 #, {"@id":"https://w3id.org/workflowhub/workflow-ro-crate/1.0"}#This description does not conform 
                                 ]
        self.dico["@graph"].append(general)
        #ROOT
        root = {}
        root["@id"] = "./"
        root["@type"] = "Dataset"
        root["name"] = self.workflow.get_name()
        root["datePublished"] = self.workflow.get_datePublished()
        root["description"] = self.workflow.get_description()
        root["mainEntity"] = {"@id": self.workflow.get_main_file()}
                              #, "@type":["File", "SoftwareSourceCode"]} #We do not consider a File as a "ComputationalWorkflow" since multiple (sub)workflows can be defined in a same file
        root["license"] = {"@id":self.workflow.get_license()}
        authors = self.workflow.get_authors()
        tab_authors = []
        for author in authors:
            try:
                tab_authors.append({"@id":author["@id"], "email":author["email"]})
            except:
                tab_authors.append({"@id":author["@id"]})
        root["author"] = tab_authors
        root["maintainer"] = tab_authors #Right now i'm assuming that all the authors are maintainers
        files = self.get_files()
        tab_files = []
        for file in files:
            tab_files.append({"@id":file["@id"]})
        root["hasPart"] = tab_files
        root["publisher"] = {"@id":self.workflow.get_publisher()}
        #subjectOf TODO
        root["subjectOf"] = None
        root["creativeWorkStatus"] = self.workflow.get_creativeWorkStatus()
        root["@version"] = self.workflow.get_version()
        root["keywords"] = self.workflow.get_keywords()
        root["producer"] = self.workflow.get_producer()
        self.dico["@graph"].append(root)

    #TODO 
    def get_programming_language(self, file):
        if(file[-3:]==".nf"):
            return "https://w3id.org/workflowhub/workflow-ro-crate#nextflow"
        return None
    
    def get_contentSize(self, file):
        file_stats = os.stat(file)
        return file_stats.st_size/1e3
    
    def fill_log_file(self, file, reverse = True):
        info = ""
        current_directory = os.getcwd()
        os.chdir("/".join(self.workflow.nextflow_file.get_file_address().split("/")[:-1]))
        try:           
            os.system(f"git log {'--reverse'*reverse} \"{file}\" > temp_{id(self)}.txt")
            with open(f'temp_{id(self)}.txt') as f:
                info = f.read()
            os.system(f"rm temp_{id(self)}.txt")
        except:
            None
        os.chdir(current_directory)
        return info

    def get_dateCreated(self, file):
        info = self.fill_log_file(file, reverse = True)
        for match in re.finditer(r"Date: +\w+ +(\w+) +(\d+) +\d+:\d+:\d+ +(\d+)", info):
            month = constant.month_mapping[match.group(1)]
            day = match.group(2)
            year = match.group(3)
            return f"{year}-{month}-{day}"
        return None
    
 
    def get_dateModified(self, file):
        info = self.fill_log_file(file, reverse = False)
        for match in re.finditer(r"Date: +\w+ +(\w+) +(\d+) +\d+:\d+:\d+ +(\d+)", info):
            month = constant.month_mapping[match.group(1)]
            day = match.group(2)
            year = match.group(3)
            return f"{year}-{month}-{day}"
        return None
    
    #TODO -> update this -> it's incomplet
    def get_url(self, file):
        if(self.workflow.dico!={}):
            return f"https://github.com/{self.workflow.get_address()}/blob/main/{file}"
        return None
    

    def get_creators(self, file):
        info = self.fill_log_file(file, reverse = True)
        for match in re.finditer(r"Author: ([^>]+)<([^>]+)>",info):
            return [{"@id": match.group(1).strip()}]
        return []


    def get_types(self, file):
        types = ["File"]
        if(file[-3:]==".nf"):
            types.append("SoftwareSourceCode")
        return types
        

    def initialise_file(self, file):
        key = file[len(self.directory)+1:]
        dico = {}
        dico["@id"] = key
        dico["name"] = key
        dico["@type"] = self.get_types(file)
        dico["programmingLanguage"] = {"@id":self.get_programming_language(file)}
        dico["contentSize"] = self.get_contentSize(file)
        dico["dateCreated"] = self.get_dateCreated(key)
        dico["dateModified"] = self.get_dateModified(key)
        dico["url"] = self.get_url(key)
        creators = self.get_creators(key)
        dico["creator"] = []
        for creator in creators:
            dico["creator"].append({"@id": creator["@id"]})
        dico["isPartOf"] = []
        dico["hasPart"] = []
        self.dico["@graph"].append(dico)    

    def fill_from_workflow(self):
        self.workflow.add_2_rocrate(self.dico)

    def initialise(self):
        self.initialise_dico()
        for file in self.files:
            self.initialise_file(file)
        self.fill_from_workflow()
        self.dico.pop("temp_directory")

        name = self.workflow.get_name()
        name = name.replace('github.com/', '')
        name = re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "-", name)

        with open(f"{self.workflow.get_output_dir()}/ro-crate-metadata-{name}.json", 'w') as output_file :
            json.dump(self.dico, output_file, indent=2)