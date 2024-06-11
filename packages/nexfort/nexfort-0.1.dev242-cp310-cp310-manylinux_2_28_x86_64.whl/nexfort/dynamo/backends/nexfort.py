from typing import Any, Dict, List, Optional

import torch
from torch._dynamo.backends.registry import register_backend

from nexfort.fx_compiler import compile_fx


@register_backend
def nexfort(
    gm: torch.fx.GraphModule,
    example_inputs: List[torch.Tensor],
    mode: Optional[str] = None,
    options: Dict[str, Any] = None,
):
    return compile_fx(gm, example_inputs, mode=mode, options=options)
