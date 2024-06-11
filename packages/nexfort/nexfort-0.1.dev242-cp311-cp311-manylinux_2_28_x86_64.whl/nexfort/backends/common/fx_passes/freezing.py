from typing import List

import torch

from nexfort.utils import checks
from nexfort.utils.logging import logger


def fx_pass_freeze(gm: torch.fx.GraphModule, example_inputs: List[torch.Tensor]) -> torch.fx.GraphModule:
    if not checks.is_inductor_supported():
        logger.warning("Inductor is not supported. Skip freezing.")
        return gm

    from torch._guards import tracing
    from torch._inductor.freezing import freeze

    with tracing(None):
        gm = freeze(None, gm, example_inputs)[0]

    return gm
