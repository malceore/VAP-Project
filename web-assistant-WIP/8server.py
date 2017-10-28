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
        elif ext==".js":
            thisFile=File(self.serverRoot+request.path)
            return File.render_GET(thisFile,request)

        elif filename=="index.html":
            return """
<html>
<script src="binary.js" type="text/javascript" language="javascript"></script>

<button onclick="startRecording()">Start</button>
<button onclick="stopRecording()">Stop</button>

<script>

// # Socket decalre
var client = new BinaryClient('ws://localhost:8081');

// # Drop in script
  client.on('open', function() {
    window.Stream = client.createStream();

    if (!navigator.getUserMedia)
      navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia || navigator.msGetUserMedia;

    if (navigator.getUserMedia) {
      navigator.getUserMedia({audio:true}, success, function(e) {
        alert('Error capturing audio.');
      });
    } else alert('getUserMedia not supported in this browser.');

    var recording = false;

    window.startRecording = function() {
      recording = true;
    }

    window.stopRecording = function() {
      recording = false;
      window.Stream.end();
    }

    function success(e) {
      audioContext = window.AudioContext || window.webkitAudioContext;
      context = new audioContext();

      // the sample rate is in context.sampleRate
       audioInput = context.createMediaStreamSource(e);

      var bufferSize = 2048;
      recorder = context.createScriptProcessor(bufferSize, 1, 1);

      recorder.onaudioprocess = function(e){
        if(!recording) return;
        console.log ('recording');
        var left = e.inputBuffer.getChannelData(0);
        window.Stream.write(convertoFloat32ToInt16(left));
      }

      audioInput.connect(recorder)
      recorder.connect(context.destination); 
    }

    function convertoFloat32ToInt16(buffer) {
      var l = buffer.length;
      var buf = new Int16Array(l)

      while (l--) {
        buf[l] = buffer[l]*0xFFFF;    //convert to 16 bit
      }
      return buf.buffer
    }
  })



//#Socket Stuff
//var conn = new BinaryClient('ws://localhost:8081');
/*var conn = new WebSocket('ws://localhost:8081');

conn.onopen = function(e) {
  console.log("Connected... sending data.");
  window.Stream = conn.createStream();
};

conn.onmessage = function(e) {
  console.log( "Received: " + e.data);
};

conn.onclose = function(e) {
  console.log("Connection closed");
};
*/
</script>
</html>"""


# Websocket Server
class SomeServerProtocol(WebSocketServerProtocol):
    #file = wave.open('voice.wav', 'w')
    #file.setnchannels(1) # mono
    def onConnect(self, request):
        print("some request connected")

    def onMessage(self, payload, isBinary):
        #self.sendMessage("Recieved :")
        print("Receied: ")

    def onMessageFrameBegin(self, length):
        print("frame begin")

    def onMessageFrameData(self, payload):
        print("data begin")

    def onClose(self, wasClean, code, reason):
        print("Oh so cute, bubye now!") 
        #file.close()

factory = WebSocketServerFactory(u"ws://127.0.0.1:8081")
factory.protocol = SomeServerProtocol
resource = WebSocketResource(factory)
reactor.listenTCP(8081, factory)

resource = webserver()
factory = Site(resource)
reactor.listenTCP(8080, factory)
reactor.run()

