#Script for Lab 1
#By Thomas Ryan
#For Geog 458

#Import modules
import arcpy
import sys
import os
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\ArcToolbox\\Scripts')

#Set workspace and grab input files
from arcpy import env
env.workspace = r"C:\Users\Thomas\Desktop\Lab 1 Geog 458\\"
env.overwriteOutput = True
input_shapefile = r"C:\Users\Thomas\Desktop\Lab 1 Geog 458\saep_bg10.shp"
input_table = r"C:\Users\Thomas\Desktop\Lab 1 Geog 458\WashingtonFIPS.dbf"

#Shapefile to GeoJSON conversion
from subprocess import call
os.environ["GDAL_DATA"] = "C:\\OSGeo4W\\share\\gdal"
os.environ["GDAL_DRIVER_PATH"] = "C:\\OSGeo4W\\bin\\gdalplugins"
os.environ["PROJ_LIB"] = "C:\\OSGeo4W\\share\\proj"
os.environ["PATH"] = "C:\\OSGeo4W\\bin;"+os.environ["PATH"]+";C:\\OSGeo4W\\apps\\msys\\bin;C:\\OSGeo4W\\apps\\Python27\\Scripts"

#Create cursor and list
table_cursor = arcpy.da.UpdateCursor(input_table,["CountyName", "FIPSCounty"])
countypopdict = dict()

#Create GeoJSON files for each county containing only FIPS matched blocks
for cur_FIPS in table_cursor:
    
    cur_shapefile = arcpy.CopyFeatures_management(str(input_shapefile), str(cur_FIPS[0]) + ".shp")
    arcpy.AddField_management(cur_shapefile, "CountyName", "TEXT", "")
    shapefile_cursor = arcpy.da.UpdateCursor(cur_shapefile,["COUNTYFP10","POP2013","FID", "CountyName"])
    countypop = 0
    
    for cur_row in shapefile_cursor:
        if cur_row[0] == cur_FIPS[1]:
            cur_row[3] = cur_FIPS[0]
            countypop += cur_row[1]
        elif cur_row[0] != cur_FIPS[1]:
            shapefile_cursor.deleteRow()
            
    countypopdict[int(countypop)] = str(cur_FIPS[0])
    GeoJSONoutputfile = r"C:\Users\Thomas\Desktop\Lab 1 Geog 458\\" + str(cur_FIPS[0]) + ".geojson"
    print cur_shapefile
    print arcpy.Exists(cur_shapefile)
    call(['C:\\OSGeo4W\\bin\\ogr2ogr','-f','GeoJSON','-t_srs','WGS84','-s_srs','EPSG:26913',
          GeoJSONoutputfile,
          cur_shapefile])
    del shapefile_cursor
    
del table_cursor

#Sort and print county population values
tosort = countypopdict.keys()
tosort = tosort.sort()
tosort = tosort.reverse()

print "A list of top 10 most populated county's in Washington:"
i = 0
while i < 10:
    tosort.
    print countypopdict.get(key) + ": " + str(tosort[i])
    i += 1
