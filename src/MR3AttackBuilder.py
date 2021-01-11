from collections import Iterator
import sys


class Attack:
    def __init__(self, monster_derivation_id, attack_name, stat_used, attack_type, item_required,
                 guts_used, damage, guts_down, critical_chance, hit_chance,
                 max_level, attack_range, growth, effect=""):
        self.monster_derivation_id = int(monster_derivation_id) if monster_derivation_id != "" else 0
        self.attack_name = attack_name if attack_name != "" else "Unknown"
        self.stat_used = stat_used if stat_used != "" else "Unknown"
        self.attack_type = attack_type if attack_type != "" else "Unknown"
        self.item_required = item_required if item_required != "" else "Unknown"
        self.guts_used = int(guts_used) if guts_used != "" else 0
        self.damage = int(damage) if damage != "" else 0
        self.guts_down = int(guts_down) if guts_down != "" else 0
        self.critical_chance = int(critical_chance) if critical_chance != "" else 0
        self.hit_chance = int(hit_chance) if hit_chance != "" else 0
        self.max_level = int(max_level) if max_level != "" else 0
        self.attack_range = attack_range if attack_range != "" else "Unknown"
        self.growth = growth if growth != "" else "Unknown"
        self.effect = effect if effect != "" else "None"

    def __str__(self):
        return (", ".join([
            str(self.monster_derivation_id), f"'{self.attack_name}'", f"'{self.stat_used}'",
            f"'{self.attack_type}'", f"'{self.item_required}'",
            str(self.guts_used), str(self.damage), str(self.guts_down), str(self.critical_chance), str(self.hit_chance),
            str(self.max_level), f"'{self.attack_range}'", f"'{self.growth}'", f"'{self.effect}'"
        ]))


class MR3AttackParser:
    @staticmethod
    def parse_text(file) -> list[Attack]:
        def create_attack(line_iterator: Iterator[str], line: str, monster_derivation: int):
            """Parses through provided text to create an Attack object.

            :param Iterator[str] line_iterator: Iterator currently set at line
            :param str line: Current value of line_iterator
            :param int monster_derivation: Monster's derivation ID
            :return: An Attack parsed from the lines of text
            :rtype: Attack
            """
            # Set all fields to defaults.
            attack_name = stat_used = attack_type = item_required = ""
            guts_used = damage = guts_down = critical_chance = hit_chance = max_level = ""
            attack_range = growth = effect = ""

            # Populate all of the present fields with their values.
            while not is_empty(line):  # The next blank line separates this attack from the next.
                key, value = line.split(": ")
                if value == "-":
                    value = ""
                if key == "Attack":
                    attack_name = value
                elif key == "Stat Used":
                    stat_used = value
                elif key == "Type":
                    attack_type = value
                elif key == "Item":
                    item_required = value
                elif key == "Guts Used":
                    guts_used = value
                elif key == "Damage":
                    damage = value
                elif key == "Guts Down":
                    guts_down = value
                elif key == "Critical":
                    critical_chance = value
                elif key == "Hit":
                    hit_chance = value
                elif key == "Max Level":
                    max_level = value
                elif key == "Range":
                    attack_range = value
                elif key == "Growth":
                    growth = value
                elif key == "Effect":
                    effect = value

                try:
                    line = next(line_iterator)
                except StopIteration:  # Gracefully stop if at the end of the file.
                    break

            # Create and return an Attack.
            return Attack(monster_derivation, attack_name, stat_used, attack_type, item_required,
                          guts_used, damage, guts_down, critical_chance, hit_chance, max_level,
                          attack_range, growth, effect)

        def is_empty(line: str) -> bool:
            """Returns if the given text is empty.

            :param str line: Text to analyze
            :return: True if the line is empty
            :rtype: bool
            """
            return not line.strip()

        with open(file) as f:
            attack_document = '\n'.join([line.strip() for line in f.readlines()])

        attacks = []
        derivation_id = 0
        iterator = iter(attack_document.splitlines())
        for line in iterator:
            if is_empty(line):
                continue  # Ignore empty lines.
            if "Derivation:" in line:   # Sections are grouped by monster type.
                derivation_id = derivation_id + 1
            elif 'Attack:' in line:
                attacks.append(create_attack(iterator, line, derivation_id))
        return attacks


def main(file):
    attacks = []
    for attack in MR3AttackParser.parse_text(file):
        attacks.append(f"({str(attack)})")
    first_line = "INSERT INTO Attack (DerivationId, Attack, StatUsed, AttackType, ItemRequired, GutsUsed, Damage, " \
                 "GutsDown, Critical, Hit, MaxLevel, AttackRange, Growth, Effect) VALUES"
    print(first_line + "\n\t" + ",\n\t".join(attacks) + ";")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: MR3AttackBuilder.py <input-file>")
        exit(1)
    main(sys.argv[1])
