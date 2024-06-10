import keyboard
import argparse
import asyncio

import sounddevice as sd
import statesman

from .actions import record_producers, whisper_consumer, text_consumer, ProcessLifecycle


class AppLifecycle(statesman.StateMachine):
    class States(statesman.StateEnum):
        starting = "Starting..."
        recording = "Recording..."
        stopping = "Stopping..."
        stopped = "Terminated."

async def wait():
    await asyncio.sleep(0.001)


async def main_loop():  # streams: Tuple[sd.Stream,asyncio.Queue]):
    """ """
    state = ProcessLifecycle()
    q_whisper = asyncio.Queue()
    q_text = asyncio.Queue()
    await state.enter_state(ProcessLifecycle.States.starting)
    await asyncio.gather(
        record_producers(state, q_whisper, (), lambda x: print(x)),
        whisper_consumer(q_whisper, q_text, state),
        text_consumer(q_text, q_whisper, state),
    )
    await state.enter_state(ProcessLifecycle.States.stopped)


def stream_typing(stream: sd.Stream, loop: asyncio.AbstractEventLoop, *args, **kwargs):
    """ """
    asyncio.ensure_future(main_loop(stream), loop=loop)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stream-hotkey",
        type=str,
        default="ctrl+shift+alt+space",
        dest="stream_hotkey",
        help="The hotkey to stream the recording to keyboard",
    )
    parser.add_argument(
        "--stop",
        type=str,
        default="ctrl+shift+alt+backspace",
        dest="stop",
        help="The hotkey to stop the recording",
    )
    parser.add_argument(
        "--whisper-duration",
        type=int,
        default=1,
        dest="whisper_duration",
        help="The duration of the frame for recording to whisper model",
    )

    kwargs = {}

    sound_device = kwargs.get("sound_device", None)
    if sound_device is None:
        sound_device = 0

    # Add any other arguments you need for your ASR system
    args, _ = parser.parse_known_args()

    loop = asyncio.get_event_loop()

    
    async def listen_for_keys():
        task = asyncio.create_task(wait())
        while True:
            if keyboard.is_pressed(args.stream_hotkey) and task.done():
                task = loop.create_task(main_loop())
            if keyboard.is_pressed(args.stop):
                task.cancel()
                break
            await asyncio.sleep(0.01)

    loop.run_until_complete(listen_for_keys())

if __name__ == "__main__":
    main()
