
import json
import networkx as nx
import numpy as np
import copy

from .outils_graph import *

class Graph():
    def __init__(self, nextflow_file):
        self.workflow = nextflow_file
        self.full_dico = nextflow_file.get_structure()
        with open(f"{self.get_output_dir()}/graphs/specification_graph.json", 'w') as output_file :
            json.dump(self.full_dico, output_file, indent=4)
        #This dico give for the nodes its sister nodes
        self.link_dico = None
        #Dico to graph without operations
        self.dico_process_dependency_graph = {}
        self.dico_wo_branch_operation = {}

        #Dictionaries for metadata
        #Dico flattened (without any subworkflows)
        self.dico_flattened = {}
        self.initialised = False


    

    def initialise(self, processes_2_remove = []):

        def get_node_id(dico, process):
            for node in dico["nodes"]:
                if(node['name']==process):
                    return node['id']
            for sub in dico['subworkflows']:
                res = get_node_id(dico['subworkflows'][sub], process)
                if(res!=-1):
                    return res
            return -1

        #This function removes the process -> by the simpliest way -> it doesn't create new links
        def remove_node(dico, node_id):
            #Remove nodes
            nodes_to_remove = []
            for node in dico["nodes"]:
                if(node['id']==node_id):
                    nodes_to_remove.append(node)
            for node in nodes_to_remove:
                dico["nodes"].remove(node)

            #Remove edges
            edges_to_remove = []
            for edge in dico["edges"]:
                if(edge['A']==node_id):
                    edges_to_remove.append(edge)
                if(edge['B']==node_id):
                    edges_to_remove.append(edge)
            for edge in edges_to_remove:
                dico["edges"].remove(edge)

            for sub in dico['subworkflows']:
                remove_node(dico['subworkflows'][sub], node_id)

        for process in processes_2_remove:
            node_id = get_node_id(self.full_dico, process)
            remove_node(self.full_dico, node_id)


        self.get_dependency_graph()
        self.get_process_dependency_graph()

        
        #self.networkX_wo_operations = self.get_networkx_graph(self.dico_process_dependency_graph, self.networkX_wo_operations)
        self.dico_flattened["nodes"] = []
        self.dico_flattened["edges"] = []
        #This will stay empty -> it's just so we can use the same function
        self.dico_flattened["subworkflows"] = []
        self.initialised = True
    
    def is_initialised(self):
        return self.initialised

    def get_output_dir(self):
        return self.workflow.get_output_dir()  

    #Creates the networkX graph
    def get_networkx_graph(self, graph, networkX, first_call=True):
        if(first_call):
            networkX = nx.MultiDiGraph()
        for node in graph['nodes']:
            #Case node is process
            if(is_process(node['id'])):
                networkX.add_node(node['id'], type='Process', code=node['name'])
            #Case node is operation
            elif(is_operation(node['id'])):
                networkX.add_node(node['id'], type='Operation', code=node['xlabel'])
            elif(node['id']=="source"):
                networkX.add_node("source", type='source', code="source")
            elif(node['id']=="sink"):
                networkX.add_node("sink", type='sink', code="sink")
            else:
                raise Exception("This shoudn't happen!")
        
        for edge in graph['edges']:
            if(is_process(edge['A']) and is_process(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='process_2_process')
            elif(is_process(edge['A']) and is_operation(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='process_2_operation')
            elif(is_operation(edge['A']) and is_process(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='operation_2_process')
            elif(is_operation(edge['A']) and is_operation(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='operation_2_operation')
            else:
                networkX.add_edge(edge['A'], edge['B'], label = "", edge_type='')      
        for subworkflow in graph['subworkflows']:
            networkX = self.get_networkx_graph(graph['subworkflows'][subworkflow], networkX, first_call=False)
        return networkX



    #Method that initalisise the link dico
    def intia_link_dico(self):
        if(self.link_dico==None):
            self.link_dico = initia_link_dico_rec(self.full_dico)

    def get_specification_graph(self, filename = "specification_graph", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.full_dico, render_graphs = render_graphs)

    def get_specification_graph_wo_labels(self, filename = "specification_graph_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.full_dico, label_edge=False, label_node=False, render_graphs = render_graphs)
    
    def get_specification_graph_wo_orphan_operations(self, filename = "specification_wo_orphan_operations", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.full_dico), render_graphs = render_graphs)
    
    def get_specification_graph_wo_orphan_operations_wo_labels(self, filename = "specification_wo_orphan_operations_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.full_dico), label_edge=False, label_node=False, render_graphs = render_graphs)

    def get_process_dependency_graph_dico(self):
        return self.dico_process_dependency_graph

    def get_process_dependency_graph(self):
        self.intia_link_dico()

        #Function that replicates the workflow's structure wo the operations in the nodes
        def replicate_dico_process_dependency_graphs(dico_struct):
            dico = {}
            dico['nodes'] = []
            dico['edges'] = []
            dico['subworkflows'] = {}
            for node in dico_struct["nodes"]:
                if(is_process(node['id'])):
                    dico['nodes'].append(node)
            for sub in dico_struct['subworkflows']:
                dico['subworkflows'][sub] = replicate_dico_process_dependency_graphs(dico_struct['subworkflows'][sub])
            return dico

        dico = replicate_dico_process_dependency_graphs(self.full_dico)

        #This is a dictionnary which links every node to it's connected process
        node_2_processes = copy.deepcopy(self.link_dico)
        already_searched = {}
        for node in node_2_processes:
            already_searched[node] = [node]
        changed = True
        while(changed):
            changed = False
            for node in node_2_processes:
                temp = node_2_processes[node].copy()
                for give in node_2_processes[node]:
                    if(is_operation(give)):
                        temp.remove(give)
                        if(node!=give and give not in already_searched[node]):
                            already_searched[node] += give
                            temp_temp = node_2_processes[give]
                            for node_temp in already_searched[node]:
                                try:
                                    temp_temp.remove(node_temp)
                                except:
                                    None
                            temp+=temp_temp
                            changed = True
                node_2_processes[node] = list(set(temp))

 
        links_added = []
        def add_edges(dico):
            for node in dico['nodes']:
                edges = node_2_processes[node['id']]
                for B in edges:
                    link = f"{node['id']} -> {B}"
                    if(link not in links_added):
                        dico['edges'].append({'A': node['id'], 'B': B, 'label': ''})
                        links_added.append(link)   
            for sub in dico['subworkflows']:
                add_edges(dico["subworkflows"][sub]) 
            
        
        add_edges(dico)


        self.dico_process_dependency_graph = dico

        with open(f"{self.get_output_dir()}/graphs/process_dependency_graph.json", 'w') as output_file :
            json.dump(self.dico_process_dependency_graph, output_file, indent=4)

    
    def render_graph_wo_operations(self, filename = "process_dependency_graph", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.dico_process_dependency_graph, render_graphs = render_graphs, label_edge=False, label_node=False)
    

    def get_dependency_graph(self):
        self.intia_link_dico()
        nodes_in_graph = []
        branch_operation_ids = []
        #Function that replicates the workflow's structure wo the operations in the nodes
        def replicate_dico(dico_struct):
            dico = {}
            dico['nodes'] = []
            dico['edges'] = []
            dico['subworkflows'] = {}
            for node in dico_struct["nodes"]:
                if(get_type_node(node)!="Branch Operation"):
                    dico['nodes'].append(node)
                    nodes_in_graph.append(node['id'])
            for sub in dico_struct['subworkflows']:
                dico['subworkflows'][sub] = replicate_dico(dico_struct['subworkflows'][sub])
            return dico
        
        dico = replicate_dico(self.full_dico)

        #This is a dictionnary which links every node to it's connected process
        node_2_none_branch = copy.deepcopy(self.link_dico)
        already_searched = {}
        for node in node_2_none_branch:
            already_searched[node] = [node]
        changed = True
        while(changed):
            changed = False
            for node in node_2_none_branch:
                temp = node_2_none_branch[node].copy()
                for give in node_2_none_branch[node]:
                    if(is_operation(give) and give not in nodes_in_graph):
                        temp.remove(give)
                        if(node!=give and give not in already_searched[node]):
                            already_searched[node] += give
                            temp_temp = node_2_none_branch[give]
                            for node_temp in already_searched[node]:
                                try:
                                    temp_temp.remove(node_temp)
                                except:
                                    None
                            temp+=temp_temp
                            changed = True
                node_2_none_branch[node] = list(set(temp))

 
        links_added = []
        def add_edges(dico):
            for node in dico['nodes']:
                edges = node_2_none_branch[node['id']]
                for B in edges:
                    link = f"{node['id']} -> {B}"
                    if(link not in links_added):
                        dico['edges'].append({'A': node['id'], 'B': B, 'label': ''})
                        links_added.append(link)   
            for sub in dico['subworkflows']:
                add_edges(dico["subworkflows"][sub]) 
            
        add_edges(dico)
        self.dico_wo_branch_operation = dico

        with open(f"{self.get_output_dir()}/graphs/dependency_graph.json", 'w') as output_file :
            json.dump(self.dico_wo_branch_operation, output_file, indent=4)
    

    def render_dependency_graph(self, filename = "dependency_graph", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.dico_wo_branch_operation, render_graphs = render_graphs)
    
    def get_dependency_graph_wo_labels(self, filename = "dependency_graph_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.dico_wo_branch_operation, label_edge=False, label_node=False, render_graphs = render_graphs)

    def get_dependency_graph_wo_orphan_operations(self, filename = "dependency_graph_wo_orphan_operations", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.dico_wo_branch_operation), render_graphs = render_graphs)
    
    def get_dependency_graph_wo_orphan_operations_wo_labels(self, filename = "dependency_graph_wo_orphan_operations_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.dico_wo_branch_operation), label_edge=False, label_node=False, render_graphs = render_graphs)


    #============================
    #METADATA FROM GRAPH
    #============================

    def initialise_flattened_dico(self, dico):

        flatten_dico(dico, self.dico_flattened)
        #for node in dico["nodes"]:
        #    self.dico_flattened["nodes"].append(node)
        #for edge in dico["edges"]:
        #    self.dico_flattened["edges"].append(edge)
        #for subworkflow in dico["subworkflows"]:
        #    self.initialise_flattened_dico(dico["subworkflows"][subworkflow])

    def get_metadata(self, graph):
        G = self.get_networkx_graph(graph, None)
        dico = {}
        for node in G.nodes(data=True):
            if(node[1]=={}):
                print(node)
        process_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'Process']
        operation_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'Operation']

        dico['number_of_processes'] =  len(process_nodes)
        dico['number_of_operations'] =  len(operation_nodes)
        dico['number_of_nodes'] = dico['number_of_processes']+dico['number_of_operations']

        dico['number_of_edges_process_2_process'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="process_2_process")
        dico['number_of_edges_process_2_operation'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="process_2_operation")
        dico['number_of_edges_operation_2_process'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="operation_2_process")
        dico['number_of_edges_operation_2_operation'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="operation_2_operation")
        
        dico['number_of_edges_source_process'] = dico['number_of_edges_process_2_process'] + dico['number_of_edges_process_2_operation']
        dico['number_of_edges_source_operation'] = dico['number_of_edges_operation_2_process'] + dico['number_of_edges_operation_2_operation']
        dico['number_of_edges_sink_process'] = dico['number_of_edges_process_2_process'] + dico['number_of_edges_operation_2_process']
        dico['number_of_edges_sink_operation'] = dico['number_of_edges_process_2_operation'] + dico['number_of_edges_operation_2_operation']
        dico['number_of_edges'] = dico['number_of_edges_process_2_process'] + dico['number_of_edges_process_2_operation'] + dico['number_of_edges_operation_2_process'] + dico['number_of_edges_operation_2_operation']
        
        dico["number_of_simple_loops"] = nx.number_of_selfloops(G)

        distribution_in_degrees_for_processes = list(dict(G.in_degree(process_nodes)).values())
        distribution_out_degrees_for_processes = list(dict(G.out_degree(process_nodes)).values())
        distribution_in_degrees_for_operations= list(dict(G.in_degree(operation_nodes)).values())
        distribution_out_degrees_for_operations= list(dict(G.out_degree(operation_nodes)).values())

        dico["distribution_in_degrees_for_processes"] = distribution_in_degrees_for_processes
        dico["distribution_out_degrees_for_processes"] = distribution_out_degrees_for_processes
        dico["distribution_in_degrees_for_operations"] = distribution_in_degrees_for_operations
        dico["distribution_out_degrees_for_operations"] = distribution_out_degrees_for_operations

        dico["distribution_in_degrees_for_all"] = dico["distribution_in_degrees_for_processes"]+dico["distribution_in_degrees_for_operations"]
        dico["distribution_out_degrees_for_all"] = dico["distribution_out_degrees_for_processes"]+dico["distribution_out_degrees_for_operations"]

        dico["average_in_degrees_for_processes"]   = np.array(distribution_in_degrees_for_processes).mean()
        dico["average_out_degrees_for_processes"]  = np.array(distribution_out_degrees_for_processes).mean()
        dico["average_in_degrees_for_operations"]  = np.array(distribution_in_degrees_for_operations).mean()
        dico["average_out_degrees_for_operations"] = np.array(distribution_out_degrees_for_operations).mean()
        dico["average_in_degrees_for_all"] = np.array(dico["distribution_in_degrees_for_all"] ).mean()
        dico["average_out_degrees_for_all"] = np.array(dico["distribution_out_degrees_for_all"] ).mean()


        dico["median_in_degrees_for_processes"]   = np.median(np.array(distribution_in_degrees_for_processes))
        dico["median_out_degrees_for_processes"]  = np.median(np.array(distribution_out_degrees_for_processes))
        dico["median_in_degrees_for_operations"]  = np.median(np.array(distribution_in_degrees_for_operations))
        dico["median_out_degrees_for_operations"] = np.median(np.array(distribution_out_degrees_for_operations))
        dico["median_in_degrees_for_all"] =  np.median(np.array(dico["distribution_in_degrees_for_all"]))
        dico["median_out_degrees_for_all"] = np.median(np.array(dico["distribution_out_degrees_for_all"]))

        #DEsnity = m/n(n-1), where n is the number of nodes and m is the number of edges
        dico['density'] = nx.density(G)
        weakly_connected_components = list(nx.weakly_connected_components(G))
        dico['number_of_weakly_connected_components'] = len(weakly_connected_components)
        
        components_with_over_2_nodes = [comp for comp in weakly_connected_components if len(comp) >= 2]
        dico['number_of_weakly_connected_components_with_2_or_more_nodes'] = len(components_with_over_2_nodes)

        #Getting the number of cycles
        self.initialise_flattened_dico(graph)
        links_flattened = initia_link_dico_rec(self.dico_flattened)
        not_source_2_sink = []
        node_2_sink = []

        for node in links_flattened:
            if(links_flattened[node]==[]):
                node_2_sink.append(node)
            else:
                not_source_2_sink+=links_flattened[node]
        not_source_2_sink = set(not_source_2_sink)
        source_2_node = list(set(links_flattened.keys()).difference(not_source_2_sink))
        links_flattened_source_sink = links_flattened.copy()
        links_flattened_source_sink["source"], links_flattened_source_sink["sink"] = source_2_node, []
        for node in node_2_sink:
            links_flattened_source_sink[node].append("sink")
 
        #The simple loops are included in this
        dico['number_of_cycles'], edges_create_cycles = get_number_cycles(links_flattened_source_sink)
        
        #Remove the edges which create the cycles
        #Since the number of paths from Source 2 sink and the longest path depend on the 
        #Topological ordering 
        #A topological ordering is possible if and only if the graph has no directed cycles, that is, if it is a directed acyclic graph (DAG)
        #We turn the CDG (cyclic directed graphs) into a DAG (directed acyclic graph)
        for A, B in edges_create_cycles:
            links_flattened_source_sink[A].remove(B)

        structure_type = ""
        if(len(edges_create_cycles)==0):
            structure_type = "DAG"
        else:
            structure_type = "CDG"
        
        dico['structure_type'] = structure_type

        dico['number_of_paths_source_2_sink'] = get_number_paths_source_2_sink(links_flattened_source_sink)
        dico['shortest_path'] = dijkstra(links_flattened_source_sink)
        dico['longest_path'] = get_longest_distance(links_flattened_source_sink)

        
        """#Check that the values calculated are the same than what gives networkX
        dico_check = {}
        dico_check['nodes'] = []
        dico_check['edges'] = []
        dico_check['subworkflows'] = {}
        for node in links_flattened_source_sink:
            dico_check["nodes"].append({'id':node, 'xlabel':"", 'name':""})
            for B in links_flattened_source_sink[node]:
                dico_check["edges"].append({'A':node, "B":B, "label":""})

        G_DAG = self.get_networkx_graph(dico_check, None)
        #=====================================
        #ADDING SINK AND SOURCE TO THE GRAPH
        #=====================================
        source_node = "source"
        sink_node = "sink"
        
        if(dico['shortest_path']!=nx.shortest_path_length(G_DAG, source=source_node, target=sink_node)):
            raise Exception(f"{dico['shortest_path']}, {nx.shortest_path_length(G_DAG, source=source_node, target=sink_node)}")
        #print("test1")
        if(dico['longest_path']+1!=len(nx.dag_longest_path(G_DAG))):
            raise Exception(f"{dico['longest_path']}, {len(nx.dag_longest_path(G_DAG))}")
        #print("test2")
        
        #if(len(list(nx.all_simple_paths(G_DAG, source=source_node, target=sink_node)))!=dico['number_of_paths_source_2_sink']):
        #    raise Exception(f"{len(list(nx.all_simple_paths(G_DAG, source=source_node, target=sink_node)))}, {dico['number_of_paths_source_2_sink']}")
        #print("test3")"""
        
        return dico


    def get_metadata_specification_graph(self):
        
        dico = self.get_metadata(self.full_dico)
        with open(self.get_output_dir()/ "graphs/metadata_specification_graph.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    def get_metadata_dependency_graph(self):

        dico = self.get_metadata(self.dico_wo_branch_operation)
        with open(self.get_output_dir()/ "graphs/metadata_dependency_graph.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    def get_metadata_process_dependency_graph(self):
        
        dico = self.get_metadata(self.dico_process_dependency_graph)
        with open(self.get_output_dir()/ "graphs/metadata_process_dependency_graph.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    #def get_metadata_graph_wo_operations(self):
    #    G = self.networkX_wo_operations
    #    dico = self.get_metadata(G)
    #    with open(self.get_output_dir() / "graphs/metadata_graph_wo_operations.json", 'w') as output_file :
    #        json.dump(dico, output_file, indent=4)
