import sys


class Characteristic:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"'{self.name}', '{self.description}'"


class MR3CharacteristicBuilder:
    @staticmethod
    def parse_text(file: str) -> list[Characteristic]:
        with open(file) as f:
            text = '\n'.join([line.strip() for line in f.readlines()[1:]])  # Take [1:] to remove the header row.

        characteristics = []
        for line in text.splitlines():
            name, description = line.split(';')
            if name == "Name":
                continue
            else:
                description = description.replace("'", "''")
            characteristics.append(Characteristic(name, description))

        return characteristics


def main(file: str) -> str:
    """Creates an SQL INSERT query from the data in file.

    :param str file:
    :return: An SQL INSERT query featuring all MR3 Attacks
    :rtype: str
    """
    characteristics = []
    for characteristic in MR3CharacteristicBuilder.parse_text(file):
        characteristics.append(f"({str(characteristic)})")
    first_line = "INSERT INTO Characteristic (Characteristic, Description) VALUES"
    return first_line + "\n\t" + ",\n\t".join(characteristics) + ";"


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: MR3CharacteristicBuilder.py <input-file>")
        exit(1)
    print(main(sys.argv[1]))
