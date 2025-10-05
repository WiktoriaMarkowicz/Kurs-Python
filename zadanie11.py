# 11) Opracować według własnego pomysłu graficzną prezentację zawierającą informacje o
# konkretnym genie lub genach, substancjach leczniczych, które z tym genem/genami
# wchodzą w interakcje, oraz produktach farmaceutycznych, które zawierają daną substancję
# leczniczą. Wybór dotyczący tego, czy prezentacja graficzna jest realizowana dla
# konkretnego genu, czy wszystkich genów jednocześnie pozostawiamy Państwa decyzji.
# Przy dokonywaniu wyboru należy kierować się czytelnością i atrakcyjnością prezentacji
# graficznej.

import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

def parse_gene_interactions(xml_file, gene_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    # Listy do przechowywania danych
    statistics_about_all_genes = {}
    interactions = []

    for drug in root.findall(".//db:drug", ns):
        id = drug.find("db:drugbank-id[@primary='true']", ns)
        if id is not None:
            id = id.text
            products = []
            for target in drug.findall(".//db:target", ns):
                if target is not None:
                    polypeptide = target.find("db:polypeptide", ns)
                    if polypeptide is not None:
                        gene_name = polypeptide.find("db:gene-name", ns)
                        gene_name = gene_name.text
                        statistics_about_all_genes[gene_name] = statistics_about_all_genes.get(gene_name, 0) + 1
                        if gene_name is not None and gene_name == gene_id:
                            interactions.append(id)
                            for product in drug.findall(".//db:product", ns):
                                if product is not None:
                                    products.append(product.findtext("db:name", namespaces = ns))
                            plot_products_graph(products, id)

    statistics_about_all_genes_df = pd.DataFrame(
        list(statistics_about_all_genes.items()), columns=["Nazwa genu", "Liczba substancji"]
    )

    print(statistics_about_all_genes_df)
    plot_gene_graph(interactions, gene_id)

    return

def plot_products_graph(products_data, drug_id):
    G = nx.Graph()

    G.add_node(drug_id, color='lightblue', size=4000)  # Kolor głównego węzła
    for product in products_data:
        G.add_node(product, color='pink', size=3000)  # Kolor węzłów synonimów
        G.add_edge(drug_id, product)

    # Pobranie kolorów i rozmiarów dla węzłów
    node_colors = [G.nodes[n]['color'] for n in G.nodes]
    node_sizes = [G.nodes[n]['size'] for n in G.nodes]

    plt.figure(figsize=(15, 10))
    pos = nx.shell_layout(G)
    plt.title(f"Graf produktów farmaceutycznych, które zawierają substancję leczniczą: {drug_id}", fontsize=25)

    nx.draw(
        G,
        pos,
        node_color=node_colors,
        node_size=node_sizes,
        edge_color='gray',
        width=2,
        with_labels=True,
        font_size=10,
        font_color='black',
        font_weight='bold'
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


def plot_gene_graph(drugs_data, gene_name):
    G = nx.Graph()

    G.add_node(gene_name, color='lightblue', size=4000)
    for drug in drugs_data:
        G.add_node(drug, color='pink', size=3000)
        G.add_edge(gene_name, drug)

    node_colors = [G.nodes[n]['color'] for n in G.nodes]
    node_sizes = [G.nodes[n]['size'] for n in G.nodes]

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42, k=0.8)
    plt.title(f"Graf substancji leczniczych, które wchodzą w interakcje z genem {gene_name}", fontsize=15)

    nx.draw(
        G,
        pos,
        node_color=node_colors,
        node_size=node_sizes,
        edge_color='gray',
        width=2,
        with_labels=True,
        font_size=10,
        font_color='black',
        font_weight='bold'
    )

    labels = {n: n for n in G.nodes}
    nx.draw_networkx_labels(
        G,
        pos,
        labels,
        font_size=10,
        font_color='black',
        font_weight='bold',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
    )

    plt.show()

def main(xml_file):
    gene_id = "F2"

    parse_gene_interactions(xml_file, gene_id)

if __name__ == "__main__":
    main("drugbank_partial.xml")