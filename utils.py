import os
import pandas as pd
from typing import Tuple
import tempfile
import stat
from git import Repo, GitCommandError
from pathlib import Path
import streamlit as st

def get_git_repo_root():
    repo = Repo(Path(__file__).resolve(), search_parent_directories=True)
    return repo.working_tree_dir  # Absolute path to the repo root

def create_temp_ssh_key_file():
    ssh_key = st.secrets['SSH_PRIVATE_KEY']
    if not ssh_key:
        raise EnvironmentError("Environment variable SSH_PRIVATE_KEY is not set")

    # Create a temporary file for the SSH key
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as key_file:
        key_file.write(ssh_key)
        key_file_path = key_file.name

    os.chmod(key_file_path, stat.S_IRUSR | stat.S_IWUSR)  # chmod 600
    return key_file_path

def git_environment_with_key(ssh_key_path):
    env = os.environ.copy()
    env['GIT_SSH_COMMAND'] = f'ssh -i {ssh_key_path} -o StrictHostKeyChecking=no'
    return env

def git_pull(repo: Repo, env: dict):
    print("Pulling latest changes...")
    try:
        repo.git.pull(env=env)
        print("Pull complete.")
    except GitCommandError as e:
        print(f"Error during pull: {e}")

def git_push(repo: Repo, env: dict, commit_message="Automated commit"):
    print("Staging changes...")
    repo.git.add(all=True)

    if repo.is_dirty(untracked_files=True):
        print("Committing changes...")
        repo.index.commit(commit_message)
        print("Pushing to remote...")
        try:
            repo.git.push(env=env)
            print("Push complete.")
        except GitCommandError as e:
            print(f"Error during push: {e}")
    else:
        print("No changes to commit or push.")

def git_workflow():
    repo_path = get_git_repo_root()
    ssh_key_path = create_temp_ssh_key_file()
    env = git_environment_with_key(ssh_key_path)

    try:
        repo = Repo(repo_path)
        if repo.bare:
            raise ValueError(f"Repository at {repo_path} is bare.")

        # git_pull(repo, env)
        git_push(repo, env)

    finally:
        os.remove(ssh_key_path)


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
