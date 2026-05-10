Welcome to AstroTurf Image Collector

Purpose: to have a easy access to user friendly online or local collection of your personal astronomical images.

Images are displayed and sorted by catalogue number in what ever object type categories you wish to access them in.

There is no magic here as is described in the processes below.

Workflow: 

Gather your images either in bulk or one at a time. Crop, resize and/or label them if you want.
# Supported image extensions are as follows
".jpg", ".jpeg", ".png", ".gif", ".webp"

Provide a descriptive filename to each image.

Examples   

C 15 NGC 6826 Planetary Nebula.jpg
Allows for Caldwell and NGC catelog grouping as well as Nebula and even Planetary Nebula

Lunar 11.jpg
Allows for Lunar image grouping as well as ordering since a rounded off percent illumination was added to filename

M 10 Clusters_Globular  20250314.JPG
Allows for Messier grouping as well as Cluster and even Globular Clusters grouping

NGC3913 SN2016dix.gif
Allos for NGC catalog and Supernova grouping of same image.  Note Image is not duplicated, it just appears in both Catalogs

The more information you add in a consistent manner the more categories you can slice and dice your images.

Rules for what qualifies for grouping determination is in the categories_rules.json file.  Out of the box rules are provided however you can write new rules if you so desire.

So the Rules determine the categories which also in turn denote information that may appear in the Information Box popup associated with each image.

Additional enhanced object information can also be displayed if you have an NGC and/or IC categories as extracted from the file ic_ngc_index.csv   
This file is a personally curated version from # Credits: Mattia Verga https://github.com/mattiaverga/OpenNGC for ic_ngc_index.csv raw data which is an extensive extraction from multiple database such as HyperLeda, SIMBAD and others.
Thank you Mattia Verga for this contribution.

Some of the enhanced info available in this file is in the extended_info snippet of the json file. 

,
    {
      "file": "NGC 891 Silver Sliver.jpg",
      "categories": [
        "NGC"
      ],
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

You can enhance this file manually or add columns into ic_ngc_index.csv.
Note this csv file has almost 14,000 rows of IC and NGC cataloged objects. 

Specific Images are displayed on the web page of your choice based on which Category Buttons are available.  Again those categories are defined in file categories_rules.json

Images are stored in the images subfolder associated with this code base.

The file image.json is whats created from generate_json.py which can be automatically run from github when a new image is added or modifications to files are created. This is driven by build-images-collection_orig.yml on github. More detail to come on this.

Script.js and stype.css is for web page display particulars.

I have included files extract_info.py and extract_ic_ngc_info.py in the event you want to add any information identifiers in a bulk fashion to the images.json file after you have already processed files previously.

Previously processed image filenames can be changed at will however you must manually modify its entry in the iimages.json file in order for it to show.  In addition the categories_rules.json file needs to have any new categories added after the fact.
To review or modify any json files, i recommend either a basic text editor like notepad or a json editor.

index.html will drive the frontend UI. 

If on a private network an example of a url would be 
http://localhost:8000/   
or you can replace "localhost" with the ip address of the computer running a web service.

To access from github the following url should work.
https://{Your github account}.github.io/astroturf/index.html

Only python modules utilized in this project are as follows:  os, json, re, pandas

You can download this repository to your local machine, install python and save the astroturf directory and files in your personal folder.


Enhancements, consolidation and fixes may be made to this codebase anytime in the future.