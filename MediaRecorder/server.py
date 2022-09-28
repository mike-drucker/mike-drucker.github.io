## @server.py
#  This file contains the server side of the Autobahn websocket service
import uuid
import os
from twisted.internet import reactor

from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol, \
                                       listenWS

## @StreamingServerProtocol
#
#  Parse JSON-formatted string
#
#    # Encode JSON-formatted string
#    json_input = json.dumps([ "one": 1, "two": { "list": [ {"aa":"A"},{"ab":"B"} ] } ])
#
#    # Prints 'B'
#    print decoded['two']['list'][1]['ab']
#
#    # Prints entire JSON-formatted string nicely
#    print json.dumps(decoded, sort_keys=True, indent=4)
#
#  The following methods are triggered on the server side:
#
#  onConnect(self, requestOrResponse) callback fired during WebSocket opening handshake
#    when client connects, or when server connection established (by a client with 
#    response from server).
#
#  onOpen(self) callback fired when initial WebSocket opening handshake was completed.
#    You now can send and receive WebSocket messages.
#
#  sendMessage(self, payload, isBinary = False, fragmentSize = None, sync = False,
#    doNotCompress = False) send a WebSocket message over the connection to the peer.
#
#  onMessage(self, payload, isBinary) callback fired when a complete WebSocket message
#    was received.
#
#  sendClose(self, code = None, reason = None) starts WebSocket closing handshake.
#
#  onClose(self, wasClean, code, reason) callback when the WebSocket connection has been
#    closed (WebSocket closing handshake has been finished or the connection was closed
#    uncleanly).
#
#  A more complete list of available 'WebSocket' interfaces:
#
#  github.com/tavendo/AutobahnPython/blob/master/autobahn/autobahn/websocket/interfaces.py

class StreamingServerProtocol(WebSocketServerProtocol):
  fileHandle = None
   
  def onMessage(self, msg, binary):
    if len(msg) < 30 and msg.decode('utf-8').startswith('mp3_start'):
      filename = str(uuid.uuid4()) + ".webm"
      print("Starting:" + filename)
      if self.fileHandle:
        self.fileHandle.close()
      self.fileHandle = open(filename,"wb")
    elif len(msg) < 30 and msg.decode('utf-8').startswith('mp3_stop'):
      if self.fileHandle:
        print("Closing")
        self.fileHandle.close()
        self.fileHandle = None
    else:
      print('chunk received')
      self.fileHandle.write(msg)
    # send 'msg' back to the client (i.e. javascript)
    # self.sendMessage(msg, binary)
  def onClose(self,wasClean: bool, code: int, reason: str):
    print('closing')
    if self.fileHandle:
      print("Closing")
      self.fileHandle.close()
      self.fileHandle = None
  

if __name__ == '__main__':
   factory = WebSocketServerFactory("ws://localhost:9001")
   factory.protocol = StreamingServerProtocol
   listenWS(factory)
   reactor.run()
