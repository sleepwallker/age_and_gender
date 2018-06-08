import sys
import tornado.ioloop
import tornado.web
import os.path
import json
import main_nn


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        image = self.request.body

        with open('./image_repository/frist.png' , 'wb') as f:
            f.write(image)
        result = main_nn.prediction('./image_repository/frist.png')
        print(result)
        self.set_header('Content-type', 'application/json')
        self.write(json.dumps({'picture':result}))


# r"/" == root website address
apllication = tornado.web.Application([
    (r"/", MainHandler)
])

# Start the server at port n
if __name__ == "__main__":
    print('Server Running...')
    print('Press ctrl + c to close')

    apllication.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
