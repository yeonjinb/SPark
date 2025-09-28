import http.server
import ssl
import socketserver
import os

# HTTPS 서버 설정
PORT = 5001
CERT_FILE = "server.crt"
KEY_FILE = "server.key"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

# 인증서 생성 (자체 서명)
def create_self_signed_cert():
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        import subprocess
        try:
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096', 
                '-keyout', KEY_FILE, '-out', CERT_FILE, '-days', '365', 
                '-nodes', '-subj', '/C=US/ST=State/L=City/O=Organization/CN=localhost'
            ], check=True, capture_output=True)
            print("자체 서명 인증서가 생성되었습니다.")
        except:
            print("OpenSSL이 설치되지 않았습니다. HTTP 서버를 사용하세요.")
            return False
    return True

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        if create_self_signed_cert():
            # HTTPS 설정
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(CERT_FILE, KEY_FILE)
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            
            print(f"HTTPS 서버 시작: https://localhost:{PORT}")
            print(f"SPARK 웹앱: https://localhost:{PORT}/spark_final_algorithm.html")
        else:
            print(f"HTTP 서버 시작: http://localhost:{PORT}")
            print(f"SPARK 웹앱: http://localhost:{PORT}/spark_final_algorithm.html")
        
        httpd.serve_forever()
