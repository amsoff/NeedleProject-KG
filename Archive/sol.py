from wikidata.client import Client
from Archive.entity_graph import Node as Node

client = Client()
entities = {}
base = len('http://www.wikidata.org/entity/')

import networkx as nx
import matplotlib.pyplot as plt





from wikidata.client import Client

client = Client()
entities = {}
base = len('http://www.wikidata.org/entity/')
edges = []


def parse_file(file):
    nodes = []
    first_line_flag = False
    with open(file, "r") as f:
        for line in f.readlines():
            if not first_line_flag:
                first_line_flag = True
            else:
                line_split = line.split(',')
                if len(line_split) > 1 and line_split[0] != "":
                    nodes.append(line_split[0][base:])

    temp_nodes = [node for node in nodes]
    for q_entity in nodes:
        entity = client.get(q_entity, load='true')
        att = (entity.attributes)['claims']

        if 'P31' in att:
            for inst in att['P31']:
                parent_id = inst['mainsnak']['datavalue']['value']['id']
                edges.append((parent_id, q_entity))
                if parent_id not in temp_nodes:
                    temp_nodes.append(parent_id)

        if 'P279' in att:
            for inst in att['P279']:
                parent_id = inst['mainsnak']['datavalue']['value']['id']
                edges.append((parent_id, q_entity))
                if parent_id not in temp_nodes:
                    temp_nodes.append(parent_id)
    return temp_nodes, edges



def file_runner():

    nodes_obj = {}
    edges_list_obj = []

    for i in range(12):
        file_name = "/cs/usr/sofferam/Needle_project/data/query" + str(i) + ".csv"
        nodes_list, edges = parse_file(file_name)
        with open("data/edges_file.txt", "a+") as f:
            f.write("\n---------node file " + str(i) + "-----------------\n")
            f.write(str(nodes_list))
            f.write("\n")
            f.write(str(edges))
            f.write("\n--------------------------\n")

        for node in nodes_list:
            try:
                entity = client.get(node, load='true')
                nodes_obj[node] = Node(node, entity.label.texts['en'])
                print(entity.label)
            except:
                pass

        for edge in edges:
            try:
                edges_list_obj.append((nodes_obj[edge[0]], nodes_obj[edge[1]]))
            except:
                pass

    G = nx.Graph()
    for node in nodes_obj.values():
        G.add_node(node)
    for edge in edges_list_obj:
        G.add_edge(edge[0], edge[1])
    nx.draw(G, with_labels=True)
    plt.show()


# if _name_ == '_main_':
file_runner()
