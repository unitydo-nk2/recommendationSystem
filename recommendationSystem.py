import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process

user_category_ranking_df = pd.read_csv(os.getcwd()+"/userCategoryRank.csv")
activities_df = pd.read_csv(os.getcwd()+"/activityWithCategoryView.csv")

ranking_df = pd.merge(user_category_ranking_df, activities_df, left_on='mainCategoryId', right_on='mainCategoryId')
ranking_df = ranking_df.drop_duplicates(['userId', 'activityId'])

user_item_matrix = (ranking_df.pivot(index=['userId'], columns=['activityId'], values='categoryRank').fillna(0)
                    .transpose())

# cosine similarity
# Define a KNN model on cosine similarity
cf_knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)

# Fitting the model on our matrix
cf_knn_model.fit(user_item_matrix)


def recommender_engine(user_id):
    # Fit model on matrix
    cf_knn_model.fit(user_item_matrix)

    # Check if the user ID exists in the index of the matrix
    if user_id not in user_item_matrix.columns:
        print(f"User ID {user_id} not found in the matrix.")
        return None

    # Calculate neighbor distances based on user preferences
    distances, indices = cf_knn_model.kneighbors(user_item_matrix.loc[:, user_id].values.reshape(1, -1), n_neighbors=10)

    user_rec_ids = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])

    # List to store recommendations
    cf_recs = []
    for i in user_rec_ids:
        cf_recs.append({'activityId': activities_df['activityId'].loc[i[0]],
                        'activityName': activities_df['activityName'].loc[i[0]],
                        'mainCategory': activities_df['mainCategory'].loc[i[0]],
                        'Distance': i[1]})

    # Select top number of recommendations needed
    df = pd.DataFrame(cf_recs, index=range(1, 10 + 1))
    recommendations = df.to_dict(orient='records')
    return recommendations

