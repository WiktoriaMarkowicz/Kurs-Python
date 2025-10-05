# 2) Utworzyć ramkę danych pozwalającą na wyszukiwanie po DrugBank ID informacji o
# wszystkich synonimach pod jakimi dany lek występuje. Napisać funkcję, która dla podanego
# DrugBank ID utworzy i wyrysuje graf synonimów za pomocą biblioteki NetworkX. Należy
# zadbać o czytelność generowanego rysunku.

import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt

def parse_synonyms(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    # Słownik przechowujący synonimy
    synonym_data = {}

    for drug in root.findall(".//db:drug", ns):
        id = drug.find("db:drugbank-id[@primary='true']", ns)
        if id is not None:
            id = id.text
            synonyms = [
                synonym.text for synonym in drug.findall("db:synonyms/db:synonym", ns)
            ]
            if synonyms:
                synonym_data[id] = synonyms

    return synonym_data


def print_synonyms(synonym_data):
    for id, synonyms in synonym_data.items():
        print(f"DrugBank ID: {id}")
        print("Synonimy:")
        for synonym in synonyms:
            print(f"  - {synonym}")
        print("-" * 50)


def plot_synonym_graph(synonym_data, drug_id):
    G = nx.Graph()

    synonyms = synonym_data.get(drug_id, [])
    if not synonyms:
        print(f"Brak synonimów dla: {drug_id}")
        return

    G.add_node(drug_id, color='lightblue', size=4000)
    G.add_nodes_from([(syn, {'color': 'pink', 'size': 3000}) for syn in synonyms])
    G.add_edges_from([(drug_id, syn) for syn in synonyms])

    node_colors = [G.nodes[n]['color'] for n in G.nodes]
    node_sizes = [G.nodes[n]['size'] for n in G.nodes]

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42, k=0.8)
    plt.title(f"Graf synonimów dla {drug_id}", fontsize=15)

    nx.draw(
        G,
        pos,
        node_color=node_colors,
        node_size=node_sizes,
        edge_color='gray',
        width=2,
        with_labels=True,
        font_size=10,
        font_color='black'
    )

    labels = {n: n for n in G.nodes}
    nx.draw_networkx_labels(
        G,
        pos,
        labels,
        font_size=10,
        font_color='black',
        font_weight='bold',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')  # Ramki wokół etykiet
    )

    plt.show()

def main(xml_file):
    synonym_data = parse_synonyms(xml_file)
    print_synonyms(synonym_data)

    plot_synonym_graph(synonym_data, "DB00005")

if __name__ == "__main__":
    main("drugbank_partial.xml")