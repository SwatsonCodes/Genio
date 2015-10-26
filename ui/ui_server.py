import http.server
import socketserver

PORT = 9080

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving UI at port", PORT)
httpd.serve_forever()