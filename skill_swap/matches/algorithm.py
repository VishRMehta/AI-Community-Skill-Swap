import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from geopy.distance import geodesic
from scipy.spatial.distance import cdist
from users.models import UserProfile
import requests
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
# OpenCage API key
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')

def get_lat_long(location):
    try:
        encoded_location = requests.utils.quote(location)
        response = requests.get(f'https://api.opencagedata.com/geocode/v1/json?q={encoded_location}&key={OPENCAGE_API_KEY}')
        data = response.json()
        
        if data['results']:
            coords = data['results'][0]['geometry']
            return (coords['lat'], coords['lng'])
        else:
            return (None, None)
    except Exception as e:
        return (None, None)

def get_user_profiles():
    profiles = UserProfile.objects.all()
    data = []
    
    for profile in profiles:
        lat, long = get_lat_long(profile.location)
        data.append({
            'user_id': profile.user.id,
            'skills_offered': ' '.join([skill.name for skill in profile.skills_offered.all()]),
            'skills_sought': ' '.join([skill.name for skill in profile.skills_sought.all()]),
            'location': profile.location,
            'latitude': lat,
            'longitude': long,
        })
    
    return pd.DataFrame(data)

def compute_similarity_matrix(df):
    # TF-IDF for skill similarity
    df['combined_features'] = df.apply(lambda row: f"{row['skills_offered']} {row['skills_sought']}", axis=1)
    vectorizer = TfidfVectorizer().fit_transform(df['combined_features'])
    skill_similarity = cosine_similarity(vectorizer)
    
    # Normalize skill similarity between 0 and 1
    skill_similarity = (skill_similarity - skill_similarity.min()) / (skill_similarity.max() - skill_similarity.min())
    
    # Geographical similarity based on distance
    coords = df[['latitude', 'longitude']].dropna().values
    if len(coords) == 0:
        return skill_similarity
    
    distances = cdist(coords, coords, metric=lambda u, v: geodesic(u, v).kilometers)
    max_distance = distances.max() if distances.size > 0 else 1
    geo_similarity = 1 - (distances / max_distance)
    
    # Penalize distances beyond the threshold
    distance_threshold = 2000  # 2000 kilometers
    geo_similarity[distances > distance_threshold] = 0
    
    # Normalize geo similarity between 0 and 1
    geo_similarity = (geo_similarity - geo_similarity.min()) / (geo_similarity.max() - geo_similarity.min())
    
    # Adjust weighting between skills and geography
    skill_weight = 1.5
    geo_weight = 1.1
    combined_similarity = (skill_similarity * skill_weight) + (geo_similarity * geo_weight)
    
    return combined_similarity

def find_best_matches(user_id, top_n=5, similarity_threshold=1.1):
    profiles_df = get_user_profiles()

    # Debugging: Log the profiles DataFrame
    print(f"Profiles DataFrame:\n{profiles_df}")

    if profiles_df.empty:
        print("No profiles available.")
        return []

    if user_id not in profiles_df['user_id'].values:
        print(f"User ID {user_id} not found in profiles.")
        return []

    similarity_matrix = compute_similarity_matrix(profiles_df)

    user_idx = profiles_df.index[profiles_df['user_id'] == user_id].tolist()[0]
    similarity_scores = list(enumerate(similarity_matrix[user_idx]))
    
    # Filter out matches with similarity score <= similarity_threshold and exclude the user's own profile
    filtered_scores = [score for score in similarity_scores if score[1] > similarity_threshold and score[0] != user_idx]
    
    # Sort by similarity score in descending order
    sorted_scores = sorted(filtered_scores, key=lambda x: x[1], reverse=True)

    # Debugging: Log similarity scores
    print(f"Similarity Scores for user_id {user_id}: {similarity_scores}")
    print(f"Filtered and sorted matches: {sorted_scores}")

    best_matches = sorted_scores[:top_n]  # Get the top N matches

    # Debugging: Log the best matches found
    print(f"Best matches found: {best_matches}")

    return [profiles_df.iloc[i[0]]['user_id'] for i in best_matches]

