# Caption Generation

As an addition to its [built-in AI capabilities](classification.md), PhotoPrism lets you generate image captions through either a [dedicated Vision Service](service/index.md) or direct [Ollama](https://ollama.com/search?c=vision) integration, as [described in this guide](#ollama-setup-guide).[^1]

It allows you to choose from the [available vision models](https://ollama.com/search?c=vision) and [customize the prompts](#step-3-configure-photoprism) according to your needs.

!!! tldr ""
    This guide only covers a [direct Ollama API integration](https://github.com/photoprism/photoprism/issues/5123). If you are interested in AI and would like to run a dedicated [Vision Service](service/index.md), we recommend [reading the introduction](service/index.md) to get started. [Learn more ›](service/index.md)

!!! warning ""
    The Ollama integration is **under active development**, so the configuration, commands, and other details may change or break unexpectedly. Please keep this in mind and notify us when something doesn't work as expected. Thank you for your help in keeping this documentation updated!

## Ollama Setup Guide

If you only want to use [Ollama](https://ollama.com/search?c=vision) vision models for caption generation, the easiest way is to follow these instructions to set up an Ollama service instance and connect it directly to PhotoPrism.

### Step 1: Install Ollama

To run Ollama on the same server as PhotoPrism, add the `ollama` service to the `services` section of your `compose.yaml` (or `docker-compose.yml`) file, as shown in the example below.[^2]

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
        ## Start ollama first:
        depends_on:
        - ollama 
        ...

      ## Ollama AI Model Runner (optional)
      ## Run "ollama pull [name]:[version]" to download a vision model
      ## listed at <https://ollama.com/search?c=vision>, for example:
      ## docker compose exec ollama ollama pull qwen2.5vl:3b
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
          OLLAMA_MODELS: "/root/.ollama" # model storage path (see volumes section below)
          OLLAMA_MAX_QUEUE: "100"        # maximum number of queued requests
          OLLAMA_NUM_PARALLEL: "1"       # maximum number of parallel requests
          OLLAMA_MAX_LOADED_MODELS: "1"  # maximum number of loaded models per GPU
          OLLAMA_LOAD_TIMEOUT: "5m"      # maximum time for loading models (default "5m")
          OLLAMA_KEEP_ALIVE: "10m"       # duration that models stay loaded in memory (default "5m")
          OLLAMA_CONTEXT_LENGTH: "4096"  # maximum input context length
          OLLAMA_MULTIUSER_CACHE: "1"    # optimize prompt caching for multi-user scenarios
          # OLLAMA_DEBUG: "1"              # shows additional debug information
          # OLLAMA_NOPRUNE: "1"            # disables pruning of model blobs at startup
          # OLLAMA_NOHISTORY: "1"          # disables readline history
          # OLLAMA_FLASH_ATTENTION: "1"    # enables the experimental flash attention feature
          # OLLAMA_SCHED_SPREAD: "1"       # allows scheduling models across all GPUs.
          # OLLAMA_GPU_OVERHEAD: "0"       # reserves a portion of VRAM per GPU (bytes)
          # OLLAMA_INTEL_GPU: "1"          # enables experimental Intel GPU detection
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
    Since neither [Vision Service](service/index.md) nor Ollama support authentication, both services should only be used within a secure, private network. They must not be exposed to the public internet.

### Step 2: Download Models

Run the following command to start the Ollama service:

```bash
docker compose up -d
```

If Ollama does not start as expected when using one of our configuration examples, you may need to add the `--profile ollama` flag to the command, as explained in [Step 1](#step-1-install-ollama).

You can then download [any of the listed vision models](https://ollama.com/search?c=vision) that match your hardware capabilities and preferences, as you will need it for the next step. For example:

```bash
docker compose exec ollama ollama pull qwen2.5vl:3b
```

### Step 3: Configure PhotoPrism

Now, create a new `config/vision.yml` file or edit the existing file in [the *storage* folder](../../getting-started/docker-compose.md#photoprismstorage) of your PhotoPrism instance, following the example below. Its absolute path from inside the container is `/photoprism/storage/config/vision.yml`:

!!! example "vision.yml"
    ```yaml
    Models:
    - Type: labels
      Default: true
    - Type: nsfw
      Default: true
    - Type: face
      Default: true
    - Type: caption
      Resolution: 720
      Name: "qwen2.5vl:3b"
      Prompt: |
        Write a journalistic caption that is informative
        and briefly describes the most important visual
        content in up to 3 sentences.
      Service:
        # Ollama API endpoint (adjust as needed):
        Uri: "http://ollama:11434/api/generate"
        FileScheme: base64
        RequestFormat: ollama
        ResponseFormat: ollama
    Thresholds:
      Confidence: 10
    ```

!!! note ""
    The config file must be named `vision.yml`, not `vision.yaml`, as otherwise it won't be found and will have no effect.

#### Model Defaults

When using a custom `vision.yml` config file, you can apply the default settings to one or more model types by setting the `Default` flag to `true`, as shown in the following example:

!!! example "vision.yml"
    ```yaml
    Models:
    - Type: labels
      Default: true
    - Type: nsfw
      Default: true
    - Type: face
      Default: true
    ```

This simplifies your configuration, allowing you to customize only specific model types.

### Step 4: Restart PhotoPrism

Run the following commands to restart `photoprism` and apply the new settings:

```bash
docker compose stop
docker compose up -d
```

You should now be able to use the `photoprism vision` CLI commands when [opening a terminal](../../getting-started/docker-compose.md#opening-a-terminal), e.g. `photoprism vision run -m caption` to generate captions.

Further details and usage examples can be found below.

## Generating Captions

Once you have configured your preferred computer vision models and services in the `vision.yml` file, you can use the following command to update the metadata of pictures that match the specified search filter:

```bash
photoprism vision run [options] [filter]
```

### Command Options

| Command Flag                   | Description                                                                                                          |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------|
| `--models MODELS`, `-m MODELS` | computer vision MODELS to run, e.g. caption, labels, or nsfw (default: "caption")                                    |
| `--source TYPE`, `-s TYPE`     | custom data source TYPE, e.g. estimate, image, meta, or manual (default: "image")                                    |
| `--force`, `-f`                | force existing data to be updated if the source priority is equal to or higher than the current one (default: false) |

To generate captions for all photos in your library, you can run:

```bash
docker compose exec photoprism \
  photoprism vision run --models=caption
```

Note: Processing time will vary based on your library size and hardware performance and may take a considerable amount of time for large collections.

If you have a model for labels configured in your `vision.yml` you can run the following to generate labels:

```bash
docker compose exec photoprism \
  photoprism vision run --models=labels
```

To generate captions or labels only for photos matching a specific search filter such as those in a particular album, use the following command:
```bash
docker compose exec photoprism \
  photoprism vision run --models=caption album:Holidays
```

```bash
docker compose exec photoprism photoprism vision run \
  --models=labels album:Holidays
```
To re-generate captions for photos that already have some, add the --force flag to your command:

```bash
docker compose exec photoprism \
  photoprism vision run --models=caption --force
```

This is especially useful when testing different models or prompts. Note that the configured source must have a equal or higher priority than the source of the existing captions for them to be replaced.

## Troubleshooting ##

### Verifying Your Configuration ###

If you encounter issues, a good first step is to verify how PhotoPrism has loaded your `vision.yml` configuration. You can do this by running: 

```bash
docker compose exec photoprism photoprism vision ls
```

This command outputs the settings for all supported and configured model types. Compare the results with your `vision.yml` file to confirm that your configuration has been loaded correctly and to identify any parsing errors or misconfigurations.

### GPU Performance Issues ###

When using Ollama with GPU acceleration, you may experience performance degradation over time due to VRAM management issues. This typically manifests as processing times gradually increasing and the Ollama service appearing to "crash" while still responding to requests, but without GPU acceleration.

The issue occurs because Ollama's VRAM allocation doesn't properly recover after processing multiple requests, leading to memory fragmentation and eventual GPU processing failures.

The Ollama service does not automatically recover from these VRAM issues. To restore full GPU acceleration, manually restart the Ollama container:

```bash
docker compose restart ollama
```

This will clear the VRAM and restore normal GPU-accelerated processing performance.

[^1]: Available to all users with the [next stable version](../../release-notes.md), see our [release notes](../../release-notes.md#development-preview) for details.
[^2]: Unrelated configuration details have been omitted for brevity.