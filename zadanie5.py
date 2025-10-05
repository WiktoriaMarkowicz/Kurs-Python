# 5) Dla każdego szlaku sygnałowego/metabolicznego w bazie danych podać leki, które
# wchodzą z nim w interakcje. Wyniki należy przedstawić w postaci ramki danych jak i w
# opracowanej przez siebie formie graficznej. Przykładem takiej grafiki może być graf
# dwudzielny, gdzie dwa rodzaje wierzchołków to szlaki sygnałowe i leki, a poszczególne
# krawędzie reprezentują interakcję danego leku z danym szlakiem sygnałowym. Należy
# zadbać o czytelność i atrakcyjność prezentacji graficznej.

import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def parse_pathways_and_drugs(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    interaction_data = []

    for pathway in root.findall(".//db:pathway", ns):
        pathway_name = pathway.findtext("db:name", namespaces=ns) or "Brak nazwy"
        pathway_id = pathway.findtext("db:smpdb-id", namespaces=ns) or "Brak ID"

        for drug in pathway.findall("db:drugs/db:drug", ns):
            drug_name = drug.findtext("db:name", namespaces=ns) or "Brak nazwy"
            drug_id = drug.findtext("db:drugbank-id", namespaces=ns) or "Brak ID"

            interaction_data.append({
                "ID szlaku": pathway_id,
                "Nazwa szlaku": pathway_name,
                "DrugBank ID": drug_id,
                "Nazwa leku": drug_name
            })

    interaction_df = pd.DataFrame(interaction_data)

    return interaction_df


def plot_graph(interaction_df):
    G = nx.Graph()

    for _, row in interaction_df.iterrows():
        pathway_node = f"{row['Nazwa szlaku']}"
        drug_node = row['Nazwa leku']
        G.add_node(pathway_node, bipartite=0, color='lightblue')
        G.add_node(drug_node, bipartite=1, color='pink')
        G.add_edge(drug_node, pathway_node)

    # Tworzenie układu: węzły leków po lewej, węzły szlaków po prawej
    drug_nodes = [node for node, attr in G.nodes(data=True) if attr['bipartite'] == 1]
    pathway_nodes = [node for node, attr in G.nodes(data=True) if attr['bipartite'] == 0]

    pos = {}
    for i, node in enumerate(drug_nodes):
        pos[node] = (0, -i)
    for i, node in enumerate(pathway_nodes):
        pos[node] = (1, -i)

    node_colors = [G.nodes[node]['color'] for node in G.nodes]

    plt.figure(figsize=(19, 12))
    plt.title("Graf przedstawiający interakcje między lekami i szlakami", fontsize=20)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        font_size=10,
        font_color='black',
        edge_color='gray',
        linewidths=1,
        alpha=0.8
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
    plt.axis("off")
    plt.show()


def main(xml_file):
    interaction_df = parse_pathways_and_drugs(xml_file)
    print(interaction_df)
    plot_graph(interaction_df)

if __name__ == "__main__":
    main("drugbank_partial.xml")