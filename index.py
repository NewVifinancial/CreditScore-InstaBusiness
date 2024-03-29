import tornado.web
import tornado.ioloop
import subprocess
import pathlib

class uploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        files = self.request.files["imgFile"]
        for f in files:
            fh = open(f"img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        self.write(f"http://localhost::8080/img/{f.filename}")

        # file_extension = pathlib.Path(r'C:\Users\Chakdahah\ReginaOdoi.csv').suffix
        file_extension = pathlib.Path(r'C:\Users\Chakdahah\lastlast.pdf').suffix
        print("File Extension: ", file_extension)


        # Run the other scripts

        if file_extension == '.csv':
            subprocess.run(["python", "CSVeditingLoanDecisioning.py"])
            print("Done")
            
        elif file_extension == '.pdf':
            subprocess.run(["python", "OCRInstaBusinessLoanDecisioning.py"])
            print("Submitted")
        print("File Successfully Uploaded. Get out!")

if (__name__ == "__main__"):
    app = tornado.web.Application([
        ("/", uploadHandler),
        ("/img/(.*)", tornado.web.StaticFileHandler, {"path" : "img"})
    ])

    app.listen(8080)
    print("Listening on port 8080")

    tornado.ioloop.IOLoop.instance().start() 