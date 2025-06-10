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
    # Reading the Titanic dataset
    df = pd.read_csv("titanic.csv")
    
    # Removing stuff from column names
    stuff_to_remove = string.punctuation + string.whitespace
    pattern = f"[{re.escape(stuff_to_remove)}]"
    df.columns = df.columns.str.replace(pattern, "", regex=True)
    
    # Renaming columns for children
    df.loc[df["Age"] < 18, "Sex"] = "child"
    #print(df)
    
    # Grouping and calculating mean fare
    df2 = df.copy()  
    df2_mean = df2.groupby("Sex")["Fare"].mean()
    #print(df2_mean)
    
    # Grouping and calculating mean fare and class
    df3 = df.copy()  
    df3_mean = df3.groupby(["Sex", "Pclass"])["Fare"].mean().reset_index()
    #print(df3_mean)
    
    # Grouping and calculating mean fare, class for survivors
    df4 = df.copy()
    df4_mean = df4[df4["Survived"] == 1].groupby("Survived")["Fare"].mean().reset_index()
    #print(df4_mean)
    
    #Split DataFrames
    df5 = df.copy()
    split_df_by_sex = dict(tuple(df.groupby("Sex")))
    #print(split_df_by_sex)
    
    #People with any relatives aboard
    df6 = df.copy()
    ppl_with_relatives =  (df6["SiblingsSpousesAboard"] > 0) | (df6["ParentsChildrenAboard"] > 0)
    df6 = df6[ppl_with_relatives][["Pclass", "Name", "Age", "SiblingsSpousesAboard", "ParentsChildrenAboard"]]
    #print(df6)
    
    #People with both parents and children aboard
    df7 = df.copy()
    ppl_with_parents_children_aboard = (df7["ParentsChildrenAboard"] > 0) & (df7["SiblingsSpousesAboard"] > 0)
    df7 = df7[ppl_with_parents_children_aboard][["Pclass", "Name", "Age", "SiblingsSpousesAboard", "ParentsChildrenAboard", "Fare"]]
 
    df7_mean = df7["Fare"].mean()
    print(df7_mean)
    
    
    
    
    
if __name__ == "__main__":
    df = main()
    older_than_twentyfive = older_than_twentyfive(df)
    handle_missing_data = handle_missing_data(df)
    #print(main())
    #print(older_than_twentyfive)
    #mean_agegroup(df)
    #print(handle_missing_data)
    titanic_data()
   

