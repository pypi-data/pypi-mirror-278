import pyperclip
import argparse
import time
import orjson
import pynput
from typing import Annotated, List, Optional, Callable
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Request, Body, Depends
from fastapi.responses import ORJSONResponse
import uvicorn
import asyncio
import statesman
import contextlib

class ProcessTyping(statesman.StateMachine):
    class States(statesman.StateEnum):
        starting = "Starting..."
        recording = "Typing..."
        waiting = "Waiting..."
        stopping = "Stopping..."
        stopped = "Terminated."

async def text_consumer(
    q_char: asyncio.Queue, *args, **kwargs
):
    """
    Consumes text from the queue and sends it to the keyboard API.

    Args:
        q_text (asyncio.Queue): A queue containing the text to be sent to the keyboard API.
        q_status (asyncio.Queue): A queue containing the status of the keyboard API.
        *args: Additional arguments passed to the function.
        **kwargs: Additional keyword arguments passed to the function.

    Notes:
        This function consumes text from the queue and sends it to the keyboard API.
        It uses the aiohttp library to make a POST request to the API endpoint.
    """
    keyboard = pynput.keyboard.Controller()
    # Loop indefinitely to consume whispers from the queue
    while True:
        # Get the next whisper from the queue
        token = await q_char.get()
        # Convert the audio token to a hexadecimal string
        pyperclip.copy(token)
        keyboard.press(pynput.keyboard.Key.shift)
        time.sleep(0.01)
        keyboard.press(pynput.keyboard.Key.insert)
        time.sleep(0.03)
        keyboard.release(pynput.keyboard.Key.insert)
        time.sleep(0.01)
        keyboard.release(pynput.keyboard.Key.shift)
        time.sleep(0.01)
        q_char.task_done()

class Output:
    instance = None
    text_output_method: Callable[[str], None]
    q_char: asyncio.Queue

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

            q_char = asyncio.Queue()

            def text_output_method(text: str, q_char: asyncio.Queue):
                for char in text:
                    q_char.put_nowait(char)
                # pyperclip.copy(text)
                # keyboard.press(pynput.keyboard.Key.shift)
                # time.sleep(0.01)
                # keyboard.press(pynput.keyboard.Key.insert)
                # time.sleep(0.05)
                # keyboard.release(pynput.keyboard.Key.insert)
                # time.sleep(0.01)
                # keyboard.release(pynput.keyboard.Key.shift)

            cls.instance.text_output_method = text_output_method
            cls.instance.q_char = q_char

        return cls.instance


def get_output() -> Optional[Output]:
    return Output()


class Text(BaseModel):
    text: str


app = FastAPI()

@app.on_event("startup")
async def start_db():
    output = get_output()
    asyncio.create_task(text_consumer(output.q_char))



@app.post("/write/")
async def write(
    body: Annotated[
        Text,
        Body(
            openapi_examples={
                "short_audio": {
                    "summary": "A very short audio.",
                    "value": {"text": "Paste this"},
                }
            }
        ),
    ],
    output: Optional[Output] = Depends(get_output),
) -> bool:
    """Type the given message."""
    result = orjson.loads(body.text)
    text = result["text"]
    # if text != "":
    #     text += " "
    output.text_output_method(text, output.q_char)
    return True


def main():
    """
    Main entry point for the for the paste server.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port-typing", type=int, default=8081, dest="port", help="Port to listen on"
    )
    args, _ = parser.parse_known_args()
    # Start the server
    uvicorn.run(app, host="localhost", port=args.port)


if __name__ == "__main__":
    main()
