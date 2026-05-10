import os
import json
import re

CATEGORIES_FILE = "categories_rules.json"
JSON_FILE = "images.json"


def save_images(data, file_path):

    tmp_path = file_path + ".tmp"

    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    os.replace(tmp_path, file_path)


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

    for image in data["images"]:

        filename = image["file"]

        # Changed from [] to {}
        identifiers = {}

        for category_name in image["categories"]:

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

            image["info"] = image.get("info", {})
            image["info"]["identifiers"] = identifiers

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


categories = load_categories(CATEGORIES_FILE)
# print(f'categories : {categories}')

data = load_images(JSON_FILE)
# print(f'data : {data}') 


record = populate_identifiers(data, categories)
# print("record:", json.dumps(record, indent=2))

save_images(record, JSON_FILE)