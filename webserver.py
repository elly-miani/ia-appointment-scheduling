'''
    basic server handling GET and POST requests
    currently supports:
        # GET requests of files
        # POST requests to `/requestAppointment` with JSON payload, 
          to add a new appointment by calling `requestAppointment()`
    TODO: error handling:
        # POST to unknown paths

    use KeyboardInterrupt to close socket
'''

from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
import sys
from io import BytesIO
import json

sys.path.append('./webservices')
from requestAppointment import requestAppointment 
from scheduleAppointments import scheduleAppointments


class HTTPRequestHandler(BaseHTTPRequestHandler):

    # set headers
    def _set_headers(self,mimetype):
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()

    def do_GET(self):
        # if path is root, show homepage
        if self.path=="/":
            self.path="html/index.html"

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
            if self.path.endswith(".jpg"):
                mimetype="image/jpeg"
                sendReply = True

            if sendReply == True:
                # open the static file requested and send it
                f = open(curdir + sep + "webapp/" + self.path, "rb")
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

        print("Received POST request")

        print(self.path)
        if self.path == "/requestAppointment":
            requestAppointment(json.loads(body))

            self.send_response(200)
            self.end_headers()
            response = BytesIO()
            response.write(b'Received POST request for new appointment:')
            response.write(body)
            self.wfile.write(response.getvalue())
        
        if self.path == "/scheduleAppointments":
            scheduleAppointments()
            json_string = json.dumps(scheduleAppointments())

            self.send_response(200)
            self.end_headers()
            response = BytesIO()
            response.write(json_string.encode(encoding='utf_8'))
            self.wfile.write(response.getvalue())
        


try:
    httpd = HTTPServer(('localhost', 8000), HTTPRequestHandler)
    print("Starting web server on port: " + str(httpd.server_port))
    httpd.serve_forever()

except KeyboardInterrupt:
	print('\nShutting down the web server')
	httpd.socket.close()
