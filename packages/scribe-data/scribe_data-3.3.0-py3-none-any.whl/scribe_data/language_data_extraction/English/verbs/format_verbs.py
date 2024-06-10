"""
Formats the English verbs queried from Wikidata using query_verbs.sparql.

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

LANGUAGE = "English"
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
    "pastFPS",
    "pastSPS",
    "pastTPS",
    "pastFPP",
    "pastSPP",
    "pastTPP",
    "pastPart",
]

for verb_vals in verbs_list:
    # If infinitive is available add to formatted verbs, else no entry created.
    if verb_vals["infinitive"] not in verbs_formatted.keys():
        verbs_formatted[verb_vals["infinitive"]] = {}

        infinitive_key = verb_vals["infinitive"]
        # presFPS
        verbs_formatted[infinitive_key]["presFPS"] = verb_vals.get("presFPS", "")
        verbs_formatted[infinitive_key]["presSPS"] = verb_vals.get("presFPS", "")

        # presTPS
        verbs_formatted[infinitive_key]["presTPS"] = verb_vals.get("presTPS", "")

        # Copying over presFPS to remaining present cases.
        verbs_formatted[infinitive_key]["presFPP"] = verb_vals.get("presFPS", "")
        verbs_formatted[infinitive_key]["presSPP"] = verb_vals.get("presFPS", "")
        verbs_formatted[infinitive_key]["presTPP"] = verb_vals.get("presFPS", "")

        # Assigning simpPast to all past keys if available.
        verbs_formatted[infinitive_key]["pastFPS"] = verb_vals.get("simpPast", "")
        verbs_formatted[infinitive_key]["pastSPS"] = verb_vals.get("simpPast", "")
        verbs_formatted[infinitive_key]["pastTPS"] = verb_vals.get("simpPast", "")
        verbs_formatted[infinitive_key]["pastFPP"] = verb_vals.get("simpPast", "")
        verbs_formatted[infinitive_key]["pastSPP"] = verb_vals.get("simpPast", "")
        verbs_formatted[infinitive_key]["pastTPP"] = verb_vals.get("simpPast", "")

        # pastParticiple
        verbs_formatted[infinitive_key]["pastPart"] = verb_vals.get("pastPart", "")

verbs_formatted = collections.OrderedDict(sorted(verbs_formatted.items()))

export_formatted_data(
    formatted_data=verbs_formatted,
    update_data_in_use=update_data_in_use,
    language=LANGUAGE,
    data_type=DATA_TYPE,
)

os.remove(data_path)
