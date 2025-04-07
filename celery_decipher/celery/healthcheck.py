#!/usr/bin/env python3

"""Simple HTTP health check service."""

import logging
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Tuple, Type, TypeAlias

SERVER_PORT = 8000
SERVER_ADDRESS = ("", SERVER_PORT)
logging.basicConfig(level=logging.INFO)

ProcessName: TypeAlias = str
ProcessStatus: TypeAlias = str


def get_supervisord_status() -> dict[ProcessName, ProcessStatus]:
    """Check that ingestion service and task runner are running."""
    process_states = {
        line[0]: line[1]
        for line in subprocess.run(
            "supervisorctl status", shell=True, stdout=subprocess.PIPE
        )
        .stdout.decode()
        .splitlines()
        for line in [line.split()]
    }
    return process_states


def all_processes_healthy(process_states: dict[ProcessName, ProcessStatus]) -> bool:
    """Check that all processes are healthy."""
    return all(status in ("RUNNING", "STARTING") for status in process_states.values())


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            process_states = get_supervisord_status()
            if not all_processes_healthy(process_states):
                logging.error(process_states)
                self.send_error(500, message=str(process_states))
                return
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK\n")
        except Exception:  # pylint: disable=broad-except
            logging.exception("Server error.")
            self.send_error(500)


def serve(server_address: Tuple[str, int]) -> None:
    """Start the server."""
    with ThreadingHTTPServer(server_address, HealthCheckHandler) as server:  # type: ignore
        logging.info("Starting server on %s:%s", *server_address)
        server.serve_forever()


if __name__ == "__main__":
    serve(SERVER_ADDRESS)
