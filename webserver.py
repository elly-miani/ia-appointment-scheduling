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
from urllib.parse import parse_qs

from os import curdir, sep
import sys
from io import BytesIO
import json

sys.path.append('./webservices')
from requestAppointment import requestAppointment 
from requestAppointment import showRequestedAppointments 
from scheduleAppointments import scheduleAppointments
from scheduleAppointments import showAppointments
from emptyFiles import emptySchedule
from emptyFiles import emptyRequests
from randomRequests import generateRandomRequests


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
            fileRequest = False
            RESTRequest = False

            # choose correct mimetype if server is asked for files
            if self.path.endswith(".html"):
                mimetype='text/html'
                fileRequest = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                fileRequest = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                fileRequest = True
            if self.path.endswith(".jpg"):
                mimetype="image/jpeg"
                fileRequest = True

            if fileRequest == True:
                # open the static file requested and send it
                f = open(curdir + sep + "webapp/" + self.path, "rb")
                self._set_headers(mimetype)
                self.wfile.write(f.read())
                f.close()
            else:
                # REST services
                if self.path == "/showAppointments":
                    json_string = json.dumps(showAppointments())

                    self.send_response(200)
                    self.end_headers()
                    response = BytesIO()
                    response.write(json_string.encode(encoding='utf_8'))
                    self.wfile.write(response.getvalue())

                    RESTRequest = True


                if "/showRequestedAppointments" in self.path:
                    path, appID = self.path.split("?")
                    # json_string = json.dumps(showRequestedAppointments(appID))

                    self.send_response(200)
                    self.end_headers()
                    response = BytesIO()
                    # response.write(json_string.encode(encoding='utf_8'))
                    response.write(showRequestedAppointments(
                        appID).encode(encoding="utf_8"))
                    self.wfile.write(response.getvalue())

                    RESTRequest = True
                
                if self.path == "/emptySchedule":
                    emptySchedule()

                    self.send_response(200)
                    self.end_headers()
                    response = BytesIO()
                    # response.write(json_string.encode(encoding='utf_8'))
                    self.wfile.write(response.getvalue())

                    RESTRequest = True
                    
                if self.path == "/emptyRequests":
                    emptyRequests()

                    self.send_response(200)
                    self.end_headers()
                    response = BytesIO()
                    # response.write(json_string.encode(encoding='utf_8'))
                    self.wfile.write(response.getvalue())

                    RESTRequest = True
                
                if self.path == "/randomRequests":
                    generateRandomRequests(10)

                    self.send_response(200)
                    self.end_headers()
                    response = BytesIO()
                    # response.write(json_string.encode(encoding='utf_8'))
                    self.wfile.write(response.getvalue())

                    RESTRequest = True
                
                if RESTRequest == False:
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
        
        if "/scheduleAppointments" in self.path:
            post_data = json.loads(body)
            json_string = json.dumps(scheduleAppointments(int(post_data['value'])))

            self.send_response(200)
            self.end_headers()
            response = BytesIO()
            response.write(json_string.encode(encoding='utf_8'))
            self.wfile.write(response.getvalue())

            # RESTRequest = True
        
        if self.path == "/randomRequests":
            generateRandomRequests(json.loads(body))

            self.send_response(200)
            self.end_headers()
            response = BytesIO()
            # response.write(json_string.encode(encoding='utf_8'))
            self.wfile.write(response.getvalue())

        


try:
    httpd = HTTPServer(('localhost', 8000), HTTPRequestHandler)
    print("Starting web server on port: " + str(httpd.server_port))
    httpd.serve_forever()

except KeyboardInterrupt:
	print('\nShutting down the web server')
	httpd.socket.close()
