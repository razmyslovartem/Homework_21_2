#server.py

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import os


hostName = "localhost"
serverPort = 8080
ROOT_DIR = "."   # Папка с HTML‑файлами (где лежит server.py).

# Ключ - это путь, а значение это файл шаблон.
templates_map = {
    "/": "index.html",
    "/index": "index.html",
    "/index/": "index.html",
    "/catalog.html": "catalog.html",
    "/category.html": "category.html",
    "/contacts.html": "contacts.html",
}

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        # Путь html страницы.
        url_path = urlparse(self.path).path

        # index.html -> главная и т.д.
        if url_path in templates_map:
            filename = templates_map[url_path]
        else:
            # Любые другие пути 404 ошибка.
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1>")
            return

        # Полный путь к файлу.
        filepath = os.path.join(ROOT_DIR, filename)

        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1>")
            return

        # Читаем файл.
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Отдаём браузеру инфу.
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер стартовал, и доступен по адресу http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Сервер ОСТАНОВЛЕН.")
