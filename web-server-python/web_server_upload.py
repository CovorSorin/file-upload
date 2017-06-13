import os
import posixpath
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import urllib
import cgi
import shutil
import re

# read and write strings as files
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

    
class HTTPRequestHandler(BaseHTTPRequestHandler):

    # HTTP request handler with implementations GET/HEAD/POST commands

    def do_GET(self):
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):
        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        # r = request
        r, info = self.verify_file()
        print self.client_address
        
        # ready for writing
        f = StringIO()
        f.write('<!DOCTYPE html">')
        f.write("<html><title>Result Page</title>")
        
        if r:
            f.write("<h1>Success!</h1>")
            f.write("<strong>The sorted words:</strong><br><br>")
        else:
            f.write("<strong>Upload Failed!</strong><br>")

        # read the file uploaded
        match = re.findall(r'\\\w+\.\w+', info)
        file_name = match[-1]
        print "Received", file_name[1:]
        received_file = open(file_name[1:], 'r')

        # split the text into words
        words = []
        for line in received_file:
            line = line.split(' ')
            for i in range(0, len(line)):
                if line[i] != '\n':
                    words.append(line[i])

        # sort the words and merge them
        words.sort()
        sorted_text = ""
        for i in range(0, len(words)):
            sorted_text = sorted_text + str(words[i]) + " "
    
        f.write(sorted_text)
        f.write("<br><br><a href=\"%s\">Try again!</a>" % self.headers['referer'])


        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
        
    def verify_file(self):
        boundary = self.headers.plisttext.split("=")[1]
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
                
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.create_form(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def create_form(self, path):
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        
        list.sort(key=lambda a: a.lower())
        
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html">')
        f.write("<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write("Choose a file you wish to sort the words from:<br>")
        f.write("<input name=\"file\" type=\"file\"/>")
        f.write("<input type=\"submit\" value=\"upload\"/></form>\n")
        
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

def handler(HandlerClass = HTTPRequestHandler,
    ServerClass = BaseHTTPServer.HTTPServer):
        # test method is used to run on local host
        BaseHTTPServer.test(HandlerClass, ServerClass)

if __name__ == '__main__':
    handler()