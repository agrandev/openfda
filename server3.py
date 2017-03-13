# Bibliotecas
import web3
import socketserver

# Web server

PORT=8000


#Handler = http.server.SimpleHTTPRequestHandler
Handler = web3.testHTTPRequestHandler


httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
