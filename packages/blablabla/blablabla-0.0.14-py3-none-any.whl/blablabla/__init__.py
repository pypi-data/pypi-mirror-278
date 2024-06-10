__version__ = "0.0.14"

from .whisper_server import main as start_whisper_server
from .typing_server import main as start_typing_server
from .orchestrator import main as start_orchestrator

from .start_all import main as start_all

