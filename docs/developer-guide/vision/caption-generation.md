# Caption Generation

As an addition to its [built-in AI capabilities](tensorflow/index.md), PhotoPrism lets you generate image captions through a direct [Ollama](https://ollama.com/search?c=vision) integration, as [described in this guide](#ollama-setup-guide).

It allows you to choose from the [available vision models](https://ollama.com/search?c=vision) and [customize the prompts](../../user-guide/ai/ollama-models.md#caption-prompts) according to your needs.

## Ollama Setup Guide

Follow the [steps in our User Guide](../../user-guide/ai/using-ollama.md) to connect PhotoPrism directly to an Ollama instance and generate captions with [vision-capable LLMs](https://ollama.com/search?c=vision).

[Learn more ›](../../user-guide/ai/using-ollama.md)

### Configuration Tips

PhotoPrism evaluates models from the bottom of the list up, so placing the Ollama entries after the others ensures Ollama is chosen first while the others remain available as fallback options.

Ollama-generated captions and labels are stored with the `ollama` metadata source automatically, so you do not need to request a specific `source` field in the schema or pass `--source` to the CLI unless you want to override the default.

!!! tip "Prompt Localization"
    To generate output in other languages, keep the base instructions in English and add the desired language (e.g., "Respond in German"). This method works for both [caption](../../user-guide/ai/ollama-models.md#qwen3-vl-caption) and [label prompts](../../user-guide/ai/ollama-models.md#qwen3-vl-labels).

    **Verify each model type separately.** A model can honor the requested language for captions and silently ignore it for labels — `gemma4:e2b` returned correct Arabic and Hebrew captions while returning English labels on every request, with no error and nothing in the log. Correct script also does not imply correct content. [Learn more ›](../../user-guide/ai/ollama-models.md#language-support)

## Troubleshooting ##

### Verifying Your Configuration ###

If you encounter issues, a good first step is to verify how PhotoPrism has loaded your `vision.yml` configuration. You can do this by running: 

```bash
docker compose exec photoprism photoprism vision ls
```

This command outputs the settings for all supported and configured model types. Compare the results with your `vision.yml` file to confirm that your configuration has been loaded correctly and to identify any parsing errors or misconfigurations.

### Reasoning Leaking Into Captions ###

If captions contain the model's internal reasoning instead of a description — for example, starting with *"The user wants a concise description of the provided image…"* — the model is a **thinking (reasoning) model** (such as the Qwen3.5 family or `qwen3-vl:*`) with reasoning enabled. Set `Service.Think: "false"` on the model in your `vision.yml` to disable it. PhotoPrism disables Ollama reasoning by default in releases after 260601, so this only occurs on 260601 and earlier or when reasoning was explicitly re-enabled (see [Ollama Models](../../user-guide/ai/ollama-models.md)).

The flag keeps reasoning **out of the output**; it does not stop a reasoning build from generating it, so most of the cost remains. Measured on `qwen3-vl:4b` with reasoning off: about 414 output tokens and 6.6 s for a twelve-word caption, against about 24 tokens and 1.2 s for `qwen3-vl:4b-instruct`. Treat `Service.Think` as a correctness guard, and switch to an `-instruct` tag if you also want the performance back — the two are separate decisions.

### GPU Performance Issues ###

When using Ollama with GPU acceleration, you may experience performance degradation over time due to VRAM management issues. This typically manifests as processing times gradually increasing and the Ollama service appearing to "crash" while still responding to requests, but without GPU acceleration.

The issue occurs because Ollama's VRAM allocation doesn't properly recover after processing multiple requests, leading to memory fragmentation and eventual GPU processing failures.

The Ollama service does not automatically recover from these VRAM issues. To restore full GPU acceleration, manually restart the Ollama container:

```bash
docker compose stop ollama
docker compose up -d ollama
```

This should clear the VRAM and restore normal GPU-accelerated processing performance. `stop` restarts the existing container; `docker compose down ollama` works too, but removes and recreates it, which is more than a VRAM reset needs.
