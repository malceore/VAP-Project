import urlparse, os, socket, threading, time, subprocess, mimetypes
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
        print request.path
        if ext==".mp3":
            thisFile=File(self.serverRoot+request.path)
            return File.render_GET(thisFile,request)
        elif ext==".ogg":
            thisFile=File(self.serverRoot+request.path)
            return File.render_GET(thisFile,request)
        elif ext==".ico":
            thisFile=File(self.serverRoot+request.path)
            return File.render_GET(thisFile,request)

        elif filename=="index.html":
            return """
<html>
<audio id="player" controls></audio>
<div id="variable"></div>
<script>
  var player = document.getElementById('player');
  var handleSuccess = function(stream) {
    if (window.URL) {
      player.src = window.URL.createObjectURL(stream);
    } else {
      player.src = stream;
    }
  };
  navigator.mediaDevices.getUserMedia({ audio: true, video: false })
      .then(handleSuccess)



var conn = new WebSocket('ws://localhost:8081');

conn.onopen = function(e) {
  console.log("Connected");
};

conn.onmessage = function(e) {
  console.log( "Received: " + e.data);
};

conn.onclose = function(e) {
  console.log("Connection closed");
};

</script>
</html>"""


# Websocket Server
class SomeServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("some request connected")

    def onMessage(self, payload, isBinary):
        self.sendMessage("message received")

 
factory = WebSocketServerFactory(u"ws://127.0.0.1:8081")
factory.protocol = SomeServerProtocol
resource = WebSocketResource(factory)
reactor.listenTCP(8081, factory)

resource = webserver()
factory = Site(resource)
reactor.listenTCP(8080, factory)
reactor.run()
