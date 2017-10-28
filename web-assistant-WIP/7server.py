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
        <script src="http://cdn.binaryjs.com/0/binary.js" type="text/javascript" language="javascript"></script>
        <script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript" language="javascript"></script>
<audio id="player" controls></audio>
<script>
  var player = document.getElementById('player');
  var handleSuccess = function(stream) {
      //player.src = window.URL.createObjectURL(stream);
    var audioContext = window.AudioContext;
    var context = new audioContext();
    var audioInput = context.createMediaStreamSource(stream);
    var bufferSize = 2048;

    // create a javascript node
    var recorder = context.createJavaScriptNode(bufferSize, 1, 1);

   // specify the processing function
    recorder.onaudioprocess = recorderProcess;

   // connect stream to our recorder
    audioInput.connect(recorder);

    // connect our recorder to the previous destination
    recorder.connect(context.destination);
  };

  function recorderProcess(e) {
    var left = e.inputBuffer.getChannelData(0);
    window.Stream.write(left);
  }

  navigator.mediaDevices.getUserMedia({ audio: true, video: false })
      .then(handleSuccess)


//var conn = new BinaryClient('ws://localhost:8081');
var conn = new WebSocket('ws://localhost:8081');

conn.onopen = function(e) {
  console.log("Connected... sending data.");
  //window.Stream = conn.createStream();
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
        self.sendMessage(payload + "   " + isBinary)

 
factory = WebSocketServerFactory(u"ws://127.0.0.1:8081")
factory.protocol = SomeServerProtocol
resource = WebSocketResource(factory)
reactor.listenTCP(8081, factory)

resource = webserver()
factory = Site(resource)
reactor.listenTCP(8080, factory)
reactor.run()
