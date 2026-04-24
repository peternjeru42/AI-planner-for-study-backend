import os
import sys

from gunicorn.app.wsgiapp import run


if __name__ == "__main__":
    port = os.environ.get("PORT", "8000")
    sys.argv = [
        "gunicorn",
        "config.wsgi:application",
        "--bind",
        f"0.0.0.0:{port}",
        "--log-file",
        "-",
        "--access-logfile",
        "-",
    ]
    run()
