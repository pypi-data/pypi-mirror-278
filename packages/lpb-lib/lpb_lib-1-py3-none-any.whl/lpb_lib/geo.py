import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import json


def reverse_geocode(lat, lon, details=False, municipality=False):
    """
    Cette fonction permet de faire une recherche inversée à partir des coordonnées géographiques
    On utilise l'API de geopy pour effectuer cette recherche
    Args:
        lat: float, latitude
        lon: float, longitude
    Returns:
        postal_code: str, code postal
        option - municipality: str, nom de la commune. default False
        option - details: bool, retourner les détails. default False

    """
    # Créer un objet Nominatim pour effectuer des recherches inversées
    geolocator = Nominatim(user_agent="geoapiExercice")
    geolocator.timeout = 10

    location = geolocator.reverse([lat, lon])
    if location.raw['address']['postcode']:
        details = location.raw['address']
        municipality = location.raw['address']['municipality']
        postal_code = location.raw['address']['postcode']
        if details and municipality:
            return municipality, details, postal_code
        elif details:
            return details, postal_code
        elif municipality:
            return municipality, postal_code
        else:
            return postal_code
    else:
        return None

def read_geo_json_file(path):
    """
    Cette fonction permet de lire un fichier GeoJSON et de retourner le contenu.
    Pour obtenir un fichier facilement, on peut utiliser le site https://www.geoportail.gouv.fr/carte
    Puis Outils -> Mesures -> Calculer un isochrone 
    Args:
        path: str, chemin du fichier GeoJSON
    Returns:
        poly: dict, contenu du fichier GeoJSON
    """

    # Charger le contenu du fichier JSON
    with open(path) as f:
        data = json.load(f)

    # Accéder à l'élément polygon
    poly = data['features'][0]['geometry']['coordinates']  
    return poly

def postalcode_from_geojson_file(path, limit=20, municipality=False, details=False, echo = False):
    """
    Cette fonction retourne les codes postaux à partir d'un fichier GeoJSON.
    Args:
        path: str, chemin du fichier GeoJSON
        limit: int, nombre de codes postaux à retourner, default 20
        option - municipality: bool, retourner le nom de la commune, default False
        option - details: bool, retourner les détails, default False
        option - echo: bool, print les résultats, default False
        option - unique: bool, retourner les valeurs uniques, default False
        Returns:
        liste_postal : list, liste des codes postaux
        option - liste_municipality : list, liste des noms de communes
        option - liste_details : list, liste des détails
        order - municipality, details, postal
    """
    poly = read_geo_json_file(path)    
    list_postal = []
    list_municipality = []
    list_details = []

    i=0
    for elts in poly:
        for point in elts: 
            if i > limit:
                break
            else:
                municipality, details, postal_code = reverse_geocode(
                point[1], 
                point[0], 
                details = True,
                municipality = True)
            list_postal.append(postal_code)
            list_municipality.append(municipality)
            list_details.append(details)
            if echo:
                print(f"Details: {details}")
            i=i+1
    if details and municipality:
        return list_municipality, list_details, list_postal
    elif details:
        return list_details, list_postal
    elif municipality:
        return list_municipality, list_postal
    else:
        return list_postal