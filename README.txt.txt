"""--------------------------------------------------------------------------------
  Script Name: Clean Street Names
  Description: This script fixes and cleans a layer with a "FullName" street
  field. A "FullName" street field includes street name and street prefix. A "FLAG"
  field is created in the output layer that shows fields with one element in its 
  string or fewer, or 5 elements in the string or more. This field can be used as
  a inspect field for data integerity.
 
  Examples: 
  INPUT                            OUTPUT
  ---------------------------------------------
  walnut blv.            --->      WALNUT BLVD
  MaIn Street.           --->      MAIN ST
  Silver road east       --->      E SILVER RD
  89 Highway (Eastbound) --->      EB 89 HWY
  knoll    creek         --->      KNOLL CR
  SOUTH / richmond av    --->      S RICHMOND AVE

  An excel sheet is needed in order to run the script. The excel sheet is called "NameABBRVs"
  and needs to be saved within the same directory as the script. It 
  contains two lists. One with street prefix's and one with street abrvs
  
  Created By:  Eric Samson.
  Date:        3/25/2020.
------------------------------------------------------------------------------------"""
ADD TOOL TO ARCGIS PRO PROJECT:

-ADD TOOL FOLDER TO DIRECTORY OF CHOOSING
-IN CATALOG ON ARCGIS PRO, OPEN TOOLBOXES
-RIGHT CLICK, ADD TOOLBOX
-NAVIGATE TO CleanStreetNameTool TOOLBOX
-CLICK OK
-OPEN GEOPROCESSING, SEARCH FOR CLEAN STREET NAME
-OPEN SCRIPT
-ENTER FEATURE CLASS
-ENTER FIELD
-ENTER AN OUTPUT FEATURE LAYER

THE SCRIPT WILL OUTPUT A FEATURE LAYER WITH A NEW FIELD LABELED FLAG, 
AND A CLEAN VERSION OF THE FIELD THAT WAS USED AS INPUT