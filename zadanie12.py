# 12) Zaproponować własną analizę i prezentację danych dotyczących leków. Można w tym
# celu pozyskiwać dodatkowe informacje z innych biomedycznych i bioinformatycznych baz
# danych dostępnych online. Należy jednak upewnić się, czy dana baza danych pozwala na
# zautomatyzowane pobieranie danych przez program. Na przykład baza danych GeneCards
# wprost tego zabrania, co zostało na czerwono podkreślone na tej stronie. Przykładowe bazy
# danych to: UniProt (https://www.uniprot.org/), Small Molecule Pathway Database
# (https://smpdb.ca/), The Human Protein Atlas (https://www.proteinatlas.org/).

import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

def parse_drugs(xml_file, drugbank_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    # Lista przechowująca informację o cenach produktów
    prices = []
    # Lista przechowująca informację o cenach produktów zawierających daną substancję
    prices_drug = []
    # Lista patentów dla danej substancji leczniczej
    patents_drug = []
    # Słownik zliczający liczbę wystąpień danego kraju
    country_counts = {}
    # Słownik zliczający ile patentów jest w terminie
    date_counts = {}
    # Słownik zliczający ile patentów jest przystosowanych do dzieci
    pediatric_counts = {}
    # Lista przechowująca wartości punktów izoelektrycznych
    property_iso = []
    #Lista przechowująca wartości mas cząsteczkowych
    property_weight = []
    # Lista własności wszystkich leków
    property_drug = []

    for drug in root.findall(".//db:drug", ns):
        drug_id = drug.find("db:drugbank-id[@primary='true']", ns)
        if drug_id is not None:
            drug_id = drug_id.text

            # Obsługa cen leku
            drug_prices = drug.find("db:prices", ns)
            if drug_prices is not None:
                for price in drug_prices.findall("db:price", ns):
                    if price is not None:
                        description = price.findtext("db:description", namespaces=ns) or "Brak nazwy"
                        cost = price.findtext("db:cost", namespaces=ns) or "Brak ceny"
                        prices.append(cost)
                        if drug_id == drugbank_id:
                            prices_drug.append({
                                "Nazwa produktu" : description,
                                "Cena" : cost + " $"
                            })

            # Obsługa patentów
            drug_patents = drug.find("db:patents", ns)
            if drug_patents is not None:
                for patent in drug_patents.findall("db:patent", ns):
                    if patent is not None:
                        country = patent.findtext("db:country", namespaces=ns) or "Brak kraju"
                        date = patent.findtext("db:expires", namespaces=ns) or "Brak daty"
                        pediatric = patent.findtext("db:pediatric-extension", namespaces=ns) or "Brak informacji"
                        country_counts[country] = country_counts.get(country, 0) + 1
                        date1 = datetime.strptime(date, "%Y-%m-%d").date()
                        currently_date = "2025-02-01"
                        date2 = datetime.strptime(currently_date, "%Y-%m-%d").date()
                        if date1 < date2:
                            date_counts["nieważny"] = date_counts.get("nieważny", 0) + 1
                        else:
                            date_counts["ważny"] = date_counts.get("ważny", 0) + 1
                        pediatric_counts[pediatric] = pediatric_counts.get(pediatric, 0) + 1
                        if drug_id == drugbank_id:
                            patents_drug.append({
                                "Kraj patentu": country,
                                "Data ważności patentu": date,
                                "Rozszerzenie pediatryczne": pediatric
                            })

            # Obsługa właśności
            experimental_properties = drug.find("db:experimental-properties", ns)
            if experimental_properties is not None:
                for property in experimental_properties.findall("db:property", ns):
                    if property is not None:
                        kind = property.findtext("db:kind", namespaces=ns) or "Brak rodzaju"
                        if kind == "Isoelectric Point":
                            value = property.findtext("db:value", namespaces=ns) or "Brak informacji"
                            property_iso.append(value)
                            if drug_id == drugbank_id:
                                property_drug.append({
                                    "Rodzaj" : kind,
                                    "Wartość": value
                                })
                        if kind == "Molecular Weight":
                            value = property.findtext("db:value", namespaces=ns) or "Brak informacji"
                            property_weight.append(value)
                            if drug_id == drugbank_id:
                                property_drug.append({
                                    "Rodzaj": kind,
                                    "Wartość": value
                                })

    print_parameters(prices_drug, patents_drug, property_drug, drugbank_id)
    plot_prices_graph(prices)
    plot_patents_graph(country_counts, date_counts, pediatric_counts)
    plot_properties_graph(property_iso, property_weight)
    return



def print_parameters(prices, patents, properties, drug_id):
    print(f"DRUGBANK ID: {drug_id}")

    # Inicjujemy kolumny jeśli frame jest pusty
    if not prices:
        print("Brak cen")
    else:
        prices_df = pd.DataFrame(prices)
        print(prices_df.to_string())
    print("-" * 70)
    if not patents:
        print("Brak patentów")
    else:
        patents_df = pd.DataFrame(patents)
        print(patents_df.to_string())
    print("-" * 70)
    if not properties:
        print("Brak własności")
    else:
        properties_df = pd.DataFrame(properties)
        print(properties_df.to_string())

def plot_prices_graph(prices):
    plt.figure(figsize=(12, 6))

    grouped_counts = {
        "<5": 0,
        "<50": 0,
        "<500": 0,
        "<2000": 0,
        ">=2000": 0
    }

    for elem in prices:
        try:
            price = float(elem)
            if price < 5:
                grouped_counts["<5"] += 1
            elif price < 50:
                grouped_counts["<50"] += 1
            elif price < 500:
                grouped_counts["<500"] += 1
            elif price < 2000:
                grouped_counts["<2000"] += 1
            else:
                grouped_counts[">=2000"] += 1
        except ValueError:
            continue  # Pomijanie błędnych wartości

    plt.pie(
        grouped_counts.values(),
        labels=grouped_counts.keys(),
        colors=plt.cm.Set3.colors,
        wedgeprops={'edgecolor': 'black'},
        autopct='%1.1f%%'
    )
    plt.title("Podział cen produktów w USD", fontsize=30)

    plt.tight_layout()
    plt.show()


def plot_patents_graph(countries, dates, pediatric):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.pie(
        countries.values(),
        labels=countries.keys(),
        colors=plt.cm.Set3.colors,
        wedgeprops={'edgecolor': 'black'},
        autopct='%1.1f%%'
    )
    plt.title("Kraje patentów", fontsize=14)

    plt.subplot(1, 3, 2)
    plt.pie(
        dates.values(),
        labels=dates.keys(),
        colors=plt.cm.Set3.colors,
        wedgeprops={'edgecolor': 'black'},
        autopct='%1.1f%%'
    )
    plt.title("Ważności patentów", fontsize=14)

    plt.subplot(1, 3, 3)
    plt.pie(
        pediatric.values(),
        labels=pediatric.keys(),
        colors=plt.cm.Set3.colors,
        wedgeprops={'edgecolor': 'black'},
        autopct='%1.1f%%'
    )
    plt.title("Patenty przystosowane do dzieci", fontsize=14)
    plt.suptitle("Wykresy przedstawiające własności patentów", fontsize=30)

    plt.tight_layout()
    plt.show()

def plot_properties_graph(iso, weight):
    plt.figure(figsize=(12, 6))

    iso_grouped_counts = {
        "<5": 0,
        "<6": 0,
        "<7": 0,
        "<8": 0,
        "<9": 0,
        ">=9": 0
    }

    for elem in iso:
        try:
            value = float(elem)
            if value < 5:
                iso_grouped_counts["<5"] += 1
            elif value < 6:
                iso_grouped_counts["<6"] += 1
            elif value < 7:
                iso_grouped_counts["<7"] += 1
            elif value < 8:
                iso_grouped_counts["<8"] += 1
            elif value < 9:
                iso_grouped_counts["<9"] += 1
            else:
                iso_grouped_counts[">=9"] += 1
        except ValueError:
            continue  # Pomijanie błędnych wartości

    plt.subplot(1, 2, 1)
    plt.pie(
        iso_grouped_counts.values(),
        labels=iso_grouped_counts.keys(),
        colors=plt.cm.Set3.colors,
        wedgeprops={'edgecolor': 'black'},
        autopct = '%1.1f%%'
    )
    plt.title("Wartość punktu izoelektrycznego", fontsize=14)

    weight_grouped_counts = {
        "<10000": 0,
        "<30000": 0,
        "<80000": 0,
        "<150000": 0,
        "<250000": 0,
        ">=250000": 0,
    }

    for elem in weight:
        try:
            value = float(elem)
            if value < 10000:
                weight_grouped_counts["<10000"] += 1
            elif value < 30000:
                weight_grouped_counts["<30000"] += 1
            elif value < 80000:
                weight_grouped_counts["<80000"] += 1
            elif value < 150000:
                weight_grouped_counts["<150000"] += 1
            elif value < 250000:
                weight_grouped_counts["<250000"] += 1
            else:
                weight_grouped_counts[">=250000"] += 1
        except ValueError:
            continue  # Pomijanie błędnych wartości

    plt.subplot(1, 2, 2)
    plt.pie(
        weight_grouped_counts.values(),
        labels=weight_grouped_counts.keys(),
        colors=plt.cm.Set3.colors,
        wedgeprops={'edgecolor': 'black'},
        autopct='%1.1f%%'
    )
    plt.title("Masa cząsteczkowa", fontsize=14)
    plt.suptitle("Własności substancji", fontsize=25)

    plt.tight_layout()
    plt.show()


def main(xml_file):
    drug_id = "DB00108"

    parse_drugs(xml_file, drug_id)

if __name__ == "__main__":
    main("drugbank_partial.xml")