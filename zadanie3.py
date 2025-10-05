# 3) Utworzyć ramkę danych o produktach farmaceutycznych zawierających dany lek
# (substancję leczniczą). Ramka powinna zawierać informacje o ID leku, nazwie produktu,
# producencie, kod w narodowym rejestrze USA (ang. *National Drug Code*), postać w jakiej
# produkt występuje, sposób aplikacji, informacje o dawce, kraju i agencji rejestrującej
# produkt.

import xml.etree.ElementTree as ET
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

def parse_products(xml_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    # Lista przechowująca informacje o produktach farmaceutycznych
    product_data = []

    for drug in root.findall(".//db:drug", ns):
        drug_id_elem = drug.find("db:drugbank-id[@primary='true']", ns)
        if drug_id_elem is not None:
            drug_id = drug_id_elem.text
        else:
            continue

        for product in drug.findall("db:products/db:product", ns):
            product_name = product.findtext("db:name", namespaces=ns) or "Brak nazwy"
            labeller = product.findtext("db:labeller", namespaces=ns) or "Brak producenta"
            ndc_code = product.findtext("db:ndc-product-code", namespaces=ns) or "Brak kodu"
            form = product.findtext("db:dosage-form", namespaces=ns) or "Brak postaci"
            route = product.findtext("db:route", namespaces=ns) or "Brak"
            strength = product.findtext("db:strength", namespaces=ns) or "Brak"
            country = product.findtext("db:country", namespaces=ns) or "Brak państwa"
            source = product.findtext("db:source", namespaces=ns) or "Brak agencji"

            product_data.append({
                "DrugBank ID": drug_id,
                "Nazwa produktu": product_name,
                "Producent": labeller,
                "Kod NDC": ndc_code,
                "Postać": form,
                "Sposób aplikacji": route,
                "Dawka": strength,
                "Kraj": country,
                "Agencja": source
            })

    product_df = pd.DataFrame(product_data)

    # Zapisujemy dane do pliku csv, ponieważ nie mieszcza sie w terminalu.
    product_df.to_csv(output_file, index=False)
    print(f"Dane o produktach zostały zapisane do pliku: {output_file}")
    return product_df


def display_products_for_id(product_df, drug_id):
    filtered_df = product_df[product_df["DrugBank ID"] == drug_id]
    print(f"\nTabela produktów dla {drug_id}:")
    print(filtered_df)

def main(xml_file):
    output_file = "result3.csv"
    product_df = parse_products(xml_file, output_file)

    # Nie trzeba bylo, ale dzieki temu mozna wyswietlic informacje w terinalu.
    display_products_for_id(product_df, "DB00005")

if __name__ == "__main__":
    main("drugbank_partial.xml")
