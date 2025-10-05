# 8) Utworzyć wykres kołowy prezentujący procentowe występowanie targetów w różnych
# częściach komórki.

import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt


def parse_target_locations(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns = {'db': 'http://www.drugbank.ca'}

    # Słownik do przechowywania liczby targetów w różnych częściach komórki
    location_counts = {}

    for target in root.findall(".//db:target", ns):
        polypeptide = target.find("db:polypeptide", namespaces=ns)
        if polypeptide is not None:
            cell_location = polypeptide.findtext("db:cellular-location", namespaces=ns) or "Nieznana lokalizacja"

            location_counts[cell_location] = location_counts.get(cell_location, 0) + 1

    return location_counts


def plot_pie_charts(location_counts, threshold=0.03):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.pie(
        location_counts.values(),
        # labels=location_counts.keys(),     Niestety z nazwami jest nieczytelnie
        colors=plt.cm.Set3.colors,
        wedgeprops={'edgecolor': 'black'}
    )
    plt.title("Procentowy podział targetów\nw różnych częściach komórki", fontsize=14)

    total = sum(location_counts.values())
    grouped_counts = {}
    other_count = 0

    for key, value in location_counts.items():
        if value / total < threshold:
            other_count += value
        else:
            grouped_counts[key] = value

    if other_count > 0:
        grouped_counts["Other"] = other_count

    plt.subplot(1, 2, 2)
    plt.pie(
        grouped_counts.values(),
        labels=grouped_counts.keys(),
        colors=plt.cm.Set3.colors,
        wedgeprops={'edgecolor': 'black'},
        autopct='%1.1f%%'
    )
    plt.title("Podział targetów (z wartościami <3% jako 'Other')", fontsize=14)

    plt.tight_layout()
    plt.show()


def main(xml_file):
    location_counts = parse_target_locations(xml_file)

    plot_pie_charts(location_counts)


if __name__ == "__main__":
    main("drugbank_partial.xml")