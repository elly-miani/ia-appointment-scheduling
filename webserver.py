from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
from io import BytesIO
import json

class HTTPRequestHandler(BaseHTTPRequestHandler):

    # set headers
    def _set_headers(self,mimetype):
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()

    def do_GET(self):
        # if path is root
        if self.path=="/":
            self.path="/index.html"

        try:
            sendReply = False

            # choose correct mimetype
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path, "rb")
                self._set_headers(mimetype)
                self.wfile.write(f.read())
                f.close()
            else:
                self.send_error(404, 'Page Not Found: %s' % self.path)

        except IOError:
            self.send_error(404, 'Page Not Found: %s' % self.path)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        self.send_response(200)
        self.end_headers()

        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

        datastore = json.loads(body)

        print(datastore["hello"])


try:
    httpd = HTTPServer(('localhost', 8000), HTTPRequestHandler)
    print("Starting web server on port: " + str(httpd.server_port))
    httpd.serve_forever()

except KeyboardInterrupt:
	print('\nShutting down the web server')
	httpd.socket.close()
