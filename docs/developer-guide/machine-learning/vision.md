# ⚠️ Beta Feature: Vision Service (Active Development)

> **Warning:** The PhotoPrism Vision feature is currently in **beta** and under **active development**. Configuration examples, commands, and integration details are subject to change without notice. Use with caution and expect breaking changes as the feature evolves.

# PhotoPrism Vision

PhotoPrism can automatically generate descriptive labels and captions for your photos using advanced AI models through an optional, external service called **PhotoPrism Vision**. This allows you to enrich your library's metadata without manual effort.

There are two primary methods to integrate these AI capabilities:

*   **A) Recommended: Using the PhotoPrism Vision Service:** This method offers maximum flexibility by offloading the intensive AI processing to a separate, potentially more powerful, computer (e.g., one with a GPU).
*   **B) Alternative: Using Ollama Directly:** A simpler setup for running everything on a single machine, where PhotoPrism communicates directly with a local Ollama service.

---

## A) Recommended: Using the PhotoPrism Vision Service

This approach uses a dedicated service that acts as a bridge between your main PhotoPrism instance and various AI models, including both simple built-in models and more powerful models served by Ollama.

**Key Advantage:** You can run the resource-heavy Vision service on a separate, more powerful machine with a GPU, while your main PhotoPrism instance runs on a less powerful server or NAS.

!!! warning "Security Notice"
    The PhotoPrism Vision service does not currently implement authentication. For security reasons, it should only be used within a secure private network and should not be exposed to the internet or untrusted networks.

### Step 1: Set Up the PhotoPrism Vision Service

1.  Create a new, empty folder on the machine where you want to run the Vision service.
2.  Inside this folder, create a `compose.yaml` file with the following content:

    !!! example "`compose.yaml` for Vision Service"
        ```yaml
        services:
          photoprism-vision:
            image: photoprism/vision:latest
            restart: unless-stopped
            ports:
              - "5000:5000"
            user: "1000:1000"
            environment:
              # Enable this and set the host if you want this service to use Ollama.
              # - OLLAMA_ENABLED=true
              # - OLLAMA_HOST=http://<ollama-ip>:11434
            volumes:
              - "vision-models:/app/models"
              - "vision-venv:/app/venv"
        
        volumes:
          vision-models:
          vision-venv:
        ```
3.  If you plan to use Ollama through this service, uncomment the `OLLAMA...` lines and replace `<ollama-ip>` with the IP of your Ollama machine.
4.  Start the service: `docker compose up -d`

### Step 2: Configure Your Main PhotoPrism Instance

On your main PhotoPrism server, navigate to your `storage/config` folder and create/edit the `vision.yml` file to point to your new Vision service.

!!! warning "Important: File Extension"
    The configuration file **must** be named `vision.yml` with the `.yml` extension, **not** `.yaml`. Files with the `.yaml` extension will be ignored by PhotoPrism and could cause the Vision service to appear non-functional.

=== "Example 1: Using a Built-in Model"

    This example uses the built-in `kosmos-2` model for generating captions. It does not require Ollama.

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
            Uri: "http://<vision-service-ip>:5000/api/v1/vision/caption"
        
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
          Name: "llava-phi3:latest"
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
            Uri: "http://<vision-service-ip>:5000/api/v1/vision/caption"
        
        Thresholds:
          Confidence: 10
        ```

### Step 3: Restart and Generate

After saving `vision.yml`, restart your main PhotoPrism instance (`docker compose stop photoprism && docker compose up -d`) and proceed to [Step 4: Start Generating](#step-4-start-generating).

---

## B) Alternative: Using Ollama Directly

This method is simpler if you plan to run everything on a single server. It involves adding the Ollama service directly to your main PhotoPrism `compose.yaml`.

### Step 1: Update PhotoPrism's `compose.yaml`

Add the `ollama` service to the same `compose.yaml` file as your `photoprism` service.

!!! example "Main `compose.yaml` with Ollama"
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
          - "./data/ollama:/root/.ollama"
    
    volumes:
      ollama-data:
    ```

### Step 2: Download Ollama Models

Start your stack (`docker compose up -d`) and then pull the models you need:

```bash
docker compose exec ollama ollama pull llava-phi3:latest
docker compose exec ollama ollama pull minicpm-v:latest

# For other models, you can also use the interactive run command
# docker compose exec ollama ollama run llama3

# Or pull specific model variants
# docker compose exec ollama ollama pull qwen2.5-coder:3b
```

### Step 3: Configure `vision.yml` for Direct Connection

On your PhotoPrism server, navigate to `storage/config` and create/edit `vision.yml` to communicate directly with the Ollama service.

!!! warning "Important: File Extension"
    The configuration file **must** be named `vision.yml` with the `.yml` extension, **not** `.yaml`. Files with the `.yaml` extension will be ignored by PhotoPrism and could cause the Vision service to appear non-functional.

!!! example "`storage/config/vision.yml`"
    ```yaml
    Models:
    - Type: caption
      Resolution: 720
      Name: "llava-phi3:latest"
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
      Name: "minicpm-v:latest"
      Service:
        Uri: "http://ollama:11434/api/generate"
        FileScheme: base64
        RequestFormat: ollama
        ResponseFormat: ollama
            
    Thresholds:
      Confidence: 10
    ```

### Step 4: Restart and Generate

After saving `vision.yml`, restart your PhotoPrism instance (`docker compose stop photoprism && docker compose up -d`) and proceed to [Step 4: Start Generating](#step-4-start-generating).

---

## Step 4: Start Generating

Your setup is now complete! You can start generating metadata using PhotoPrism's command-line interface. You can run these commands on your entire library or on specific albums.

#### For the Entire Library

To generate captions for **all** photos in your library, run the following command. This may take a long time depending on the size of your library and your hardware.

```bash
docker compose exec photoprism photoprism vision run --models=caption
```

To generate labels for your entire library (only works with a compatible label-generating model):

```bash
docker compose exec photoprism photoprism vision run --models=labels
```

#### For a Specific Album

To test the process on a smaller set of photos, you can run the commands on a specific album, for example one named "Holidays":

```bash
docker compose exec photoprism photoprism vision run --models=caption album:Holidays
```

```bash
docker compose exec photoprism photoprism vision run --models=caption album:Holidays
```

!!! tip "Re-running and Testing"
    If you want to re-generate captions or labels for photos that already have them, add the `--force` flag to the command: `photoprism vision run --models=caption --force`. This is very useful for testing different models or prompts.

---

## Troubleshooting

### Verifying Your Configuration

If you're having trouble, a useful first step is to verify how PhotoPrism has loaded your `vision.yml` configuration. You can do this with the `vision ls` command.

Run the following command in a terminal from your main PhotoPrism directory:

```bash
docker compose exec photoprism photoprism vision ls
```

This command will output the settings for all supported and configured model types. You can compare this output with your `vision.yml` file to ensure that your settings have been read correctly and to spot any parsing errors or misconfigurations.
