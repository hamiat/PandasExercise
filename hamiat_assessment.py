import pandas as pd

def main_assessment():
    df = pd.read_csv("assessment.csv")
    df = df[["Category", "Material", "Price"]]
    df = df.rename(columns={"Price": "AveragePrice"})
    df = df[df["AveragePrice"].notna()]
    df = df.sort_values(by=["Category", "Material"]).reset_index(drop=True)  
    
    df["Category"] = df["Category"].str.replace(r"&", "", regex=True)
    df["Category"] = df["Category"].str.replace(r" ", "", regex=True)
    
    df = df.groupby(["Category", "Material"])["AveragePrice"].mean().reset_index()
    df = df.round({"AveragePrice": 2})
    print("\nResult:")
    print(df)
    
def additional_task():
    df = pd.read_csv("assessment.csv")
    df = df[df["Price"].notna()]
    df["lowquality"] = df["Rating (out of 5)"] <= 2
    average_total_price = df["Price"].mean()
    average_lowquality_price = df.loc[df["lowquality"] == True, "Price"].mean()
    average_highquality_price = df.loc[df["lowquality"] == False, "Price"].mean()
    
    print("\n--------------------")
    print("\nAverage prices by quality:")
    print(f"\nTotal average price: ${average_total_price:.2f}")
    print(f"Average price of low quality items: ${average_lowquality_price:.2f}")
    print(f"Average price of high quality items: ${average_highquality_price:.2f}\n")
    print(f"The low quality items are in average ({round(average_lowquality_price - average_total_price, 2)} eur) more expensive than the total average price.\nThe high quality items are in average ({round(average_total_price - average_highquality_price, 2)} eur) cheaper than the total average price.\n")
    
    #print(df)
    df_most_lowquality_category = df[df["lowquality"] == True].groupby("Category")["Price"].sum().nlargest(n=1)
    print(f"The category with the most low quality rows is: \n{df_most_lowquality_category.to_string(header=False)}")

if __name__ == "__main__":
    main_assessment()
    additional_task()