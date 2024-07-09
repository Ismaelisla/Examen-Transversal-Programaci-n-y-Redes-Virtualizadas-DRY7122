import hashlib
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# Función para almacenar usuario y contraseña hasheada en la base de datos SQLite
def almacenar_usuario(username, password_hash):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (username TEXT PRIMARY KEY, password_hash TEXT)')
    cursor.execute('INSERT INTO usuarios VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()

# Función para validar usuario y contraseña hasheada
def validar_usuario(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        stored_password_hash = user[1]
        # Verificar si el hash de la contraseña almacenada coincide con el hash de la contraseña proporcionada
        if hashlib.sha256(password.encode()).hexdigest() == stored_password_hash:
            return True
    return False

# Manejador de peticiones HTTP para el servidor web
class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        
        if 'username' in params and 'password' in params:
            username = params['username'][0]
            password = params['password'][0]
            
            # Hash de la contraseña
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Almacenar usuario y contraseña en la base de datos
            almacenar_usuario(username, password_hash)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'Usuario {username} almacenado correctamente.'.encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('Error: Se requieren campos "username" y "password" en la solicitud POST.'.encode('utf-8'))

# Función para inicializar y ejecutar el servidor web en el puerto 5800
def iniciar_servidor_web():
    server_address = ('', 5800)
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    print(f'Servidor web iniciado en el puerto {server_address[1]}...')
    httpd.serve_forever()

if __name__ == '__main__':
    # Iniciar servidor web en un hilo aparte
    import threading
    server_thread = threading.Thread(target=iniciar_servidor_web)
    server_thread.start()
    
    # Ejemplos de almacenamiento de usuarios y contraseñas hasheadas
    almacenar_usuario('usuario1', hashlib.sha256('password1'.encode()).hexdigest())
    almacenar_usuario('usuario2', hashlib.sha256('password2'.encode()).hexdigest())
    
    # Ejemplo de validación de usuarios
    print(validar_usuario('usuario1', 'password1'))  # True
    print(validar_usuario('usuario2', 'password2'))  # True
    print(validar_usuario('usuario3', 'password3'))  # False
