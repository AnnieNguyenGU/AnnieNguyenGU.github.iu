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


# ========== 2. Stacked Rating Distribution ==========
rating_columns = ['Food Rating', 'Drink Rating', 'Service Rating', 'Price Rating', 'Cleanliness Rating', 'Overall Experience']
rating_distribution = pd.DataFrame({
    col: portland_df[col].value_counts().sort_index() for col in rating_columns
}).fillna(0).astype(int).T

rating_distribution.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='RdYlGn')
plt.title('Rating Distributions by Category - Portland')
plt.xlabel('Rating Category')
plt.ylabel('Number of Ratings')
plt.legend(title='Stars', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("rating_distribution_portland.png", bbox_inches="tight")
plt.show()

