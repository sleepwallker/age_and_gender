import sys
import tornado.ioloop
import tornado.web
import os.path
import json
import main_nn


class MainHandler(tornado.web.RequestHandler):

    def post(self):
        image = self.request.body
        # with open('./image_repository/' + make_a_unique_name(), 'w') as f:
        #     f.write(urllib2.urlopen(your_url).read())
        print(image)
        self.write(json.dumps({'lol': "krasavchik"}))




# This tells tornado where to find the static files
setting = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True
)

# r"/" == root website address
apllication = tornado.web.Application([
    (r"/", MainHandler)
], **setting)

# Start the server at port n
if __name__ == "__main__":
    print('Server Running...')
    print('Press ctrl + c to close')

    apllication.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
