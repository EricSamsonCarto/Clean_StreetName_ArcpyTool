
[![LinkedIn][linkedin-shield]][linkedin-url]

<p align="center">
  <h3 align="center">Clean StreetName Arcpy Tool</h3>

  <p align="center">
    An ArcGIS Pro Arcpy/Pandas tool that will create a new feature class with an updated clean version of street names<br>
    Project Description page:<br>
  <a href='#'>Clean StreetName Arcpy Tool</a>
  </p>
</p>

<!-- ABOUT THE PROJECT -->
<div align="center">
  
<img src="https://lh3.googleusercontent.com/jqjeu7Me452qzRuVmN14eAg2UEpQyqU8ddkwsJX3xavJQKYqAYdabksl76aorKelR-xwbUcA9p0Y3GabXRpoFSH56QCIWqXPmfR5_1wtL-NAM4ZWQiIDFYBiFvj9aCsDKwRE-zC_QQ=w2400" width="400px">
  
</div>

  Description: This script fixes and cleans a layer with a "FullName" street <br>
  field. A "FullName" street field includes street name and street prefix. A "FLAG" <br>
  field is created in the output layer that shows fields with one element in its <br>
  string or fewer, or 5 elements in the string or more. This field can be used as <br>
  a inspect field for data integerity. <br>

   Example Outputs (Streetname is the output field from tool, OriginalStr is what the original field looked like):
  <br>
  <div align="center">
  
  <img src="https://lh3.googleusercontent.com/Pb_LxlltZttgSdhHqH0rx3Hg9HlWdyNIW935lyuIrsSxu2cVC6_-3oqNEUhy4Wv1VUyN3YCqj6ZRMzDI5FRV3zk8pJJ4lu1qhahYJR_48rWQRjUtMU1LYR80QnSvO1Onb51vDmd87A=w2400" width="500px">
  
  </div>

  An excel sheet is needed in order to run the script. The excel sheet is called "NameABBRVs"<br>
  and needs to be saved within the same directory as the script. It <br>
  contains two lists. One with street prefix's and one with street abrvs <br>
  <br>
------------------------------------------------------------------------------------"""
ADD TOOL TO ARCGIS PRO PROJECT:<br>
-ADD TOOL FOLDER TO DIRECTORY OF CHOOSING <br>
-IN CATALOG ON ARCGIS PRO, OPEN TOOLBOXES <br>
-RIGHT CLICK, ADD TOOLBOX <br>
-NAVIGATE TO CleanStreetNameTool TOOLBOX <br>
-CLICK OK <br>
-OPEN GEOPROCESSING, SEARCH FOR CLEAN STREET NAME <br>
-OPEN SCRIPT <br> 
-ENTER FEATURE CLASS <br>
-ENTER FIELD <br>
-ENTER AN OUTPUT FEATURE LAYER <br>

THE SCRIPT WILL OUTPUT A FEATURE LAYER WITH A NEW FIELD LABELED FLAG, <br>
AND A CLEAN VERSION OF THE FIELD THAT WAS USED AS INPUT<br>


### Built With
* [Arcpy](https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy/a-quick-tour-of-arcpy.htm)
* [Pandas](https://pandas.pydata.org/)

<!-- CONTACT -->
## Contact
Eric Samson: [@MyTwitter](https://twitter.com/EricSamsonGIS) <br>
Email: ericsamsonwx@gmail.com <br>
Website: [EricSamson.com](https://ericsamson.com) <br>

Project Link: [https://github.com/EricSamsonCarto/Clean_StreetName_ArcpyTool](https://github.com/EricSamsonCarto/Clean_StreetName_ArcpyTool)

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/iamericsamson
