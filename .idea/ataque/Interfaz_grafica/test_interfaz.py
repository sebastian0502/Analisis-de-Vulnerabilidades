import unittest
from unittest.mock import MagicMock, patch
from pywifi import const
import time
from Interfaz import WiFiScanner, FuncionesPrograma

class TestWiFiScanner(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.scanner = WiFiScanner()

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="password1\npassword2\npassword3\n")
    
    def test_leer_contrasenas_archivo(self, mock_open, mock_isfile):
        scanner = WiFiScanner()
        passwords = scanner.leer_contrasenas_archivo("fake_path.txt")
        self.assertEqual(passwords, ["password1", "password2", "password3"])

    @patch("Interfaz.PyWiFi")  
    def test_scan_networks(self, mock_wifi):
        """Prueba del escaneo de redes WiFi"""
        
        mock_interface = MagicMock()
        mock_wifi.return_value.interfaces.return_value = [mock_interface]
        mock_interface.scan_results.return_value = [
            MagicMock(ssid="UNI_LIBRE_H"),
            MagicMock(ssid="LIFIEE"),
            MagicMock(ssid=""),
        ]

        redes = self.scanner.scan_networks()

        self.assertIn("UNI_LIBRE_H", redes)
        self.assertIn("LIFIEE", redes)
        self.assertNotIn("", redes)

    @patch("Interfaz.PyWiFi")
    def test_conectar_red_fallida(self, mock_wifi):
        """Prueba de conexión fallida a una red WiFi"""
        
        mock_interface = MagicMock()
        mock_wifi.return_value.interfaces.return_value = [mock_interface]
        mock_interface.status.return_value = const.IFACE_DISCONNECTED

        self.scanner.interface = mock_interface
        resultado = self.scanner.conectar_red("RedPrueba", "passwordIncorrecta")

        self.assertFalse(resultado)

class TestWifi(unittest.TestCase):

    def setUp(self):
        
        self.funciones = FuncionesPrograma()
            
    @patch("Interfaz.WiFiScanner.ataque_fuerza_bruta_wifi")
    def test_iniciar_ataque_red(self, mock_ataque):
        """Prueba del inicio de un ataque de fuerza bruta a una red"""
        mock_ataque.return_value = None  

        funciones = FuncionesPrograma()
        funciones.redes_disponibles = ["RedPrueba"]
        funciones.opcion_red = MagicMock(get=MagicMock(return_value="RedPrueba"))

        funciones.iniciar_ataque_red()

        mock_ataque.assert_called_once_with("RedPrueba", 8, 10, unittest.mock.ANY)

class TestFormulario(unittest.TestCase):
    def setUp(self):
        
        self.funciones = FuncionesPrograma()

    def test_generate_passwords(self):
        
        passwords = list(self.funciones.generate_passwords(1, 1, None))
        expected = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2' ,'3',
                    '4', '5', '6', '7', '8', '9']
        self.assertEqual(passwords, expected)

    @patch("Interfaz.requests.get")
    def test_fetch_login_token(self, mock_get):
        
        mock_response = MagicMock()
        mock_response.text = '<input name="logintoken" value="fake_token">'
        mock_get.return_value = mock_response
        
        token = self.funciones.fetch_login_token("http://example.com")
        self.assertEqual(token, "fake_token")

    @patch("Interfaz.FuncionesPrograma.fetch_login_token", return_value="fake_token")
    @patch("Interfaz.requests.post")
    @patch("Interfaz.requests.get")
    def test_brute_force_moodle(self, mock_get, mock_post, mock_fetch_token):
        mock_ventana_progreso = MagicMock()

        mock_response_get = MagicMock()
        mock_response_get.text = '<input name="logintoken" value="fake_token">'
        mock_get.return_value = mock_response_get
        
        mock_response_post = MagicMock()
        mock_response_post.text = "success"
        mock_post.return_value = mock_response_post

        self.funciones.brute_force_moodle(
            "https://univirtual.uni.pe/login/index.php", 
            "user", 2, 2, ["password"], 
            mock_ventana_progreso
        )
        
        mock_ventana_progreso.actualizar_texto.assert_called()

        mock_post.assert_called_with(
            "https://univirtual.uni.pe/login/index.php",
            data={
                "logintoken": "fake_token",  
                "username": "user",
                "password": "password"
            }
        )

if __name__ == "__main__":
    unittest.main()
