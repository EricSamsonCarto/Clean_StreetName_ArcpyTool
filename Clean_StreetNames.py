import arcgis
import pandas as pd
import os
import arcpy

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
def main():
	arcpy.env.overwriteOutput = True
	#inFC, AS PARAMETER, fcName REPRESENTS PATH TO THE FC, GET INFIELD FROM USER, GET OUTFC FROM USER
	inFC = arcpy.GetParameterAsText(0)
	fcName = os.path.basename(inFC)

	inField = arcpy.GetParameterAsText(1)
	outFC = arcpy.GetParameterAsText(2)

	fc_df = pd.DataFrame.spatial.from_featureclass(fcName)
	fc_df.head()

#-------------------------------------------------------------------------------------

	#UPPERCASE, REMOVE LEADING AND TRAILING WHITE SPACES, REMOVE EXTRA SPACES
	fc_df[inField] = fc_df[inField].str.upper()
	fc_df[inField] = fc_df[inField].str.strip()
	fc_df[inField] = fc_df[inField].replace('\s+', ' ', regex=True)

	#REMOVE SPECIAL CHARECTERS
	SpecialCHAR = ['.', '&', ')', '(', '/', '-','{', '}', '*', '$', '%', '^', '@', '!', '_', '~', ':', '?', ']', '[', '=']
	for x in SpecialCHAR:
		fc_df[inField] = fc_df[inField].str.replace(x, '')

#-------------------------------------------------------------------------------------

	#REPLACE DIRECTIONW WITH ABBREVIATIONS
	# REPLACE HEADINGS
	HeadingsFULL = ['EAST', 'WEST', 'SOUTH', 'NORTH', 'EASTBOUND', 'WESTBOUND', 'SOUTHBOUND', 'NORTHBOUND']
	HeadingsABRV = ['E', 'W', 'S', 'N', 'EB', 'WB', 'SB', 'NB']

	#------REPLACE ABBRV AND MOVE TO FRONT!
	fc_df[inField] = fc_df[inField].str.strip()
	fc_df[inField] = fc_df[inField].replace('\s+', ' ', regex=True)

	#Copy Over StreetName
	fc_df['StreetName_Copy'] = fc_df[inField]

	#LOOP THROUGH, LOOK FOR STRING WITH MORE THAN 2 WORDS
	def find_LargeStrings(x):
		if x is not None and len(x.split()) > 2:
			return x
		if x is not None and len(x.split()) <= 2:
			return ''

	fc_df['StreetName_Copy'] = fc_df['StreetName_Copy'].apply(find_LargeStrings)

	#REPLACE HEADINGS THAT ARE AT THE END OF THE STRING
	for x,y in zip(HeadingsFULL, HeadingsABRV):
		fc_df['StreetName_Copy'] = fc_df['StreetName_Copy'].str.replace(rf'\b{x}\b$', y, regex=True)


	#MOVE HEADING TO NEW COLUMN
	fc_df['Headings'] = fc_df['StreetName_Copy'].str.split().str[-1]

	#LOOP THROUGH, LOOK FOR ABBRIEVIATIONS
	def fix_direction(x):
		if x in HeadingsABRV:
			return x
		else:
			return ''


	fc_df['Headings_Fixed'] = fc_df['Headings'].apply(fix_direction)

	#If a heading has been fixed, drop that from the streetname
	fc_df.loc[fc_df['Headings_Fixed'] != '', 'StreetName_Copy'] = fc_df.StreetName_Copy.str.rsplit(' ',1).str[0]
	fc_df = fc_df.drop(['Headings'], 1)

	#Repeat REPLACE of last word for duplicates headings:
	for x,y in zip(HeadingsFULL, HeadingsABRV):
		fc_df['StreetName_Copy'] = fc_df['StreetName_Copy'].str.replace(rf'\b{x}\b$', y, regex=True)


	#Move last word to new column
	fc_df['Headings2'] = fc_df['StreetName_Copy'].str.split().str[-1]

	#LOOP THROUGH, LOOK FOR ABBRIEVIATIONS
	def fix_direction(x):
		if x in HeadingsABRV:
			return x
		else:
			return ''


	fc_df['Headings_Fixed2'] = fc_df['Headings2'].apply(fix_direction)

	fc_df = fc_df.drop(['Headings2'], 1)

	fc_df.loc[fc_df['Headings_Fixed2'] != '', 'StreetName_Copy'] = fc_df.StreetName_Copy.str.rsplit(' ',1).str[0]

	fc_df['Headings_Final'] = fc_df['Headings_Fixed2'] + ' ' + fc_df['Headings_Fixed']

	#Drop Left Over Fields
	fc_df = fc_df.drop(['Headings_Fixed'], 1)
	fc_df = fc_df.drop(['Headings_Fixed2'], 1)

	#Look for large strings greater than 2 again

	fc_df['StreetName_Clean'] = fc_df['StreetName_Copy'].apply(find_LargeStrings)

	#REPLACE FIRST Word WITH ABBRV if it's a heading
	for x,y in zip(HeadingsFULL, HeadingsABRV):
		fc_df['StreetName_Clean'] = fc_df['StreetName_Clean'].str.replace(rf'^\b{x}\b', y, regex=True)


	#CLEAN FIELDS
	fc_df['StreetName_Clean'] = fc_df['StreetName_Clean'].str.strip()
	fc_df.StreetName_Clean = fc_df.StreetName_Clean.replace('\s+', ' ', regex=True)

	fc_df['StreetName_Copy'] = fc_df['StreetName_Copy'].str.strip()
	fc_df.StreetName_Copy = fc_df.StreetName_Copy.replace('\s+', ' ', regex=True)

	#MOVE FIRST StreetName_Copy OVER WHERE THE SECOND IS NULL
	fc_df['StreetName_Clean'].loc[(fc_df['StreetName_Clean'] == '')] = fc_df['StreetName_Copy']

	#ADD DIRECTIONS TO THE FRONT OF THE STREET NAME
	fc_df['StreetName_Clean'] = fc_df['Headings_Final'] + ' ' + fc_df['StreetName_Clean']

	#WHERE StreetName_Clean IS NULL, REPLACE WITH THE STREETNAME:
	fc_df['StreetName_Clean'] = fc_df['StreetName_Clean'].str.strip()
	fc_df.StreetName_Clean = fc_df.StreetName_Clean.replace('\s+', ' ', regex=True)

	fc_df.loc[fc_df['StreetName_Clean'] == '', 'StreetName_Clean'] = fc_df[inField]

	#Make new StreetName column
	fc_df[inField] = fc_df['StreetName_Clean']

	#Drop Left Over Fields
	fc_df = fc_df.drop(['Headings_Final'], 1)
	fc_df = fc_df.drop(['StreetName_Clean'], 1)
	fc_df = fc_df.drop(['StreetName_Copy'], 1)

	#remove WhiteSpace
	fc_df[inField] = fc_df[inField].str.strip()
	fc_df[inField] = fc_df[inField].replace('\s+', ' ', regex=True)

#-----------------------------------------------------------
	#Replace street name prefix's with abbrv's

	#READ CSV OF STREET PREFIX's and ABBREVIATIONS
	config_file = os.path.join(os.path.dirname(__file__), "NameABBRV.csv")
	csv_df = pd.read_csv(config_file)
	csv_df.dropna(inplace = True)

	csv_df['Streetname'] = csv_df['Streetname'].str.strip()
	csv_df['Abbrv'] = csv_df['Abbrv'].str.strip()

	#STREET LISTS
	streetprefix_list = csv_df['Streetname'].tolist()
	Abbrv_list = csv_df['Abbrv'].tolist()

	#OTHERS:
	Others = ['AV','BLVE','BL','CI','PARKWY','EX','PY','TE','PW','PK','BLV']
	Others_re = ['AVE','BLVD','BLVD','CIR','PKY','EXPY','PKWY','TER','PKWY','PARK','BLVD']

	#MAKE NEW FIELD WITH ONLY LAST ELEMENT
	fc_df['ABBRV'] = fc_df[inField].str.split().str[-1]

	#LOOP THROUGH, LOOK FOR ABBRIEVIATIONS
	def fix_direction(x):
		if x in streetprefix_list:
			return x
		elif x in Others:
			return x
		else:
			return ''

	#CREATED FIELD WITH ONLY ROAD PREFIX'S, ELSE none's
	fc_df['ABBRV_fixed'] = fc_df['ABBRV'].apply(fix_direction)

	#REPLACE PREFIX WITH ABBRV
	for x,y in zip(streetprefix_list, Abbrv_list):
		fc_df['ABBRV_fixed'] = fc_df['ABBRV_fixed'].str.replace(rf'\b{x}\b$', y, regex=True)

	for x,y in zip(Others, Others_re):
		fc_df['ABBRV_fixed'] = fc_df['ABBRV_fixed'].str.replace(rf'\b{x}\b$', y, regex=True)

	#LOCATE WHERE THERE ARE Prefix's, REMOVE Prefix FROM STREETNAME COLUMN
	#Since we just moved it above
	fc_df.loc[fc_df['ABBRV_fixed'] != '', inField] = fc_df[inField].str.rsplit(' ',1).str[0]

	#ADD THE abbrv back TO THE END OF FIELD
	fc_df[inField] = fc_df[inField] + ' ' + fc_df['ABBRV_fixed']

	fc_df[inField] = fc_df[inField].str.strip()
	fc_df[inField] = fc_df[inField].replace('\s+', ' ', regex=True)

	#Drop remaining fields
	fc_df = fc_df.drop(['ABBRV_fixed'], 1)
	fc_df = fc_df.drop(['ABBRV'], 1)

#-----------------------------------------------------------
	#FLAG ROWS WITH LESS THAN ONE ELEMENT (NO PREFIX)

	#CREATES NEW FIELD CALLED 'FLAG'
	fc_df['FLAG'] = fc_df[inField]

	#COUNT ELEMENTS IN EACH ROW OF STREET NAME, OVERWRITE FLAG ROWS WITH ELEMENT COUNT
	fc_df['FLAG'] = fc_df[inField].str.split().str.len()

	#SET UP FUNCTION TO ITERATE THROUGH FLAGS, LOOKING FOR WHERE STREETNAME HAS 1 ELEMENT OR LESS, OR 5 ELEMENTS OR MORE
	def check_elements(x):
		if x <= 1 or x >= 5:
			return 'FLAG'
		else:
			return ''
        
	fc_df['FLAG'] = fc_df['FLAG'].apply(check_elements)

#-----------------------------------------------------------

	#BACK TO FEATURE LAYER, DF TO OUT FC
	outFC_sp = fc_df.spatial.to_featureclass(os.path.join(outFC))

	#PRINT TO MAP
	outFC_sp
if __name__ == "__main__":
    main()
