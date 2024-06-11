import os

import torch

from nexfort.dynamo.backends.nexfort import nexfort
from nexfort.fx_compiler import apply_mode, apply_options


def nexfort_compile(
    model,
    *,
    fullgraph=False,
    dynamic=None,
    mode=None,
    options=None,
    disable=False,
    backend="nexfort",
):
    if dynamic is None:
        dynamic = os.environ.get("NEXFORT_COMPILE_DYNAMIC")
        if dynamic is not None:
            dynamic = dynamic == "1"

    cublaslt_workspace_size = os.environ.get("CUBLASLT_WORKSPACE_SIZE")
    if cublaslt_workspace_size is None:
        from nexfort.utils import checks

        # https://docs.nvidia.com/cuda/cublas/#cublassetworkspace
        if checks.cuda_capability_compare("lt", 9, 0):
            os.environ["CUBLASLT_WORKSPACE_SIZE"] = str(4 * 1024)
        elif checks.cuda_capability_compare("ge", 9, 0):
            os.environ["CUBLASLT_WORKSPACE_SIZE"] = str(32 * 1024)

    if backend == "nexfort":
        config = {}
        if dynamic is not None:
            config["inductor.dynamic"] = dynamic
        apply_mode(config, mode, model=model)
        apply_options(config, options)
        mode = None
        options = config

    model = torch.compile(
        model,
        fullgraph=fullgraph,
        dynamic=dynamic,
        backend=nexfort if backend == "nexfort" else backend,
        mode=mode,
        options=options,
        disable=disable,
    )
    return model
