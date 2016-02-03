#Script for Lab 1
#By Thomas Ryan
#For Geog 458

#Import modules
import arcpy
import sys

#Set workspace and grab input files
arcpy.env.workspace = r"C:\Users\Thomas\Desktop\Lab 1 Geog 458\"
input_shapefile = ("saep_bg10.shp")
input_table = ("WashingtonFIPS.dbf")

#Shapefile to GeoJSON conversion
from subprocess import call
import os

import os
os.chdir(r"C:\Users\Thomas\Desktop\Lab 1 Geog 458\\")

os.environ["GDAL_DATA"] = "C:\\OSGeo4W\\share\\gdal"
os.environ["GDAL_DRIVER_PATH"] = "C:\\OSGeo4W\\bin\\gdalplugins"
os.environ["PROJ_LIB"] = "C:\\OSGeo4W\\share\\proj"
os.environ["PATH"] = "C:\\OSGeo4W\\bin;"+os.environ["PATH"]+";C:\\OSGeo4W\\apps\\msys\\bin;C:\\OSGeo4W\\apps\\Python27\\Scripts"



#Create cursors
shapefile_cursor = arcpy.da.UpdateCursor(input_shapefile,["COUNTYFP10","POP2013","FID"])
table_cursor = arcpy.da.UpdateCursor(input_table,["CountyName", "FIPSCounty"])


#Create list of blocks 
FIPS_list = []
CountyName = ""
FID = []
POP2013_list = []


#Loop through shapefile comparing each row to the table
for cur_FIPS in table_cursor:
    for cur_row in shapefile_cursor:
        CountyName = cur_FIPS[0]
        if cur_row[0] == cur_FIPS[1]:
            FIPS_list.append(cur_row[0])
            FID.append(cur_row[2])
            POP2013_list.append(cur_row[1])
    call(['C:\\OSGeo4W\\bin\\ogr2ogr',
      '-f','GeoJSON','-t_srs','WGS84',
      '-s_srs','EPSG:26913',
      'C:\\Users\\lrb9\\MYOUTPUTFILENAME.geojson',
      'C:\\Users\\lrb9\\MYINPUTFILENAME.shp'])



    
#Sum population values from blocks to county total
return sum(POP2013_list)
            
#Clean up file locks        
del shapefile_cursor 
del table_cursor
