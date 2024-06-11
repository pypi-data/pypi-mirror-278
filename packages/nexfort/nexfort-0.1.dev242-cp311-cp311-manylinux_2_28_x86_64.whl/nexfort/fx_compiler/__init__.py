import json
import os
import sys
from typing import Any, Dict, Optional

import torch

from nexfort.utils import checks

from nexfort.utils.logging import logger
from .fx_compiler import compile_fx  # noqa: F401


def list_mode_options(mode: Optional[str] = None, dynamic: Optional[bool] = None, model=None) -> Dict[str, Any]:
    quant_options = {
        "inductor.options": {
            "force_fuse_int_mm_with_mul": True,
            "use_mixed_mm": True,
        },
    }
    if checks.triton_version_compare("lt", "3.0.0"):
        # Avoid misaligned address
        quant_options["inductor.options"]["epilogue_fusion"] = False

    mode_options: Dict[str, Dict[str, bool]] = {
        "default": {},
        "cache-all": {
            "inductor.options": {
                "fx_graph_cache": True,
            },
        },
        "max-autotune": {
            "inductor.optimize_linear_epilogue": True,
            "inductor.options": {
                "max_autotune": True,
            },
        },
        "max-optimize": {
            "inductor.unquantized_linear_use_triton_template": True,
            "inductor.fp8_linear_use_triton_template": True,
            "inductor.max_autotune_cublaslt_algos": 3,
            "inductor.options": {
                "coordinate_descent_tuning": True,
                # It causes the compilation to be too slow
                # "coordinate_descent_check_all_directions": True,
                # See torch._inductor.codegen.triton.TritonKernel.should_use_persistent_reduction
                "triton.multi_kernel": 1,
                # TODO: Remove triton.max_block for torch>=2.4.0 once it gets released
                "triton.max_block": {
                    "X": 2048,
                    "Y": 1024,
                    "Z": 1024,
                    "R": 4096 * 16,
                },
            },
        },
        "cudagraphs": {
            "cudagraphs": True,
        },
        "inductor-cudagraphs": {
            "inductor.options": {
                "triton.cudagraphs": True,
            },
        },
        "cpp-wrapper": {
            "inductor.options": {
                "cpp_wrapper": True,
            },
        },
        "freezing": {
            "common.freezing": True,
            # Inductor freezing raises BypassFxGraphCache
            # "inductor.options": {
            #     "freezing": True,
            # },
            "jit.freezing": True,
        },
        "inductor-freezing": {
            "inductor.options": {
                "freezing": True,
            },
        },
        "jit": {
            "inductor.disable": True,
            "jit.disable": False,
        },
        "disable-inductor": {
            "inductor.disable": True,
        },
        "quant": quant_options,
        "low-precision": {
            "overrides.conv_allow_tf32": True,
            "overrides.matmul_allow_tf32": True,
            "overrides.matmul_allow_fp16_reduction": True,
            "overrides.matmul_allow_bf16_reduction": True,
            "triton.enable_fast_math": True,
        },
        "fast-accum": {
            "gemm_use_fast_accum": True,
        },
        "benchmark": {
            "overrides.conv_benchmark": True,
        },
        "disable-runtime-fusion": {
            "inductor.options": {
                "max_fusion_size": 1,
            },
            "jit.disable_optimized_execution": True,
        },
    }
    if mode is None:
        return mode_options
    modes = mode.split(":")
    options = {}
    # Make front modes have higher priority
    for mode in reversed(modes):
        if mode:
            if mode.startswith("quant") and isinstance(model, torch.nn.Module):
                if "torchao" in sys.modules:
                    from nexfort.ao import is_quantized_module

                    if not is_quantized_module(model):
                        continue
                else:
                    continue

            m_o = mode_options.get(mode)
            if m_o is None:
                raise ValueError(f"Unknown mode: {mode}")
            prev_inductor_options = options.get("inductor.options")
            if prev_inductor_options is not None:
                new_inductor_options = m_o.get("inductor.options", {})
                prev_inductor_options.update(new_inductor_options)
            options.update(m_o)
            if prev_inductor_options is not None:
                options["inductor.options"] = prev_inductor_options
    return options


def apply_mode(output_config: Dict[str, Any], mode: Optional[str], model=None):
    if mode is None or mode == "default":
        pass
    else:
        from nexfort.fx_compiler import list_mode_options

        logger.debug(f"Apply mode options for {mode}")
        apply_options(output_config, list_mode_options(mode, model=model))


def apply_options(output_config: Dict[str, Any], options: Optional[Dict[str, Any]]):
    if not options:
        return

    from nexfort.fx_compiler import config as fx_config

    if hasattr(fx_config, "shallow_copy_dict"):
        current_config: Dict[str, Any] = fx_config.shallow_copy_dict()
    else:
        # torch<2.2.0
        current_config: Dict[str, Any] = fx_config.to_dict()

    for key, val in options.items():
        attr_name = key.replace("-", "_")
        if attr_name not in current_config:
            raise RuntimeError(f"Unexpected optimization option {key}, known options are {list(current_config.keys())}")
        if current_config[attr_name] is not None and type(val) is not type(current_config[attr_name]):  # noqa: E721
            val_type_str = type(val).__name__
            expected_type_str = type(current_config[attr_name]).__name__
            raise RuntimeError(f"Unexpected type of attr {key}, got {val_type_str} should be {expected_type_str}")
        if attr_name == "inductor.options" and val is not None and current_config[attr_name] is not None:
            val = val.copy()
            for k, v in current_config[attr_name].items():
                if k not in val:
                    val[k] = v
        output_config[attr_name] = val


def apply_config():
    fx_config = None
    fx_config_str = os.environ.get("NEXFORT_FX_CONFIG")
    if fx_config_str:
        from . import config as fx_config

        if fx_config_str.startswith("{"):
            fx_config_dict = json.loads(fx_config_str)
        else:
            with open(fx_config) as f:
                fx_config_dict = json.load(f)
        fx_config.load_config(fx_config_dict)
    fx_mode_str = os.environ.get("NEXFORT_FX_MODE")
    if fx_mode_str:
        if fx_config is None:
            from . import config as fx_config

        fx_config_dict = {}
        apply_mode(fx_config_dict, fx_mode_str)
        fx_config.load_config(fx_config_dict)


apply_config()
