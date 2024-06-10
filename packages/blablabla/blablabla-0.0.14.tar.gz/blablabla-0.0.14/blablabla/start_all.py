
from multiprocessing import Process
import requests
import argparse

from .whisper_server import main as start_whisper_server
from .typing_server import main as start_typing_server
from .orchestrator import main as start_orchestrator


def main():
    p_whisper = Process(target=start_whisper_server, args=())
    p_whisper.start()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port-whisper", type=int, default=8080, dest="port", help="Port to listen on"
    )
    args, _ = parser.parse_known_args()

    requests.get(f"http://localhost:{args.port}/")

    p_typing = Process(target=start_typing_server, args=())
    p_typing.start()

    p_orchestrator = Process(target=start_orchestrator, args=())
    p_orchestrator.start()

    p_orchestrator.join()
    p_typing.terminate()
    p_whisper.terminate()


if __name__ == "__main__":
    main()
