import shutil
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt

path = "data/northwind.db"
# save a copy of the file to apply changes
shutil.copy(path, "data/northwind_new.db")

con = sqlite3.connect("data/northwind_new.db")
cur = con.cursor()

# check the tables in the database
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print(tables)

# check the tables using pandas
df_products = pd.read_sql_query("SELECT * FROM Products", con)
print(df_products.head())

df_order_details = pd.read_sql_query("SELECT * FROM [Order Details]", con)
print(df_order_details.head())

# add a new column to the order details table for product names
cur.execute("""ALTER TABLE [Order Details] ADD COLUMN ProductName TEXT""")
cur.execute("""ALTER TABLE [Order Details] ADD COLUMN CompanyName TEXT""")
# update the new columns
new_table = cur.execute("""
    UPDATE [Order Details]
    SET ProductName = (SELECT ProductName FROM Products 
    WHERE Products.ProductID = [Order Details].ProductID),
    CompanyName = (SELECT CompanyName FROM Suppliers
    WHERE [Order Details].ProductID = Suppliers.SupplierID)
""")
print(new_table)

# Check the five most ordered products
df_most_ordered = pd.read_sql_query("""
    SELECT ProductId, ProductName, SUM(Quantity) As TotalQuantity  
    FROM [Order Details]                                 
    GROUP BY ProductId                            
    ORDER BY TotalQuantity DESC
    LIMIT 5
    """, con)
print(df_most_ordered)

# Plot the most ordered products
plt.bar(df_most_ordered['ProductName'], df_most_ordered['TotalQuantity'])
plt.xlabel('Product Name')
plt.ylabel('Total Quantity')
plt.title('Most Ordered Products')
plt.xticks(rotation=45)
plt.ylim(204000, 207000)
plt.tight_layout()
plt.savefig('most_ordered_products.png')
plt.show()

# Check the five most discounted products
df_most_discounted = pd.read_sql_query("""
    SELECT  ProductName, Quantity, SUM(Discount) As TotalDiscount  
    FROM [Order Details]                                 
    GROUP BY ProductId                            
    ORDER BY TotalDiscount DESC
    LIMIT 5
    """, con)
print(df_most_discounted)

# Plot the most discounted products
plt.bar(df_most_discounted['ProductName'], df_most_discounted['TotalDiscount'])
plt.xlabel('Product Name')
plt.ylabel('Total Discount')
plt.title('Most Discounted Products')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('most_discounted_products.png')
plt.show()  

