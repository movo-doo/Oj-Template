# Oj — Observatory Jukebox Image Collector

## Overview

Oj (Observatory Jukebox) is a lightweight system for organizing, viewing, and categorizing personal astronomical images.

It allows images to be:
- Stored locally or served via GitHub Pages
- Automatically grouped into categories
- Filtered by astronomical catalog systems (Messier, NGC, IC, Caldwell, etc.)
- Enhanced with optional metadata from astronomical catalogs

---

## Core Idea

Images are not manually sorted into folders.

Instead, they are:
- Named consistently
- Parsed automatically
- Categorized dynamically using rules

This allows a single image to appear in multiple categories without duplication.

---

## Image Workflow

### 1. Collect Images
Gather astronomical images (bulk or individual).

Supported formats:

.jpg, .jpeg, .png, .gif, .webp

Optional: crop, resize, or annotate before adding.

---

### 2. Naming Convention (IMPORTANT)

Image filenames determine how they are categorized.

Examples:

#### Messier + Cluster + Globular

M 10 Clusters_Globular 20250314.jpg


#### Caldwell + NGC + Planetary Nebula

C 15 NGC 6826 Planetary Nebula.jpg


#### Lunar with metadata encoding

Lunar 11.jpg


#### NGC + Supernova association

NGC3913 SN2016dix.gif


Each filename can drive multiple category associations.

---

## Category System

Categories are defined in:


categories_rules.json


This file determines:
- How filenames are parsed
- Which categories are assigned
- What appears in the UI filter buttons
- What metadata appears in the image info popup

You may:
- Modify existing rules
- Add custom categories
- Remove unused categories

---

## Astronomical Metadata (NGC / IC)

Enhanced object data is available for NGC and IC objects using:


ic_ngc_index.csv


This dataset is derived from:
:contentReference[oaicite:0]{index=0} by Mattia Verga

It integrates data from multiple astronomical sources including:
- SIMBAD
- HyperLeda
- Other catalog archives

### Example enriched image entry:

```json
{
  "file": "NGC 891 Silver Sliver.jpg",
  "categories": ["NGC"],
  "info": {
    "identifiers": {
      "NGC": "NGC 891"
    },
    "extended_info": {
      "Type": "G",
      "Coordinates": "02:22:33.41 +42:20:56.9",
      "Constellation": "Andromeda",
      "Axis": "13.03 3.03",
      "PosAng": "22",
      "V-Mag": "10.01",
      "SurfBr": "24.17",
      "Hubble": "Sb"
    }
  }
}

Data Generation Pipeline

The system is fully automated.

Image Index Creation
generate_json.py

Builds:

images.json
GitHub Automation

On image upload or changes:

build-images-collection_orig.yml

This GitHub Action:

Spins up a Python environment
Runs generate_json.py
Updates images.json automatically
Frontend System

The web interface is driven by:

index.html → UI layout
script.js → logic + filtering + rendering
style.css → styling

All displayed data comes from:

images.json
Optional Utilities

Included Python tools:

extract_info.py
extract_ic_ngc_info.py

These are optional utilities for:

Bulk metadata updates
Backfilling catalog information into existing images

Basic Python knowledge is recommended if using them.

File Management Notes
Images are stored in:
/images
Previously processed images can be renamed, but:
You must update images.json manually
You may need to update categories_rules.json if categories change
Local Development

Run a local server:

http://localhost:8000/

Or replace localhost with your local machine IP for network access.

GitHub Deployment

## Public Access (GitHub Pages)

Your site will be available at:

https://<your-github-username>.github.io/<repository-name>/

---

### Important Note

If you rename your repository, the GitHub Pages URL changes automatically.

Also ensure that any **hardcoded absolute paths** in `index.html` match your repository name, for example:

https://<your-github-username>.github.io/<repository-name>/images/your-image.jpg


Dependencies

Python standard libraries used:

os
json
re
pandas
Design Philosophy

Oj is designed to be:

Lightweight
File-driven (no database)
Extensible via naming conventions
Fully automatable via GitHub Actions
Maintenance Notes

This system is actively evolving.
You are encouraged to:

Modify rules
Extend categories
Improve automation scripts
Iterate on naming conventions

Always commit changes locally before pushing to GitHub.

