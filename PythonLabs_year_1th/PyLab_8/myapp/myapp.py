from http.server import HTTPServer
from controllers.BaseHTTPRequestHandler import SimpleHTTPRequestHandler

if __name__ == '__main__':
    # server = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    httpd = HTTPServer(('localhost', 8080), RequestHandlerClass=SimpleHTTPRequestHandler)
    print('server is running in \"localhost:8080\"')
    httpd.serve_forever()