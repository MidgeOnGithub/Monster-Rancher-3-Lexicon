# Monster Rancher 3 Lexicon
## Table of Contents
* [Description](#description)
* [License Info](#license-info)
  * [CC-BY-SA](#cc-by-sa)
  * [MIT](#mit) 

## Description
Remember the enthrallment and curiosity you felt whenever you tried a disk, anxiously awaiting to see what cool monster was generated?
The Monster Rancher games left a lasting impression and nostalgia; recently, I found my old copy of Monster Rancher 3 and played again.
As I was generating monsters, I used a spreadsheet to document which disks (Saucer Stones) I tried and what monster they output.
I started to realize the spreadsheet has some annoying limitations: I could not cleaning create many-to-many or one-to-many relationship.
I eventually realized: this would be a great small database project.

This repo includes some Python scripts which helped scrape/parse data for reference table `INSERT` queries.
It also contains some SQL scripts/queries which are meant to run against an SQLite database.
SQLite was chosen since this is a smaller project, and having a simple file database makes learning/tinkering easier for me.

Eventually, I'd like to create a simple webpage with some search filters to demonstrate the kinds of queries that can be done.
Perhaps I'll add users/authentication to allow inserts, management for admins, etc., but that will be in some time.

## License Info
### CC-BY-SA
Data scraped from the [Monster Rancher 3 Fandom wiki](https://monster-rancher.fandom.com/wiki/Monster_Rancher_3),
specifically the [Encyclopedia](https://monster-rancher.fandom.com/wiki/Monster_Rancher_3_Encyclopedia)
and the individual monster pages which are linked from the encyclopedia,
are subject to the [CC-BY-SA](https://creativecommons.org/licenses/by-sa/4.0/) license.

Thus, some items in accordance to the license's terms:
* Credit for the `Monster` table's original data is given to all relevant wiki page contributors (including myself).
* I declare that I made changes (spelling/format edits) to the scraped data for my uses.
* The `Monster` table data I have used or altered is hereby licensed under the same CC-BY-SA license.

### MIT
Excepting the specific data stated above, my work and products within this project are licensed under the MIT License.
You can view it [here](https://mit-license.org/) or in the `LICENSE` file. 