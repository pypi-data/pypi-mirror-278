"""
Formats the Russian verbs queried from Wikidata using query_verbs.sparql.

.. raw:: html
    <!--
    * Copyright (C) 2024 Scribe
    *
    * This program is free software: you can redistribute it and/or modify
    * it under the terms of the GNU General Public License as published by
    * the Free Software Foundation, either version 3 of the License, or
    * (at your option) any later version.
    *
    * This program is distributed in the hope that it will be useful,
    * but WITHOUT ANY WARRANTY; without even the implied warranty of
    * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    * GNU General Public License for more details.
    *
    * You should have received a copy of the GNU General Public License
    * along with this program.  If not, see <https://www.gnu.org/licenses/>.
    -->
"""

import collections
import os
import sys

from scribe_data.utils import export_formatted_data, load_queried_data

LANGUAGE = "Russian"
DATA_TYPE = "verbs"
file_path = sys.argv[0]

verbs_list, update_data_in_use, data_path = load_queried_data(
    file_path=file_path, language=LANGUAGE, data_type=DATA_TYPE
)

verbs_formatted = {}

all_conjugations = [
    "presFPS",
    "presSPS",
    "presTPS",
    "presFPP",
    "presSPP",
    "presTPP",
    "pastFeminine",
    "pastMasculine",
    "pastNeutral",
    "pastPlural",
]

for verb_vals in verbs_list:
    verbs_formatted[verb_vals["infinitive"]] = {}

    for conj in all_conjugations:
        if conj in verb_vals.keys():
            verbs_formatted[verb_vals["infinitive"]][conj] = verb_vals[conj]
        else:
            verbs_formatted[verb_vals["infinitive"]][conj] = ""

verbs_formatted = collections.OrderedDict(sorted(verbs_formatted.items()))

export_formatted_data(
    formatted_data=verbs_formatted,
    update_data_in_use=update_data_in_use,
    language=LANGUAGE,
    data_type=DATA_TYPE,
)

os.remove(data_path)
