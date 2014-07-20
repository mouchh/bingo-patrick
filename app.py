from tornado import websocket, web, ioloop
import json, random

cl = []

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):

    def open(self):
        if self not in cl:
            cl.append(self)
            self.pseudo = 'Player ' + str(len(cl))
            self.color = '#' + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])

    def on_close(self):
        if self in cl:
            cl.remove(self)

    def on_message(self, message):
        decoded = json.loads(message)
        decoded['pseudo'] = self.pseudo
        decoded['color'] = self.color
        encoded = json.dumps(decoded)

        for c in cl:
            c.write_message(encoded)

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
], debug=True)

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()