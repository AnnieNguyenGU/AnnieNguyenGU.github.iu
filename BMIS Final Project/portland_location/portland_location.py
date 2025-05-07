import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv("customers_feedback.csv")

# Convert ratings
def convert_star(rating):
    if isinstance(rating, str) and 'Star' in rating:
        return int(rating.split()[0])
    return None

cleanliness_map = {
    'Very Dirty': 1, 'Dirty': 2, 'Neutral': 3,
    'Clean': 4, 'Very Clean': 5
}
experience_map = {
    'Very Bad': 1, 'Bad': 2, 'Neutral': 3,
    'Good': 4, 'Excellent': 5
}
price_map = {
    'Very Cheap': 1, 'Cheap': 2, 'Average': 3,
    'Expensive': 4, 'Very Expensive': 5
}

# Apply mappings
df['Food Rating'] = df['Food Rating'].apply(convert_star)
df['Drink Rating'] = df['Drink Rating'].apply(convert_star)
df['Service Rating'] = df['Service Rating'].apply(convert_star)
df['Cleanliness Rating'] = df['Cleanliness Rating'].map(cleanliness_map)
df['Overall Experience'] = df['Overall Experience'].map(experience_map)
df['Price Rating'] = df['Price Rating'].map(price_map)

# Filter for Portland
portland_df = df[df['Location'] == 'Portland, OR'].copy()

# Experience groups
portland_df['Experience Group'] = portland_df['Overall Experience'].apply(
    lambda x: '1-3 Stars' if x <= 3 else '4-5 Stars'
)

# Clean eating time
portland_df['Eating Time'] = portland_df['Eating Time'].astype(str).replace('', 'Unknown')
eating_order = ['Breakfast', 'Brunch', 'Lunch', 'Dinner', 'Take-Out']

# ========== 1. Average Ratings ==========
avg_ratings = portland_df[[
    'Food Rating', 'Drink Rating', 'Service Rating',
    'Price Rating', 'Cleanliness Rating', 'Overall Experience'
]].mean()

plt.figure(figsize=(8, 6))
sns.barplot(x=avg_ratings.index, y=avg_ratings.values, palette='viridis')
plt.title('Average Ratings Overview - Portland')
plt.ylabel('Average Rating')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("average_ratings_portland.png", bbox_inches="tight")
plt.show()

# ========== 2. Stacked Rating Distribution ==========
rating_columns = ['Food Rating', 'Drink Rating', 'Service Rating', 'Price Rating', 'Cleanliness Rating', 'Overall Experience']
rating_distribution = pd.DataFrame({
    col: portland_df[col].value_counts().sort_index() for col in rating_columns
}).fillna(0).astype(int).T

rating_distribution.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='RdYIGn')
plt.title('Rating Distributions by Category - Portland')
plt.xlabel('Rating Category')
plt.ylabel('Number of Ratings')
plt.legend(title='Stars', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("rating_distribution_portland.png", bbox_inches="tight")
plt.show()

# ========== 3. Stacked Bar by Eating Time ==========
eating_time_counts = pd.crosstab(portland_df['Eating Time'], portland_df['Experience Group']).reindex(eating_order)

eating_time_counts.plot(kind='bar', stacked=True, color=['#FF9999', '#66C2A5'], figsize=(8, 6))
plt.title('Overall Experience by Eating Time (Stacked) - Portland')
plt.xlabel('Eating Time')
plt.ylabel('Number of Feedbacks')
plt.xticks(rotation=45)
plt.legend(title='Rating Group')
plt.tight_layout()
plt.savefig("eating_time_experience_portland.png", bbox_inches="tight")
plt.show()

# ========== 4. Histogram - Party Size vs Experience ==========
plt.figure(figsize=(8, 5))
sns.histplot(data=portland_df, x='Overall Experience', hue='Party Size', multiple='dodge', shrink=0.8, bins=5)
plt.title('Experience Rating Distribution by Party Size - Portland')
plt.xlabel('Overall Experience')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("party_size_experience_portland.png", bbox_inches="tight")
plt.show()

# ========== 5. Histogram - Price Rating vs Experience ==========
plt.figure(figsize=(8, 5))
sns.histplot(data=portland_df, x='Overall Experience', hue='Price Rating', multiple='dodge', shrink=0.8, bins=5)
plt.title('Experience Rating Distribution by Price Rating - Portland')
plt.xlabel('Overall Experience')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("price_rating_experience_portland.png", bbox_inches="tight")
plt.show()

