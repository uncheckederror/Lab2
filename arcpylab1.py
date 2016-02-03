#Script for Lab 1
#By Thomas Ryan
#For Geog 458

#Import modules
import arcpy
import sys
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\ArcToolbox\\Scripts')

#Set workspace and grab input files
from arcpy import env
env.workspace = r"C:\Users\tomaryan\Downloads\\"
env.overwriteOutput = True
input_shapefile = r"C:\Users\tomaryan\Downloads\saep_bg10.shp"
input_table = r"C:\Users\tomaryan\Downloads\WashingtonFIPS.dbf"

#Shapefile to GeoJSON conversion
from subprocess import call
import os
os.chdir(r"C:\Users\tomaryan\Downloads")
os.environ["GDAL_DATA"] = "C:\\OSGeo4W\\share\\gdal"
os.environ["GDAL_DRIVER_PATH"] = "C:\\OSGeo4W\\bin\\gdalplugins"
os.environ["PROJ_LIB"] = "C:\\OSGeo4W\\share\\proj"
os.environ["PATH"] = "C:\\OSGeo4W\\bin;"+os.environ["PATH"]+";C:\\OSGeo4W\\apps\\msys\\bin;C:\\OSGeo4W\\apps\\Python27\\Scripts"

#Create cursor and list
table_cursor = arcpy.da.UpdateCursor(input_table,["CountyName", "FIPSCounty"])
countypoplist = []

#Create GeoJSON files for each county containing only FIPS matched blocks
for cur_FIPS in table_cursor:
    
    cur_shapefile = arcpy.CopyFeatures_management(str(input_shapefile), str(cur_FIPS[0]))
    arcpy.AddField_management(cur_shapefile, "CountyName", "TEXT", "")
    shapefile_cursor = arcpy.da.UpdateCursor(cur_shapefile,["COUNTYFP10","POP2013","FID", "CountyName"])
    countypop = 0
    
    for cur_row in shapefile_cursor:
        if cur_row[0] == cur_FIPS[1]:
            cur_row[3] = cur_FIPS[0]
            countypop += cur_row[1]
        elif cur_row[0] != cur_FIPS[1]:
            shapefile_cursor.deleteRow()
            
    del shapefile_cursor
    countypoplist.append(str(countypop) + ": " + str(cur_FIPS[0]))
    GeoJSONoutputfile = r"C:\Users\tomaryan\Downloads\\" + str(cur_FIPS[0]) + ".geojson"
    shapefiletoconvert = r"C:\Users\tomaryan\Downloads\\" + str(cur_FIPS[0]) + ".shp"
    call(['C:\\OSGeo4W\\bin\\ogr2ogr',
      '-f','GeoJSON','-t_srs','WGS84',
      '-s_srs','EPSG:26913',
      GeoJSONoutputfile,
      shapefiletoconvert])
    
del table_cursor
    
#Sort and print county population values
countypoplist.sort()
countypoplist.reverse()
print "A list of top 10 most populated county's in Washington:"
i = 0
while i < 10:
    print countypoplist[i]
    i += 1
