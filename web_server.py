from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi
import Queue

PORT_NUMBER = 8000

def sort(words):
	words.sort()
	print words
	return words

# This class will handles any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):

	def __init__(self, text, endchar, *args):
		BaseHTTPRequestHandler.__init__(self, *args)

	# Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			# Check the file extension required and set the right mime type
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				# Open the static file requested and send it
				f = open(curdir + sep + self.path)
				self.send_response(200)
				self.send_header('Content-type', mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	# Handler for the POST requests
	def do_POST(self):
                global text
		if self.path=="/send":
                        form = cgi.FieldStorage(
                                fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST',
                                'CONTENT_TYPE':self.headers['Content-Type']
                        })

                        if (form.getvalue('input_text') != endchar):
                                print "Received text: %s" %  form.getvalue('input_text')
                                text.append(form.getvalue('input_text'))
                                self.send_response(200)
                                self.end_headers()
                        else:
                                self.send_response(200)
                                self.end_headers()
                                sort(text)
                                self.wfile.write("RWRW")
                                text = []


			return

try:
	text = []
	endchar = 'eof'

	def handler(*args):
		myHandler(text, endchar, *args)

	# Create a web server and define the handler to manage the incoming request
	server = HTTPServer(('', PORT_NUMBER), handler)
	print 'Started httpserver on port ' , PORT_NUMBER

	# Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
