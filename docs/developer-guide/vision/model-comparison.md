# Vision Model Comparison

!!! note ""
    This page compares models. For configuration examples you can copy into `vision.yml`, see [Ollama Models](../../user-guide/ai/ollama-models.md) in the User Guide. [Learn more ›](../../user-guide/ai/ollama-models.md)

## What Was Measured

All figures on this page come from a single benchmark run on **August 8, 2026**, using **Ollama 0.32.6** at a 4096-token context, over a fixed set of 16 images at 720 px — the resolution PhotoPrism sends. The images span wildlife, pets, macro, food, people, sport, vehicles, architecture, cityscape, OCR, and a UI screenshot, and several are deliberately adversarial.

- **Self-hosted models** ran on an **NVIDIA RTX 4060 (8 GB VRAM, ~7 GB free)**. Every model saw the same daemon, so the self-hosted numbers are valid *relative to each other*.
- **Cloud models** were proxied through the same instance, so their latencies include one extra network hop.

Captions and labels are **measured separately** throughout. They are different workloads with different failure modes, and a model that is good at one is not necessarily good at the other.

!!! warning "Read Latency as Approximate, Especially for Cloud Models"
    Repeating the cloud table a few hours apart on the same day moved one model's label latency from 1.6 s to 10.8 s while its output barely changed. Self-hosted timings reproduced to within a tenth of a second across the same pair of runs. **Rank hosted models on output quality; measure latency yourself when it matters.**

    The self-hosted run also predates capture of the daemon's KV cache and flash-attention settings, so these numbers are not directly comparable against a differently tuned instance. Qwen models are the most sensitive to KV cache quantization — re-measure those locally before acting on them.

## Label Generation

Subject **coverage** is the share of images where the label set named both the main subject and its setting. **Multi-word** is the share of label names containing a space or separator, which matters because [PhotoPrism cannot repair a compound label](label-generation.md#label-behavior-worth-knowing) after the fact.

### Self-Hosted, Built-In Prompt

| Model                           | Size   | Labels p50 | Labels/img | Multi-word | Coverage |
|:--------------------------------|:-------|-----------:|-----------:|-----------:|---------:|
| `qwen3.5:4b`                    | 3.4 GB |      3.0 s |        3.6 |       3.4% |  **88%** |
| `gemma4:e2b`                    | 7.2 GB |      2.5 s |        4.4 |   **0.0%** |      81% |
| `gemma3:4b`                     | 3.3 GB |      3.0 s |        4.1 |       0.0% |      81% |
| `minicpm-v4.5:8b`               | 6.1 GB |      4.3 s |        3.3 |       5.7% |      81% |
| `gemma4:latest` (e4b)           | 9.6 GB |      2.6 s |        2.9 |       0.0% |      78% |
| `minicpm-v4.6:1b`               | 1.6 GB |      0.9 s |        3.3 |      22.6% |      78% |
| `qwen3-vl:4b-instruct`          | 3.3 GB |      2.4 s |        3.0 |       0.0% |      75% |
| `qwen3-vl:8b-instruct`          | 6.1 GB |      5.5 s |        3.0 |       2.1% |      75% |
| `qwen3-vl:4b` (reasoning build) | 3.3 GB |      2.4 s |        2.9 |      21.3% |      69% |
| `qwen3.5:9b`                    | 6.6 GB |      3.5 s |        1.9 |       6.5% |      69% |
| `qwen2.5vl:7b`                  | 6.0 GB |      2.7 s |        1.5 |       0.0% |      59% |
| `qwen3.5:2b`                    | 2.7 GB |      0.8 s |        1.2 |       5.0% |      47% |

Bigger is not reliably better: `qwen3.5:4b` beat both the `2b` and `9b` tiers of its own family, and `gemma4:e2b` beat the larger `e4b`.

### Self-Hosted, With a Label Count in the Prompt

The built-in prompt asks for "label objects" without stating how many, and self-hosted models under-generate as a result. Adding an explicit range (the [Qwen3-VL example](../../user-guide/ai/ollama-models.md#qwen3-vl-labels) shows the shape) multiplied the label set by 1.9–3.5× and raised coverage on **every** model tested, at 1.7–2.8× the latency:

| Model                  | Labels p50 | Labels/img | Multi-word | Coverage |
|:-----------------------|-----------:|-----------:|-----------:|---------:|
| `qwen3-vl:4b-instruct` |      5.1 s |       10.1 |       5.6% |  **97%** |
| `qwen3-vl:8b-instruct` |     11.4 s |        8.5 |       1.5% |      97% |
| `gemma4:e2b`           |      3.9 s |        8.9 |   **0.0%** |      91% |
| `gemma3:4b`            |      8.4 s |       14.1 |       0.4% |      91% |
| `qwen3.5:4b`           |      5.1 s |        7.1 |       3.5% |      91% |
| `minicpm-v4.5:8b`      |      8.7 s |        6.9 |       9.1% |      91% |
| `gemma4:latest` (e4b)  |      6.2 s |        8.7 |       0.0% |      88% |

This is the largest single lever on label quality, and it reverses the ranking above: Qwen3-VL gains the most (+22 points) and leads once the count is stated, while `qwen3.5:4b` — the strongest model on the built-in prompt — gains the least (+3) because it was already close to its ceiling.

### Ollama Cloud

| Model                  | Labels p50 | Labels/img | Multi-word | Coverage |
|:-----------------------|-----------:|-----------:|-----------:|---------:|
| `kimi-k2.7-code:cloud` |      2.3 s |        8.6 |       0.0% |     100% |
| `kimi-k2.6:cloud`      |      2.9 s |        8.6 |       0.0% |     100% |
| `minimax-m3:cloud`     |      2.9 s |       13.4 |       0.0% |     100% |
| `qwen3.5:397b-cloud`   |      5.2 s |        8.4 |       1.5% |     100% |
| `gemma4:31b-cloud`     |     10.8 s |        7.0 |       0.9% |      97% |

Across 192 cloud requests there were no errors, no empty responses, and no malformed JSON. Cloud models also volunteer 7–13 labels per image without being asked for a count, where models fitting in 8 GB return 1–4. Check a model's [plan coverage and per-token terms](../../user-guide/ai/ollama-cloud.md) before running one over a whole library — some sit outside the usage plans entirely.

## Caption Generation

| Model                           | Caption p50 | Length |
|:--------------------------------|------------:|-------:|
| `minicpm-v4.6:1b`               |       0.6 s |   14 w |
| `gemma4:e2b`                    |       0.7 s |    9 w |
| `gemma4:latest` (e4b)           |       0.8 s |   12 w |
| `qwen3.5:4b`                    |       0.9 s |   17 w |
| `qwen3-vl:4b-instruct`          |       1.2 s |   18 w |
| `gemma3:4b`                     |       1.4 s |    9 w |
| `qwen3-vl:4b` (reasoning build) |   **6.6 s** |   11 w |
| `minimax-m3:cloud`              |       2.9 s |   19 w |
| `gemma4:31b-cloud`              |       3.8 s |   12 w |

The outlier is the point: a **reasoning build costs roughly five times the caption latency of its `-instruct` sibling for a shorter caption** — about 414 output tokens against 24. `Service.Think: "false"` keeps that reasoning out of the stored caption but does not stop the model producing it. [Learn more ›](caption-generation.md#reasoning-leaking-into-captions)

## Multilingual Behavior

Same images and prompts with the target language appended. *In language* is a judge model's verdict on the **labels**; *accurate* is its view of whether the content is right.

| Model (self-hosted)    | de in language | ar in language | he in language | de accurate | he accurate |
|:-----------------------|---------------:|---------------:|---------------:|------------:|------------:|
| `qwen3.5:4b`           |            81% |           100% |           100% |         62% |         12% |
| `qwen3-vl:4b-instruct` |            94% |            31% |            75% |         62% |         25% |
| `gemma4:e2b`           |            62% |         **0%** |             6% |         56% |         56% |

| Model (cloud)          | de in language | ar in language | he in language |
|:-----------------------|---------------:|---------------:|---------------:|
| `minimax-m3:cloud`     |           100% |           100% |           100% |
| `gemma4:31b-cloud`     |           100% |           100% |            94% |
| `qwen3.5:397b-cloud`   |            81% |            81% |            75% |
| `kimi-k2.7-code:cloud` |            94% |            44% |            38% |

Two things stand out. **Answering in the right language is a separate question from answering correctly** — `qwen3.5:4b` produced Hebrew labels on every request and got the subject right in 12% of them, which is worse than useless for search. And **a model can honor the language for captions and ignore it for labels**: `gemma4:e2b` returned correct Arabic and Hebrew captions while returning English labels on every request, with no error and nothing in the log.

No self-hosted model that fits in 8 GB cleared both bars. A non-English library is currently better served by a cloud model.

## Prompt Token Cost

What a 720 px image costs in prompt tokens is a property of the model's **vision encoder**, not of the thumbnail:

| Model family                         | Prompt tokens (caption / labels) |
|:-------------------------------------|:---------------------------------|
| `gemma4:e2b`, `gemma4:latest`        | 208 / 284                        |
| `minicpm-v4.5:8b`, `minicpm-v4.6:1b` | 248-256 / 318-332                |
| `gemma3:4b`, `medgemma*:4b`          | 318-319 / 390-396                |
| `qwen3.5:2b / 4b / 9b`               | 408 / 486                        |
| `qwen2.5vl:7b`, `qwen3-vl:*`         | 1112-1123 / 1182                 |

A 5.7× spread for identical input. It is why `gemma4:e2b` prefills in ~140 ms where `gemma3:4b` takes ~770 ms for the same picture, and it matters on a metered endpoint, where prompt tokens are billed per request and a whole-library run multiplies the difference by the number of photos. Switching model can cut prefill more than lowering `Resolution` does.

## Models to Avoid & Compatibility Notes

- **`medgemma:4b` / `medgemma1.5:4b`** — trained for grounded detection rather than classification. `medgemma1.5:4b` returned a well-formed but **empty** label array on every image, which is a model-fit problem rather than a schema error. [Learn more ›](label-generation.md#valid-json-but-no-labels)
- **`qwen2.5vl:7b`** — the weakest general labeler measured (59% coverage, 1.5 labels per image) despite being a capable captioner. Its [documented](https://ollama.com/library/qwen2.5vl#readme) requirement for Ollama 0.7.0 no longer appears to hold: we ran 32 requests against it on Ollama 0.32.6 with zero errors. If you do hit problems, the FP16 variant (`qwen2.5vl:3b-fp16`) remains a workaround.
- **`minicpm-v4.6:1b`** — the fastest labeler here and better at subjects than its size suggests, but 22.6% of its label names were multi-word, so its output needs review before it reaches a library.

## Keeping This Page Current

These figures come from an internal harness that keeps the image set, prompts, and scoring fixed, so a refresh means re-running it rather than repeating a study by hand. Independent reproduction by readers is explicitly not a goal — the point is that *we* can refresh the page cheaply when models change.

A previous version of this page reported a caption-only study of Qwen2.5-VL and Gemma 3 run on an AMD Ryzen AI 9 365 **CPU**, with per-image times of 24–36 s. Those figures described CPU inference of models we no longer recommend and have been superseded by the run above; they are not comparable to the GPU timings on this page.

!!! example ""
    We welcome contributions to our computer vision documentation. If you have any additions or suggestions for improvements, please click the :material-file-edit-outline: button in the upper right corner of the page to send a pull request.
