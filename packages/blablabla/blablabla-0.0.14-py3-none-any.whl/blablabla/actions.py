import numpy as np
import sounddevice as sd
import asyncio

import io
import soundfile as sf

# import webrtcvad
import keyboard
import orjson
import aiohttp
from typing import Tuple
import ssl

import statesman
import logging

from datetime import datetime

def time_format():
    return f"{datetime.now()}|> "


class ProcessLifecycle(statesman.StateMachine):
    class States(statesman.StateEnum):
        starting = "Starting..."
        recording = "Recording..."
        stopping = "Stopping..."
        stopped = "Terminated."


async def record_producers(
    state: ProcessLifecycle,
    q_whisper: asyncio.Queue,
    streams: Tuple[sd.Stream, asyncio.Queue],
    *args,
    **kwargs,
):
    """
    Records audio from the default input device, detects voice activity, and adds
    the detected audio to a queue to be processed by the Whisper API.

    Args:
        status (asyncio.Queue): A queue to store the status of the recording.
        q_whisper (asyncio.Queue): A queue to store the detected audio tokens.
        stop_flag (function): A function to check if the recording should stop.
        *args: Additional arguments passed to the function.
        **kwargs: Additional keyword arguments passed to the function.

    Notes:
        This function records audio from the default input device, detects voice activity
        using the WebRTC VAD (Voice Activity Detection), and adds the detected audio
        to a queue to be processed by the Whisper API.
    """

    sound_device = kwargs.get("sound_device", None)
    if sound_device is None:
        sound_device = 0
    fs = kwargs.get("fs", 16000)
    duration = kwargs.get("duration", 30)
    whisper_duration = kwargs.get("whisper_duration", 4)  ## in seconds
    channels = kwargs.get("channels", 1)
    dtype = kwargs.get("dtype", np.int16)
    device_index = kwargs.get("device_index", 0)
    device_name = kwargs.get("device_name", None)
    recording_type = kwargs.get("recording_type", "press_to_toggle")
    activation_key = kwargs.get("activation_key", "ctrl+shift+space")
    num_silence_frames = kwargs.get("silence_duration", 800) // duration
    # vad = webrtcvad.Vad(3)  # Aggressiveness mode: 3 (highest)
    buffer = []
    recording = []
    if device_name is None:
        device_name = sd.query_devices(device_index, kind="input")
    q_in = asyncio.Queue()
    loop = asyncio.get_event_loop()

    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(q_in.put_nowait, (indata.copy(), status))

    await state.enter_state(ProcessLifecycle.States.recording)

    stream = sd.InputStream(
        samplerate=fs,
        channels=channels,
        dtype=dtype,
        blocksize=fs * duration // 1000,
        device=sound_device,
        callback=callback,
        **kwargs,
    )
    await state.enter_state(ProcessLifecycle.States.recording)
    with stream:
        while True:
            indata, status = await q_in.get()
            buffer.extend(indata[:, 0])
            if len(buffer) >= fs * duration // 1000:
                frame = buffer[: fs * duration // 1000]
                buffer = buffer[fs * duration // 1000 :]
                if recording_type == "press_to_toggle":
                    if len(recording) > 0 and keyboard.is_pressed(activation_key):
                        await state.enter_state(ProcessLifecycle.States.stopping)
                        break
                    else:
                        recording.extend(frame)
                if recording_type == "hold_to_record":
                    if keyboard.is_pressed(activation_key):
                        recording.extend(frame)
                    else:
                        await state.enter_state(ProcessLifecycle.States.stopping)
                        break
                elif recording_type == "voice_activity_detection":
                    is_speech = True  # vad.is_speech(np.array(frame).tobytes(), fs)
                    if is_speech:
                        recording.extend(frame)
                        num_silent_frames = 0
                    else:
                        if len(recording) > 0:
                            num_silent_frames += 1
                        if num_silent_frames >= num_silence_frames:
                            await state.enter_state(ProcessLifecycle.States.stopping)
                            break

                if len(recording) % (fs * whisper_duration) < fs * duration // 1000:
                    ## Add the audio sound to the whisper queue.
                    await state.enter_state(ProcessLifecycle.States.recording)
                    q_whisper.put_nowait(recording[-fs * whisper_duration :])
                    if len(recording) > fs * whisper_duration * 10:
                        ## Avoid infinitely long recording
                        recording = recording[fs * whisper_duration :]

        recording_left = len(recording) % fs * whisper_duration
        q_whisper.put_nowait(recording[-recording_left:])


async def whisper_consumer(
    q_whisper: asyncio.Queue,
    q_text: asyncio.Queue,
    state: ProcessLifecycle,
    *args,
    **kwargs,
):
    """
    Consumes audio tokens from the whisper queue, sends them to the Whisper API,
    and puts the resulting text into the text queue.

    Args:
        q_whisper (asyncio.Queue): A queue containing the audio tokens to be processed.
        q_text (asyncio.Queue): A queue to store the resulting text.
        q_status (asyncio.Queue): A queue to store the status of the function.
        *args: Additional arguments passed to the function.
        **kwargs: Additional keyword arguments passed to the function.

    Notes:
        This function consumes audio tokens from the whisper queue, sends them to the
        Whisper API, and puts the resulting text into the text queue. It uses the aiohttp
        library to make a POST request to the Whisper API endpoint.
    """
    whisper_port = kwargs.get("whisper_port", 8080)
    # Create an aiohttp client session
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    conn = aiohttp.TCPConnector(verify_ssl=False)  # ,ssl_context=ssl_ctx)
    async with aiohttp.ClientSession(
        base_url=f"http://127.0.0.1:{whisper_port}", trust_env=True, connector=conn
    ) as session:
        session._default_verified = False  # disable SSL verification
        # Loop indefinitely to consume whispers from the queue
        while True:
            # Get the next whisper from the queue
            token = await q_whisper.get()
            payload = orjson.dumps({"audio": token}, option=orjson.OPT_SERIALIZE_NUMPY)
            headers = {
                "Content-Type": "application/json",
                "accept": "application/json",
            }
            # Post the payload to the REST API endpoint
            if state.state == ProcessLifecycle.States.recording:
                async with session.post(
                    "/translate/",
                    data=payload,
                    headers=headers,
                    ssl=False,
                ) as response:
                    try:
                        # Wait for the response text
                        text = await response.text()
                        if orjson.loads(text)['text'].strip():  # only send to the queue if the text is not empty or only whitespaces
                            q_text.put_nowait(text)
                    except aiohttp.ClientError as e:
                        print("Whisper did not process correctly the audio")
                    q_whisper.task_done()
            if q_whisper.qsize() > 2:
                logging.warning(
                    f"The whisper queue size is dangerously large {q_whisper.qsize()}, the whisper buffer needs to be increase to allow whisper to process the audio file."
                )
            if state.state == ProcessLifecycle.States.stopping:
                if q_whisper.qsize() > 1:
                    async with session.post(
                        "/translate/",
                        data=payload,
                        headers=headers,
                        ssl=False,
                    ) as response:
                        try:
                            # Wait for the response text
                            text = await response.text()
                            if orjson.loads(text)['text'].strip():  # only send to the queue if the text is not empty or only whitespaces
                                q_text.put_nowait(text)
                        except aiohttp.ClientError as e:
                            print("Whisper did not process correctly the audio")
                        q_whisper.task_done()

                if q_whisper.qsize() == 1:
                    async with session.post(
                        "/finish/",
                        data=payload,
                        headers=headers,
                        ssl=False,
                    ) as response:
                        try:
                            # Wait for the response text
                            text = await response.text()
                            if orjson.loads(text)['text'].strip():  # only send to the queue if the text is not empty or only whitespaces
                                q_text.put_nowait(text)
                        except aiohttp.ClientError as e:
                            print("Whisper did not process correctly the audio")
                        q_whisper.task_done()

                if q_whisper.qsize() == 0:
                    ## Stop the consumer after the queue is empty and the recording is stopping
                    q_text.put_nowait("<<STOP>>")
                    break


async def text_consumer(
    q_text: asyncio.Queue, q_whisper: asyncio.Queue,  state: ProcessLifecycle, *args, **kwargs
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
    keyboard_port = kwargs.get("keyboard_port", 8081)
    # Create an aiohttp client session
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    conn = aiohttp.TCPConnector(verify_ssl=False)  # ,ssl_context=ssl_ctx)
    async with aiohttp.ClientSession(
        base_url=f"http://127.0.0.1:{keyboard_port}", trust_env=True, connector=conn
    ) as session:
        session._default_verified = False  # disable SSL verification
        # Loop indefinitely to consume whispers from the queue
        while True:
            # Get the next whisper from the queue
            token = await q_text.get()
            if token == "<<STOP>>":
                break
            # Convert the audio token to a hexadecimal string
            payload = orjson.dumps({"text": token})
            # Post the payload to the REST API endpoint
            try:
                async with session.post(
                    "/write/",
                    data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "accept": "application/json",
                    },
                    ssl=False,
                ) as response:
                    # Wait for the response text
                    await response.text()
                    q_text.task_done()

            except (aiohttp.ClientError, asyncio.TimeoutError, aiohttp.ClientOSError):
                print("Error processing tokens")
                await asyncio.sleep(0.1)
                
            if state.state == ProcessLifecycle.States.stopping and q_text.empty() and q_whisper.empty():
                ## Stop the consumer after the queue is empty and the recording is stopping
                break
