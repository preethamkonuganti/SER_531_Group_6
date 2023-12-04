import pandas as pd



columns_to_keep1=['ID','Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Arrest', 'District','Ward','Latitude','Longitude']#nocity add city as chicago   'Vict Age','Vict Sex',
columns_to_keep2=['Incident ID','Start_Date_Time', 'Block Address', 'NIBRS Code', 'Crime Name2', 'Crime Name3', 'Police District Number','Sector','Latitude','Longitude','City']#noarrest
columns_to_keep3=['DR_NO','DATE OCC','TIME OCC', 'LOCATION', 'Crm Cd', 'Crm Cd Desc', 'Status Desc', 'Rpt Dist No','AREA','LAT','LON','Vict Age','Vict Sex']#NO subtype,Add city as LA, Infer arrest from status
columns_to_keep4=['ARREST_KEY','ARREST_DATE','KY_CD','OFNS_DESC','PD_DESC','ARREST_PRECINCT','ARREST_BORO','Latitude','Longitude','AGE_GROUP','PERP_SEX']#BORO IS DISTRICT#PRECINCT IS WARD


file1=pd.read_csv('C:/Users/srava/OneDrive/Desktop/531_Project/Processed/chicago_processed.csv', usecols=columns_to_keep1)
file2=pd.read_csv('C:/Users/srava/OneDrive/Desktop/531_Project/Processed/crime_maryland.csv', usecols=columns_to_keep2)
file3=pd.read_csv('C:/Users/srava/OneDrive/Desktop/531_Project/Processed/LA_10Krandom.csv', usecols=columns_to_keep3)
file4=pd.read_csv('C:/Users/srava/OneDrive/Desktop/531_Project/Processed/NYPD_Arrestdata_10krandom.csv', usecols=columns_to_keep4)

file1['City'] = 'Chicago'
file1['Vict Age']=None
file1['Vict Sex']=None
file1['Perp Age']=None
file1['Perp Sex']=None

file2['Vict Age']=None
file2['Vict Sex']=None
file2['Perp Age']=None
file2['Perp Sex']=None
file2['Arrest']="Unknown"

file3["City"]="Los Angeles"
file3['Crime Subtype'] = file3['Crm Cd Desc']
file3['Perp Age']=None
file3['Perp Sex']=None

file3['Arrest'] = file3['Status Desc'].str.contains("arrest", case=False, na=False)

file4['Vict Age']=None
file4['Vict Sex']=None
file4['Arrest']=True
file4['City']="New York"


file1.to_csv("C:/Users/srava/OneDrive/Desktop/531_Project/Processed/SemiProcessed/chicago.csv",index=False)
file2.to_csv("C:/Users/srava/OneDrive/Desktop/531_Project/Processed/SemiProcessed/Maryland.csv",index=False)
file3.to_csv("C:/Users/srava/OneDrive/Desktop/531_Project/Processed/SemiProcessed/LA.csv",index=False)
file4.to_csv("C:/Users/srava/OneDrive/Desktop/531_Project/Processed/SemiProcessed/NY.csv",index=False)


