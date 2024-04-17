import pandas as pd
from sklearn.neighbors import NearestNeighbors
from DBConnection import get_activitywithcategoryview, get_usercategoryrankingview

def recommender_engine(user_id, cf_model):
    user_category_ranking_df = get_usercategoryrankingview()
    activities_df = get_activitywithcategoryview()

    ranking_df = pd.merge(user_category_ranking_df, activities_df, left_on='mainCategoryId', right_on='mainCategoryId')
    ranking_df = ranking_df.drop_duplicates(['userId', 'activityId'])

    user_item_matrix = (ranking_df.pivot(index='userId', columns='activityId', values='categoryRank').fillna(0))

    # Fit model on matrix
    cf_model.fit(user_item_matrix)

    if user_id not in user_item_matrix.index:
        print(f"User ID {user_id} not found in the matrix.")
        return None

    # Use loc instead of iloc to select rows based on index label
    distances, indices = cf_model.kneighbors(user_item_matrix.loc[[user_id]], n_neighbors=10)

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

def get_recommend(user_id):
    cf_knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)
    return recommender_engine(user_id, cf_knn_model)
