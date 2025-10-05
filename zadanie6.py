# 6) Dla każdego leku w bazie danych podać liczbę szlaków, z którymi dany lek wchodzi w
# interakcje. Przedstawić wyniki w postaci histogramu z odpowiednio opisanymi osiami.

import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

def parse_drug_pathway_counts(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    # Słownik do przechowywania liczby szlaków dla każdego leku
    drug_pathway_counts = {}
    counted_pathways = {}

    for pathway in root.findall(".//db:pathway", ns):
        pathway_name = str(pathway.findtext("db:name", namespaces=ns) or "Brak ID")
        if pathway_name not in counted_pathways:
            counted_pathways[pathway_name] = True
            for drug in pathway.findall("db:drugs/db:drug", ns):
                drug_id = drug.findtext("db:drugbank-id", namespaces=ns) or "Brak ID"
                drug_pathway_counts[drug_id] = drug_pathway_counts.get(drug_id, 0) + 1

    drug_counts_df = pd.DataFrame(list(drug_pathway_counts.items()), columns=["DrugBank ID", "Liczba szlaków"]
    ).sort_values(by="DrugBank ID")

    plot_histogram(drug_counts_df)
    return drug_counts_df

def plot_histogram(drug_counts_df):
    plt.figure(figsize=(12, 7))
    plt.bar(drug_counts_df["DrugBank ID"], drug_counts_df["Liczba szlaków"], color="lightpink", edgecolor="black", alpha=0.8)
    plt.xlabel("ID leku", fontsize=12)
    plt.ylabel("Liczba szlaków", fontsize=12)
    plt.title("Liczba szlaków dla poszczególnych leków", fontsize=14)

    plt.xticks(rotation=90)

    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.show()

def main(xml_file):
    drug_counts_df = parse_drug_pathway_counts(xml_file)
    print(drug_counts_df)


if __name__ == "__main__":
    main("drugbank_partial.xml")