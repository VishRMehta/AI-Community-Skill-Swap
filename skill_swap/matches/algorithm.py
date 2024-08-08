import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from scipy.spatial.distance import cdist
from users.models import UserProfile

# Initialize Geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to get latitude and longitude from a location name
def get_lat_long(location):
    try:
        location = geolocator.geocode(location)
        return (location.latitude, location.longitude) if location else (None, None)
    except:
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
    # Compute similarity based on skills
    df['combined_features'] = df.apply(lambda row: f"{row['skills_offered']} {row['skills_sought']}", axis=1)
    vectorizer = CountVectorizer().fit_transform(df['combined_features'])
    skill_vectors = vectorizer.toarray()
    skill_similarity = cosine_similarity(skill_vectors)

    # Compute geographical distances
    coords = df[['latitude', 'longitude']].dropna().values
    distances = cdist(coords, coords, metric=lambda u, v: geodesic(u, v).kilometers)

    # Normalize distances and convert them to similarity scores (1 - normalized distance)
    max_distance = distances.max()
    if max_distance > 0:
        geo_similarity = 1 - (distances / max_distance)
    else:
        geo_similarity = distances

    # Combine both skill and geographic similarities
    combined_similarity = skill_similarity * 0.7 + geo_similarity * 0.3

    return combined_similarity

def find_best_matches(user_id, top_n=5):
    profiles_df = get_user_profiles()
    similarity_matrix = compute_similarity_matrix(profiles_df)
    user_idx = profiles_df.index[profiles_df['user_id'] == user_id].tolist()
    if not user_idx:
        return []  # Return empty if no index found
    user_idx = user_idx[0]
    similarity_scores = list(enumerate(similarity_matrix[user_idx]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    best_matches = sorted_scores[1:top_n+1]
    return [profiles_df.iloc[i[0]]['user_id'] for i in best_matches]
