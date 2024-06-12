import graphviz
import copy
import numpy as np

process_id = "<src.process.Process"
operation_id = "<src.operation.Operation"

def is_process(node_id):
    if(node_id[:len(process_id)]==process_id):
        return True
    return False

def is_operation(node_id):
    if(node_id[:len(operation_id)]==operation_id):
        return True
    return False

def fill_dot(dot, dico, label_node = True, label_edge = True):
    for n in dico["nodes"]:
        if(label_node):
            dot.node(n["id"], n["name"], shape=n["shape"], xlabel= n["xlabel"], fillcolor=n["fillcolor"])
        else:
            dot.node(n["id"], n["name"], shape=n["shape"], fillcolor=n["fillcolor"])
    for e in dico["edges"]:
        if(label_edge):
            dot.edge(e['A'], e['B'], label= e['label'])
        else:
            dot.edge(e['A'], e['B'])
    for sub in dico["subworkflows"]:
        with dot.subgraph(name="cluster"+sub) as c:
            fill_dot(c, dico["subworkflows"][sub], label_node, label_edge)
            c.attr(label=sub)

def generate_graph_dot(filename, dico, label_node = True, label_edge = True, render_graphs = True):
    dot = graphviz.Digraph(filename=filename, format='png', comment="temp")
    fill_dot(dot, dico, label_node, label_edge)
    dot.save(filename=f'{filename}.dot')
    if(render_graphs):
        dot.render(filename=f'{filename}.dot', outfile=f'{filename}.png')

def generate_graph_mermaid(filename, dico, label_node = True, label_edge = True, render_graphs = True):
    txt= "graph TB;\n"
 
    def get_id(txt):
        import re
        for match in re.finditer(r"object at (\w+)>", txt):
            return match.group(1)

    def quoted(label):
        if not label.strip():
            return label
        return f'"{label}"'

    def get_graph_wo_operations_mermaid_temp(dico, txt, count):
        count+=1
        for node in dico["nodes"]:
            tab= count*"\t"
            if(node['name']==''):
                if(label_node):
                    txt+=f"{tab}{get_id(node['id'])}(({quoted(node['xlabel'])}));\n"
                else:
                    txt+=f"{tab}{get_id(node['id'])}(({' '}));\n"
            else:
                txt+=f"{tab}{get_id(node['id'])}({quoted(node['name'])});\n"
        
        for edge in dico["edges"]:
            tab= count*"\t"
            if(label_edge):
                txt+=f"{tab}{get_id(edge['A'])}--{quoted(edge['label'])}-->{get_id(edge['B'])};\n"
            else:
                txt+=f"{tab}{get_id(edge['A'])}-->{get_id(edge['B'])};\n"
        for subworkflow in dico["subworkflows"]:
            tab= count*"\t"
            txt += f"{tab}subgraph {subworkflow}\n{tab}\tdirection TB;\n"
            count+=1
            txt = get_graph_wo_operations_mermaid_temp(dico["subworkflows"][subworkflow], txt, count)
            count-=1
            txt += f"{tab}end\n"
        return txt
    txt = get_graph_wo_operations_mermaid_temp(dico, txt, 0)

    with open(f"{filename}.mmd", "w") as text_file:
        text_file.write(txt)



def generate_graph(filename, dico, label_node = True, label_edge = True, render_graphs = True, dot = True, mermaid = True):
    if(dot):
        generate_graph_dot(filename, dico, label_node, label_edge, render_graphs)
    if(mermaid):
        generate_graph_mermaid(filename, dico, label_node, label_edge, render_graphs)


#Function that merges to dictionnaries
def merge(x, y):
    return { key:list(set(x.get(key,[])+y.get(key,[]))) for key in set(list(x.keys())+list(y.keys())) }

#This function returns a listof the orphan operations in the graph
def get_id_orphan_operation(graph):
    id_operations = []

    def get_id_operations(graph):
        for node in graph['nodes']:
            if(is_operation(node['id'])):
                id_operations.append(node['id'])
        for subworkflow in graph["subworkflows"]:
            get_id_operations(graph["subworkflows"][subworkflow])
    
    def get_dico_operation_is_linked(graph, dico_operation_is_linked = {}):
        #First call
        if(dico_operation_is_linked == {}):
            for id in id_operations:
                dico_operation_is_linked[id] = False
        for edge in graph["edges"]:
            dico_operation_is_linked[edge["A"]] = True
            dico_operation_is_linked[edge["B"]] = True
        for subworkflow in graph["subworkflows"]:
            get_dico_operation_is_linked(graph["subworkflows"][subworkflow], dico_operation_is_linked)
        return dico_operation_is_linked
    

    get_id_operations(graph)
    dico = get_dico_operation_is_linked(graph)
    tab = []
    for operation_id in dico:
        if(not dico[operation_id]):
            tab.append(operation_id)
    return tab

def graph_dico_wo_orphan_operations(graph_tmp):
    graph = copy.deepcopy(graph_tmp)
    orphans = get_id_orphan_operation(graph)

    def remove_orphans(graph, orphans):
        to_remove = []
        for node in graph["nodes"]:
            if(node["id"] in orphans):
                to_remove.append(node)
        for r in to_remove:
            try:
                graph["nodes"].remove(r)
            except:
                None
        for subworkflow in graph["subworkflows"]:
            remove_orphans(graph["subworkflows"][subworkflow], orphans)
    remove_orphans(graph, orphans)
    return graph

#Function that returns the type of a given node
def get_type_node(node):
    if(is_process(node['id'])):
        return "Process"
    else:
        if(node["fillcolor"]=="white"):
            return "Branch Operation"
        else:
            return "Create Operation"

#Function that creates the link dico from a given graph dico      
def initia_link_dico_rec(dico):
    links = {}
    for node in dico['nodes']:
        try:
            temp = links[node['id']]
        except:
            links[node['id']] = []
    for edge in dico['edges']:
        A = edge['A']
        B = edge['B']
        try:
            temp = links[A]
        except:
            links[A] = []
        links[A].append(B)
    
    for sub in dico['subworkflows']:
        links = merge(links, initia_link_dico_rec(dico['subworkflows'][sub]))
    return links





#Returns the number of cycles in a graph (rootes with "Source" and "Sink")
#The input parameter is a links dico
#https://en.wikipedia.org/wiki/Cycle_(graph_theory)#Algorithm
def get_number_cycles(links):
    dico_nb_cycles = {'nb':0}
    dfs_dico = {}
    for node in links:
        dfs_dico[node] = {}
        dfs_dico[node]['visited'] = False
        dfs_dico[node]['finished'] = False

    edges_create_cycles = []

    def DFS(mother):
        if(dfs_dico[mother]["finished"]):
            return 
        if(dfs_dico[mother]["visited"]):
            dico_nb_cycles["nb"]+=1
            return "found cycle"
        dfs_dico[mother]["visited"] = True
        for daughter in links[mother]:
            _ = DFS(daughter)
            if(_ == "found cycle"):
                edges_create_cycles.append((mother, daughter))
        dfs_dico[mother]["finished"] = True

    for node in links:
        DFS(node)
    return dico_nb_cycles['nb'], edges_create_cycles


#https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search
def topological_sort(graph):
    L = []  # Empty list that will contain the sorted nodes
    temporary_marks = set()
    permanent_marks = set()

    def visit(node):
        if node in permanent_marks:
            return
        
        if node in temporary_marks:
            None
            #raise ValueError("Graph has at least one cycle")
        else:

            temporary_marks.add(node)

            for neighbor in graph.get(node, []):
                visit(neighbor)

            temporary_marks.remove(node)
            permanent_marks.add(node)
            L.insert(0, node)  # add node to head of L

    while set(graph.keys()) - permanent_marks:
        node = (set(graph.keys()) - permanent_marks).pop()
        visit(node)

    return L

#A variant of this answer https://stackoverflow.com/a/5164820
def get_number_paths_source_2_sink(graph):
    topo_sort  = topological_sort(graph)

    dict_paths_from_node_2_sink = {}
    for node in topo_sort:
        dict_paths_from_node_2_sink[node] = 1

    for i in range(len(topo_sort)-2, -1, -1):
        sum= 0
        for y in range(i+1, len(topo_sort)):
            sum += graph[topo_sort[i]].count(topo_sort[y])*dict_paths_from_node_2_sink[topo_sort[y]]
        dict_paths_from_node_2_sink[topo_sort[i]] = sum

    return dict_paths_from_node_2_sink["source"]


#For the shortest path
#https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
def dijkstra(graph):
    dist, prev = {}, {}
    Q = []
    for node in graph:
        dist[node] = np.Infinity
        prev[node] = None
        Q.append(node)
    dist['source'] = 0

    def get_node_in_Q_min_dist():
        min, node_min = dist[Q[0]], Q[0]
        for node in Q:
            if(min>dist[node]):
                min, node_min = dist[node], node
        return node_min

    while(len(Q)>0):
        u = get_node_in_Q_min_dist()
        Q.remove(u)
        for v in graph[u]:
            if(v in Q):
                alt = dist[u] + 1
                if(alt<dist[v]):
                    dist[v] = alt 
                    prev[v] = u
    return dist["sink"]

#https://www.geeksforgeeks.org/find-longest-path-directed-acyclic-graph/
def get_longest_distance(graph):
    dist = {}
    for node in graph:
        dist[node] = -np.Infinity
    dist["source"] = 0
    topo = topological_sort(graph)
    for u in topo:
        for v in graph[u]:
            if(dist[v]<dist[u]+1):
                dist[v] = dist[u]+1
    return dist["sink"]

##Returns the of paths, the longest and the shortes (not counting the source and sink)
#def get_paths(links):
#    PATHS = []
#    shortest_path = {"nb":0}
#    longest_path = {"nb":0}
#    nb_paths = {"nb":0}
#    
#    def get_paths_temp(links, mother, path_temp):
#        path = path_temp.copy()
#        path.append(mother)
#        if(mother=="Sink"):
#            nb_paths["nb"]+=1
#            if(shortest_path["nb"]==0):
#                shortest_path["nb"] = len(path)
#            if(longest_path["nb"]==0):
#                longest_path["nb"] = len(path)
#            if(longest_path["nb"]<len(path)):
#                longest_path["nb"]=len(path)
#            if(shortest_path["nb"]>len(path)):
#                shortest_path["nb"]=len(path)
#            return
#        for daughter in links[mother]:
#            if(daughter!=mother):
#                if(daughter not in path):
#                    get_paths_temp(links, daughter, path)
#
#
#    get_paths_temp(links, "Source", [])
#    number_paths_source_2_sink = nb_paths["nb"]
#    longest_path = longest_path["nb"]
#    smallest_path = shortest_path["nb"]
#
#    return number_paths_source_2_sink, longest_path, smallest_path


def flatten_dico(dico, dico_flattened):
    for node in dico["nodes"]:
        dico_flattened["nodes"].append(node)
    for edge in dico["edges"]:
        dico_flattened["edges"].append(edge)
    for subworkflow in dico["subworkflows"]:
        flatten_dico(dico["subworkflows"][subworkflow], dico_flattened)
    return dico_flattened