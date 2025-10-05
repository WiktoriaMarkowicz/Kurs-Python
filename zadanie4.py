# Utworzyć ramkę danych zawierającą informacje o wszystkich szlakach wszystkich
# rodzajów, tj. sygnałowych, metabolicznych, itd., z jakimi jakikolwiek lek wchodzi w interakcje.
# Podać całkowitą liczbę tych szlaków.

import xml.etree.ElementTree as ET
import pandas as pd


def parse_pathways(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    # Lista przechowująca infromacje o szlakach
    pathway_data = []

    for drug in root.findall(".//db:drug", ns):
        drug_id_elem = drug.find("db:drugbank-id[@primary='true']", ns)
        if drug_id_elem is not None:
            drug_id = drug_id_elem.text
        else:
            continue

        for pathway in drug.findall("db:pathways/db:pathway", ns):
            pathway_name = pathway.findtext("db:name", namespaces=ns) or "Brak nazwy"
            pathway_id = pathway.findtext("db:smpdb-id", namespaces=ns) or "Brak ID"

            pathway_data.append({
                "DrugBank ID": drug_id,
                "Nazwa szlaku": pathway_name,
                "ID szlaku": pathway_id,
            })

    pathway_df = pd.DataFrame(pathway_data)

    # Dodawanie kolumn, jeśli frame jest pusty
    if pathway_df.empty:
        pathway_df = pd.DataFrame(columns=["DrugBank ID", "Nazwa szlaku", "ID szlaku"])

    unique_pathways_count = pathway_df["ID szlaku"].nunique()
    print(f"Całkowita liczba unikalnych szlaków: {unique_pathways_count}")

    return pathway_df

def main(xml_file):
    pathway_df = parse_pathways(xml_file)
    print(pathway_df)

if __name__ == "__main__":
    main("drugbank_partial.xml")

