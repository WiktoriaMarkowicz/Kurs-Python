# 9) Utworzyć ramkę danych, pokazującą ile leków zostało zatwierdzonych, wycofanych, ile
# jest w fazie eksperymentalnej (ang. *experimental* lub *investigational*) i dopuszczonych w
# leczeniu zwierząt. Przedstawić te dane na wykresie kołowym. Podać liczbę zatwierdzonych
# leków, które nie zostały wycofane.

import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt


def parse_group(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    # Słownik do przechowywania liczby targetów w różnych częściach komórki
    group_counts = {}
    approved_and_withdrawn = 0;
    for drug in root.findall(".//db:drug", ns):
        approved = 0
        withdrawn = 0
        for group in drug.findall(".//db:group", ns):
            group = group.text
            if group is not None:
                group_counts[group] = group_counts.get(group, 0) + 1
                if group == "approved" :
                    approved = 1
                if group == "withdrawn" :
                    withdrawn = 1

        if approved == 1 and withdrawn == 0:
            approved_and_withdrawn += 1

    exp_and_inv = group_counts.get("experimental", 0) + group_counts.get("investigational", 0)
    if exp_and_inv > 0:
        group_counts["experimental"] = exp_and_inv
    group_counts.pop("investigational", None)  # Usuwamy klucz, o ile istnieje

    print(approved_and_withdrawn)
    return group_counts


def plot_pie_charts(group_counts, threshold=0.03):
    plt.figure(figsize=(12, 6))

    plt.pie(
        group_counts.values(),
        labels=group_counts.keys(),
        colors=plt.cm.Set3.colors,
        wedgeprops={'edgecolor': 'black'},
        autopct='%1.1f%%'  # Dodaje wartości procentowe
    )
    plt.title("Leki", fontsize=14)

    plt.tight_layout()
    plt.show()


def main(xml_file):
    group_counts = parse_group(xml_file)

    plot_pie_charts(group_counts)

if __name__ == "__main__":
    main("drugbank_partial.xml")