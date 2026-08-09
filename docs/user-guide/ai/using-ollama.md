# Ollama Setup Guide

Learn how to set up and connect a self-hosted Ollama instance to generate detailed captions and accurate labels for your pictures with [vision-capable LLMs](https://ollama.com/search?c=vision).

## Step 1: Install Ollama

To run Ollama on the same server as PhotoPrism, add the `ollama` service to the `services` section of your `compose.yaml` (or `docker-compose.yml`) file, as shown in the example below.[^1]

Alternatively, most of the [`compose.yaml`](../../getting-started/docker-compose.md) [configuration examples](https://dl.photoprism.app/docker/compose.yaml) on our download server already have Ollama preconfigured, so you can start it with the following command (remove `profiles: ["ollama"]` from the `ollama` service to start it by default, without using `--profile ollama`):

```
docker compose --profile ollama up -d
```

Note that Ollama does not require authentication by default, so only expose port `11434` within **trusted networks** or behind a reverse proxy with access control.
Experienced users can set up and operate Ollama on a dedicated server shared by multiple instances.
The [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) must be installed for NVIDIA GPU acceleration to work.

!!! example "compose.yaml"
    ```yaml
    services:
      photoprism:
        ## The ":preview" build gives early access to new features:
        image: photoprism/photoprism:preview
        ...

      ## Ollama Large-Language Model Runner (optional)
      ## Run "ollama pull [name]:[version]" to download a vision model
      ## listed at <https://ollama.com/search?c=vision>, for example:
      ## docker compose exec ollama ollama pull gemma4:latest
      ollama:
        image: ollama/ollama:latest
        restart: unless-stopped
        stop_grace_period: 15s
        ## Insecurely exposes the Ollama service on port 11434
        ## without authentication (for private networks only):
        # ports:
        #  - "11434:11434"
        environment:
          ## Ollama Configuration Options:
          OLLAMA_HOST: "0.0.0.0:11434"
          OLLAMA_MODELS: "/root/.ollama"  # model storage path (see volumes section below)
          OLLAMA_MAX_QUEUE: "100"         # maximum number of queued requests
          OLLAMA_NUM_PARALLEL: "1"        # maximum number of parallel requests
          OLLAMA_MAX_LOADED_MODELS: "1"   # maximum number of loaded models per GPU
          OLLAMA_LOAD_TIMEOUT: "5m"       # maximum time for loading models (default "5m")
          OLLAMA_KEEP_ALIVE: "5m"         # duration that models stay in memory (default "5m")
          OLLAMA_CONTEXT_LENGTH: "4096"   # maximum input context length
          OLLAMA_MULTIUSER_CACHE: "false" # optimize prompt caching for multi-user scenarios
          OLLAMA_NOPRUNE: "false"         # disables pruning of model blobs at startup
          OLLAMA_NOHISTORY: "true"        # disables readline history
          OLLAMA_FLASH_ATTENTION: "true"  # required for OLLAMA_KV_CACHE_TYPE quantization
          OLLAMA_KV_CACHE_TYPE: "f16"     # cache precision: f16 (default), q8_0, q4_0
          OLLAMA_SCHED_SPREAD: "false"    # allows scheduling models across all GPUs.
          # OLLAMA_DEBUG: "true"            # shows additional debug information
          # OLLAMA_INTEL_GPU: "true"        # enables experimental Intel GPU detection
          ## Telemetry / privacy opt-outs (containers do not inherit /etc/environment):
          DO_NOT_TRACK: "true"
          HF_HUB_DISABLE_TELEMETRY: "1"
          # OLLAMA_NO_CLOUD: "1"            # uncomment to disable Ollama Cloud models/features
          ## NVIDIA GPU Hardware Acceleration (optional):
          # NVIDIA_VISIBLE_DEVICES: "all"
          # NVIDIA_DRIVER_CAPABILITIES: "compute,utility"
        volumes:
          - "./ollama:/root/.ollama"
        ## NVIDIA GPU Hardware Acceleration (optional):
        # deploy:
        #  resources:
        #    reservations:
        #      devices:
        #        - driver: "nvidia"
        #          capabilities: [ gpu ]
        #          count: "all"
    ```

### Flash Attention & KV Cache

**`OLLAMA_FLASH_ATTENTION`** enables a small speedup on supported model architectures (`gemma3`, `gptoss`, `mistral3`, `qwen3*`). It silently no-ops on unsupported architectures and on CPU. **Required** if you also enable `OLLAMA_KV_CACHE_TYPE` quantization. Set to `"false"` if you use [Qwen3-2507 builds](https://github.com/ollama/ollama/issues/12432) — they are incompatible with flash attention.

**`OLLAMA_KV_CACHE_TYPE`** controls the precision of the per-token attention key/value cache:

- **`f16`** (default) — native precision, works for every architecture, no quality loss.
- **`q8_0`** — halves cache VRAM; clean for `qwen3*` / `gpt-oss` / `mistral3`; causes [a 5x slowdown](https://github.com/ollama/ollama/issues/11949) on [`gemma3`](https://ollama.com/library/gemma3); silently falls back to `f16` for [`gemma4`](https://ollama.com/library/gemma4) / [`qwen2.5vl`](https://ollama.com/library/qwen2.5vl) (not on the [flash-attention allowlist](https://github.com/ollama/ollama/issues/13337)).
- **`q4_0`** — quarters cache VRAM; still usable on Qwen, noticeably degrades Gemma; only reach for it when VRAM-constrained.

!!! tldr ""
    The defaults [used in the example](#step-1-install-ollama) above (`OLLAMA_FLASH_ATTENTION: "true"` + `OLLAMA_KV_CACHE_TYPE: "f16"`) are a safe combination for our [recommended models](ollama-models.md) on typical hardware.

## Step 2: Download Models

Once the Ollama service is running (see [Step 1](#step-1-install-ollama)), you can download [any of the listed vision models](https://ollama.com/search?c=vision) that match your hardware capabilities and preferences, as you will need it for the next step. For example:

```bash
docker compose exec ollama ollama pull gemma4:latest
```

[Learn more ›](ollama-models.md)

## Step 3: Configure Models

Now, create a new `vision.yml` file in your config path (default: `storage/config`) or edit the existing file in [the *storage/config* folder](../../getting-started/docker-compose.md#photoprismstorage) of your PhotoPrism instance, following the example below. Its absolute path from inside the container is `/photoprism/storage/config/vision.yml`:

!!! info ""
    If PhotoPrism can’t read your config file, make sure the file exists at the config path configured for your instance. Older installations may use `storage/settings`.

    Run `docker compose exec photoprism photoprism show config | grep config-path` to find out what's your configured config path.

!!! example "vision.yml"
    ```yaml
    Models:
    - Type: labels
      Model: gemma4:latest
      Engine: ollama
      Run: auto
      Service:
        Uri: http://ollama:11434/api/generate
        Think: "false"
    - Type: caption
      Model: gemma4:latest
      Engine: ollama
      Run: auto
      Service:
        Uri: http://ollama:11434/api/generate
        Think: "false"
    ```

[Learn more ›](ollama-models.md#gemma-4-labels)

### Scheduling Options

- `Run: auto` (recommended) automatically runs the model after indexing is complete to prevent slowdowns during indexing or importing. It also [allows manual](cli.md#run-vision-models) and [scheduled invocations](../../getting-started/config-options.md#computer-vision).
- `Run: manual` disables automatic execution, allowing you to [run the model manually](cli.md#run-vision-models) via `photoprism vision run -m caption` or `photoprism vision run -m labels`.

[Learn more ›](index.md#run-modes)

### Configuration Tips

PhotoPrism evaluates models from the bottom of the list up, so placing the Ollama entries after the others ensures Ollama is chosen first while the others remain available as fallback options.

Ollama-generated captions and labels are stored with the `ollama` metadata source automatically, so you do not need to request a specific `source` field in the schema or pass `--source` to the CLI unless you want to override the default.

!!! tip "Prompt Localization"
    To generate output in other languages, keep the base instructions in English and add the desired language (e.g., "Respond in German"). This method works for both [caption](ollama-models.md#qwen3-vl-caption) and [label prompts](ollama-models.md#qwen3-vl-labels).

!!! info "NSFW Detection"
    When you serve the `labels` model through Ollama, NSFW detection is **not** automatic. PhotoPrism asks the model to include NSFW classification in the same response only when **both** `PHOTOPRISM_DETECT_NSFW=true` and `PHOTOPRISM_EXPERIMENTAL=true` are set. Without that combination, running `photoprism vision run -m labels` skips NSFW flagging even if the LLM "knows" the content is unsafe. See [NSFW Detection](nsfw.md) for the full matrix.

## Step 4: Restart PhotoPrism

Run the following commands to restart `photoprism` and apply the new settings:

```bash
docker compose stop photoprism
docker compose up -d
```

You should now be able to use the `photoprism vision` [CLI commands](./cli.md#run-vision-models) when [opening a terminal](../../getting-started/docker-compose.md#opening-a-terminal), e.g. `photoprism vision run -m caption` to generate captions, or `photoprism vision run -m labels` to generate labels.

[Learn more ›](cli.md#run-vision-models)

## Troubleshooting

### Verifying Your Configuration

If you encounter issues, a good first step is to verify how PhotoPrism has loaded your [`vision.yml`](index.md#visionyml-reference) configuration. You can do this by running:

```bash
docker compose exec photoprism photoprism vision ls
```

This command outputs the settings for all supported and configured model types. Compare the results with your [`vision.yml`](index.md#visionyml-reference) file to confirm that your configuration has been loaded correctly and to identify any parsing errors or misconfigurations.

### Performing Test Runs

The following [terminal commands](../../getting-started/docker-compose.md#opening-a-terminal) will perform a single run for the specified model type:

```bash
photoprism vision run -m labels --count 1 --force
photoprism vision run -m caption --count 1 --force
```

If you don't get the expected results or notice any errors, you can re-run the commands with trace log mode enabled to inspect the request and response:

```bash
photoprism --log-level=trace vision run -m labels --count 1 --force
photoprism --log-level=trace vision run -m caption --count 1 --force
```

### Incomplete Captions with Thinking Models

If you use a reasoning or "thinking" model and notice incomplete or truncated captions, the model may be spending most of its output token budget on internal reasoning, leaving too few tokens for the actual caption.

To fix this, either disable reasoning for that model with `Service.Think: "false"`, switch to a non-thinking model, or increase the `NumPredict` value in your [`vision.yml`](index.md#visionyml-reference) [options](index.md#options) to give the model more room:

```yaml
Models:
- Type: caption
  Model: qwen3-vl:latest
  Engine: ollama
  Service:
    Think: "false"
```

If you still need reasoning enabled, increase the output budget for the final caption:

```yaml
Options:
  NumPredict: 4096
```

### GPU Performance Issues

When using Ollama with GPU acceleration, you may experience performance degradation over time due to VRAM management issues. This typically manifests as processing times gradually increasing and the Ollama service appearing to "crash" while still responding to requests, but without GPU acceleration.

The issue occurs because Ollama's VRAM allocation doesn't properly recover after processing multiple requests, leading to memory fragmentation and eventual GPU processing failures.

The Ollama service does not automatically recover from these VRAM issues. To restore full GPU acceleration, manually restart the Ollama container:

```bash
docker compose down ollama
docker compose up -d ollama
```

This should clear the VRAM and restore normal GPU-accelerated processing performance.

[^1]: Unrelated configuration details have been omitted for brevity.
