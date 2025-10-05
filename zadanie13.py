# 13) Stworzyć symulator, który generuje testową bazę 20000 leków. Wartości generowanych
# 19900 leków w kolumnie “DrugBank Id” powinny mieć kolejne numery, a w pozostałych
# kolumnach wartości wylosowane spośród wartości istniejących 100 leków. Zapisz wyniki w
# pliku drugbank_partial_and_generated.xml. Przeprowadź analizę według punktów 1-12
# testowej bazy

import xml.etree.ElementTree as ET
import random
import copy
import zadanie1
import zadanie2
import zadanie3
import zadanie4
import zadanie5
import zadanie6
import zadanie7
import zadanie8
import zadanie9
import zadanie10
import zadanie11
import zadanie12


def generate_drugbank_data(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    drugs = root.findall("{http://www.drugbank.ca}drug")
    drug_samples = drugs[:100]

    base_id = 109  # Pierwszy generowany lek zaczyna się od 109, ponieważ ostatni lek w bazie podstawowej ma numer 108.
    drugbank_ns = "{http://www.drugbank.ca}"

    ET.register_namespace("", "http://www.drugbank.ca")

    for i in range(0, 200):
        sample_drug = random.choice(drug_samples)
        new_drug = copy.deepcopy(sample_drug)

        new_id = f"DB{str(base_id + i).zfill(5)}"
        new_drug.find(f"{drugbank_ns}drugbank-id").text = new_id

        for elem in new_drug:
            if elem.tag != f"{drugbank_ns}drugbank-id":
                sample_value = random.choice(drug_samples).find(elem.tag)
                if sample_value is not None:
                    elem.text = sample_value.text

        root.append(new_drug)

    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(" Wygenerowano plik drugbank_partial_and_generated.xml")

def analyzing_tasks(xml_file):
    print("Zadanie 1:")
    zadanie1.main(xml_file)
    print("*" * 1000)
    print("Zadanie 2:")
    zadanie2.main(xml_file)
    print("*" * 1000)
    print("Zadanie 3:")
    zadanie3.main(xml_file)
    print("*" * 1000)
    print("Zadanie 4:")
    zadanie4.main(xml_file)
    print("*" * 1000)
    print("Zadanie 5:")
    zadanie5.main(xml_file)
    print("*" * 1000)
    print("Zadanie 6:")
    zadanie6.main(xml_file)
    print("*" * 1000)
    print("Zadanie 7:")
    zadanie7.main(xml_file)
    print("*" * 1000)
    print("Zadanie 8:")
    zadanie8.main(xml_file)
    print("*" * 1000)
    print("Zadanie 9:")
    zadanie9.main(xml_file)
    print("*" * 1000)
    print("Zadanie 10:")
    zadanie10.main(xml_file)
    zadanie11.main(xml_file)
    zadanie12.main(xml_file)


def main(xml_file):
    output_file = "drugbank_partial_and_generated.xml"
    generate_drugbank_data(xml_file, output_file)
    analyzing_tasks(xml_file)

if __name__ == "__main__":
    main("drugbank_partial.xml")