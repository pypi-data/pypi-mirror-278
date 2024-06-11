import importlib.util
import os
import sys

# Avoid ImportError when importing C extensions.
# ImportError: libc10.so: cannot open shared object file: No such file or directory
import torch

for extension, notice in [
    ["_C", None],
    ["_C_inductor", None],
    ["_C_cuda", "Or is it compatible with your CUDA Toolkit installation?"],
    ["_C_cutlass", "Or is it compatible with your CUDA Toolkit installation?"],
]:
    if importlib.util.find_spec(f"nexfort.{extension}") is None:
        exec(f"{extension} = None")
        continue

    try:
        exec(f"import nexfort.{extension} as {extension}")
    except ImportError:
        print(
            "Unable to load nexfort.{extension} module. Is it compatible with your PyTorch installation?",
            file=sys.stderr,
        )
        if notice is not None:
            print(notice, file=sys.stderr)
        raise

try:
    from ._version import version as __version__, version_tuple
except ImportError:
    __version__ = "unknown version"
    version_tuple = (0, 0, "unknown version")

if os.getenv("NEXFORT_DEBUG") == "1":
    from nexfort.utils.logging import logger

    logger.setLevel("DEBUG")
