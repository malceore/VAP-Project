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
</script>
</html>"""


# Websocket Server
class SomeServerProtocol(WebSocketServerProtocol):
    file=open('noise10.wav', 'w')
    file.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
    values = []
    def onConnect(self, request):
        print("Connection")

    def onMessageFrameData(self, payload):
        print("FrameData")
        #packed_value = struct.pack('h', payload)
        #values.append(packed_value)
        file.write(payload.encode('utf8'))
    #def onMessage(self, payload, isBinary):
    #    print("Message Received: ")# + payload)

    def onClose(self, wasClean, code, reason):
        #file.write(values)
        print("Oh so cute, bubye now!")

factory = WebSocketServerFactory(u"ws://127.0.0.1:8081")
factory.protocol = SomeServerProtocol
resource = WebSocketResource(factory)
reactor.listenTCP(8081, factory)

resource = webserver()
factory = Site(resource)
reactor.listenTCP(8080, factory)
reactor.run()
