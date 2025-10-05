# 1) Utworzyć ramkę danych, która dla każdego leku zawiera następujące informacje: unikalny
# identyfikator leku w bazie DrugBank, nazwę leku, jego typ, opis, postać w jakiej dany lek
# występuje, wskazania, mechanizm działania oraz informacje z jakimi pokarmami dany lek
# wchodzi w interakcje.

import xml.etree.ElementTree as ET
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

def parse_drugbank(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}  # Namespace dla XML

    # Lista przechowująca informacje o lekach
    drug_data = []

    for drug in root.findall(".//db:drug", ns):
        id = drug.find("db:drugbank-id[@primary='true']", ns)
        if id is not None:
            id = id.text

            name = drug.findtext("db:name", namespaces=ns) or "Brak nazwy"
            type = drug.get("type", "Brak typu")
            description = drug.findtext("db:description", namespaces=ns) or "Brak opisu"
            state = drug.findtext("db:state", namespaces=ns) or "Brak postaci"
            indication = drug.findtext("db:indication", namespaces=ns) or "Brak wskazań"
            mechanism = drug.findtext("db:mechanism-of-action", namespaces=ns) or "Brak mechanizmu"
            food_interactions_elem = drug.findall("db:food-interactions/db:food-interaction", ns)
            food_interactions = ", ".join(
                [fi.text for fi in food_interactions_elem if fi.text]) if food_interactions_elem else "Brak informacji"

            drug_data.append({
                "DrugBank ID": id,
                "Nazwa": name,
                "Typ": type,
                "Opis": description,
                "Postać": state,
                "Wskazania": indication,
                "Mechanizm działania": mechanism,
                "Pokarmy, z którymi wchodzi w interakcję": food_interactions
            })

    drug_df = pd.DataFrame(drug_data)
    return drug_df


def display_drug_data(drug_df):
    for _, row in drug_df.iterrows():
        print(f"DrugBank ID: {row['DrugBank ID']}")
        print(f"Nazwa: {row['Nazwa']}")
        print(f"Typ: {row['Typ']}")
        print(f"Opis: {row['Opis']}")
        print(f"Postać: {row['Postać']}")
        print(f"Wskazania: {row['Wskazania']}")
        print(f"Mechanizm działania: {row['Mechanizm działania']}")
        print(f"Pokarmy, z którymi wchodzi w interakcję: {row['Pokarmy, z którymi wchodzi w interakcję']}")
        print("\n")
        print("*" * 1000)
        print("\n")

def main(xml_file):
    drug_df = parse_drugbank(xml_file)
    display_drug_data(drug_df)

    # Można też w formie tabelki, ale mniej czytelnie.
    print(drug_df)

if __name__ == "__main__":
    main("drugbank_partial.xml")
