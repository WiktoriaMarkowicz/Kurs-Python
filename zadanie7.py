# 7) Utworzyć ramkę danych zawierającą informacje o białkach, z którymi poszczególne leki
# wchodzą w interakcje. Białka te to tzw. targety. Ramka danych powinna zawierać
# przynajmniej DrugBank ID targetu, informację o zewnętrznej bazie danych (ang. *source*,
# np. Swiss-Prot), identyfikator w zewnętrznej bazie danych, nazwę polipeptydu, nazwę genu
# kodującego polipeptyd, identyfikator genu GenAtlas ID, numer chromosomu, umiejscowienie
# w komórce.

import xml.etree.ElementTree as ET
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

def parse_drug_targets(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    # Lista do przechowywania danych o targetach
    target_data = []

    for target in root.findall(".//db:target", ns):
        drugbank_id = target.findtext("db:id", namespaces=ns) or "Brak ID"

        polypeptide = target.find("db:polypeptide", namespaces=ns)
        if polypeptide is not None:
            target_id = polypeptide.get("id") or "Brak ID"
            source = polypeptide.get("source") or "Brak źródła"
            name = polypeptide.findtext("db:name", namespaces=ns) or "Brak nazwy"
            gene_name = polypeptide.findtext("db:gene-name", namespaces=ns) or "Brak nazwy"
            cellular_location = polypeptide.findtext("db:cellular-location", namespaces=ns) or "Brak umiejscowienia"
            chromosome_location = polypeptide.findtext("db:chromosome-location", namespaces=ns) or "Brak numeru"
            identifier = "Brak"

            for external_identifier in target.findall(".//db:external-identifier", ns):
                resource = external_identifier.findtext("db:resource", namespaces=ns)
                if resource == "GenAtlas" :
                    identifier = external_identifier.findtext("db:identifier", namespaces=ns) or "Brak"

            target_data.append({
                "DrugBank ID": drugbank_id,
                "Zewnetrzna baza": source,
                "ID zewnetrznej bazy": target_id,
                "Nazwa polipeptydu": name,
                "Nazwa genu kodujacego": gene_name,
                "GenAtlas ID": identifier,
                "Numer chromosomu": chromosome_location,
                "Umiejscowienie w komorce": cellular_location,
            })

    # Inicjujemy kolumny jeśli frame jest pusty
    if not target_data:
        target_df = pd.DataFrame(columns=[
            "DrugBank ID", "Zewnetrzna baza", "ID zewnetrznej bazy",
            "Nazwa polipeptydu", "Nazwa genu kodujacego",
            "GenAtlas ID", "Numer chromosomu", "Umiejscowienie w komorce"
        ])
    else:
        target_df = pd.DataFrame(target_data)
    return target_df


def main(xml_file):
    target_df = parse_drug_targets(xml_file)

    print(target_df)

    target_df.to_csv("drug_targets.csv", index=False)
    print("Dane o targetach zostały zapisane do pliku 'drug_targets.csv'.")

if __name__ == "__main__":
    main("drugbank_partial.xml")