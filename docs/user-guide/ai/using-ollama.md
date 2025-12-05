# Ollama Setup Guide

Learn how to set up and connect a self-hosted Ollama instance to generate detailed captions and accurate labels for your pictures with [vision-capable LLMs](https://ollama.com/search?c=vision).

## Step 1: Install Ollama

To run Ollama on the same server as PhotoPrism, add the `ollama` service to the `services` section of your `compose.yaml` (or `docker-compose.yml`) file, as shown in the example below.[^1]

Alternatively, most of the [`compose.yaml`](../../getting-started/docker-compose.md) [configuration examples](https://dl.photoprism.app/docker/compose.yaml) on our download server already have Ollama preconfigured, so you can start it with the following command (remove `profiles: ["ollama"]` from the `ollama` service to start it by default, without using `--profile ollama`):

```
docker compose --profile ollama up -d
```

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
      ## docker compose exec ollama ollama pull gemma3:latest
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
          OLLAMA_FLASH_ATTENTION: "false" # enables the experimental flash attention feature
          OLLAMA_KV_CACHE_TYPE: "f16"     # cache quantization (f16, q8_0, or q4_0)
          OLLAMA_SCHED_SPREAD: "false"    # allows scheduling models across all GPUs.
          OLLAMA_NEW_ENGINE: "true"       # enables the new Ollama engine
          # OLLAMA_DEBUG: "true"            # shows additional debug information
          # OLLAMA_INTEL_GPU: "true"        # enables experimental Intel GPU detection
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

Note that the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) must be installed for GPU hardware acceleration to work. Experienced users may also run Ollama on a separate, more powerful server.

!!! danger ""
    Ollama does not enforce authentication by default. Only expose port `11434` inside trusted networks or behind a reverse proxy that adds access control.

## Step 2: Download Models

Once the Ollama service is running (see [Step 1](#step-1-install-ollama)), you can download [any of the listed vision models](https://ollama.com/search?c=vision) that match your hardware capabilities and preferences, as you will need it for the next step. For example:

```bash
docker compose exec ollama ollama pull gemma3:latest
```

[Learn more ›](ollama-models.md)

## Step 3: Configure Models

Now, create a new `config/vision.yml` file or edit the existing file in [the *storage* folder](../../getting-started/docker-compose.md#photoprismstorage) of your PhotoPrism instance, following the example below. Its absolute path from inside the container is `/photoprism/storage/config/vision.yml`:

!!! example "vision.yml"
    ```yaml
    Models:
    - Type: labels
      Model: gemma3:latest
      Engine: ollama
      Run: auto
      Service:
        Uri: http://ollama:11434/api/generate
    - Type: caption
      Model: gemma3:latest
      Engine: ollama
      Run: auto
      Service:
        Uri: http://ollama:11434/api/generate
    ```

[Learn more ›](ollama-models.md#gemma-3-labels)

### Scheduling Options

- `Run: auto` (recommended) automatically runs the model after indexing is complete to prevent slowdowns during indexing or importing. It also [allows manual](cli.md#run-vision-models) and [scheduled invocations](../../getting-started/config-options.md#computer-vision).
- `Run: manual` disables automatic execution, allowing you to [run the model manually](cli.md#run-vision-models) via `photoprism vision run -m caption` or `photoprism vision run -m labels`.

[Learn more ›](index.md#run-modes)

### Configuration Tips

PhotoPrism evaluates models from the bottom of the list up, so placing the Ollama entries after the others ensures Ollama is chosen first while the others remain available as fallback options.

Ollama-generated captions and labels are stored with the `ollama` metadata source automatically, so you do not need to request a specific `source` field in the schema or pass `--source` to the CLI unless you want to override the default.

!!! tip "Prompt Localization"
    To generate output in other languages, keep the base instructions in English and add the desired language (e.g., "Respond in German"). This method works for both [caption](ollama-models.md#qwen3-vl-caption) and [label prompts](ollama-models.md#qwen3-vl-labels).

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

