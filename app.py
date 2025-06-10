import re
import string
import pandas as pd

#1.0 Creating dataframes
def main() -> pd.DataFrame:
    data = {
    "name": ["Hami", "Lami", "Bror", "Snoop", "Santa"],
    "age": [33, 49, 45, 15, 15],
    "score": [200, 20, None, 80, 12000],
    }
    
    data2 ={
    "name": ["Hams", "Lams", "Sis", "Dogg", "Claus"],
    "age": [33, 49, 45, 15, 15],
    "occupation": ["Engineer", "Doctor", "Artist", "Musician", "Teacher"],
    }
    
    data3 = {
        "id" : [1, 2, 3, 4, 5],
        "name": ["Ham", "Lam", "Bro", "Sno", "San"],
        "age": [33, 49, 45, 15, 15],
    }
         
    data4 = {
        "id": [1, 2, 3, 4, 5],
        "occupation": ["Engineer", "Doctor", "Artist", "Musician", "Teacher"],
        "salary": [50000, 60000, 70000, 80000, 90000],
    }
    
    data5 = {
        "birthday": ["1990-01-01", "1980-02-02", "1975-03-03", "2005-04-04", "2010-05-05"],
        "prices": [100.5, 200.75, 300.0, 400.25, 500.0],
    }
    
    df = pd.DataFrame(data)
    
    #3.0 Data type conversion
    df["score"] = pd.to_numeric(df["score"], downcast="float", errors="coerce")
    
    #6.0 Concatenation
    df1 = pd.DataFrame(data)
    df2 = pd.DataFrame(data2)
    frames = [df1, df2]
    concat_df = pd.concat(frames, ignore_index=True)
    #print(concat_df)  
    
    #7.0 Merging
    df3 = pd.DataFrame(data3)
    df4 = pd.DataFrame(data4)
    merged_df = pd.merge(df3, df4, on="id", how="outer")
    #print(merged_df)
    
    #8.0 Datetime manipulation
    df5 = pd.DataFrame(data5)
    datetime_df = pd.to_datetime(df5["birthday"], errors="coerce")
    #print(datetime_df)

    #9.0 Renaming columns
    renamed_df = df5.rename(columns={"birthday": "EventDate", "prices": "EventValue"})
    #print(renamed_df)
    
    #10.0 Unique values
    unique_ages_df = df["age"].unique()
    print(f"Unique ages: {unique_ages_df}")
    
    return df

#2.0 Indexing and slicing
def older_than_twentyfive(df: pd.DataFrame) -> pd.DataFrame:
    older_than_twentyfive = df[df["age"] > 25]
    return older_than_twentyfive  
  
#4.0 Grouping and aggregation
def mean_agegroup(df: pd.DataFrame):
    bins = [0, 18, 120]
    labels = ["Kid", "Adult"]
    df["AgeGroup"] = pd.cut(df["age"], bins=bins, labels=labels)
    mean_age = df.groupby("AgeGroup")["age"].mean().to_list()
    for i in range(len(mean_age)):
        print(f"The mean age for {labels[i]} is: {mean_age[i]}")

#5.0 Handling missing data
def handle_missing_data(df: pd.DataFrame) -> pd.DataFrame: 
   df = df["score"].fillna(df["score"].mean())
   return df

# Exercise 2    
def titanic_data():
    df = pd.read_csv("titanic.csv")
    stuff_to_remove = string.punctuation + string.whitespace
    pattern = f"[{re.escape(stuff_to_remove)}]"
    df.columns = df.columns.str.replace(pattern, "", regex=True)
    print(df)

if __name__ == "__main__":
    df = main()
    older_than_twentyfive = older_than_twentyfive(df)
    handle_missing_data = handle_missing_data(df)
    #print(main())
    #print(older_than_twentyfive)
    #mean_agegroup(df)
    #print(handle_missing_data)
    titanic_data()
   

