import urlparse, os, socket, threading, time, subprocess, mimetypes, struct, wave
from wave import open
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.static import File


from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource


# Webserver
class webserver(Resource):
    isLeaf = True
    def render_GET(self, request):
        this=urlparse.urlparse(request.path)#scheme,netloc,path,query
        root,ext=os.path.splitext(this.path)
        filename=os.path.basename(request.path)
        fileFolder=request.path.replace(filename,"")
        self.serverRoot=os.getcwd()
        #print request.path
        if ext==".wav":
            thisFile=File(self.serverRoot+request.path)
            return File.render_GET(thisFile,request)
        elif filename=="off.html":
            print "OFF"
            return """
<html>
	Currently: OFF <br>
	<button onclick="window.location='/on.html';">Change</button>
</html>"""
        elif filename=="on.html":
            print "ON"
            return """
<html>
        Currently: ON <br>
        <button onclick="window.location='/off.html';">Change</button>
</html>"""


resource = webserver()
factory = Site(resource)
reactor.listenTCP(8080, factory)
reactor.run()
