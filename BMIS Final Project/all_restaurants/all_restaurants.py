import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("customers_feedback.csv")

# Convert star ratings to numbers
def convert_star(rating):
    if isinstance(rating, str) and 'Star' in rating:
        return int(rating.split()[0])
    return None

# Map other categorical ratings to numbers
price_map = {
    'Very Cheap': 1,
    'Cheap': 2,
    'Average': 3,
    'Expensive': 4,
    'Very Expensive': 5
}
cleanliness_map = {
    'Very Dirty': 1,
    'Dirty': 2,
    'Neutral': 3,
    'Clean': 4,
    'Very Clean': 5
}
experience_map = {
    'Very Bad': 1,
    'Bad': 2,
    'Neutral': 3,
    'Good': 4,
    'Excellent': 5
}

# Apply conversions
df['Food Rating'] = df['Food Rating'].apply(convert_star)
df['Drink Rating'] = df['Drink Rating'].apply(convert_star)
df['Service Rating'] = df['Service Rating'].apply(convert_star)
df['Price Rating'] = df['Price Rating'].map(price_map)
df['Cleanliness Rating'] = df['Cleanliness Rating'].map(cleanliness_map)
df['Overall Experience'] = df['Overall Experience'].map(experience_map)

# Define custom order and colors
location_order = ['Seattle, WA', 'Portland, OR', 'Boise, ID', 'Denver, CO']
colors = {
    'Seattle, WA': 'tab:blue',
    'Portland, OR': 'tab:green',
    'Boise, ID': 'tab:orange',
    'Denver, CO': 'tab:red'
}

# Group and average ratings
avg = df.groupby("Location")[[
    "Food Rating", "Drink Rating", "Service Rating", "Price Rating",
    "Cleanliness Rating", "Overall Experience"
]].mean().reindex(location_order)

# Plotting loop
for col in avg.columns:
    plt.figure(figsize=(8, 6))
    bars = plt.bar(avg.index, avg[col], color=[colors[loc] for loc in avg.index])
    plt.title(f'{col} by Location')
    plt.ylabel("Average Rating")
    plt.xticks(rotation=45)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f'{yval:.2f}', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(f"{col.replace(' ', '_').lower()}_rating.png")
    plt.show()
