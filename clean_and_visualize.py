import pandas as pd
import matplotlib.pyplot as plt

messy = pd.DataFrame({
    "product": ["Widget A", "Widget B", "widget a", "Widget C", "Widget B",
                "Widget A", " Widget C", "Widget D", None, "Widget A"],
    "sales": ["150", "200", "175", "300", "200",
              "180", "250", "abc", "100", "-50"],
    "date": ["2025-01-01", "2025-01-01", "2025-01-02", "2025-01-02", "2025-01-03",
             "2025-01-03", "2025-01-04", "2025-01-04", "2025-01-05", "2025-01-05"],
    "region": ["North", "South", "north", "East", "South",
               "West", "east", "North", "South", "West"],
})

df = pd.DataFrame(messy)
print("=== Raw Data ===")
print(df)
print(f"\nShape: {df.shape}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# Standardize names/regions
df["product"] = df["product"].str.strip().str.title()
df["region"] = df["region"].str.strip().str.title()

# Convert types
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Handle missing/invalid values
# Removed rows that contained missing values to keep the data consitant and reliable
df.loc[df["sales"] < 0, "sales"] = pd.NA
df = df.dropna(subset=["product", "sales"])

print("\n=== Clean Data ===")
print(df)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Chart 1: Total Sales by Product
product_sales = df.groupby("product")["sales"].sum()
axes[0].bar(product_sales.index, product_sales.values, color="deepskyblue")
axes[0].set_title("Total Sales by Product")
axes[0].set_ylabel("Sales ($)")
axes[0].tick_params(axis="x", rotation=45)

# Chart 2: Daily Trend
daily_sales = df.groupby("date")["sales"].sum().sort_index()
axes[1].plot(daily_sales.index.strftime("%b %d"), daily_sales.values, marker="o",color="forestgreen", linewidth=2)
axes[1].set_title("Daily Trend")
axes[1].set_xlabel("Date")
axes[1].set_ylabel("Sales ($)")
axes[1].tick_params(axis="x", rotation=45)

# Chart 3: Distribution
df["sales"].hist(ax=axes[2], bins=5, color="orangered", edgecolor="black")
axes[2].set_title("Distribution")
axes[2].set_xlabel("Sales ($)")
axes[2].set_ylabel("Frequency")

plt.tight_layout()
plt.savefig("Clean and Visualize.png", dpi=150)
plt.show()