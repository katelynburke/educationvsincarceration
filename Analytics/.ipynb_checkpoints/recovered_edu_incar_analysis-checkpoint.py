#!/usr/bin/env python
# coding: utf-8

# # To create a database with Education and Incarceration Data

# In[1]:


import numpy as np 
import pandas as pd 

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# ## Read in the Incarceration Data

# In[2]:


crime = pd.read_csv('../Data/incarceration_data/ucr_by_state.csv')
prisoners_in_custody = pd.read_csv('../Data/incarceration_data/prison_custody_by_state.csv')
incarceration = pd.read_csv('../Data/incarceration_data/crime_and_incarceration_by_state.csv')
vera_incarceration_trends = pd.read_csv('../Data/incarceration_data/incarceration_trends.csv')


# #### Preview Incarceration CSVs
# 

# In[3]:


display('BJS: Crime Rates by Crime Type State and Year')
display(crime.head(10))
display(crime.columns)

display('BJS: In Custody Counts by State and Year')
display(prisoners_in_custody.head(10))
display(prisoners_in_custody.columns)

display('BJS: In Custody Counts, Crime Rates by Type, By State and Year')
display(incarceration.head(10))
display(incarceration.columns)

display('Vera Justice: In Custody breakout by Demographic and Prison')
display(vera_incarceration_trends.head(10))
display(vera_incarceration_trends.columns)


# #### Drop Columns that will be excluded from report (exclude Federal)

# In[4]:


incarceration_trim = incarceration.drop(columns=['includes_jails','crime_reporting_change','crimes_estimated',
                                        'murder_manslaughter', 'rape_legacy', 'rape_revised',
                                        'robbery', 'agg_assault', 'burglary', 'larceny', 'vehicle_theft'])

incarceration_df = incarceration_trim.loc[incarceration_trim['jurisdiction'] != 'FEDERAL']
incarceration_format = incarceration_df.rename(columns={'jurisdiction': 'state'})
incarceration_format.columns = map(str.upper, incarceration_format.columns)
incarceration_format.head()


# #### Estimate Missing NY Incarceration values to repair 2015 NaN

# In[5]:


incarceration_ny_fix = incarceration_format[incarceration_format['STATE'] == 'NEW YORK']
ny_14 = incarceration_ny_fix[(incarceration_ny_fix.STATE == 'NEW YORK') & (incarceration_ny_fix.YEAR == 2014)]
ny_16 = incarceration_ny_fix[(incarceration_ny_fix.STATE == 'NEW YORK') & (incarceration_ny_fix.YEAR == 2016)]

ny_15_state_pop = (ny_14.iloc[0]['STATE_POPULATION'].astype(int) 
                   + ny_16.iloc[0]['STATE_POPULATION'].astype(int))/2
                        
ny_15_vc_tot = (ny_14.iloc[0]['VIOLENT_CRIME_TOTAL'].astype(int) + 
                ny_16.iloc[0]['VIOLENT_CRIME_TOTAL'].astype(int))/2
                      
ny_15_pc_tot = (ny_14.iloc[0]['PROPERTY_CRIME_TOTAL'].astype(int) + ny_16.iloc[0]['PROPERTY_CRIME_TOTAL'].astype(int))/2
print(ny_15_state_pop, ny_15_vc_tot, ny_15_pc_tot)


# #### Update NY Incarceration NaNs to estimated values  //  Check Repair

# In[6]:


values = {'STATE_POPULATION': ny_15_state_pop, 
            'VIOLENT_CRIME_TOTAL': ny_15_vc_tot, 
            'PROPERTY_CRIME_TOTAL': ny_15_pc_tot
            }
incarceration_format.fillna(value=values, inplace=True)

display(incarceration_format.head())

ny_edit_check = round(incarceration_format[(incarceration_format.STATE == 'NEW YORK') & 
                                                  (incarceration_format.YEAR == 2015)],0)
display(ny_edit_check)


# In[7]:


incarceration_format['STATE'] = incarceration_format['STATE'].str.replace(' ', '_', regex=True)
# incarceration_order = incarceration_format[['YEAR','STATE','PRISONER_COUNT', 'STATE_POPULATION', 
  #                                           'VIOLENT_CRIME_TOTAL', 'PROPERTY_CRIME_TOTAL']]
incarceration_sort = incarceration_format.sort_values(['STATE','YEAR'])
incarceration_index = incarceration_sort.reset_index()
incarceration_format = incarceration_index.drop(columns=['index'])
incarceration_format.head()


# #### Export cleaned Incarceration Data for Snapshot // Preview Dataframe

# In[8]:


incarceration_report = round(incarceration_format,0)
incarceration_report.to_csv('../Reports/incarceration_report.csv')
incarceration_report


# ## Read in the Vera Justice Incarceration Data
# * Provides breakout by race

# In[9]:


vera_incarceration_trends.columns


# In[10]:


vera_incarceration_trends_trim = vera_incarceration_trends.drop(columns=[
'yfips','fips', 'county_name', 'total_pop_15to64', 'female_pop_15to64', 'male_pop_15to64',
'asian_pop_15to64', 'black_pop_15to64', 'latino_pop_15to64', 'native_pop_15to64', 'other_pop_15to64', 
'division', 'jail_from_state_prison', 'jail_from_other_state_prison', 'jail_from_state_jail', 
'total_jail_pretrial', 'female_jail_pretrial', 'male_jail_pretrial', 'female_jail_pop', 'male_jail_pop',
'jail_from_other_state_jail', 'jail_from_fed','jail_from_ice', 'urbanicity', 'commuting_zone','female_prison_pop', 'male_prison_pop', 
'metro_area', 'land_area', 'total_jail_adm_dcrp', 'female_jail_adm_dcrp', 'male_jail_adm_dcrp', 'total_jail_pop_dcrp', 'female_jail_pop_dcrp', 'male_jail_pop_dcrp',
'white_pop_15to64', 'total_prison_adm', 'female_prison_adm', 'male_prison_adm', 'asian_prison_adm', 'black_prison_adm',
'latino_prison_adm', 'native_prison_adm', 'other_prison_adm', 'white_prison_adm', 'index_crime', 'violent_crime',
'property_crime', 'murder_crime', 'rape_crime', 'robbery_crime', 'agr_assault_crime', 'burglary_crime', 'larceny_crime',
'mv_theft_crime', 'arson_crime', 'num_facilites', 'num_employees', 'confined_pop', 'capacity', 'ucr_population', 
                                    ])

vera_incarceration_trends_df = vera_incarceration_trends_trim.loc[vera_incarceration_trends_trim['year'] > 2000 ]
vit_drop = vera_incarceration_trends_df.dropna()
vit_group = vit_drop.groupby(by=['year','state']).sum()
vera_incarceration = vit_group.reset_index()
vera_incarceration


# In[11]:


vera_incarceration['state'] = vera_incarceration['state'].map({'AL':'ALABAMA',
'AK':'ALASKA', 'AZ':'ARIZONA','AR':'ARKANSAS','CA':'CALIFORNIA',
'CO':'COLORADO','CT':'CONNECTICUT','DE':'DELAWARE','FL':'FLORIDA',
'GA':'GEORGIA','HI':'HAWAII','ID':'IDAHO','IL':'ILLINOIS','IN':'INDIANA',
'IA':'IOWA','KS':'KANSAS','KY':'KENTUCKY','LA':'LOUISIANA','ME':'MAINE',
'MD':'MARYLAND','MA':'MASSACHUSETTS','MI':'MICHIGAN','MN':'MINNESOTA',
'MS':'MISSISSIPPI','MO':'MISSOURI','MT':'MONTANA','NE':'NEBRASKA',
'NV':'NEVADA','NH':'NEW HAMPSHIRE','NJ':'NEW JERSEY','NM':'NEW MEXICO',
'NY':'NEW YORK','NC':'NORTH CAROLINA','ND':'NORTH DAKOTA','OH':'OHIO',
'OK':'OKLAHOMA','OR':'OREGON','PA':'PENNSYLVANIA','RI':'RHODE ISLAND',
'SC':'SOUTH CAROLINA','SD':'SOUTH DAKOTA','TN':'TENNESSEE','TX':'TEXAS',
'UT':'UTAH','VT':'VERMONT','VA':'VIRGINIA','WA':'WASHINGTON',
'WV':'WEST VIRGINIA','WI':'WISCONSIN','WY':'WYOMING',})
vera_incarceration.head()


# In[12]:


vera_incarceration['state'] = vera_incarceration['state'].str.replace(' ', '_', regex=True)
vera_incarceration.columns = map(str.upper, vera_incarceration.columns)
vera_incarceration = round(vera_incarceration, 0)
vera_incarceration.columns


# In[13]:


vera_incarceration['ASIAN_JAIL_POP'] = ((vera_incarceration['ASIAN_JAIL_POP'] / 
                                            vera_incarceration['TOTAL_JAIL_POP']) * 100)

vera_incarceration['BLACK_JAIL_POP'] = ((vera_incarceration['BLACK_JAIL_POP'] / 
                                            vera_incarceration['TOTAL_JAIL_POP']) * 100)

vera_incarceration['LATINO_JAIL_POP'] = ((vera_incarceration['LATINO_JAIL_POP'] / 
                                            vera_incarceration['TOTAL_JAIL_POP']) * 100)

vera_incarceration['NATIVE_JAIL_POP'] = ((vera_incarceration['NATIVE_JAIL_POP'] / 
                                            vera_incarceration['TOTAL_JAIL_POP']) * 100)

vera_incarceration['WHITE_JAIL_POP'] = ((vera_incarceration['WHITE_JAIL_POP'] / 
                                            vera_incarceration['TOTAL_JAIL_POP']) * 100)

vera_incarceration['ASIAN_PRISON_POP'] = ((vera_incarceration['ASIAN_PRISON_POP'] / 
                                            vera_incarceration['TOTAL_PRISON_POP']) * 100)

vera_incarceration['BLACK_PRISON_POP'] = ((vera_incarceration['BLACK_PRISON_POP'] / 
                                            vera_incarceration['TOTAL_PRISON_POP']) * 100)

vera_incarceration['LATINO_PRISON_POP'] = ((vera_incarceration['LATINO_PRISON_POP'] / 
                                            vera_incarceration['TOTAL_PRISON_POP']) * 100)

vera_incarceration['NATIVE_PRISON_POP'] = ((vera_incarceration['NATIVE_PRISON_POP'] / 
                                            vera_incarceration['TOTAL_PRISON_POP']) * 100)

vera_incarceration['OTHER_PRISON_POP'] = ((vera_incarceration['OTHER_PRISON_POP'] / 
                                            vera_incarceration['TOTAL_PRISON_POP']) * 100)

vera_incarceration['WHITE_PRISON_POP'] = ((vera_incarceration['WHITE_PRISON_POP'] / 
                                            vera_incarceration['TOTAL_PRISON_POP']) * 100)


# In[14]:


vera_incarceration_final = vera_incarceration.drop(columns=['TOTAL_POP','TOTAL_JAIL_POP','TOTAL_PRISON_POP'])
vir_sort = vera_incarceration_final.sort_values(['STATE', 'YEAR'])
vir_index = vir_sort.reset_index()
vera_incarceration_reset = vir_index.drop(columns=['index'])
vera_incarceration_report = vera_incarceration_reset[[
       'STATE','YEAR', 'TOTAL_JAIL_ADM', 
       'ASIAN_JAIL_POP', 'BLACK_JAIL_POP', 'LATINO_JAIL_POP',
       'NATIVE_JAIL_POP', 'WHITE_JAIL_POP',
       'ASIAN_PRISON_POP', 'BLACK_PRISON_POP', 'LATINO_PRISON_POP',
       'NATIVE_PRISON_POP', 'OTHER_PRISON_POP', 'WHITE_PRISON_POP']]
vera_incarceration_report.head()


# In[15]:


vera_incarceration_report.to_csv('../Reports/vera_incarceration_report.csv')
vera_incarceration_report.head()


# In[16]:


STATE = vera_incarceration_report['STATE'].nunique()
display(f'We have summary breakouts of Race for {STATE} states')
display(f'But we dont have coverage for every year, so we are just gonna keep this to ourselves')
display(vera_incarceration_report['STATE'].value_counts())
display(f'Still worth it for other projects')


# ## Read in the Education Data

# In[17]:


education_file = "../Data/education_data/states_all.csv"
education_df = pd.read_csv(education_file)
display(education_df.head())
display(education_df.columns)


# #### Notes on what some of the columns mean: 
# 
# * <b>Academic Achievement -  National Assessment of Educational Progress (NAEP)</b><br>
# A breakdown of student performance as assessed by the corresponding exams (math and reading, grades 4 and 8).<br><br>
# 
# * <b>AVG_MATH_4_SCORE:</b> The state's average score for fourth graders taking the NAEP math exam.
# * <b>AVG_MATH_8_SCORE:</b> The state's average score for eight graders taking the NAEP math exam.
# * <b>AVG_READING_4_SCORE:</b> The state's average score for fourth graders taking the NAEP reading exam.
# * <b>AVG_READING_8_SCORE:</b> The state's average score for eighth graders taking the NAEP reading exam.

# In[18]:


# Create a filtered dataframe from specific columns

education_cols = ['STATE', 'YEAR', 'TOTAL_EXPENDITURE', 'INSTRUCTION_EXPENDITURE', 'GRADES_4_G', 'GRADES_8_G', 'GRADES_ALL_G', 'AVG_MATH_4_SCORE', 'AVG_MATH_8_SCORE', 'AVG_READING_4_SCORE', 'AVG_READING_8_SCORE']
education_transformed = education_df[education_cols].copy()

education_transformed.head()


# In[ ]:





# In[19]:


# Rename the column headers
education_transformed = education_transformed.rename(columns={"GRADES_4_G": "4TH_ENROLLED",
                                                         "GRADES_8_G": "8TH_ENROLLED",
                                                         "GRADES_ALL_G": "TOTAL_ENROLLMENT",
                                                         "AVG_MATH_4_SCORE": "4_AVG_MATH_SCORE",
                                                         "AVG_MATH_8_SCORE": "8_AVG_MATH_SCORE",
                                                         "AVG_READING_4_SCORE": "4_AVG_RDG_SCORE",
                                                         "AVG_READING_8_SCORE": "8_AVG_RDG_SCORE"})
education_transformed.head()


# In[20]:


# Filter by year - greater than the year 2000

education_year = education_transformed[education_transformed['YEAR'] > 2000]
education_year.head()


# In[21]:


# Filter by year - less than the year 2017

education_years = education_year[education_year['YEAR'] < 2017]
education_years.head()


# ## A Quick view on NaNs and Missing Data
# * Not all states evaluate their students on the NAEP rubric
# * Finance and Enrollment data not available for all years for all Territories (States mostly seem fine)

# In[22]:


display(education_years.count())
display(education_years['STATE'].value_counts().value_counts())


# In[23]:


# Drop rows that are not in the US
#nonUS = ['GUAM', 'PUERTO_RICO', 'AMERICAN_SAMOA','VIRGIN_ISLANDS',
 #       'NORTHERN_MARIANAS','DOD_DOMESTIC','DOD_OVERSEAS',
  #      'BUREAU_OF_INDIAN_AFFAIRS','NORTHERN_MARIANA_ISLANDS','BI',
   #     'DD','DOD_-_DOMESTIC','BIE','DOD_-_OVERSEAS','BUREAU_OF_INDIAN_EDUCATION',
    #    'DEPARTMENT_OF_DEFENSE','DEPARTMENT_OF_DEFENSE_EDUCATION_ACTIVITY',
     #   'BUREAU_OF_INDIAN_EDUCATIO','U.S._VIRGIN_ISLANDS','DOD_(OVERSEAS_AND_DOMESTIC_COMBINED)'
      #  ]

updated_ed_df = education_years.loc[(education_years['STATE'] != 'GUAM') &
                                    (education_years['STATE'] != 'PUERTO_RICO') &
                                    (education_years['STATE'] != 'AMERICAN_SAMOA') &
                                    (education_years['STATE'] != 'VIRGIN_ISLANDS') &
                                    (education_years['STATE'] != 'NORTHERN_MARIANAS') &
                                    (education_years['STATE'] != 'DOD_DOMESTIC') &
                                    (education_years['STATE'] != 'DOD_OVERSEAS') &
                                    (education_years['STATE'] != 'BUREAU_OF_INDIAN_AFFAIRS') &
                                    (education_years['STATE'] != 'NORTHERN_MARIANA_ISLANDS') &
                                    (education_years['STATE'] != 'BI') &
                                    (education_years['STATE'] != 'DD') &
                                    (education_years['STATE'] != 'DOD_-_DOMESTIC') &
                                    (education_years['STATE'] != 'BIE') &
                                    (education_years['STATE'] != 'DOD_-_OVERSEAS') &
                                    (education_years['STATE'] != 'BUREAU_OF_INDIAN_EDUCATION') &
                                    (education_years['STATE'] != 'DEPARTMENT_OF_DEFENSE') &
                                    (education_years['STATE'] != 'DEPARTMENT_OF_DEFENSE_EDUCATION_ACTIVITY') &
                                    (education_years['STATE'] != 'BUREAU_OF_INDIAN_EDUCATIO') &
                                    (education_years['STATE'] != 'U.S._VIRGIN_ISLANDS') &
                                    (education_years['STATE'] != 'DOD_(OVERSEAS_AND_DOMESTIC_COMBINED)') &
                                    (education_years['STATE'] != 'DISTRICT_OF_COLUMBIA')]
updated_ed_df.head()


# #### Highlighting the issue with Virginia
# * Three rows with different info

# In[24]:


display(updated_ed_df['STATE'].value_counts().head()) # Virginia seems to have extra and is the only one
VA_ed = updated_ed_df.loc[(education_years['STATE'] == 'VIRGINIA')]
display(VA_ed['YEAR'].value_counts().head()) # 2008 seems to have Three observations
VA_data_error = VA_ed.loc[(VA_ed['YEAR'] == 2008)]
display(VA_data_error) # Unique Values in Enrollment Columns [4TH_ENROLLED, 8TH_ENROLLED, TOTAL_ENROLLMENT]


# In[25]:


ed_group_df = updated_ed_df.groupby(['STATE','YEAR']).mean()
ed_group_df.reset_index(inplace=True)
# ed_group_df['STATE'].value_counts() # Check to make sure we have the right number of obs
ed_group_df


# In[26]:


# Export to Reports

education_report = ed_group_df

education_report.to_csv('../Reports/education_report.csv')

education_report


# # Joining the Cleaned Datasets

# ### Quick preview to remember what we've done

# In[27]:


display('Cleaned Incarceration Info')
display(incarceration_report.head())
display('Cleaned Vera Info [we will make an SQL, but not join]')
display(vera_incarceration_report.head())
display('Cleaned Education Info')
display(education_report.head())


# In[28]:


education_v_incarceration_format = education_v_incarceration
education_v_incarceration_format['TOTAL_EXPENDITURE'] = education_v_incarceration_format['TOTAL_EXPENDITURE']                                                        .map("${:,.2f}".format)
education_v_incarceration_format['INSTRUCTION_EXPENDITURE'] = education_v_incarceration_format['INSTRUCTION_EXPENDITURE']                                                        .map("${:,.2f}".format)
education_v_incarceration_format['4TH_ENROLLED'] = education_v_incarceration_format['4TH_ENROLLED']                                                        .map("{:,.0f}".format)
education_v_incarceration_format['8TH_ENROLLED'] = education_v_incarceration_format['8TH_ENROLLED']                                                        .map("{:,.0f}".format)
education_v_incarceration_format['TOTAL_ENROLLMENT'] = education_v_incarceration_format['TOTAL_ENROLLMENT']                                                        .map("{:,.0f}".format)
education_v_incarceration_format['4_AVG_MATH_SCORE'] = education_v_incarceration_format['4_AVG_MATH_SCORE']                                                        .map("{:,.2f}".format)
education_v_incarceration_format['8_AVG_MATH_SCORE'] = education_v_incarceration_format['8_AVG_MATH_SCORE']                                                        .map("{:,.2f}".format)
education_v_incarceration_format['4_AVG_RDG_SCORE'] = education_v_incarceration_format['4_AVG_RDG_SCORE']                                                        .map("{:,.2f}".format)
education_v_incarceration_format['8_AVG_RDG_SCORE'] = education_v_incarceration_format['8_AVG_RDG_SCORE']                                                        .map("{:,.2f}".format)
education_v_incarceration_format['PRISONER_COUNT'] = education_v_incarceration_format['PRISONER_COUNT']                                                        .map("{:,.0f}".format)
education_v_incarceration_format['STATE_POPULATION'] = education_v_incarceration_format['STATE_POPULATION']                                                        .map("{:,.0f}".format)
education_v_incarceration_format['VIOLENT_CRIME_TOTAL'] = education_v_incarceration_format['VIOLENT_CRIME_TOTAL']                                                        .map("{:,.0f}".format)
education_v_incarceration_format['PROPERTY_CRIME_TOTAL'] = education_v_incarceration_format['PROPERTY_CRIME_TOTAL']                                                        .map("{:,.0f}".format)
education_v_incarceration_format['ASIAN_JAIL_POP'] = education_v_incarceration_format['ASIAN_JAIL_POP'].map("{:,.2f}%".format)
education_v_incarceration_format['BLACK_JAIL_POP'] = education_v_incarceration_format['BLACK_JAIL_POP'].map("{:,.2f}%".format)
education_v_incarceration_format['LATINO_JAIL_POP'] = education_v_incarceration_format['LATINO_JAIL_POP'].map("{:,.2f}%".format)
education_v_incarceration_format['NATIVE_JAIL_POP'] = education_v_incarceration_format['NATIVE_JAIL_POP'].map("{:,.2f}%".format)
education_v_incarceration_format['WHITE_JAIL_POP'] = education_v_incarceration_format['WHITE_JAIL_POP'].map("{:,.2f}%".format)
education_v_incarceration_format['ASIAN_PRISON_POP'] = education_v_incarceration_format['ASIAN_PRISON_POP'].map("{:,.2f}%".format)
education_v_incarceration_format['BLACK_PRISON_POP'] = education_v_incarceration_format['BLACK_PRISON_POP'].map("{:,.2f}%".format)
education_v_incarceration_format['LATINO_PRISON_POP'] = education_v_incarceration_format['LATINO_PRISON_POP'].map("{:,.2f}%".format)
education_v_incarceration_format['NATIVE_PRISON_POP'] = education_v_incarceration_format['NATIVE_PRISON_POP'].map("{:,.2f}%".format)
education_v_incarceration_format['OTHER_PRISON_POP'] = education_v_incarceration_format['OTHER_PRISON_POP'].map("{:,.2f}%".format)
education_v_incarceration_format['WHITE_PRISON_POP'] = education_v_incarceration_format['WHITE_PRISON_POP'].map("{:,.2f}%".format)
education_v_incarceration_format.head()


# In[ ]:


ed_prison_df = education_report.merge(incarceration_report, on=['STATE', 'YEAR'])
education_v_incarceration = ed_prison_df.merge(vera_incarceration_report, on=['STATE', 'YEAR'])
education_v_incarceration.to_csv('../Reports/education_v_incarceration.csv')
display(education_v_incarceration.head(25))
display(education_v_incarceration.dtypes)


# ## Loading Output Reports

# In[ ]:


education_v_incarceration_complete = education_v_incarceration_format[['STATE', 'YEAR', 'TOTAL_EXPENDITURE', 
                                 'INSTRUCTION_EXPENDITURE','4TH_ENROLLED', '8TH_ENROLLED', 'TOTAL_ENROLLMENT',
                                 'PRISONER_COUNT', 'STATE_POPULATION', 'VIOLENT_CRIME_TOTAL', 'PROPERTY_CRIME_TOTAL']]
education_v_incarceration_complete


# In[ ]:


education_v_incarceration.to_csv('../Outputs/education_v_incarceration_raw.csv')
education_v_incarceration.to_json('../Outputs/education_v_incarceration_raw.json', orient='table')
education_v_incarceration_format.to_csv('../Outputs/education_v_incarceration_format.csv')
education_v_incarceration_format.to_json('../Outputs/education_v_incarceration_format.json', orient='table')
education_v_incarceration_complete.to_csv('../Outputs/education_v_incarceration_complete.csv')
education_v_incarceration_complete.to_json('../Outputs/education_v_incarceration_complete.json', orient='table')


# ## API Calls can be made
# 
# * Here via github
#  
#     https://raw.githubusercontent.com/katelynburke/educationvsincarceration/master/Outputs/education_v_incarceration_complete.json <br>
#     https://raw.githubusercontent.com/katelynburke/educationvsincarceration/master/Outputs/education_v_incarceration_format.json <br>
#     https://raw.githubusercontent.com/katelynburke/educationvsincarceration/master/Outputs/education_v_incarceration_raw.json <br><br>
#             
# * or Here via github pages
# 
#     https://srmonteiro.github.io/data/education_v_incarceration_complete.json <br>
#     https://srmonteiro.github.io/data/education_v_incarceration_format.json <br>
#     https://srmonteiro.github.io/data/education_v_incarceration_raw.json 
#         

# ## Connect to local database
# 

# In[ ]:


connection_string = "<insert user name>:<insert password>@127.0.0.1/customer_db"
engine = create_engine(f'mysql://{connection_string}')


# ### Check for tables 

# In[ ]:


engine.table_names()


# ### Use pandas to load csv converted DataFrame into database

# In[ ]:


education_v_incarceration_complete.to_sql(name='', con=engine, if_exists='append', index=True) 


# ### Use pandas to load json converted DataFrame into database
# 

# In[ ]:





# ### Confirm data has been added by querying the table
# 
# 

# In[ ]:


pd.read_sql_query('select * from ', con=engine).head()


# In[ ]:





# In[ ]:





# In[ ]:


engine = create_engine('sqlite://', echo=False)


# In[ ]:


education_v_incarceration_format.to_sql(name='education_v_incarceration_format', con=engine, 
                                        if_exists = 'append', index=False)

