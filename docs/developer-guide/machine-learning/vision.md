# 🚧 Setup Additional AI Models 🚧

!!! warning 
    The enhanced AI features are currently in **beta** and undergoing **active development**. Configuration examples, commands, and integration details may change without prior notice. Use with caution and anticipate potential breaking changes as the feature evolves.

<!--PhotoPrism can automatically generate descriptive labels and captions for your photos using advanced AI models through an optional, external service called **PhotoPrism Vision**. This allows you to enrich your library's metadata without manual effort.

There are two primary methods to integrate these AI capabilities:

*   **A) Recommended: Using the PhotoPrism Vision Service:** This method offers maximum flexibility by offloading the intensive AI processing to a separate, potentially more powerful, computer (e.g., one with a GPU).
*   **B) Alternative: Using Ollama Directly:** A simpler setup for running everything on a single machine, where PhotoPrism communicates directly with a local Ollama service.-->

In addition to the built-in image classification, PhotoPrism now supports advanced AI models for generating captions and labels. These models also support custom prompts, enabling you to tailor results to your specific needs.

Additional AI models can be integrated through:

- **The Ollama API Integration** – Simplifies setup and is easy to configure.
- **The PhotoPrism Vision Service** – Provides maximum flexibility and access to a broader range of models, ideal for advanced users and Python developers.

## Using the Ollama API Integration ##

<!--This method is simpler if you plan to run everything on a single server. It involves adding the Ollama service directly to your main PhotoPrism `compose.yaml`.-->
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

<!-- Other models can also be downloaded using the interactive run command:

```bash
docker compose exec ollama ollama run llama3
``` 
-->

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
        - Try providing a casual description of what the subjects look like, including their gender and age.
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

### Step:4 Restart and Generate Captions/Labels ###

After saving the `vision.yml`, restart your PhotoPrism instance:

```bash
docker compose stop photoprism
docker compose up -d
``` 

and proceed to [Generate Captions/Labels](#generate-captionslabels-using-the-vision-run-command).

## Using the PhotoPrism Vision Service ##

This approach uses a dedicated service that  serves as an intermediary between your PhotoPrism instance and a range of AI models. These include both lightweight, pre-installed models and advanced, high-performance models powered by Ollama.

**Key Advantage:** Provides maximum flexibility and access to a broader range of models, ideal for advanced users and Python developers.

!!! warning "Security Notice"
    The PhotoPrism Vision service currently does not support authentication. For security reasons, it should only be used within a secure, private network and must not be exposed to the Internet or any untrusted networks.

### Step 1: Install PhotoPrism Vision Service ###

1.  Create a new, empty folder on the server where you want to run the Vision service.
2.  Inside this folder, create a `compose.yaml` file with the following content:

    !!! example "`compose.yaml` for Vision Service"
        ```yaml
        services:
          photoprism-vision:
            image: photoprism/vision:latest
            restart: unless-stopped
            ports:
              - "5000:5000"
            environment:
              # Set OLLAMA_ENABLED=true and configure the host if you want this service to use Ollama
              - OLLAMA_ENABLED=false
              - OLLAMA_HOST=http://<ollama-ip>:11434
            volumes:
              - "./models:/app/models"
              - "./venv:/app/venv"
        ```

3.  If you plan to use Ollama through this service, set `OLLAMA_ENABLED=true` and replace `<ollama-ip>` with the IP address of your Ollama machine.
4.  Start the service: `docker compose up -d`

### Step 2: Configure ###

Create a vision.yml file in the config path (default: `storage/config`) of your PhotoPrism instance, and change the configuration as needed:

!!! warning "Important: File Extension"
    The configuration file **must** be named `vision.yml` using the `.yml` extension, **not** `.yaml`. Files with the `.yaml` extension will be ignored by PhotoPrism.

=== "Example 1: Using a pre-installed Model"

    This example uses the pre-installed `kosmos-2` model for generating captions. It does not require Ollama.

    !!! tip "Available pre-installed Models"
        The Vision service also provides additional pre-installed models, such as `vit-gpt2` and `blip` for image captioning, as well as `nsfw_image_detector` for NSFW content detection. You can enable these models by updating the `Name` field in your vision.yml configuration.
    !!! example "`storage/config/vision.yml`"
        ```yaml
        Models:
        - Type: caption
          Resolution: 720
          Name: "kosmos-2"
          Version: "latest"
          Prompt: |
            Write a journalistic caption that is informative and briefly describes the most important visual content in up to 3 sentences:
            - Use explicit language to describe the scene if necessary for a proper understanding.
            - Avoid text formatting, meta-language, and filler words.
            - Do not start captions with boring phrases such as "This image", "The image", "This picture", "The picture", "A picture of", "Here are", or "There is".
            - Instead, start describing the content by first identifying the subjects and any actions that might be performed.
            - Try providing a casual description of what the subjects look like, including their gender and age.
            - If the place seems special or familiar, provide a brief, interesting description without being vague.
          Service:
            # IMPORTANT: Replace this IP with the address of your Vision service machine.
            Uri: "http://<vision-service-ip>:5000/api/v1/vision"
        
        Thresholds:
          Confidence: 10
        ```

=== "Example 2: Using an Ollama Model"

    This example uses Ollama's `llava-phi3` model for generating captions, proxied through the Vision service.

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
            - Try providing a casual description of what the subjects look like, including their gender and age.
            - If the place seems special or familiar, provide a brief, interesting description without being vague.
          Service:
            # IMPORTANT: Replace this IP with the address of your Vision service machine.
            Uri: "http://<vision-service-ip>:5000/api/v1/vision"
        
        Thresholds:
          Confidence: 10
        ```

### Step 3: Restart and Generate Captions/Labels ###

After saving the `vision.yml`, restart your PhotoPrism instance:

```bash
docker compose stop photoprism
docker compose up -d
``` 

and proceed to [Step 4: Generate Captions](#generate-captionslabels-using-the-vision-run-command).

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