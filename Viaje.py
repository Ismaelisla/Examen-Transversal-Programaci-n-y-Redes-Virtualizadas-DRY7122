from geopy.distance import distance
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geopy.units
import textwrap

def obtener_coordenadas(ciudad):
    geolocator = Nominatim(user_agent="mi_app")
    try:
        location = geolocator.geocode(ciudad)
        return (location.latitude, location.longitude)
    except GeocoderTimedOut:
        print(f"No se pudo obtener la ubicación de {ciudad}.")
        return None

def calcular_distancia_y_tiempo(origen, destino):
    coords_origen = obtener_coordenadas(origen)
    coords_destino = obtener_coordenadas(destino)
    
    if coords_origen and coords_destino:
        dist_millas = distance(coords_origen, coords_destino).miles
        dist_kms = distance(coords_origen, coords_destino).kilometers
        
        # Suponiendo una velocidad promedio de 60 km/h
        tiempo_horas = dist_kms / 60
        
        return dist_millas, dist_kms, tiempo_horas
    else:
        return None, None, None

def obtener_medio_de_transporte():
    while True:
        medio = input("Elige el tipo de medio de transporte (auto, avión, tren, bus): ").lower()
        if medio in ['auto', 'avión', 'tren', 'bus']:
            return medio
        else:
            print("Opción no válida. Inténtalo de nuevo.")

def main():
    while True:
        ciudad_origen = input("Ingrese la ciudad de origen en español (Chile): ")
        if ciudad_origen.lower() == 's':
            print("¡Hasta luego!")
            break
        
        ciudad_destino = input("Ingrese la ciudad de destino en español (Argentina): ")
        if ciudad_destino.lower() == 's':
            print("¡Hasta luego!")
            break
        
        dist_millas, dist_kms, tiempo_horas = calcular_distancia_y_tiempo(ciudad_origen, ciudad_destino)
        
        if dist_kms is None:
            print("No se pudo calcular la distancia. Por favor verifica las ciudades ingresadas.")
            continue
        
        medio_transporte = obtener_medio_de_transporte()
        
        # Narrativa del viaje
        narrativa = textwrap.fill(f"Viajar desde {ciudad_origen} a {ciudad_destino} en {medio_transporte} tomará aproximadamente {tiempo_horas:.1f} horas. La distancia es de {dist_millas:.1f} millas o {dist_kms:.1f} kilómetros.", width=70)
        
        print(narrativa)
        print()
    
if __name__ == "__main__":
    main()
