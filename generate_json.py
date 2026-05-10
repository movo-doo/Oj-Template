import os
import json
import re
import pandas as pd

IMAGE_FOLDER = "images"
CATEGORIES_FILE = "categories_rules.json"
JSON_FILE = "images.json"

# Credits: Mattia Verga https://github.com/mattiaverga/OpenNGC for ic_ngc_index.csv raw data
IC_NGC_FILE = "ic_ngc_index.csv"


# Supported image extensions
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")


def save_images(data, file_path):

    tmp_path = file_path + ".tmp"

    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    os.replace(tmp_path, file_path)


def populate_extended_info(record, extended_info_df):

    if extended_info_df is None:
        return record

    info = record.get("info")
    if not info:
        return record

    identifiers = info.get("identifiers")
    if not identifiers:
        return record

    lookup_key = None

    if "NGC" in identifiers:
        lookup_key = identifiers["NGC"]

    elif "IC" in identifiers:
        lookup_key = identifiers["IC"]

    if not lookup_key:
        return record

    lookup_key = lookup_key.strip()

    if lookup_key not in extended_info_df.index:
        return record

    row = extended_info_df.loc[lookup_key]

    extended_info = {}

    for col_name, value in row.items():

        if pd.notna(value):

            value = str(value).strip()

            if value:
                extended_info[col_name] = value

    if extended_info:

        info["extended_info"] = extended_info

    return record


def normalize_identifier(match):

    identifier = match.group(0)

    # unify separators first
    identifier = identifier.replace("_", " ")

    # collapse multiple whitespace
    identifier = re.sub(r"\s+", " ", identifier)

    identifier = identifier.strip()

    # uppercase alphabetic chars
    identifier = identifier.upper()

    # insert missing space before digits
    identifier = re.sub(
        r"([A-Z]+)\s*(\d+)",
        r"\1 \2",
        identifier
    )

    return identifier


def populate_identifiers(data, categories):

    # Fast lookup:
    category_lookup = {
        category["name"]: category["patterns"]
        for category in categories
    }

    filename = data["file"]

    identifiers = {}

    for category_name in data["categories"]:

        patterns = category_lookup.get(category_name, [])

        for pattern in patterns:

            # Only catalog-style patterns
            if r"\d" not in pattern.pattern:
                continue

            match = pattern.search(filename)

            if not match:
                continue

            identifier = normalize_identifier(match)

            # Store by full catalog name
            identifiers[category_name] = identifier

            # One identifier per category
            break

    if identifiers:

        data["info"] = data.get("info", {})
        data["info"]["identifiers"] = identifiers

    return data


def classify_filename(filename, categories_rules):
    categories = []

    print(f"\nChecking file: {filename}")

    for category in categories_rules:
        name = category["name"]

        for pattern in category["patterns"]:
            if pattern.search(filename):  # assumes precompiled regex
                print(f"  MATCH → {name} using {pattern.pattern}")
                if name not in categories:
                    categories.append(name)
                break  # stop checking patterns for this category

    if not categories:
        categories.append("Uncategorized")

    return {
        "file": filename,
        "categories": categories
    }

def process_new_images(new_files, categories_rules, data, extended_info_df):

    images = data.setdefault("images", [])

    uncategorized_count = 0

    for filename in new_files:
        record = classify_filename(filename, categories_rules)
        record = populate_identifiers(record, categories_rules)
        record = populate_extended_info(record, extended_info_df)

        if "Uncategorized" in record["categories"]:
            uncategorized_count += 1
        images.append(record)

    return data, uncategorized_count


def find_new_images(image_folder, existing_files):
    new_files = []

    for filename in os.listdir(image_folder):

        original = filename.strip()

        if not original.lower().endswith(VALID_EXTENSIONS):
            continue

        if original not in existing_files:
            new_files.append(original)

    return new_files

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
 
def load_categories(categories_file):
    if not os.path.exists(categories_file):
        return []

    with open(categories_file, "r") as f:
        data = json.load(f)

    categories = []
    for cat in data.get("categories", []):
        name = cat.get("name")
        patterns = cat.get("patterns", [])

        if name and patterns:
            compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

            categories.append({
                "name": name,
                "patterns": compiled_patterns
            })

    return categories


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

categories = load_categories(CATEGORIES_FILE)
# print(f'categories : {categories}')

data = load_images(JSON_FILE)

existing_files = {item["file"].strip() for item in data.get("images", [])}

new_files = find_new_images(IMAGE_FOLDER, existing_files)
print(f'new_files : {new_files}')

new_data, uncategorized_count = process_new_images(new_files, categories, data, extended_info_df)

# print("new_data:", json.dumps(new_data, indent=2))

save_images(new_data, JSON_FILE)

print(
    f'Done updating json_images.json with {len(new_data["images"])} images '
    f'({uncategorized_count} uncategorized)'
)