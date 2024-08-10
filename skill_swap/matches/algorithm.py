import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from geopy.distance import geodesic
from scipy.spatial.distance import cdist
from users.models import UserProfile
import requests

# OpenCage API key
OPENCAGE_API_KEY = '8fb3dcfa8c644975bc9bae5281adafdf'


def get_lat_long(location):
    try:
        # URL encode the location to handle spaces and special characters
        encoded_location = requests.utils.quote(location)
        response = requests.get(f'https://api.opencagedata.com/geocode/v1/json?q={encoded_location}&key={OPENCAGE_API_KEY}')
        data = response.json()
        
        # Debugging: print the API response
        #print(f"Geocoding API response for '{location}': {data}")
        
        if data['results']:
            coords = data['results'][0]['geometry']
            print(coords)
            return (coords['lat'], coords['lng'])
        else:
            print(f"No results for location '{location}'")
            return (None, None)
    except Exception as e:
        print(f"Error geocoding location '{location}': {e}")
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
    
    # Debugging: print the collected data
    print("User profiles data:")
    print(data)
    
    return pd.DataFrame(data)

def compute_similarity_matrix(df):
    # Compute similarity based on skills
    df['combined_features'] = df.apply(lambda row: f"{row['skills_offered']} {row['skills_sought']}", axis=1)
    vectorizer = CountVectorizer().fit_transform(df['combined_features'])
    skill_vectors = vectorizer.toarray()
    skill_similarity = cosine_similarity(skill_vectors)

    # Compute geographical distances
    coords = df[['latitude', 'longitude']].dropna().values
    if len(coords) == 0:
        print("No coordinates available for similarity calculation.")
        return skill_similarity  # Return only skill similarity

    # Calculate distances and normalize
    distances = cdist(coords, coords, metric=lambda u, v: geodesic(u, v).kilometers)
    max_distance = distances.max() if distances.size > 0 else 1
    geo_similarity = 1 - (distances / max_distance)

    # Apply a distance threshold to penalize far locations
    distance_threshold = 5000  # 5000 kilometers
    geo_similarity[distances > distance_threshold] = 0  # Penalize profiles further than the threshold

    # Debugging outputs
    print(f"Coords: {coords}")
    print(f"Distances: {distances}")
    print(f"Geo Similarity: {geo_similarity}")

    # Ensure geographic similarity does not go below 0
    geo_similarity = geo_similarity.clip(lower=0)

    # Combine both skill and geographic similarities with adjusted weights
    combined_similarity = skill_similarity * 0.5 + geo_similarity * 0.5  # Adjust weights as needed

    return combined_similarity

def find_best_matches(user_id, top_n=5):
    profiles_df = get_user_profiles()
    
    # Check if profiles_df is empty
    if profiles_df.empty:
        print("No profiles available.")
        return []

    similarity_matrix = compute_similarity_matrix(profiles_df)
    
    # Ensure user_id is present in profiles_df
    if user_id not in profiles_df['user_id'].values:
        print(f"User ID {user_id} not found in profiles.")
        return []

    user_idx = profiles_df.index[profiles_df['user_id'] == user_id].tolist()[0]
    similarity_scores = list(enumerate(similarity_matrix[user_idx]))
    
    # Sort by similarity scores, excluding the self-match
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    best_matches = sorted_scores[1:top_n+1]  # Exclude self-matching
    
    return [profiles_df.iloc[i[0]]['user_id'] for i in best_matches]