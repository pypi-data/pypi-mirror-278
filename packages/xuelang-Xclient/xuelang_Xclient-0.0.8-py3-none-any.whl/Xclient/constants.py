import os
import pathlib

DEFAULT_HTTP_PORT = 8000
DEFAULT_GRPC_PORT = 8001
DEFAULT_METRICS_PORT = 8002
TRITON_LOCAL_IP = "127.0.0.1"
TRITON_CONTEXT_FIELD_NAME = "triton_context"
TRITON_PYTHON_BACKEND_INTERPRETER_DIRNAME = "python_backend_interpreter"
DEFAULT_TRITON_STARTUP_TIMEOUT_S = 120
CREATE_TRITON_CLIENT_TIMEOUT_S = 10

__DEFAULT_PYTRITON_HOME = os.path.join(os.getenv("XDG_CACHE_HOME", "$HOME/.cache"), "pytriton")
__PYTRITON_HOME = os.path.expanduser(os.path.expandvars(os.getenv("PYTRITON_HOME", __DEFAULT_PYTRITON_HOME)))
PYTRITON_HOME = pathlib.Path(__PYTRITON_HOME).resolve().absolute()