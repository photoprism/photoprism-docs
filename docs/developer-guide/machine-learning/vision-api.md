# Vision API

!!! warning 
    The enhanced AI features are currently in **beta** and undergoing **active development**. Configuration examples, commands, and integration details may change without prior notice. Use with caution and anticipate potential breaking changes as the feature evolves.

In addition to the built-in image classification, PhotoPrism now supports advanced AI models for generating captions and labels. These models also support custom prompts, enabling you to tailor results to your specific needs.

This page covers the **Ollama API Integration** method – which simplifies setup and is easy to configure.

## Using the Ollama API Integration ##

If you plan to only use Ollama models, the easiest approach is to use PhotoPrism's Ollama API Integration.

#### Step 1: Install Ollama ####

To install Ollama on the same server as PhotoPrism, add the `ollama` service to your compose.yaml file, placing it below the `photoprism` service.

!!! example "`compose.yaml` example with ollama service"
    ```yaml
    services:
      photoprism:
        image: photoprism/photoprism:latest

        # ... your existing photoprism config ...

        depends_on:
        - ollama # Ensures Ollama starts before PhotoPrism
      ollama:
        image: ollama/ollama:latest
        container_name: ollama
        restart: unless-stopped
        # Expose the port if you need to access it from outside.
        # ports:
        #   - "11434:11434"
        environment:
          # Ollama server configuration
          OLLAMA_HOST: "0.0.0.0:11434"
          OLLAMA_MAX_LOADED_MODELS: "1"
          OLLAMA_NUM_PARALLEL: "1"
          OLLAMA_MAX_QUEUE: "100"
          OLLAMA_KEEP_ALIVE: "15m"
          OLLAMA_MODELS: "/root/.ollama"
          # NVIDIA Container Toolkit (uncomment if using GPU)
          # NVIDIA_VISIBLE_DEVICES: "all"
          # NVIDIA_DRIVER_CAPABILITIES: "compute,utility"
        volumes:
          - "ollama-data:/root/.ollama"
    volumes:
      ollama-data:
    ```
!!! warning

    The Ollama API integration currently does not support authentication. For security reasons, it should only be used within a secure, private network and must not be exposed to the Internet or any untrusted networks.
!!! info
    Experienced users can also install Ollama on a separate, more powerful server.

### Step 2: Download AI Models ###

Start the application: 

```bash
docker compose up -d
```

Download the models you intend to use, for example:

```bash
docker compose exec ollama ollama pull llava-phi3:latest
docker compose exec ollama ollama pull minicpm-v:latest
docker compose exec ollama ollama pull qwen2.5-coder:3b
```

### Step 3: Configure ###

Create a vision.yml file in the config path (default: `storage/config`) of your PhotoPrism instance, and change the configuration as needed:

!!! warning "Important: File Extension"
    The configuration file **must** be named `vision.yml` using the `.yml` extension, **not** `.yaml`. Files with the `.yaml` extension will be ignored by PhotoPrism.

!!! example "`storage/config/vision.yml`"
    ```yaml
    Models:
    - Type: caption
      Resolution: 720
      Name: "llava-phi3"
      Version: "latest"
      Prompt: |
        Write a journalistic caption that is informative and briefly describes the most important visual content in up to 3 sentences:
        - Use explicit language to describe the scene if necessary for a proper understanding.
        - Avoid text formatting, meta-language, and filler words.
        - Do not start captions with boring phrases such as "This image", "The image", "This picture", "The picture", "A picture of", "Here are", or "There is".
        - Instead, start describing the content by first identifying the subjects and any actions that might be performed.
        - Try providing a casual description of what the subjects look like, including their gender and age.z
        - If the place seems special or familiar, provide a brief, interesting description without being vague.
      Service:
        # This points directly to the Ollama service within the same Docker network.
        Uri: "http://ollama:11434/api/generate"
        FileScheme: base64
        RequestFormat: ollama
        ResponseFormat: ollama
    - Type: labels
      Resolution: 720
      Name: "minicpm-v"
      Version: "latest"
      Service:
        Uri: "http://ollama:11434/api/generate"
        FileScheme: base64
        RequestFormat: ollama
        ResponseFormat: ollama

    Thresholds:
      Confidence: 10
    ```

#### Using Model Default Configs ####

You can now use model default configurations even if you have a custom `vision.yml` file. This simplifies configuration by allowing you to use default settings for specific model types.

To use default configs, simply set the `Default` flag to `true` for the model types you want to use with their default settings:

!!! example "Using Default Model Configs"
    ```yaml
    Models:
    - Type: labels
      Default: true
    - Type: nsfw
      Default: true
    - Type: face
      Default: true
    ```

When `Default: true` is set, PhotoPrism will use the built-in default configuration for that model type. To switch back to custom configuration, simply remove the `Default` flag from your model configuration.

### Step 4: Restart and Generate Captions/Labels ###

After saving the `vision.yml`, restart your PhotoPrism instance:

```bash
docker compose stop photoprism
docker compose up -d
``` 

and proceed to [Generate Captions/Labels](#generate-captionslabels-using-the-vision-run-command).

## Generate Captions/Labels using the vision run command ##

Your setup is complete! You can now use the `photoprism vision run [options] [filter]` command to generate captions or labels.

### Command Options

| Command Flag                   | Description                                                                                                          |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------|
| `--models MODELS`, `-m MODELS` | computer vision MODELS to run, e.g. caption, labels, or nsfw                                                         |
| `--source TYPE`, `-s TYPE`     | custom data source TYPE, e.g. estimate, image, meta, or manual (default: "image")                                    |
| `--force`, `-f`                | force existing data to be updated if the source priority is equal to or higher than the current one (default: false) |

To generate captions for all photos in your library, you can run:

```bash
docker compose exec photoprism photoprism vision run --models=caption
```

Note: Processing time will vary based on your library size and hardware performance and may take a considerable amount of time for large collections.

If you have a model for labels configured in your `vision.yml` you can run the following to generate labels:

```bash
docker compose exec photoprism photoprism vision run --models=labels
```

To generate captions or labels only for photos matching a specific search filter such as those in a particular album, use the following command:
```bash
docker compose exec photoprism photoprism vision run --models=caption album:Holidays
```

```bash
docker compose exec photoprism photoprism vision run --models=labels album:Holidays
```
To re-generate captions for photos that already have some, add the --force flag to your command:

```bash
docker compose exec photoprism photoprism vision run --models=caption --force
```

This is especially useful when testing different models or prompts. Note that the configured source must have a equal or higher priority than the source of the existing captions for them to be replaced.

## Troubleshooting ##

### Verifying Your Configuration ###

If you encounter issues, a good first step is to verify how PhotoPrism has loaded your vision.yml configuration. You can do this by running: 

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