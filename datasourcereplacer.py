#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# basemap.py
# This script automates data source updates for unique feature classes in a set of MXDs.
#
# C:\Python27\ArcGIS10.4\python.exe featureclassreplacer.py
#
# ---------------------------------------------------------------------------
import os, glob, shutil, datetime, timeit, zipfile, arcpy
from zipfile import *

title ='''

     _______  _______  _______  _______    __   __  _______  _______
    |  _    ||   _   ||       ||       |  |  |_|  ||   _   ||       |
    | |_|   ||  |_|  ||  _____||    ___|  |       ||  |_|  ||    _  |
    |       ||       || |_____ |   |___   |       ||       ||   |_| |
    |  _   | |       ||_____  ||    ___|  |       ||       ||    ___|
    | |_|   ||   _   | _____| ||   |___   | ||_|| ||   _   ||   |
    |_______||__| |__||_______||_______|  |_|   |_||__| |__||___|'''
root = os.path.abspath(os.path.curdir)
mxds = {
   "list":[
      {
         "mxd":"NYCDOTBaseMap_Dark.mxd",
      },
      {
         "file":"nybb_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nybb_",
         "name":"Borough_Boundary"
      },
      {
         "file":"nycc_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nycc_",
         "name":"City_Council_Disrtricts"
      },
      {
         "file":"nycd_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nycd_",
         "name":"Community_Districts"
      },
      {
         "file":"nycg_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nycg_",
         "name":"US_Congressional_Districts"
      },
      {
         "file":"nyed_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyed_",
         "name":"Election_Districts"
      },
      {
         "file":"nyfb_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyfb_",
         "name":"Fire_Battalions"
      },
      {
         "file":"nyfc_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyfc_",
         "name":"Fire_Companies"
      },
      {
         "file":"nyfd_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyfd_",
         "name":"Fire_Divisions"
      },
      {
         "file":"nyha_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyha_",
         "name":"Health_Area"
      },
      {
         "file":"nymc_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nymc_",
         "name":"Municipal_Court_Districts"
      },
      {
         "file":"nypp_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nypp_",
         "name":"Police_Precincts"
      },
      {
         "file":"nysd_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nysd_",
         "name":"School_Districts"
      },
      {
         "file":"nyss_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyss_",
         "name":"State_Senate_Districts"
      },
      {
         "file":"nycb2000_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nycb2000_",
         "name":"Census_Blocks_2000"
      },
      {
         "file":"nycb2010_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nycb2010_",
         "name":"Census_Blocks_2010"
      },
      {
         "file":"nyct2000_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyct2000_",
         "name":"Census_Tracts_2000"
      },
      {
         "file":"nyct2010_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyct2010_",
         "name":"Census_Tracks_2010"
      },
      {
         "file":"nyclion_",
         "url":"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyclion_",
         "name":"LION"
      }
   ]
}

root = os.path.abspath(os.path.curdir)
dynamic_path = os.path.join(root, "dynamic")
static_path = os.path.join(root, "static")

def manageDirectories():
    #start trying to devlop this function
    print("Step 1: Create two folders labeled dynamic and static. If these folder already exist replace them. Inside of the static folder make two folders labled WGS84 and NAD83\n")

    if os.path.exists(dynamic_path): shutil.rmtree(dynamic_path)

    if os.path.exists(static_path): shutil.rmtree(static_path)

    os.mkdir(dynamic_path)
    os.mkdir(static_path)
    os.mkdir(os.path.join(static_path, "WGS84"))
    os.mkdir(os.path.join(static_path, "NAD83"))

def copyTemplates():
    print("Step 2: Copy the mxds from the template folder into the folders labeled dynamic, WGS84, and NAD83. Rename the mxds with a the latest version of lion like 17B\n")

    template_path = os.path.join(root, "templates")

    for x in os.listdir(template_path):
        shutil.copy(os.path.join(template_path, x), os.path.join(dynamic_path, x))
        shutil.copy(os.path.join(template_path, x), os.path.join(static_path, x))

def updateFeatureClasses(fc_id, fc_ver):
    print("Step 3. For each mxd in the dynamic folder replace the source of each lion based layers with updated version on SDE (Borough Boundary and various LION files.)\n")
    newest_fc = fc_id + '_' + fc_ver
    print "replacing, all %s with version number %s" %(fc_id, fc_ver)

    for file in os.listdir(static_path):
        if file.endswith(".mxd"):
            mxd_file = os.path.join(static_path, file)
            mxd = arcpy.mapping.MapDocument(mxd_file)
            for lyr in arcpy.mapping.ListLayers(mxd):
                if lyr.supports("DATASOURCE"):
                    if fc_id in lyr.datasetName:
                        lyr.replaceDataSource(lyr.workspacePath, "SDE_WORKSPACE", newest_fc , False)
                        print lyr.name, 'with' ,newest_fc, 'in', mxd_file
            mxd.save()

#def create_fgdb():
#    print("Step 4: Create a file gdb, label it with a Export all the unique feature classes used by the mxds to a file gdb.")

def main():
    manageDirectories()
    copyTemplates()
    fc_to_id = {
       "LION" : "GISGRID.GISADMIN.LION",
       "BUILDING_FOOTPRINT" : "GISGRID.GISADMIN.BUILDING_FOOTPRINT",
       "NYAD" : "GISGRID.GISADMIN.nyad",
       "NYBB" : "GISGRID.GISADMIN.nybb",
       "TAMED_LION" : "GISGRID.GISADMIN.TAMED_LION",
       "HYDROGRAPHY" : "GISGRID.GISADMIN.HYDROGRAPHY",
       "NY_COUNTIES" : "gisgrid.GISADMIN.NY_COUNTIES",
       "CT_COUNTY" : "gisgrid.GISADMIN.CT_COUNTY",
       "NJ_COUNTY" : "gisgrid.GISADMIN.NJ_COUNTY",
       "NYC_COUNTY_BORDERS" : "GISGRID.GISADMIN.NYC_County_Borders",
       "OPEN_SPACE_NO_PARK" : "GISGRID.GISADMIN.OPEN_SPACE_NO_PARK",
       "NEIGHBORHOOD_POINTS" : "GISGRID.GISADMIN.Neighborhood_Points",
       "WATER" : "GISGRID.GISADMIN.WATER",
       "HYDROGRAPHY_LINES" : "gisgrid.GISADMIN.HYDROGRAPHY_LINES",
       "PARK" : "GISGRID.GISADMIN.PARK",
       "AIRPORT_POINTS" : "GISGRID.GISADMIN.Airport_Points",
       "PAVEMENT_EDGE" : "GISGRID.GISADMIN.PAVEMENT_EDGE",
       "ROADBED" : "GISGRID.GISADMIN.ROADBED",
       "JAMACIA_BAY_POLYGON" : "GISGRID.GISADMIN.Jamacia_Bay_Polygon"
    }

    replace_fc = raw_input("Which feature class would you like to replace?: ").upper()
    while replace_fc not in fc_to_id.keys():
        print "%s not in list, try %s" %(replace_fc, ', '.join(fc_to_id.keys()))
    replace_ver = raw_input("What is the most recent version?: ")
    updateFeatureClasses(fc_to_id[replace_fc] , replace_ver)
    #updateFeatureClasses("GISGRID.GISADMIN.LION", "17C")


if __name__ == '__main__':
     main()
