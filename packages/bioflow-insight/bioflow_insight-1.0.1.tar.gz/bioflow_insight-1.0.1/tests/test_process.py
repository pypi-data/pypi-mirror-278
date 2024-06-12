import unittest
from src.process import *
from src.nextflow_file import Nextflow_File

class TestProcess(unittest.TestCase):

    def test_check_everything_works(self):
        self.assertTrue(True)


    def test_initialise_name(self):
        #DSL1
        file = Nextflow_File("tests/ressources/process/process_DSL1.nf", display_info=False, DSL = "DSL1")
        file.initialise()
        process_DSL1 = file.processes[0]
        self.assertEqual(process_DSL1.get_name(),  "cleanSpeciesTree")
        self.assertEqual(process_DSL1.get_alias(), "cleanSpeciesTree")
        #DSL2
        file = Nextflow_File("tests/ressources/process/process_DSL2.nf", display_info=False, DSL = "DSL2")
        file.initialise()
        process_DSL2 = file.processes[0]
        self.assertEqual(process_DSL2.get_name(),  "OPENMS_FALSEDISCOVERYRATE")
        self.assertEqual(process_DSL2.get_alias(), "OPENMS_FALSEDISCOVERYRATE")

    def test_set_alias(self):
        file = Nextflow_File("tests/ressources/process/process_DSL2.nf", display_info=False, DSL = "DSL2")
        file.initialise()
        process_DSL2 = file.processes[0]
        self.assertEqual(process_DSL2.get_alias(), "OPENMS_FALSEDISCOVERYRATE")
        new_alias = "new_alias"
        process_DSL2.set_alias(new_alias)
        self.assertEqual(process_DSL2.get_name(),  "OPENMS_FALSEDISCOVERYRATE")
        self.assertEqual(process_DSL2.get_alias(), new_alias)
    
    
    def test_which_DSL(self):
        #DSL1
        file = Nextflow_File("tests/ressources/process/process_DSL1.nf", display_info=False, DSL = "DSL1")
        file.initialise()
        process_DSL1 = file.processes[0]
        self.assertEqual(process_DSL1.which_DSL(),  "DSL1")
        #DSL2
        file = Nextflow_File("tests/ressources/process/process_DSL2.nf", display_info=False, DSL = "DSL1")
        file.initialise()
        process_DSL2 = file.processes[0]
        self.assertEqual(process_DSL2.which_DSL(),  "DSL2")
        
    def test_is_initialised(self):
        #DSL1
        file = Nextflow_File("tests/ressources/process/process_DSL1.nf", display_info=False, DSL = "DSL1")
        file.initialise()
        process_DSL1 = file.processes[0]
        self.assertTrue(process_DSL1.is_initialised())
        #DSL2
        file = Nextflow_File("tests/ressources/process/process_DSL2.nf", display_info=False, DSL = "DSL2")
        file.initialise()
        process_DSL2 = file.processes[0]
        self.assertTrue(process_DSL2.is_initialised())
    
    
    def test_get_type(self):
        #DSL1
        file = Nextflow_File("tests/ressources/process/process_DSL1.nf", display_info=False, DSL = "DSL1")
        file.initialise()
        process_DSL1 = file.processes[0]
        self.assertEqual(process_DSL1.get_type(),  "Process")
        #DSL2
        file = Nextflow_File("tests/ressources/process/process_DSL2.nf", display_info=False, DSL = "DSL2")
        file.initialise()
        process_DSL2 = file.processes[0]
        self.assertEqual(process_DSL2.get_type(),  "Process")

    #TODO define the tests for the inputs and outputs
        
    def test_get_structure(self):
        #DSL1
        file = Nextflow_File("tests/ressources/process/process_DSL1.nf", display_info=False, DSL = "DSL1")
        file.initialise()
        process_DSL1 = file.processes[0]
        dico = {}
        dico['nodes'] = []
        dico['edges'] = []
        dico['subworkflows'] = {}
        process_DSL1.get_structure(dico)
        dico_true = {'nodes': [{'id': str(process_DSL1), 'name': 'cleanSpeciesTree', 'shape': 'ellipse', 'xlabel': '', 'fillcolor': ''}], 'edges': [], 'subworkflows': {}}
        self.assertEqual(dico,  dico_true)
        
        #DSL2
        file = Nextflow_File("tests/ressources/process/process_DSL2.nf", display_info=False, DSL = "DSL2")
        file.initialise()
        process_DSL2 = file.processes[0]
        dico = {}
        dico['nodes'] = []
        dico['edges'] = []
        dico['subworkflows'] = {}
        process_DSL2.get_structure(dico)
        dico_true = {'nodes': [{'id': str(process_DSL2), 'name': 'OPENMS_FALSEDISCOVERYRATE', 'shape': 'ellipse', 'xlabel': '', 'fillcolor': ''}], 'edges': [], 'subworkflows': {}}
        self.assertEqual(dico,  dico_true)

    def test_(self):
        file = Nextflow_File("tests/ressources/process/process_DSL1.nf", display_info=False, DSL = "DSL1")
        file.initialise()
        process_DSL1 = file.processes[0]

    
