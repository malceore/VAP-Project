import urlparse
import os
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.static import File
import time
import subprocess
import mimetypes

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
        elif filename=="index.html":
            return """
<html>
<audio id="player" controls></audio>
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
</script>

</html>"""

resource = webserver()
factory = Site(resource)
reactor.listenTCP(8080, factory)
reactor.run()
