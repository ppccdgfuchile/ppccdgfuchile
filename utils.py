import os
import pandas as pd
from typing import Tuple


def usuarios_qqcc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Control de calidad de un dataframe de usuarios. Funciones:

    Convierte las columnas 'Latitud' y 'Longitud' de un DataFrame desde 
    representaciones de cadenas con comas como separadores decimales a valores 
    de tipo float.

    Args:
        df (pd.DataFrame): DataFrame de entrada que contiene las columnas 
        'Latitud' y 'Longitud' con valores en formato de cadena.

    Returns:
        pd.DataFrame: Un nuevo DataFrame con las columnas 'Latitud' y 'Longitud' 
        convertidas a valores de tipo float.
    """
    df = df.copy()
    df['Latitud'] = df['Latitud'].map(
        lambda s: float(str(s).replace(',', '.')))
    df['Longitud'] = df['Longitud'].map(
        lambda s: float(str(s).replace(',', '.')))
    return df


def eventos_qqcc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Control de calidad de un dataframe de eventos. Funciones:

    Convierte las columnas 'Latitud' y 'Longitud' de un DataFrame desde 
    representaciones de cadenas con comas como separadores decimales a valores 
    de tipo float.

    Args:
        df (pd.DataFrame): DataFrame de entrada que contiene las columnas 
        'Latitud' y 'Longitud' con valores en formato de cadena.

    Returns:
        pd.DataFrame: Un nuevo DataFrame con las columnas 'Latitud' y 'Longitud' 
        convertidas a valores de tipo float.
    """
    df = df.copy()
    df['Latitud'] = df['Latitud'].map(
        lambda s: float(str(s).replace(',', '.')))
    df['Longitud'] = df['Longitud'].map(
        lambda s: float(str(s).replace(',', '.')))
    return df


def recolectar_eventos() -> Tuple[pd.DataFrame, int]:
    """
    Recolecta los archivos de eventos desde una carpeta específica, los procesa
    para generar nombres legibles y los organiza en un DataFrame. La función
    busca en la carpeta 'eventos' los archivos disponibles. Si la carpeta no
    existe o está vacía, retorna un DataFrame vacío con columnas predefinidas.
    En caso contrario, procesa los nombres de los archivos para generar nombres
    legibles y retorna un DataFrame con esta información junto con la cantidad
    de eventos encontrados.

    Args:
        No recibe argumentos.

    Returns:
        tuple:
            - pd.DataFrame: Un DataFrame con dos columnas:
                - 'Evento': Nombres de los archivos de eventos.
                - 'name': Nombres procesados y legibles de los eventos.
            - int: Cantidad de eventos encontrados en la carpeta.
    """

    events_path = 'eventos'
    if not os.path.exists(events_path) or not os.listdir(events_path):
        # Si no hay eventos, retornar un dataframe vacío con las columnas
        # esperadas
        return pd.DataFrame(columns=['Evento', 'Nombre']), 0

    events = sorted(os.listdir(events_path), reverse=True)
    events_names = [e.split('.')[0].replace('-', '/').replace('_', ' - ')
                    for e in events]
    df = pd.DataFrame({'Evento': events, 'Nombre': events_names})
    return df, len(events)


def cargar_parametros_visualizacion(target_event_name: str) -> dict:
    """
    Carga los parámetros de visualización desde un archivo CSV para un evento
    específico.

    Args:
        target_event_name (str): Nombre del evento para el cual se cargarán
        los parámetros de visualización.

    Returns:
        dict: Un diccionario con los parámetros de visualización, incluyendo:
            - 'vmin': Valor mínimo para la escala de colores.
            - 'vmax': Valor máximo para la escala de colores.
            - 'vstep': Paso para la escala de colores.
            - 'escala_puntos': Escala para los puntos.
    """
    visparams_path = 'visparams/visparams.csv'
    parametros_vis = pd.read_csv(visparams_path, index_col=0)
    parametros_vis = parametros_vis.loc[target_event_name]
    return {
        'vmin': parametros_vis.ColorMin,
        'vmax': parametros_vis.ColorMax,
        'vstep': parametros_vis.ColorPaso,
        'escala_puntos': parametros_vis.Escala,
        'PaletaColores': parametros_vis.PaletaColores,
        'MapaFondo': parametros_vis.MapaFondo
    }
