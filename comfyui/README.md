# ComfyUI workflows — ChatrXL Uncensored

Two ready-to-run workflows, using only built-in ComfyUI nodes.

| File | Checkpoint | Steps | CFG | Sampler | Scheduler |
| --- | --- | ---: | ---: | --- | --- |
| `chatrxl-quality.json` | `chatrxl-uncensored-fp16.safetensors` | 20 | 5.0 | `euler_ancestral` | `normal` |
| `chatrxl-dmd2.json` | `chatrxl-uncensored-dmd2-fp16.safetensors` | 8 | 1.1 | `lcm` | `normal` |

The `*-api.json` files are the same graphs in ComfyUI API format, for scripting and
automated tests.

## 1. Place the files

```
ComfyUI/models/
├── checkpoints/
│   ├── chatrxl-uncensored-fp16.safetensors
│   └── chatrxl-uncensored-dmd2-fp16.safetensors
└── embeddings/
    ├── ChatrXL_General_Positives_V1_PRO.safetensors
    └── ChatrXL_Anatomy_Negatives_V1_PRO.safetensors
```

The checkpoints and both embeddings are in the Hugging Face repository. No custom
nodes are required.

## 2. Load a workflow

In ComfyUI, open the workflow file:

- `chatrxl-quality.json` for the 20-step quality build
- `chatrxl-dmd2.json` for the 8-step DMD2 build

If the checkpoint is not selected automatically, choose it in `Load Checkpoint`.

## 3. Prompt

The two ChatrXL embeddings are loaded automatically from `models/embeddings/` when their
token appears in the prompt. The workflow already uses:

Positive:

```
score_9, score_8_up, score_7_up, ChatrXL_General_Positives_V1_PRO, <your prompt>
```

Negative:

```
ChatrXL_Anatomy_Negatives_V1_PRO
```

## 4. Settings

| Setting | Quality | DMD2 |
| --- | --- | --- |
| Resolution | 768 × 1152 (or 832 × 1216) | 768 × 1152 (or 832 × 1216) |
| Steps | 20 | 8 |
| CFG | 5.0 | 1.1 |
| Sampler | `euler_ancestral` | `lcm` |
| Scheduler | `normal` | `normal` |
| Denoise | 1.0 | 1.0 |

IP-Adapter is optional. The production pipeline uses scale 0.1, but the workflows
here do not require it.

## 5. API usage

Start ComfyUI, then submit an API workflow:

```bash
curl -s http://127.0.0.1:8188/prompt \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": $(cat chatrxl-quality-api.json)}"
```

The response contains a `prompt_id`. Poll `/history/<prompt_id>` for the result.

## Tested with

- ComfyUI 0.43.0
- No custom nodes
- Built-in `euler_ancestral` and `lcm` samplers
