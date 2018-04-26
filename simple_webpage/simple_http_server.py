from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes
import shutil

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("Request made for " + self.path)
        resource_path = os.path.normpath(os.getcwd() + self.path)
        # parse check to see if the allowed folder "www" or something,
        # is in the path. If it's not, then I know that they are trying some
        # file system traversal stuff. send an email

        
        print(resource_path)

        # This is where the logic happens.
        # check permissions
        # log event
        # send them the correct response code

        # shutil.copyfileobj(file, wfile)
        # ^this makes it so you dont have to encode/decode stuff

        # use mimetypes on the path to the file being requested to figure out what file
        

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        
        f = open(resource_path, "rb")
        contents = shutils.copyfileobj(f, self.wfile.write(f))
        f.close()

    def do_HEAD(self):
        print("[+] do_HEAD")

server_address = ("127.0.0.1", 1989)
s = HTTPServer(server_address, SimpleHTTPRequestHandler)
print("[+] Serving on " + server_address[0])

s.serve_forever()
