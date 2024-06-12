import unittest
from src.channel import *
from src.nextflow_file import Nextflow_File


class EmptyNextflowFile(Nextflow_File):
    def __init__(self, address="tests/ressources/channel/empty_wf.nf", display_info=False, *args, **kwargs):
        super().__init__(address=address, display_info=display_info, *args, **kwargs)

    def check_file_correctness_after_DSL(self):
        return


class TestChannel(unittest.TestCase):

    def test_get_code(self):
        wf1 = EmptyNextflowFile()
        ch1 = Channel(name = "ch1", origin = wf1)
        self.assertIsInstance(ch1, Channel)
        self.assertEqual(ch1.get_code(), "ch1")

    def test_get_name(self):
        wf1 = EmptyNextflowFile()
        ch1 = Channel(name = "ch1", origin = wf1)
        self.assertEqual(ch1.get_name(), "ch1")

    def test_get_type(self):
        wf1 = EmptyNextflowFile()
        ch1 = Channel(name = "ch1", origin = wf1)
        self.assertEqual(ch1.get_type(), "Channel")

    def test_add_source(self):
        wf1 = EmptyNextflowFile()
        ch1 = Channel(name = "ch1", origin = wf1)
        self.assertEqual(ch1.get_source(), [])
        ele = "This is a test"
        ch1.add_source(ele)
        self.assertEqual(ch1.get_source(), [ele])

    def test_add_sink(self):
        wf1 = EmptyNextflowFile()
        ch1 = Channel(name = "ch1", origin = wf1)
        self.assertEqual(ch1.get_sink(), [])
        ele = "This is a test"
        ch1.add_sink(ele)
        self.assertEqual(ch1.get_sink(), [ele])

    def test_set_sink_null(self):
        wf1 = EmptyNextflowFile()
        ch1 = Channel(name = "ch1", origin = wf1)
        ele = "This is a test"
        ch1.add_sink(ele)
        self.assertEqual(ch1.get_sink(), [ele])
        ch1.set_sink_null()
        self.assertEqual(ch1.get_sink(), [])

    def test_remove_element_from_sink(self):
        wf1 = EmptyNextflowFile()
        ch1 = Channel(name = "ch1", origin = wf1)
        ele = "This is a test"
        ch1.add_sink(ele)
        self.assertEqual(ch1.get_sink(), [ele])
        ch1.remove_element_from_sink(ele = ele)
        self.assertEqual(ch1.get_sink(), [])

    def test_equal(self):
        wf1 = EmptyNextflowFile()
        ch1 = Channel(name = "ch1", origin = wf1)
        ch1_1 = Channel(name = "ch1", origin = wf1)
        ch2 = Channel(name = "ch2", origin = wf1)
        self.assertTrue(ch1.equal(channel=ch1_1))
        self.assertFalse(ch1.equal(channel=ch2))

    def test_get_structure(self):
        wf1 = EmptyNextflowFile()
        ch1 = Channel(name = "ch1", origin = wf1)
        dico = {}
        dico['nodes'] = []
        dico['edges'] = []
        dico['subworkflows'] = {}
        ch1.add_source("out1")
        ch1.add_source("out2")
        ch1.get_structure(dico, "in")
        dico_true = {'nodes': [], 'edges': [{'A': 'out1', 'B': 'in', 'label': 'ch1'}, {'A': 'out2', 'B': 'in', 'label': 'ch1'}], 'subworkflows': {}}
        self.assertEqual(dico, dico_true)
    
