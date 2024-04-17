import pandas as pd
from sklearn.neighbors import NearestNeighbors
from DBConnection import get_activitywithcategoryview,get_usercategoryrankingview

# Read data
user_ratings_df = get_usercategoryrankingview()
activity_metadata = get_activitywithcategoryview()

# Merge data
activity_data = user_ratings_df.merge(activity_metadata, on='mainCategoryId')

# Check for duplicate entries in merged data
activity_data = activity_data.drop_duplicates(['userId', 'activityId'])

# Pivot operation
user_item_matrix = (activity_data.pivot(index=['userId'], columns=['activityId'], values='categoryRank').fillna(0))

# Define a KNN model on cosine similarity
cf_knn_model= NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)


# Fitting the model on our matrix
cf_knn_model.fit(user_item_matrix)


def activity_recommender_engine(activity_id, cf_model):
    cf_knn_model.fit(user_item_matrix)

    # Assuming 'user_id' is the user ID for which you want to find nearest neighbors
    # Convert the Series returned by iloc into a DataFrame
    user_data = user_item_matrix.iloc[[activity_id]].copy()  # Ensure it's a copy to avoid SettingWithCopyWarning

    # Pass the DataFrame containing a single row to kneighbors method
    distances, indices = cf_model.kneighbors(user_data, n_neighbors=10)

    activity_rec_ids = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])

    # List to store recommendations
    cf_recs = []
    for i in activity_rec_ids:
        cf_recs.append({'activityId': activity_metadata['activityId'].loc[i[0]],
                        'activityName': activity_metadata['activityName'].loc[i[0]],
                        'mainCategory': activity_metadata['mainCategory'].loc[i[0]],
                        'Distance': i[1]})

    # Select top number of recommendations needed
    df = pd.DataFrame(cf_recs, index=range(1, 10+1))
    recommendations = df.to_dict(orient='records')
    print(recommendations)
    return df

activity_recommender_engine(1, cf_knn_model)