## Education vs. Incarceration in the United States
*Utilizing the ETL procedure of extracting, transforming, and loading data*

### Topic:
Is there a correlation between the incarceration rate and academic achievement by state (USA) between the years of 2001-2016?
  
### Extract
- Decided to analyze the data and draw conclusions by comparing the average assessment scores in math and reading to the crime totals and prisoner counts in each state
- Noticed that several years of NAEP test score data were missing from the education data
- The dataset also included the total expenditure in each state and the expenditure for education instruction
- Decided to also look for correlations between instruction expenditure in each state and the crime totals and prisoner counts

#### Data Sources: 
- Years 2001 - 2016
- U.S. Education Dataset - Unification Project:https://www.kaggle.com/noriuk/us-education-datasets-unification-project
  - For more on how Math and Reading Scores are assessed via NAEP : https://nces.ed.gov/nationsreportcard/ </li>
- Crime and Incarceration in the United States:https://www.kaggle.com/christophercorrea/prisoners-and-crime-in-united-states

### Transform
#### Transforming the Education Data: 
- Read in the education CSV file to preview it
- Filtered the data frame to include the columns we wanted to use (State, Year, Total Expenditure, Instruction Expenditure, 4th Grade Enrollment, 8th Grade Enrollment, Total Student Enrollment, 4th Average Math/Reading Scores, 8th Average Math/Reading Scores)
- Renamed the columns so they were consistent and made more sense with the data that was represented
- Filtered the data by year so that only the years 2001 through 2016 were represented in the data frame (the same years represented in the prisoners and crime dataset)
- Fixed the average enrollment for Virginia - we took the mean of the 4th, 8th, and total enrollment and replaced the three rows of Virginia data with the averages
- Grouped the data by State and Year which made the data frame easier to read and more organized

#### Transforming the Prisoners/Crime Data:
- Read in the prisoners and crime CSV files to preview them
- Dropped the columns to be excluded from the report, also dropped the federal row using .loc so the data only represents states
- Included the columns: State, Year, Prisoner Count, State Population, Violent Crime Total, Property Crime Total 
- Fixed the missing values for New York in 2014 - estimated the values based upon 2014 and 2016 New York data to replace the NaN values 
- Rounded the estimations for State Population, Violent Crime Total, and Property Crime Total

#### Joining the Datasets: 
- Previewed the clean datasets as data frames before joining the education and incarceration datasets
- Merged the education and incarceration data frames on the state and year 
- Output the final report in different formats - CSV and JSON

### Load
- Connected to the local SQL database - which is a relational database (stores data in tables and rows)
- Checked for the tables that were created in SQL using: engine.table_names() 
- Used Pandas to load CSV and JSON converted dataframes into the database
- Final Database: ed_prison_db
- Tables: education_v_incarceration

#### ETL Project Final Report:
https://docs.google.com/document/d/1F5uW7d8O88-X3vW-rHrkhmYFJNhQY3eVxmjDJWpgX4M/edit?usp=sharing
