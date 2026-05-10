import os
import json
import re
import pandas as pd

# Credits: Mattia Verga https://github.com/mattiaverga/OpenNGC for ic_ngc_index.csv raw data
IC_NGC_FILE = "ic_ngc_index.csv"
JSON_FILE = "images.json"


def save_images(data, file_path):

    tmp_path = file_path + ".tmp"

    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    os.replace(tmp_path, file_path)


def populate_extended_info(data, extended_info_df):

    if extended_info_df is None:
        return data

    for record in data.get("images", []):

        info = record.get("info")
        if not info:
            continue

        identifiers = info.get("identifiers")
        if not identifiers:
            continue

        lookup_key = None

        if "NGC" in identifiers:
            lookup_key = identifiers["NGC"]

        elif "IC" in identifiers:
            lookup_key = identifiers["IC"]

        if not lookup_key:
            continue

        lookup_key = lookup_key.strip()

        if lookup_key not in extended_info_df.index:
            continue

        row = extended_info_df.loc[lookup_key]

        extended_info = {}

        for col_name, value in row.items():

            if pd.notna(value):

                value = str(value).strip()

                if value:
                    extended_info[col_name] = value

        if extended_info:

            info["extended_info"] = extended_info

    return data


def load_images(json_file):
    if not os.path.exists(json_file):
        return {"images": []}

    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return {"images": []}

    # OLD FORMAT SUPPORT
    if isinstance(data, list):
        return {"images": data}

    if not isinstance(data, dict):
        return {"images": []}

    if "images" not in data:
        data["images"] = []

    return data


def load_extended_info(info_file):

    if not os.path.exists(info_file):
        return None

    df = pd.read_csv(
        info_file,
        dtype=str,
        encoding="cp1252"
    )

    df = df.fillna("")

    key_column = df.columns[0]

    df[key_column] = df[key_column].str.strip()

    df = df.set_index(key_column)

    return df


extended_info_df = load_extended_info(IC_NGC_FILE)

data = load_images(JSON_FILE)

record = populate_extended_info(data, extended_info_df)

# print("record:", json.dumps(record, indent=2))

save_images(record, JSON_FILE)