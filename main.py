from simple_server.server import start, stop
from simple_server.route import route


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        stop()
