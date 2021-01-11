import re
import time
from typing import Union

import requests
from bs4 import BeautifulSoup, Tag


class MR3Monster:
    DerivationNumberToName = {
        1: "Baku",
        2: "Beaklon",
        3: "Colorpandora",
        4: "Dragon",
        5: "Dakkung",
        6: "Durahan",
        7: "Gitan",
        8: "Golem",
        9: "Hare",
        10: "Henger",
        11: "Jell",
        12: "Joker",
        13: "Lesione",
        14: "Mew",
        15: "Mocchi",
        16: "Mogi",
        17: "Momo",
        18: "Naga",
        19: "Octopee",
        20: "Ogyo",
        21: "Pancho",
        22: "Pixie",
        23: "Plant",
        24: "Psiroller",
        25: "Raiden",
        26: "Suezo",
        27: "Suzurin",
        28: "Tiger",
        29: "Zan",
        30: "Zoom"
    }

    RegionNumberToName = {
        1: "Brillia",
        2: "Goat",
        3: "Takrama",
        4: "Kalaragi",
        5: "Morx",
        6: "Special"
    }

    def __init__(self, species, derivation_id, region_id, description):
        self.species = species
        self.derivation_id = derivation_id
        self.region_id = region_id
        self.description = description

    def __str__(self):
        derivation = self.DerivationNumberToName[self.derivation_id]
        region = self.RegionNumberToName[self.region_id]
        return f"{self.species} | {derivation} | {region} | {self.description}"


class MR3FandomScraper:
    EncyclopediaURL = "https://monster-rancher.fandom.com/wiki/Monster_Rancher_3_Encyclopedia"

    Delay = 0.150

    RegionNameToNumberDict = {
        "Brillia": 1,
        "Goat": 2,
        "Takrama": 3,
        "Kalaragi": 4,
        "Morx": 5,
        "Special": 6
    }

    @staticmethod
    def format_monster_for_url_usage(monster: str) -> str:
        """Re-formats the name according to what Fandom URLs will require.

        :param str monster: name to format
        :return: wiki-friendly monster name for URLS
        :rtype: str

        Usage:

        >>> MR3FandomScraper.format_monster_for_url_usage("Color Pandora")
        'Color_Pandora'
        >>> MR3FandomScraper.format_monster_for_url_usage("Cactun")
        'Cactan'
        """
        return (
            monster
            .replace(' ', '_')  # Wiki URLs replace spaces with underscores.
            .replace("Cactun", "Cactan")  # The wiki URL uses an alternate spelling.
        )

    @staticmethod
    def get_monster_description(monster: str, derivation: str, region: str) -> str:
        """Get the in-game description of the specified monster_name.

        :param str monster: Monster species name
        :param str derivation: Derivation (aka Type), e.g., Baku, Golem, etc.
        :param str region: Monster's region (in MR3, this acts like other games' sub-type)
        :return: The Fandom wiki's transcription of the monster_name's in-game description
        :rtype: str

        Usage:

        >>> MR3FandomScraper.get_monster_description("Coral", "Lesione", "Special")
        '"Its texture is soft like a sponge. It feels so good you want to sleep on its back."'
        """

        def format_monster_for_string_comparison(monster_name: str) -> str:
            """Cleans, then makes the name lowercase.

            :param str monster_name:
            :return: Cleaned, lowered name
            :rtype: str
            """
            return (
                monster_name
                .replace('_', ' ')
                .replace('-', ' ')
                .replace("Color Pandora", "Colorpandora")  # Translating from Encyclopedia to actual name
                .replace("Beaclon", "Beaklon")             # Translating from Encyclopedia to actual name
                .replace("Henger", "Hengar")               # Translating from Encyclopedia to actual name
                .lower()
            )

        def find_monster_summary_table(monster_to_find) -> Tag:
            """Finds the summary table for monster, searching multiple URLs as needed.

            :param str monster_to_find: Monster to find
            :return: The monster's summary table Tag
            :rtype: Tag
            """
            def get_table_from(page_url: str) -> Union[Tag, None]:
                """Finds the table tag from the given page, if present.

                :param page_url: URL to search for the table in
                :return: The table's Tag if in page_url, None otherwise
                :rtype: Union[Tag, None]
                """
                try:
                    page = requests.get(page_url)
                    soup = BeautifulSoup(page.content, features="html.parser")
                    content = soup.find("div", attrs={"class": "mw-parser-output"})
                    wiki_table = content.find("table", attrs={"class": "wikitable"})
                    return wiki_table
                except AttributeError:  # We tried to access `.find()` on a non-Tag (NavigableString)
                    return None

            direct_page_url = f"https://monster-rancher.fandom.com/wiki/{monster_to_find}"
            derivation_page_url = f"https://monster-rancher.fandom.com/wiki/{monster_to_find}_({derivation})"
            monster_derivation_page_url = f"https://monster-rancher.fandom.com/wiki/{monster_to_find}_(Monster)"
            special_derivation_page_url = f"https://monster-rancher.fandom.com/wiki/{monster_to_find}_(%3F%3F%3F_Sub)"

            for url in [direct_page_url, derivation_page_url, monster_derivation_page_url, special_derivation_page_url]:
                table = get_table_from(url)
                if table is None:
                    continue
                return table

        def is_name_column() -> bool:
            """Determines if the current text matches the monster's info.

            :return: True if the text comes from the Name column
            :rtype: bool
            """
            return (
                description_comp == monster_comp or
                description_comp == f"{monster_comp} ({derivation.lower()})" or
                description_comp == f"{monster_comp} ({region.lower()})" or
                description_comp == f"{monster_comp} (???)"
            )

        monster = MR3FandomScraper.format_monster_for_url_usage(monster)
        monster_comp = format_monster_for_string_comparison(monster)
        monster_summary_table = find_monster_summary_table(monster)

        """
        Table columns are like: 
        Game | Name | Description
        So we find the correct row via the Monster Rancher 3 <a> hyperlink in the Game column.
        The <a> tag, however, is wrapped in an <i> tag. So to get to the <td> tag, we need to go up two parents.
        """
        mr3_td = monster_summary_table.find("tbody").find("a", attrs={"title": "Monster Rancher 3"}).parent.parent
        for sibling in mr3_td.next_siblings:
            # Sibling travel within BeautifulSoup: ["\n", <Name td Tag>, "\n", <Description td Tag>];
            # non-Tags are `NavigableString`s and will throw when we try to access `.text` like a Tag
            try:
                description_text = sibling.text.strip().replace('\n', ' ')
            except AttributeError:  # We tried to access `.text` on a non-Tag (NavigableString)
                continue

            # Continue past the Name column
            description_comp = description_text.lower()
            if is_name_column():
                continue

            return description_text

    @staticmethod
    def get_all_monster_derivations() -> list[str]:
        """Gets all MR3 monster derivations (aka types).

        :return: Wrangled list of MR3 monster derivations
        :rtype: list[str]

        Usage:

        >>> MR3FandomScraper.get_all_monster_derivations()
        ['Baku', 'Beaklon', 'Colorpandora', 'Dragon', 'Dakkung', 'Durahan', 'Gitan', 'Golem', 'Hare', 'Hengar', 'Jell', 'Joker', 'Lesione', 'Mew', 'Mocchi', 'Mogi', 'Momo', 'Naga', 'Octopee', 'Ogyo', 'Pancho', 'Pixie', 'Plant', 'Psiroller', 'Raiden', 'Suezo', 'Suzurin', 'Tiger', 'Zan', 'Zoom']
        """
        def wrangle(derivation_header_tag: Tag) -> str:
            """Extracts and cleans the monster derivation from th given tag.

            :param Tag derivation_header_tag: header tag containing the derivation
            :return: Extracted and wrangled monster derivation
            :rtype: str
            """
            derivation = (
                derivation_header_tag
                .text
                .strip()
                .replace("Color Pandoras", "Colorpandoras")
                .replace("Henger", "Hengar")
                .replace("Beaclon", "Beaklon")
            )
            if " (" in derivation:
                derivation = derivation.split(" (")[0]
            elif '[' in derivation:
                derivation = derivation.split('[')[0].strip()[:-1]
            if derivation[-1] == 's':
                derivation = derivation[:-1]
            return derivation

        page = requests.get(MR3FandomScraper.EncyclopediaURL)
        soup = BeautifulSoup(page.content, features="html.parser")
        content = soup.find(id="mw-content-text")
        monster_headers = content.find_all("h2")[1:]  # Ignore table of contents header
        return [wrangle(m) for m in monster_headers]

    @staticmethod
    def get_all_monsters(count: int = 0) -> list[MR3Monster]:
        """Gets all (or the specified amount of) MR3 monsters listed in the Fandom wiki.

        :param int count: How many monsters to add; if left at 0 or > max, all will be added
        :return: All (or the specified amount of) MR3 monsters in the wiki.
        :rtype: List[MR3Monster]

        Usage:

        >>> MR3FandomScraper.get_all_monsters(1).pop().__str__()
        Got #001: Baku | Baku | Brillia | "A big furry loveable moster with a huge appetite. Contrary to its looks, it is actually very agile."
        'Baku | Baku | Brillia | "A big furry loveable moster with a huge appetite. Contrary to its looks, it is actually very agile."'
        """
        def get_monster_rows() -> list[Tag]:
            """Grabs the table row tags containing monster data.

            :return: <tr> tags with monster data
            :rtype: list[Tag]
            """
            page = requests.get(MR3FandomScraper.EncyclopediaURL)
            soup = BeautifulSoup(page.content, features="html.parser")
            content = soup.find(id="mw-content-text")
            rows = content.find_all("tr")
            return rows

        def format_monster_name(monster_name: str) -> str:
            """Corrects the spellings of some names.

            :param str monster_name: Name to format
            :return: Corrected monster name
            :rtype: str
            """
            return (
                monster_name
                .replace("Color Pandora", "Colorpandora")
                .replace("Henger", "Hengar")
                .replace("Beaclon", "Beaklon")
            )

        monsters = []
        monster_derivations = MR3FandomScraper.get_all_monster_derivations()
        monster_rows = get_monster_rows()
        monster_derivation_index = 0
        monsters_counted = 0
        derivation = ""
        for row in monster_rows:
            if monsters_counted != 0 and monsters_counted == count:
                break
            # Find the needed pieces of text.
            text = row.text.strip()
            if "Location" in text:  # Ignore header rows.
                continue
            text = text.replace('?', "Special")
            parts = text.split("\n\n")
            # Handle the first part.
            region = parts[0]
            region_number = MR3FandomScraper.RegionNameToNumberDict[region]
            if region_number == 1:  # Brillia is the first region listed for each derivation's chart
                derivation = monster_derivations[monster_derivation_index]
                monster_derivation_index = monster_derivation_index + 1
            # Handle the second part.
            name = parts[1]
            if name == '-':  # When no monster exists for a region + derivation combo, a dash is present.
                continue
            name = format_monster_name(parts[1])
            # Get the monster's description.
            time.sleep(MR3FandomScraper.Delay)  # Take a delay to lessen load/timeouts.
            description = MR3FandomScraper.get_monster_description(parts[1], derivation, region)
            # Add the monster to the list.
            monster = MR3Monster(name, monster_derivation_index, region_number, description)
            monsters.append(monster)
            monsters_counted = monsters_counted + 1
            print(f"Got #{monsters_counted:03d}: {monster}")
        return monsters


def main():
    monsters = MR3FandomScraper.get_all_monsters()
    sql_statement = (
        "INSERT INTO Monster (Monster, DerivationID, RegionID, Description) VALUES\n\t" +
        ",\n\t".join([f"('{m.species}', {m.derivation_id}, {m.region_id}, '{m.description}')" for m in monsters]) +
        ";"
    )
    sql_statement = sql_statement.replace("'\"", "'").replace("\"'", "'")
    regex = r"(?<!, )(?<!\()\'(?!\'\w)(?!\))(?!, [0-9])"
    sql_statement = re.sub(regex, "''", sql_statement)
    print(sql_statement)


if __name__ == '__main__':
    main()
