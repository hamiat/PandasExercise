from faker import Faker
import numpy as np
import pandas as pd

def data_generation_excercise():
    fake = Faker()
    amount_of_data = 50  # Number of records to generate
    df_people = generate_person_data(fake, amount_of_data)
    df_products = generate_product_data(fake, amount_of_data)
    df_trans = generate_transaction_data(fake, df_people, df_products, amount_of_data)

    #Testing missing values/faulty data
    #df_people = introduce_missing_values(df_people, missing_fraction=0.4)
    #df_products = introduce_missing_values(df_products, missing_fraction=0.4)
    df_trans = introduce_missing_values(df_trans, missing_fraction=0.4)
    
    #Remove items (rows) that are missing the following 
    df_people = df_people[df_people["user_id"].notna()]
    df_products = df_products[df_products["product_id"].notna()]
    df_products = df_products[df_products["price"].notna()]
    df_trans = df_trans[df_trans["transaction_id"].notna()]
    df_trans = df_trans[df_trans["user_id"].notna()]
    df_trans = df_trans[df_trans["product_id"].notna()]
    df_trans = df_trans[df_trans["quantity"].notna()]
    
    #Handle items (rows) missing data for the following
    df_people["name"] = df_people["name"].fillna("Unknown").astype(str)
    df_people["email"] = df_people["email"].fillna("No Email").astype(str)
    df_people["sign_up_date"] = df_people["sign_up_date"].fillna(pd.Timestamp("1900-01-01")).astype("datetime64[ns]")
    df_products["product_name"] = df_products["product_name"].fillna(" Product" + df_products["product_id"].astype(str)).astype(str)
    df_products["category"] = df_products["category"].fillna("XXXXX").astype(str)
    df_trans["transaction_date"] = df_trans["transaction_date"].fillna(pd.Timestamp("1900-01-01")).astype("datetime64[ns]")
    
    #Remove duplicates
    df_people = df_people.drop_duplicates()
    df_products = df_products.drop_duplicates()
    df_trans = df_trans.drop_duplicates()
    
    #Testing: confirming data types
    #name_data_type = type(df_people["name"].iloc[0])
    #print("Name data type:", {name_data_type})
    #email_data_type = type(df_people["email"].iloc[0])
    
    #Merging dataframes
    df_trans_people = pd.merge(df_people, df_trans, on="user_id", how="inner") 
    df_all = pd.merge(df_trans_people, df_products, on="product_id", how="inner") 

    #Calculate total spent per user
    #print(df_all["name"]) #print all the user and their transactions 
    for user_id in df_all["name"].unique():
        user_data = df_all[df_all["name"] == user_id]
        total_spent = (user_data["quantity"] * user_data["price"]).sum()
        #print(f"Total spent by {user_id}: ${total_spent:.2f}") #print total spent by each user
    
    #Get the 5 five products and their average price
    top_products = df_all.sort_values(by="price", ascending=False).head(5)
    top_items = top_products[["product_name", "price"]].reset_index(drop=True)
    top_five_mean = top_products["price"].mean()
    print(f"\nTop 5 products by price: {top_items}")
    print(f"\nTop 5 products by price (mean price: ${top_five_mean:.2f}):")

        
def generate_transaction_data(fake: Faker, person: pd.DataFrame, product: pd.DataFrame, amount: int) -> pd.DataFrame:
    transactions = []
    
    for _ in range(amount):
        id = np.random.randint(10000, 99999)
        user_id = person.sample().iloc[0]['user_id']
        product_id = product.sample().iloc[0]['product_id']
        quantity = np.random.randint(1, 100)
        transaction_date = np.datetime64(fake.date_between(start_date='-2y', end_date='today'))
        
        data = {
            "transaction_id": id,
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity,
            "transaction_date": transaction_date,
        }
        transactions.append(data)
        
    return pd.DataFrame(transactions)

def generate_product_data(fake: Faker, amount: int) -> pd.DataFrame:
    products = []
    
    for _ in range(amount):
        id = np.random.randint(1, 100)
        name = fake.word().capitalize() + " " + fake.word().capitalize()
        category = ["Electronics", "Clothing", "Home", "Books", "Toys"]
        price = round(np.random.uniform(10.0, 500.0), 2)
        
        data = {
            "product_id": id,
            "product_name": name,
            "category": np.random.choice(category),
            "price": price,
        }
        products.append(data)
        
    return pd.DataFrame(products)
    

def generate_person_data(fake: Faker, amount: int) -> pd.DataFrame:
    names = []
    people = []
      
    for _ in range(amount):
        first_name = fake.first_name()
        last_name = fake.last_name()
        name = f"{first_name} {last_name}"
        names.append(name)
    
    for name in names:
        fullname = name.replace(" ", "")
        email = f"{fullname.lower()}@fakemail.com"
        sign_up_date = np.datetime64(fake.date_between(start_date='-5y', end_date='-3y'))
        id = np.random.randint(1000, 9999)
        data = {
            "user_id": id,
            "name": name,
            "email": email,
            "sign_up_date": sign_up_date,
        }
        people.append(data)
        
    return pd.DataFrame(people)
    
    
    #This is for testing purposes
def introduce_missing_values(df, missing_fraction=0.2): # Introduce 20% missing values
    df_missing = df.copy()
    total_cells = df_missing.size
    n_missing = int(total_cells * missing_fraction)
        
    for _ in range(n_missing):
        i = np.random.randint(0, df_missing.shape[0])
        j = np.random.randint(0, df_missing.shape[1])
        df_missing.iat[i, j] = np.nan
        
    return df_missing