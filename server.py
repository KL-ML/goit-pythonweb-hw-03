from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import pathlib
import mimetypes
from jinja2 import Environment, FileSystemLoader
from handlers.json_handler import read_json_file, update_data_json

def proceed_read_template():
    file_data = read_json_file()

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("read_template.html")

    output = template.render(
        file_data=file_data,
    )

    with open("read.html", "w", encoding="utf-8") as fh:
        fh.write(output)

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/messsage':
            self.send_html_file('messsage.html')
        elif pr_url.path == "/read":
            proceed_read_template()
            self.send_html_file("read.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        print(f"data: {data}")
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(f"Data parse: {data_parse}")
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        print(data_dict)
        self.send_response(302)
        self.send_header("Location", "/read")
        self.end_headers()
        update_data_json(data_dict)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

def run(server_class=HTTPServer, handler_class=HttpHandler, port=3000):
    server_address = ('', port)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
