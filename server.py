from Genio import Genio
from flask import Flask
from flask_restful import Api, Resource, request
from flask.ext.api import status

app = Flask(__name__)
api = Api(app)
genio = Genio()

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:9080')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

class Genio(Resource):
    def get(self):
        artist = request.args.get('artist')
        related = genio.find_related_artists(artist)
        print(related)
        return {'related_artists': related}, status.HTTP_200_OK

api.add_resource(Genio, '/genio/', endpoint='genio')

if __name__ == '__main__':
    from tornado import autoreload
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    try:
        http_server = HTTPServer(WSGIContainer(app))

        http_server.listen(9090)
        print("serving API at port 9090")
        ioloop = IOLoop.instance()
        autoreload.start(ioloop)
        ioloop.start()
    except KeyboardInterrupt:
        pass