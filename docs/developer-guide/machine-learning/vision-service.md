# Vision Service

!!! warning 
    The enhanced AI features are currently in **beta** and undergoing **active development**. Configuration examples, commands, and integration details may change without prior notice. Use with caution and anticipate potential breaking changes as the feature evolves.

In addition to the built-in image classification, PhotoPrism now supports advanced AI models for generating captions and labels. These models also support custom prompts, enabling you to tailor results to your specific needs.

This page covers **The PhotoPrism Vision Service** method – which provides maximum flexibility and access to a broader range of models, ideal for advanced users and Python developers.

## Using the PhotoPrism Vision Service ##

This approach uses a dedicated service that serves as an intermediary between your PhotoPrism instance and a range of AI models. These include both lightweight, pre-installed models and advanced, high-performance models powered by Ollama.

**Key Advantage:** Provides maximum flexibility and access to a broader range of models, ideal for advanced users and Python developers.

!!! warning "Security Notice"
    The PhotoPrism Vision service currently does not support authentication. For security reasons, it should only be used within a secure, private network and must not be exposed to the Internet or any untrusted networks.

## Step 1: Install PhotoPrism Vision Service ##

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

## Step 2: Configure PhotoPrism ##

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
            Uri: "http://<vision-service-ip>:5000/api/v1/vision/caption"
        
        Thresholds:
          Confidence: 10
        ```

## Step 3: Restart and Generate Captions/Labels ##

After saving the `vision.yml`, restart your PhotoPrism instance:

```bash
docker compose stop photoprism
docker compose up -d
``` 

and proceed to [Generate Captions/Labels](vision-api.md#generate-captionslabels-using-the-vision-run-command).