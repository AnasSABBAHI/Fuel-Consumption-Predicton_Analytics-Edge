import os
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj

def process_trajectories(folder_path):
    """
    Processes all trajectory CSV files in a given folder to extract features.

    Args:
        folder_path (str): The relative path to the folder containing trajectory CSVs.

    Returns:
        pd.DataFrame: A DataFrame where each row represents a trajectory with its
                      calculated features (duration, distance, speed, acceleration).
    """
    trajets_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    trajets_data = []

    for traj_file in trajets_files:
        traj_path = os.path.join(folder_path, traj_file)
        df_trajet = pd.read_csv(traj_path)

        if df_trajet.empty:
            continue

        df_trajet['Temps'] = pd.to_datetime(df_trajet['Temps'], format='%Y-%m-%d %H:%M:%S')

        # Characteristic speeds
        vitesse_moyenne = np.mean(df_trajet['Vitesse'])
        vitesse_mediane = np.median(df_trajet['Vitesse'])
        vitesse_maximale = np.max(df_trajet['Vitesse'])

        # Instantaneous acceleration
        df_trajet['Temps_diff'] = df_trajet['Temps'].diff().dt.total_seconds()
        df_trajet['Vitesse_diff'] = df_trajet['Vitesse'].diff()
        df_trajet['Accélération_kmph2'] = (df_trajet['Vitesse_diff'] / df_trajet['Temps_diff']) * 3600
        
        # Characteristic accelerations
        acceleration_moyenne = np.mean(df_trajet['Accélération_kmph2'])
        acceleration_maximale = np.max(df_trajet['Accélération_kmph2'])

        # Total distance
        distance_totale = 0
        for i in range(1, len(df_trajet)):
            point1 = (df_trajet['Latitude'].iloc[i-1], df_trajet['Longitude'].iloc[i-1])
            point2 = (df_trajet['Latitude'].iloc[i], df_trajet['Longitude'].iloc[i])
            distance_totale += geodesic(point1, point2).km

        # Total duration
        temps_total = (df_trajet['Temps'].iloc[-1] - df_trajet['Temps'].iloc[0]).total_seconds() / 60  # in minutes

        trajet_features = {
            'ID': os.path.splitext(traj_file)[0],
            'Duree_mn': temps_total,
            'Distance_km': distance_totale,
            'Vitesse_moy_kmph': vitesse_moyenne,
            'Vitesse_med_kmph': vitesse_mediane,
            'Vitesse_max_kmph': vitesse_maximale,
            'Accélération_moy_kmph2': acceleration_moyenne,
            'Accélération_max_kmph2': acceleration_maximale
        }
        trajets_data.append(trajet_features)

    return pd.DataFrame(trajets_data)

def process_parcels(folder_path):
    """
    Processes all parcel CSV files in a given folder to extract geographic features.

    Args:
        folder_path (str): The relative path to the folder containing parcel CSVs.

    Returns:
        pd.DataFrame: A DataFrame where each row represents a parcel with its
                      calculated features (area, perimeter, complexity).
    """
    def calculate_area_and_perimeter(latitudes, longitudes):
        polygon = Polygon(zip(longitudes, latitudes))
        
        # Define projection
        wgs84 = pyproj.CRS("EPSG:4326")
        utm_zone = int((polygon.centroid.x + 180) // 6) + 1
        utm_crs = pyproj.CRS(f"EPSG:326{utm_zone}")
        
        project = pyproj.Transformer.from_crs(wgs84, utm_crs, always_xy=True).transform
        projected_polygon = transform(project, polygon)
        
        return projected_polygon.area, projected_polygon.length

    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    parcelle_data = []

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            latitudes = df['Latitude'].tolist()
            longitudes = df['Longitude'].tolist()
            
            area, perimeter = calculate_area_and_perimeter(latitudes, longitudes)
            
            parcelle_data.append({
                'Parcelle': os.path.splitext(file_name)[0],
                'Surface_ha': area * 0.0001,  # hectares
                'Perimetre_km': perimeter / 1000,  # kilometers
                'Complexite': len(latitudes)  # Number of vertices
            })

    return pd.DataFrame(parcelle_data)