# Org homepage snippets — SDXL Uncensored Omni

These blocks were removed from the public org homepages while the repositories are
private. Add them back after `chatrlabs/SDXL-Uncensored-Omni` is public.

## HF org homepage — `chatrlabs/README` Space

Insert under `## 🚀 Featured Releases`, before the Qwen entry.

```markdown
### [SDXL Uncensored Omni](https://huggingface.co/chatrlabs/SDXL-Uncensored-Omni)

Chatr Labs' uncensored SDXL/Pony-family checkpoint, released in two builds: a **20-step quality** build and an **8-step DMD2** fast build. Both are complete single-file checkpoints with the VAE and both text encoders included.

- Quality build: **20 steps**, **CFG 5.0**, `euler_a`
- DMD2 build: **8 steps**, **CFG 1.1**, `LCM`
- Includes the two BSY embeddings and a Diffusers inference example
- [Model card, weights, and samples](https://huggingface.co/chatrlabs/SDXL-Uncensored-Omni)
```

## GitHub org profile — `.github/profile/README.md`

Insert under `## Featured release`, before the Qwen entry.

```markdown
### [SDXL Uncensored Omni](https://github.com/chatrlabs/SDXL-Uncensored-Omni)

Chatr Labs' uncensored SDXL/Pony-family checkpoint, in a **20-step quality** build and an **8-step DMD2** fast build.

- Quality build: **20 steps**, **CFG 5.0**, `euler_a`
- DMD2 build: **8 steps**, **CFG 1.1**, `LCM`
- Complete single-file checkpoints; includes the two BSY embeddings and a Diffusers example
- [Model card and weights on Hugging Face](https://huggingface.co/chatrlabs/SDXL-Uncensored-Omni)
```

## GitHub Pages — `chatrlabs.github.io/index.html`

Insert before the existing `<section id="models" ...>` section. Leave the existing
`Our Models / Coming soon` block untouched.

```html
<section id="featured" style="margin-top:110px">
  <h2>Featured Model</h2>
  <div style="margin:32px auto 0;max-width:640px;border:1px solid #3f3f46;border-radius:12px;padding:28px;text-align:left">
    <h3 style="margin-top:0"><a href="https://github.com/chatrlabs/SDXL-Uncensored-Omni">SDXL Uncensored Omni</a></h3>
    <p style="font-size:17px;margin-bottom:16px">
      Chatr Labs' uncensored SDXL/Pony-family checkpoint, in a 20-step quality build and an 8-step DMD2 fast build.
    </p>
    <ul style="color:#a1a1aa;line-height:1.8;padding-left:20px;margin:0 0 20px">
      <li>Quality: 20 steps · CFG 5.0 · euler_a</li>
      <li>DMD2: 8 steps · CFG 1.1 · LCM</li>
      <li>Single-file checkpoints with BSY embeddings and a Diffusers example</li>
    </ul>
    <div class="buttons" style="margin-top:0">
      <a class="primary" href="https://huggingface.co/chatrlabs/SDXL-Uncensored-Omni">Model &amp; weights</a>
      <a href="https://github.com/chatrlabs/SDXL-Uncensored-Omni">GitHub</a>
    </div>
  </div>
</section>
```
