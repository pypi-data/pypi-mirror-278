"""
Format Nouns
------------

Formats the nouns queried from Wikidata using query_nouns.sparql.
"""

# pylint: disable=invalid-name

import collections
import json
import os
import sys

LANGUAGE = "German"
PATH_TO_SCRIBE_ORG = os.path.dirname(sys.path[0]).split("Scribe-Data")[0]
PATH_TO_SCRIBE_DATA_SRC = f"{PATH_TO_SCRIBE_ORG}Scribe-Data/src"
sys.path.insert(0, PATH_TO_SCRIBE_DATA_SRC)

from scribe_data.load.update_utils import get_path_from_et_dir

file_path = sys.argv[0]

update_data_in_use = False  # check if update_data.py is being used
if f"{LANGUAGE}/nouns/" not in file_path:
    with open("nouns_queried.json", encoding="utf-8") as f:
        nouns_list = json.load(f)
else:
    update_data_in_use = True
    with open(f"./{LANGUAGE}/nouns/nouns_queried.json", encoding="utf-8") as f:
        nouns_list = json.load(f)


def map_genders(wikidata_gender):
    """
    Maps those genders from Wikidata to succinct versions.

    Parameters
    ----------
        wikidata_gender : str
            The gender of the noun that was queried from WikiData
    """
    if wikidata_gender in ["masculine", "Q499327"]:
        return "M"
    elif wikidata_gender in ["feminine", "Q1775415"]:
        return "F"
    elif wikidata_gender in ["neuter", "Q1775461"]:
        return "N"
    else:
        return ""  # nouns could have a gender that is not valid as an attribute


def order_annotations(annotation):
    """
    Standardizes the annotations that are presented to users where more than one is applicable.

    Parameters
    ----------
        annotation : str
            The annotation to be returned to the user in the command bar.
    """
    single_annotations = ["F", "M", "N", "PL"]
    if annotation in single_annotations:
        return annotation

    annotation_split = sorted([a for a in set(annotation.split("/")) if a != ""])

    return "/".join(annotation_split)


nouns_formatted = {}

for noun_vals in nouns_list:
    if "singular" in noun_vals.keys():
        if noun_vals["singular"] not in nouns_formatted:
            # Get plural and gender.
            if "plural" in noun_vals.keys() and "gender" in noun_vals.keys():
                nouns_formatted[noun_vals["singular"]] = {
                    "plural": noun_vals["plural"],
                    "form": map_genders(noun_vals["gender"]),
                }

                # Assign plural as a new entry after checking if it's its own plural.
                if noun_vals["plural"] not in nouns_formatted:
                    if noun_vals["singular"] != noun_vals["plural"]:
                        nouns_formatted[noun_vals["plural"]] = {
                            "plural": "isPlural",
                            "form": "PL",
                        }

                    else:
                        nouns_formatted[noun_vals["plural"]] = {
                            "plural": noun_vals["plural"],
                            "form": "PL",
                        }
                else:
                    # Mark plural as a possible form if it isn't already.
                    if (
                        "PL" not in nouns_formatted[noun_vals["plural"]]["form"]
                        and nouns_formatted[noun_vals["plural"]]["form"] != ""
                    ):
                        nouns_formatted[noun_vals["plural"]]["form"] = (
                            nouns_formatted[noun_vals["plural"]]["form"] + "/PL"
                        )

                    elif nouns_formatted[noun_vals["plural"]]["form"] == "":
                        nouns_formatted[noun_vals["plural"]]["form"] = "PL"

                    # Assign itself as a plural if possible (maybe wasn't for prior versions).
                    if noun_vals["singular"] == noun_vals["plural"]:
                        nouns_formatted[noun_vals["plural"]]["plural"] = noun_vals[
                            "plural"
                        ]

            # Get plural and assign it as a noun.
            elif "plural" in noun_vals.keys() and "gender" not in noun_vals.keys():
                nouns_formatted[noun_vals["singular"]] = {
                    "plural": noun_vals["plural"],
                    "form": "",
                }

                # Assign plural as a new entry after checking if it's its own plural.
                if noun_vals["plural"] not in nouns_formatted:
                    if noun_vals["singular"] != noun_vals["plural"]:
                        nouns_formatted[noun_vals["plural"]] = {
                            "plural": "isPlural",
                            "form": "PL",
                        }

                    else:
                        nouns_formatted[noun_vals["plural"]] = {
                            "plural": noun_vals["plural"],
                            "form": "PL",
                        }
                else:
                    # Mark plural as a possible form if it isn't already.
                    if (
                        "PL" not in nouns_formatted[noun_vals["plural"]]["form"]
                        and nouns_formatted[noun_vals["plural"]]["form"] != ""
                    ):
                        nouns_formatted[noun_vals["plural"]]["form"] = (
                            nouns_formatted[noun_vals["plural"]]["form"] + "/PL"
                        )

                    elif nouns_formatted[noun_vals["plural"]]["form"] == "":
                        nouns_formatted[noun_vals["plural"]]["form"] = "PL"

                    # Assign itself as a plural if possible (maybe wasn't for prior versions).
                    if noun_vals["singular"] == noun_vals["plural"]:
                        nouns_formatted[noun_vals["plural"]]["plural"] = noun_vals[
                            "plural"
                        ]

            elif "plural" not in noun_vals.keys() and "gender" in noun_vals.keys():
                nouns_formatted[noun_vals["singular"]] = {
                    "plural": "noPlural",
                    "form": map_genders(noun_vals["gender"]),
                }

        # The singular already exists - there might be another gender of it for a different meaning.
        else:
            if (
                "gender" in noun_vals.keys()
                and nouns_formatted[noun_vals["singular"]]["form"]
                != noun_vals["gender"]
            ):
                nouns_formatted[noun_vals["singular"]]["form"] += "/" + map_genders(
                    noun_vals["gender"]
                )

    elif "plural" in noun_vals.keys():
        if noun_vals["plural"] not in nouns_formatted:
            nouns_formatted[noun_vals["plural"]] = {
                "plural": "isPlural",
                "form": "PL",
            }
        else:
            # Mark plural as a possible form if it isn't already.
            if (
                "PL" not in nouns_formatted[noun_vals["plural"]]["form"]
                and nouns_formatted[noun_vals["plural"]]["form"] != ""
            ):
                nouns_formatted[noun_vals["plural"]]["form"] = (
                    nouns_formatted[noun_vals["plural"]]["form"] + "/PL"
                )

            elif nouns_formatted[noun_vals["plural"]]["form"] == "":
                nouns_formatted[noun_vals["plural"]]["form"] = "PL"

for k in nouns_formatted:
    nouns_formatted[k]["form"] = order_annotations(nouns_formatted[k]["form"])

nouns_formatted = collections.OrderedDict(sorted(nouns_formatted.items()))

org_path = get_path_from_et_dir()
export_path = "../formatted_data/nouns.json"
if update_data_in_use:
    export_path = f"{org_path}/Scribe-Data/src/scribe_data/extract_transform/{LANGUAGE}/formatted_data/nouns.json"

with open(export_path, "w", encoding="utf-8",) as file:
    json.dump(nouns_formatted, file, ensure_ascii=False, indent=0)

print(f"Wrote file nouns.json with {len(nouns_formatted)} nouns.")
