#!/usr/bin/env python3
"""Minimal Diffusers inference example for Dreampal.

Usage:
    python inference.py --prompt "a portrait of a woman in a sunlit apartment"
    python inference.py --fast --prompt "a portrait of a woman at night"

The script expects the checkpoint and the two BSY embeddings to be in the
working directory (or pass explicit paths).
"""

import argparse
import os
import sys

import torch
from diffusers import (
    EulerAncestralDiscreteScheduler,
    LCMScheduler,
    StableDiffusionXLPipeline,
)
from safetensors.torch import load_file

PROMPT_PREFIX = "score_9, score_8_up, score_7_up,"
POSITIVE_EMBED = "BSY_General_Positives_V1_PRO"
NEGATIVE_EMBED = "BSY_Anatomy_Negatives_V1_PRO"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate an image with Dreampal")
    p.add_argument(
        "--model",
        default="dreampal-fp16.safetensors",
        help="Path to the Dreampal checkpoint (default: dreampal-fp16.safetensors)",
    )
    p.add_argument(
        "--fast",
        action="store_true",
        help="Use the DMD2 build defaults (8 steps, CFG 1.1, LCM)",
    )
    p.add_argument("--prompt", required=True, help="Your prompt, without the score prefix")
    p.add_argument(
        "--negative",
        default=NEGATIVE_EMBED,
        help=f"Negative prompt (default: {NEGATIVE_EMBED})",
    )
    p.add_argument("--steps", type=int, default=None, help="Sampling steps")
    p.add_argument("--cfg", type=float, default=None, help="Guidance scale")
    p.add_argument("--width", type=int, default=768)
    p.add_argument("--height", type=int, default=1152)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--embeddings-dir",
        default="embeddings",
        help="Directory containing the BSY embeddings (default: embeddings)",
    )
    p.add_argument("--output", default="dreampal.png")
    p.add_argument(
        "--cpu-offload",
        action="store_true",
        help="Use model CPU offload instead of keeping everything on the GPU",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if not os.path.exists(args.model):
        print(f"Checkpoint not found: {args.model}", file=sys.stderr)
        return 1

    steps = args.steps if args.steps is not None else (8 if args.fast else 20)
    cfg = args.cfg if args.cfg is not None else (1.1 if args.fast else 5.0)

    pipe = StableDiffusionXLPipeline.from_single_file(
        args.model,
        torch_dtype=torch.float16,
        use_safetensors=True,
    )

    if args.fast:
        pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    else:
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
            pipe.scheduler.config
        )

    def load_sdxl_embedding(path: str, token: str) -> None:
        """Load an SDXL textual-inversion embedding (clip_l + clip_g layout)."""
        state = load_file(path)
        if "clip_l" in state and "clip_g" in state:
            pipe.load_textual_inversion(
                state["clip_l"],
                token=token,
                text_encoder=pipe.text_encoder,
                tokenizer=pipe.tokenizer,
            )
            pipe.load_textual_inversion(
                state["clip_g"],
                token=token,
                text_encoder=pipe.text_encoder_2,
                tokenizer=pipe.tokenizer_2,
            )
        else:
            pipe.load_textual_inversion(path, token=token)

    for token in (POSITIVE_EMBED, NEGATIVE_EMBED):
        path = os.path.join(args.embeddings_dir, f"{token}.safetensors")
        if os.path.exists(path):
            load_sdxl_embedding(path, token)
        else:
            print(f"Warning: embedding not found, skipping: {path}", file=sys.stderr)

    if args.cpu_offload:
        pipe.enable_model_cpu_offload()
    else:
        pipe.to("cuda")

    prompt = f"{PROMPT_PREFIX} {POSITIVE_EMBED}, {args.prompt}"
    generator = torch.Generator(device="cuda").manual_seed(args.seed)

    image = pipe(
        prompt=prompt,
        negative_prompt=args.negative,
        num_inference_steps=steps,
        guidance_scale=cfg,
        width=args.width,
        height=args.height,
        generator=generator,
    ).images[0]

    image.save(args.output)
    print(f"Saved {args.output} ({args.width}x{args.height}, {steps} steps, CFG {cfg})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
