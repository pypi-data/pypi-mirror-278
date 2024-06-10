import argparse
import logging
import orjson
from typing import Annotated, List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Request, Body, Depends
from fastapi.responses import ORJSONResponse, RedirectResponse
from datetime import datetime

import numpy as np
import logging
import uvicorn
import io
import soundfile as sf


from .whisper_online import asr_factory, set_logging, OnlineASRProcessor

# Set up logging
logger = logging.getLogger(__name__)


class ASR:
    instance = None
    online: OnlineASRProcessor

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            parser = argparse.ArgumentParser()
            parser.add_argument(
                "--port", type=int, default=8080, dest="port", help="Port to listen on"
            )
            parser.add_argument(
                "--backend",
                type=str,
                default="faster-whisper",
                dest="backend",
                help="The backend for the whisper model",
            )
            parser.add_argument(
                "--model",
                type=str,
                default="tiny.en",
                dest="model",
                help="The model type of the whisper",
            )
            parser.add_argument(
                "--model_dir",
                type=str,
                default=None,
                dest="model_dir",
                help="The directory where the model is stored",
            )
            parser.add_argument(
                "--model_cache_dir",
                type=str,
                default=None,
                dest="model_cache_dir",
                help="The directory where the model cache is stored",
            )
            parser.add_argument(
                "--lan",
                type=str,
                default="en",
                dest="lan",
                help="The language of the model",
            )
            parser.add_argument(
                "-l",
                "--log-level",
                dest="log_level",
                choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                help="Set the log level",
                default="DEBUG",
            )
            parser.add_argument(
                "--task", type=str, default="asr", dest="task", help="The task"
            )
            parser.add_argument(
                "--buffer_trimming",
                type=str,
                default="segment",
                choices=["sentence", "segment"],
                help='Buffer trimming strategy -- trim completed sentences marked with punctuation mark and detected by sentence segmenter, or the completed segments returned by Whisper. Sentence segmenter must be installed for "sentence" option.',
            )
            parser.add_argument(
                "--buffer_trimming_sec",
                type=float,
                default=15,
                help="Buffer trimming length threshold in seconds. If buffer length is longer, trimming sentence/segment is triggered.",
                dest="buffer_trimming_sec",
            )
            parser.add_argument(
                "--compute-type",
                type=str,
                default="float16",
                dest="compute_type",
                help="The compute type of the model",
            )
            parser.add_argument(
                "--device",
                type=str,
                default="auto",
                dest="device",
                help="The device of the model (cpu, cuda, auto)",
            )
            parser.add_argument(
                "--num-workers",
                type=int,
                default=1,
                dest="num_workers",
                help="The number of workers for the model",
            )
            parser.add_argument(
                "--cpu-threards",
                type=int,
                default=0,
                dest="cpu_threards",
                help="The number of cpu threads for the model",
            )
            args, _ = parser.parse_known_args()
            kwargs = {}
            for key in ["device", "compute_type", "num_workers", "cpu_threards"]:
                kwargs[key] = getattr(args, key)
            asr, online = asr_factory(args,**kwargs)
            # Set up logging
            set_logging(args, logger)
            cls.instance.online = online
        return cls.instance


def get_asr() -> Optional[ASR]:
    return ASR()


class Audio(BaseModel):
    audio: List[int]


app = FastAPI()


@app.get("/")
async def docs(asr: Optional[ASR] = Depends(get_asr)):
    return RedirectResponse("./docs")


# Define the API endpoints
@app.post("/translate/", response_class=ORJSONResponse)
async def translate(
    body: Annotated[
        Audio,
        Body(
            openapi_examples={
                "short_audio": {
                    "summary": "A very short audio.",
                    "value": {"audio": [1, 2, 4, 3, 9, 8]},
                }
            }
        ),
    ],
    asr: Optional[ASR] = Depends(get_asr),
):
    asr.online.insert_audio_chunk(audio=np.array(body.audio, dtype=np.int16))
    begin, end, text = asr.online.process_iter()
    return ORJSONResponse({"text": text})

@app.post("/finish/", response_class=ORJSONResponse)
async def finish(
    body: Annotated[
        Audio,
        Body(
            openapi_examples={
                "short_audio": {
                    "summary": "A very short audio.",
                    "value": {"audio": [1, 2, 4, 3, 9, 8]},
                }
            }
        ),
    ],
    asr: Optional[ASR] = Depends(get_asr),
):

    asr.online.insert_audio_chunk(audio=np.array(body.audio, dtype=np.int16))
    begin, end, text = asr.online.finish()
    asr.online.init()
    return ORJSONResponse({"text": text})



@app.get("/reset/", response_class=ORJSONResponse)
async def reset(asr: Optional[ASR] = Depends(get_asr)):
    asr.online.init()
    return ORJSONResponse({"success": True})


# Main function to start the server
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port-whisper", type=int, default=8080, dest="port", help="Port to listen on"
    )
    args, _ = parser.parse_known_args()
    uvicorn.run(app, host="localhost", port=args.port)


if __name__ == "__main__":
    main()
