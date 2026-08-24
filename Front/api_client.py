import requests
import streamlit as st
import pandas as pd

class APIClient:
    def __init__(self):
        self.base_url = st.secrets["API_URL"]
        self.api_key = st.secrets["API_KEY"]

        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def obtener_ordenes(self):
        url = f"{self.base_url}/ordenes/"
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"No fue posible establecer conexión con la API. Error {response.status_code}: {response.text}")
                return []
        except requests.exceptions.ConnectionError:
            st.error(f"Error crítico. No fue posible conectarse con el servidor. Verifique que esté encendido")
            return []

    def actualizar_nombre(self, id_orden: int, nuevo_nombre: str):
        url = f"{self.base_url}/ordenes/{id_orden}/nombre"
        payload = {"nuevo_nombre":nuevo_nombre}
        try:
            response = requests.patch(url=url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return True
            else: 
                st.error(f"Error al actualizar el nombre: {response.text}")
                return False
        except requests.exceptions.ConnectionError:
            st.error("Error durante el envío de las actualizaciones")
            return False

    def actualizar_estado(self, id_orden: int, nuevo_estado: str):
        url = f"{self.base_url}/ordenes/{id_orden}/estado"
        payload = {"nuevo_estado": nuevo_estado}
        try:
            response = requests.patch(url=url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return True
            else:
                st.error(f"Error al actualizar el estado: {response.text}")
                return False
        except requests.exceptions.ConnectionError:
            st.error("Error crítico: Falló la conexión del servidor")
            return False

    def actualizar_pago(self, id_orden: int, pago: float):
        url = f"{self.base_url}/ordenes/{id_orden}/pago"
        payload = {"pago": pago}
        try:
            response = requests.patch(url=url, headers=self.headers, json=payload)
            if response.status_code == 200:
                datos = response.json()
                return datos.get("deuda", 0.0)
            else:
                st.error(f"Error al actualizar el pago: {response.text}")
                return False
        except requests.exceptions.ConnectionError:
            st.error("Error crítico. No se pudo conectar con el servidor")
            return False

    def actualizar_fecha_entrega(self, id_orden: int, nueva_fecha: str):
        url = f"{self.base_url}/ordenes/{id_orden}/fecha_entrega"
        payload = {"nueva_fecha":nueva_fecha}
        try:
            response = requests.patch(url=url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return True
            else: 
                st.error(f"Error al actualizar la fecha de entrega: {response.text}")
                return False
        except requests.exceptions.ConnectionError:
            st.error("Error crítico. No se pudo conectar con el servidor")
            return False

    def actualizar_detalle_orden(self, id_detalle: int, nuevo_detalle: str|None = None, nueva_cantidad: int|None = None):
        url = f"{self.base_url}/ordenes/detalles/{id_detalle}"
        payload = {"nuevo_detalle":nuevo_detalle, "cantidad": nueva_cantidad}
        try:
            response = requests.patch(url=url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return True
            else:
                st.error(f"No fue posible actualizar el detalle de la orden: {response.text}")
                return False
        except requests.exceptions.ConnectionError:
            st.error("Error crítico. No se pudo conectar con el servidor")
            return False

    def agregar_stock(self, datos: list):
        url = f"{self.base_url}/inventarios"
        errores = []
        for dato in datos:
            try:
                response = requests.post(url=url, json=dato, headers=self.headers)
                if response.status_code != 200:
                    errores.append({"registro":dato, "error": response.text})
                    st.error(f"No fue posible guardar el registro {dato}")
            except requests.exceptions.ConnectionError:
                st.error("Error crítico. No se pudo conectar con el servidor")
            except Exception as e:
                errores.append({"registro": dato, "error": str(e)})
                st.error(f"Error al guardar los registros: {e}")

    def traer_productos(self):
        url = f"{self.base_url}/inventarios"
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                datos = response.json()
                return pd.DataFrame(datos)
            else:
                return pd.DataFrame()
        except Exception:
            return pd.DataFrame()

    def traer_metricas(self):
        url = f"{self.base_url}/metricas/"
        try:
            response = requests.get(
                url=url,
                headers=self.headers
            )
            if response.status_code == 200:
                datos = response.json()
                return datos
            else:
                st.error(f"No fue posible establecer conexión con la API. Error {response.status_code}: {response.text}") 
                return {}
        except requests.exceptions.ConnectionError:
                st.error(f"Error crítico. No fue posible conectarse con el servidor. Verifique que esté encendido")
                return {}
        except Exception:
            return {}