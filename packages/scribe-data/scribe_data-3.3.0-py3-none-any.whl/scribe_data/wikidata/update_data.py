"""
Updates data for Scribe by running all or desired WDQS queries and formatting scripts.

Parameters
----------
    languages : list of strings (default=None)
        A subset of Scribe's languages that the user wants to update.

    word_types : list of strings (default=None)
        A subset of nouns, verbs, and prepositions that currently can be updated with this fie.

Example
-------
    python3 src/scribe_data/extract_transform/wikidata/update_data.py '["French", "German"]' '["nouns", "verbs"]'

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

import itertools
import json
import os
import sys
from urllib.error import HTTPError

import pandas as pd
from SPARQLWrapper import JSON, POST, SPARQLWrapper
from tqdm.auto import tqdm

from scribe_data.utils import (
    check_and_return_command_line_args,
)

# total_nouns = query_total_nouns()
# batch_size = 10
# num_iterations = math.ceil(total_nouns / batch_size)

SCRIBE_DATA_SRC_PATH = "src/scribe_data"
PATH_TO_LANGUAGE_EXTRACTION_FILES = f"{SCRIBE_DATA_SRC_PATH}/language_data_extraction"
PATH_TO_UPDATE_FILES = f"{SCRIBE_DATA_SRC_PATH}/load/update_files"

# Set SPARQLWrapper query conditions.
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)
sparql.setMethod(POST)

with open(f"{PATH_TO_UPDATE_FILES}/total_data.json", encoding="utf-8") as f:
    current_data = json.load(f)

current_languages = list(current_data.keys())
current_word_types = ["nouns", "verbs", "prepositions"]

# Check whether arguments have been passed to only update a subset of the data.
languages, word_types = check_and_return_command_line_args(
    all_args=sys.argv,
    first_args_check=current_languages,
    second_args_check=current_word_types,
)

# Assign current_languages and current_word_types if no arguments have been passed.
languages_update = []
languages_update = current_languages if languages is None else languages

word_types_update = []
word_types_update = current_word_types if word_types is None else word_types

# Derive directory files and language subdirectories for potential queries.
language_data_extraction_files = []

for path, _, files in os.walk(PATH_TO_LANGUAGE_EXTRACTION_FILES):
    language_data_extraction_files.extend(os.path.join(path, name) for name in files)

language_directories = [
    d
    for d in os.listdir(PATH_TO_LANGUAGE_EXTRACTION_FILES)
    if os.path.isdir(f"{PATH_TO_LANGUAGE_EXTRACTION_FILES}/{d}")
]

# Check to see if the language has all zeroes for its data, meaning it's new.
new_language_list = []
for lang in languages_update:
    check_current_data = [current_data[lang][k] for k in current_data[lang].keys()]
    if len(set(check_current_data)) == 1 and check_current_data[0] == 0:
        new_language_list.append(lang)

# Derive queries to be ran.
possible_queries = []
for d in language_directories:
    possible_queries.extend(
        f"{PATH_TO_LANGUAGE_EXTRACTION_FILES}/{d}/{target_type}"
        for target_type in word_types_update
        if f"{PATH_TO_LANGUAGE_EXTRACTION_FILES}/{d}/{target_type}"
        in [
            e[: len(f"{PATH_TO_LANGUAGE_EXTRACTION_FILES}/{d}/{target_type}")]
            for e in language_data_extraction_files
        ]
    )

queries_to_run_lists = [
    [
        q
        for q in possible_queries
        if q.split(PATH_TO_LANGUAGE_EXTRACTION_FILES + "/")[1].split("/")[0]
        in languages_update
    ]
    for lang in languages_update
]

queries_to_run = list({q for sub in queries_to_run_lists for q in sub})
queries_to_run = sorted(queries_to_run)

# Run queries and format data.
data_added_dict = {}
for q in tqdm(
    queries_to_run,
    desc="Data updated",
    unit="process",
):
    lang = q.split("/")[-2]
    target_type = q.split("/")[-1]
    query_name = f"query_{target_type}.sparql"
    query_path = f"{q}/{query_name}"

    if not os.path.exists(query_path):
        # There are multiple queries for a given target_type, so start by running the first.
        query_path = query_path[: -len(".sparql")] + "_1" + ".sparql"

    print(f"Querying and formatting {lang} {target_type}")
    # First format the lines into a multi-line string and then pass this to SPARQLWrapper.
    with open(query_path, encoding="utf-8") as file:
        query_lines = file.readlines()
    sparql.setQuery("".join(query_lines))

    results = None
    try:
        results = sparql.query().convert()
    except HTTPError as err:
        print(f"HTTPError with {query_path}: {err}")

    if results is None:
        print(f"Nothing returned by the WDQS server for {query_path}")

        # Allow for a query to be reran up to two times.
        if queries_to_run.count(q) < 3:
            queries_to_run.append(q)

    else:
        # Subset the returned JSON and the individual results before saving.
        query_results = results["results"]["bindings"]

        results_formatted = []
        for r in query_results:  # query_results is also a list
            r_dict = {k: r[k]["value"] for k in r.keys()}

            results_formatted.append(r_dict)

        with open(
            f"{PATH_TO_LANGUAGE_EXTRACTION_FILES}/{lang}/{target_type}/{target_type}_queried.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(results_formatted, f, ensure_ascii=False, indent=0)

        if "_1" in query_path:
            # Note: Only the first query was ran, so we need to run the second and append the json.
            for suffix in ["_2", "_3"]:
                query_path = query_path.replace("_1", suffix).replace("_2", suffix)

                if os.path.exists(query_path):
                    with open(query_path, encoding="utf-8") as file:
                        query_lines = file.readlines()
                        sparql.setQuery("".join(query_lines))

                        results = None
                        try:
                            results = sparql.query().convert()
                        except HTTPError as err:
                            print(f"HTTPError with {query_path}: {err}")

                        if results is None:
                            print(
                                f"Nothing returned by the WDQS server for {query_path}"
                            )

                            # Allow for a query to be reran up to two times.
                            if queries_to_run.count(q) < 3:
                                queries_to_run.append(q)

                        else:
                            # Subset the returned JSON and the individual results before saving.
                            query_results = results["results"]["bindings"]

                            # Note: Don't rewrite results_formatted as we want to extend the json and combine in formatting.
                            for r in query_results:  # query_results is also a list
                                r_dict = {k: r[k]["value"] for k in r.keys()}

                                # Note: The following is so we have a breakdown of queries for German later.
                                # Note: We need auxiliary verbs to be present as we loop to get both sein and haben forms.
                                if lang == "German":
                                    r_dict_keys = list(r_dict.keys())
                                    if "auxiliaryVerb" not in r_dict_keys:
                                        r_dict["auxiliaryVerb"] = ""

                                results_formatted.append(r_dict)

                            with open(
                                f"{PATH_TO_LANGUAGE_EXTRACTION_FILES}/{lang}/{target_type}/{target_type}_queried.json",
                                "w",
                                encoding="utf-8",
                            ) as f:
                                json.dump(
                                    results_formatted, f, ensure_ascii=False, indent=0
                                )

        # Call the corresponding formatting file and update data changes.
        os.system(
            f"python {PATH_TO_LANGUAGE_EXTRACTION_FILES}/{lang}/{target_type}/format_{target_type}.py"
        )

        # Check current data within formatted data directories.
        with open(
            f"{os.path.dirname(sys.path[0]).split('scribe_data')[0]}/../scribe_data_json_export/{lang.capitalize()}/{target_type}.json",
            encoding="utf-8",
        ) as json_file:
            new_keyboard_data = json.load(json_file)

        if lang not in data_added_dict:
            data_added_dict[lang] = {}
        data_added_dict[lang][target_type] = (
            len(new_keyboard_data) - current_data[lang][target_type]
        )

        current_data[lang][target_type] = len(new_keyboard_data)

# Update total_data.json.
with open(f"{PATH_TO_UPDATE_FILES}/total_data.json", "w", encoding="utf-8") as f:
    json.dump(current_data, f, ensure_ascii=False, indent=0)


# Update data_table.txt
current_data_df = pd.DataFrame(
    index=sorted(list(current_data.keys())),
    columns=["nouns", "verbs", "translations", "prepositions"],
)
for lang, wt in itertools.product(
    list(current_data_df.index), list(current_data_df.columns)
):
    if wt in current_data[lang].keys():
        current_data_df.loc[lang, wt] = f"{current_data[lang][wt]:,}"
    elif wt == "translations":
        current_data_df.loc[lang, wt] = f"{67652:,}"

current_data_df.index.name = "Languages"
current_data_df.columns = [c.capitalize() for c in current_data_df.columns]

# Get the current emoji data so that it can be appended at the end of the table.
current_emoji_data_strings = []
with open(f"{PATH_TO_UPDATE_FILES}/data_table.txt", encoding="utf-8") as f:
    old_table_values = f.read()

for line in old_table_values.splitlines():
    current_emoji_data_strings.append(line.split("|")[-2] + "|")

# Write the new values to the table, which overwrites the emoji keyword values.
with open(f"{PATH_TO_UPDATE_FILES}/data_table.txt", "w+", encoding="utf-8") as f:
    table_string = str(current_data_df.to_markdown()).replace(" nan ", "   - ")
    # Right justify the data and left justify the language indexes.
    table_string = (
        table_string.replace("-|-", ":|-")
        .replace("-|:", ":|-")
        .replace(":|-", "-|-", 1)
    )
    f.writelines(table_string)

# Get the new table values and then rewrite the file with the full table.
new_table_value_strings = []
with open(f"{PATH_TO_UPDATE_FILES}/data_table.txt", encoding="utf-8") as f:
    new_table_values = f.read()

for line in new_table_values.splitlines():
    # Replace headers while translation is still in beta and always for prepositions to annotate missing values.
    # Note: Spaces replaced to maintain table spacing.
    line = line.replace("Translations  ", "Translations\*")
    line = line.replace("Prepositions ", "Prepositions†")
    new_table_value_strings.append(line)

with open(f"{PATH_TO_UPDATE_FILES}/data_table.txt", "w+", encoding="utf-8") as f:
    for i in range(len(new_table_value_strings)):
        f.writelines(new_table_value_strings[i] + current_emoji_data_strings[i] + "\n")

# Update data_updates.txt.
data_added_string = ""
language_keys = sorted(list(data_added_dict.keys()))

# Check if all data added values are 0 and remove if so.
for lang in language_keys:
    if all(v <= 0 for v in data_added_dict[lang].values()):
        language_keys.remove(lang)

for lang in language_keys:
    if lang == language_keys[0]:
        data_added_string += (
            f"- {lang} (New):" if lang in new_language_list else f"- {lang}:"
        )
    else:
        data_added_string += (
            f"\n- {lang} (New):" if lang in new_language_list else f"\n- {lang}:"
        )

    for wt in word_types_update:
        if wt in data_added_dict[lang].keys():
            if data_added_dict[lang][wt] <= 0:
                pass
            elif data_added_dict[lang][wt] == 1:  # remove the s for label
                data_added_string += f" {data_added_dict[lang][wt]} {wt[:-1]},"
            else:
                data_added_string += f" {data_added_dict[lang][wt]:,} {wt},"

    data_added_string = data_added_string[:-1]  # remove the last comma

with open(f"{PATH_TO_UPDATE_FILES}/data_updates.txt", "w+", encoding="utf-8") as f:
    f.writelines(data_added_string)
