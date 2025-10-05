# 10) Utworzyć ramkę danych zawierającą informacje dotyczące potencjalnych interakcji
# danego leku z innymi lekami.

import xml.etree.ElementTree as ET
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 10000)

def parse_drug_interactions_for_id(xml_file, drugbank_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    # Lista do przechowywania danych o interakcjach
    interactions_data = []

    drug = root.find(f".//db:drug[db:drugbank-id='{drugbank_id}']", ns)

    if drug is not None:
        for interaction in drug.findall("db:drug-interactions/db:drug-interaction", ns):
            interaction_id = interaction.findtext("db:drugbank-id", namespaces=ns) or "Brak ID"
            name = interaction.findtext("db:name", namespaces=ns) or "Brak nazwy"
            description = interaction.findtext("db:description", namespaces=ns) or "Brak opisu"

            interactions_data.append({
                "DrugBank ID": interaction_id,
                "Nazwa": name,
                "Opis": description
            })


    else:
        print(f"Nie znaleziono leku o ID: {drugbank_id}")

    interactions_df = pd.DataFrame(interactions_data)

    return interactions_df


def main(xml_file):
    target_drug_id = "DB00001"

    interactions_df = parse_drug_interactions_for_id(xml_file, target_drug_id)

    print(interactions_df.to_string())


if __name__ == "__main__":
    main("drugbank_partial.xml")