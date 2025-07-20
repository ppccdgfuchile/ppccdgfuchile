import os
import sys
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import numpy as np
import pandas as pd
from datetime import datetime
from utils import recolectar_eventos, eventos_qqcc, usuarios_qqcc
from utils import git_workflow, git_rm
import time

sys.path.append('../.')

st.set_page_config(page_title='Pluviómetros Ciudadanos DGF', layout="wide")
st.sidebar.image(os.path.join("static", "logo_ppcc.png"),
                 use_container_width=True)

# ----------------------------------- Login ---------------------------------- #
with open(os.path.join('.', 'admins.yaml')) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

try:
    login = authenticator.login()
except Exception as e:
    st.error(e)
    st.stop()

# ----------------------------------- funcs ---------------------------------- #


def cargar_usuarios(sheet=None) -> tuple:
    """
    Carga un archivo CSV con información de usuarios o crea un archivo vacío si
    no existe.

    Args:
        sheet (Optional[UploadedFile]): Archivo cargado por el usuario que 
        contiene información de usuarios. Puede ser un archivo CSV o Excel. 
        Si es None, se cargará el archivo 'usuarios.csv' existente o se 
        creará uno vacío.

    Returns:
        tuple:
            - pd.DataFrame: Un DataFrame que contiene la información de los 
              usuarios con las siguientes columnas:
                - Nombre: Nombre del usuario.
                - Correo: Dirección de correo electrónico del usuario.
                - Comuna: Comuna de residencia del usuario.
                - Latitud: Latitud de la ubicación del usuario.
                - Longitud: Longitud de la ubicación del usuario.
                - Alias: Alias o apodo del usuario.
                - Actividad: Actividad principal del usuario.
                - Telefono: Número de teléfono del usuario.
                - Grupo: Grupo al que pertenece el usuario.
            - str: Ruta del archivo CSV donde se almacenan los datos de
                   usuarios.
    """
    udf_path = os.path.join('.', 'usuarios', 'usuarios.csv')
    if sheet is None:
        if os.path.isfile(udf_path):
            udf = pd.read_csv(udf_path, index_col=0)
        else:
            udf = pd.DataFrame(columns=["Nombre", "Correo", "Comuna",
                                        "Latitud", "Longitud", "Alias",
                                        "Actividad", "Telefono", "Grupo"])
            udf.to_csv(udf_path)
        return udf, udf_path
    else:
        fname = sheet.name
        if fname.split('.')[-1] == 'csv':
            udf = pd.read_csv(sheet)
        elif fname.split('.')[-1] in ['xls', 'xlsx']:
            udf = pd.read_excel(sheet)
        else:
            st.error(f'{fname} debe ser una planilla excel o csv!')
        return udf, udf_path


def cargar_visparams():
    """
    Carga un archivo CSV con parámetros de visualización o crea un archivo 
    vacío si no existe.

    Returns:
        pd.DataFrame: Un DataFrame que contiene los parámetros de 
        visualización.
    """
    visparams_path = os.path.join('visparams', 'visparams.csv')
    if os.path.isfile(visparams_path):
        visparams = pd.read_csv(visparams_path, index_col=0)
    else:
        visparams = pd.DataFrame(columns=["Eventos", "ColorMin", "ColorMax",
                                          "ColorPaso", "Escala",
                                          "PaletaColores", "MapaFondo"])
        visparams.loc['default'] = [70, 100, 10, 10, "YlGnBu_09", "Satelite"]
        visparams.to_csv(visparams_path)
    visparams = visparams.sort_index(ascending=False)
    return visparams, visparams_path


def gestionar_usuarios(st):
    """    
    Permite gestionar los usuarios registrados en la aplicación. Incluye la 
    funcionalidad de visualizar, editar y actualizar los datos de los usuarios, 
    así como cargar una nueva planilla de usuarios.
        st (Streamlit): Objeto de Streamlit utilizado para renderizar la 
        interfaz de usuario y manejar eventos.
    """
    def _update():
        st.success('Actualización exitosa!')
        udf_edit.reset_index(inplace=True, drop=True)
        udf_edit.to_csv(udf_path)
        git_workflow()

    udf, udf_path = cargar_usuarios()
    _update = st.button("Actualizar", on_click=_update,
                        key='data_update_users')
    udf_edit = st.data_editor(udf, use_container_width=True,
                              num_rows='dynamic', key='data_edit_users')
    sheet = st.file_uploader('Cargar planilla de usuarios...',
                             key='users_update')
    if sheet is not None:
        udf, _ = cargar_usuarios(sheet)
        if st.button("Actualizar registro de usuarios"):
            try:
                udf = usuarios_qqcc(udf)
                udf.to_csv(udf_path)
                st.success('Archivo usuarios.csv creado !')
                st.rerun()
            except Exception as e:
                st.warning('No se pudo crear el archivo !')
                st.error(f'Error: {e}')


def gestionar_visparams(st):
    """
    Gestiona los parámetros de visualización (visparams) mediante una 
    interfaz interactiva.
        st (Streamlit): Objeto de Streamlit utilizado para renderizar 
        componentes en la interfaz de usuario.
    """
    visparams, visparams_path = cargar_visparams()

    def _update():
        visparams_edit.to_csv(visparams_path)
        git_workflow()

    _update = st.button(
        "Actualizar", on_click=_update, key='visparams_update')
    visparams_edit = st.data_editor(visparams, use_container_width=True,
                                    num_rows='dynamic',
                                    key='visparams_edit')


def gestionar_eventos(st):
    """
    Permite gestionar los eventos registrados en la aplicación. Incluye la 
    funcionalidad de visualizar y editar los datos de un evento seleccionado.

    Args:
        st (Streamlit): Objeto de Streamlit utilizado para renderizar la 
        interfaz de usuario y manejar eventos.
    """
    def _update():
        edf_edit.reset_index(inplace=True, drop=True)
        edf_edit.index.name = 'index'
        edf_edit.to_csv(event_path)
        git_workflow()

    df_eventos, n_eventos = recolectar_eventos()
    eventos = df_eventos['Evento'].tolist()
    nombres = df_eventos['Nombre'].tolist()

    event = st.selectbox('Seleccione el evento a visualizar', nombres)
    event_path = eventos[nombres.index(event)]
    event_path = os.path.join('.', 'eventos', f'{event_path}')
    edf = pd.read_csv(event_path, index_col=0)

    _update = st.button("Actualizar", on_click=_update,
                        key='data_update_event')
    edf_edit = st.data_editor(edf, use_container_width=True,
                              num_rows='dynamic', key='data_edit_event')


def agregar_evento(st):
    """
    Permite agregar un nuevo evento a la base de datos.

    Args:
        st (Streamlit): Objeto de Streamlit utilizado para renderizar 
        elementos de la interfaz de usuario.

    Funcionalidad:
        - Permite seleccionar una fecha para el evento.
        - Permite cargar un archivo CSV o Excel con los datos del evento.
        - Valida el formato del archivo cargado.
        - Guarda los datos del evento en un archivo CSV en la carpeta 'eventos'.
        - Actualiza los parámetros de visualización con el nuevo evento.
        - Muestra un mensaje de éxito al finalizar la carga.
        - Maneja errores y muestra mensajes de advertencia en caso de fallos.
    """
    d = st.date_input("Fecha del evento a añadir:",
                      (datetime.today(), datetime.today()))
    event_name = '_'.join([dd.strftime('%F') for dd in d])
    sheet = st.file_uploader('Cargar planilla de registros...')
    if sheet is not None:
        fname = sheet.name
        if fname.split('.')[-1] == 'csv':
            edf = pd.read_csv(sheet)
        elif fname.split('.')[-1] in ['xls', 'xlsx']:
            edf = pd.read_excel(sheet)
        else:
            st.error(f'{fname} debe ser una planilla excel o csv!')

        if st.button("Agregar a la base de datos"):
            try:
                edf = eventos_qqcc(edf)
                edf.to_csv(os.path.join('eventos', f'{event_name}.csv'))

                visparams, visparams_path = cargar_visparams()
                visparams.loc[event_name] = np.nan
                visparams.to_csv(visparams_path)
                git_workflow()
                text = f'{event_name.replace('-', '/').replace('_', ' - ')}'
                text = f"Evento del {text} ha sido creado!"
                st.success(text)
            except Exception as e:
                st.warning(f'No se pudo crear el evento {event_name}!')
                st.error(f'Error: {e}')


def eliminar_evento(st):
    """
    Permite eliminar un evento de la base de datos.
    st (Streamlit): Objeto de Streamlit utilizado para renderizar 
    elementos de la interfaz de usuario.
    Funcionalidad:
        - Muestra un cuadro de selección con los nombres de los eventos 
          disponibles.
        - Elimina el archivo asociado al evento seleccionado.
        - Actualiza los parámetros de visualización eliminando la entrada 
          correspondiente.
        - Muestra un mensaje de advertencia confirmando la eliminación.
        - Recarga la aplicación para reflejar los cambios.
    """
    df_eventos, n_eventos = recolectar_eventos()
    eventos = df_eventos['Evento'].to_list()
    nombres = df_eventos['Nombre'].to_list()

    event = st.selectbox('Seleccione el evento a eliminar',
                         nombres, key='eliminarevento')
    event_fname = eventos[nombres.index(event)]
    event_path = os.path.join('.', 'eventos', f'{event_fname}')
    if st.button("Eliminar"):
        visparams, visparams_path = cargar_visparams()
        visparams.drop(event_fname.replace('.csv', ''), axis=0,
                       inplace=True)
        visparams.to_csv(visparams_path)
        # os.remove(event_path)
        git_rm(event_path)
        git_workflow()
        text = f"{event}   ha sido eliminado de la base de datos!"
        st.warning(text)
        with st.spinner('Actualizando...'):
            time.sleep(3)
        st.rerun()


# ----------------------------------- core ----------------------------------- #
if st.session_state['authentication_status']:
    st.header("Página de Administración")
    st.divider()
    with st.expander("Usuarios registrados", expanded=False):
        gestionar_usuarios(st)

    with st.expander("Configurar visualizacion", expanded=False):
        gestionar_visparams(st)

    with st.expander("Ver datos de evento", expanded=False):
        gestionar_eventos(st)

    with st.expander("Agregar nuevo evento", expanded=False):
        agregar_evento(st)

    with st.expander("Eliminar evento", expanded=False):
        eliminar_evento(st)
    st.divider()
    authenticator.logout('Logout')
