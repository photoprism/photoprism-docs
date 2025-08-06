# Using the Vision Service

With our dedicated [Vision Service](https://github.com/photoprism/photoprism-vision), you get access to additional models and configuration options for advanced computer vision tasks. For example, you can use it to generate custom captions and labels for your photos. The service runs in a separate container that acts as a proxy between the models and PhotoPrism®, extending its capabilities. It also allows Python developers to experiment with new ideas, try different models, and customize prompts.

!!! warning "" 
    The service and its integrations are **under active development**, so the configuration, commands, and other details may change or break unexpectedly. Please keep this in mind and notify us when something doesn't work as expected. Thank you for your help in keeping this documentation updated!

## Getting Started

This guide explains how to set up the dedicated service as an AI model proxy to enhance PhotoPrism's capabilities. You can use a wide range of additional models with it, including lightweight, preconfigured models, as well as popular but more demanding large language models in combination with Ollama.

While the upcoming version of PhotoPrism will also allow you to generate captions with Ollama directly, a key advantage of using the dedicated vision service is greater flexibility and access to an even broader range of models. This makes it ideal for advanced users and developers.

Developers can proceed to the [Build Setup](setup.md) guide, which explains how to set up a [Vision Service](https://github.com/photoprism/photoprism-vision) development environment.

!!! danger ""
    Since neither Vision Service nor Ollama support authentication, both services should only be used within a secure, private network. They must not be exposed to the public internet.

## Step 1: Start the Vision Service

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

## Step 2: Configure PhotoPrism

Create a `vision.yml` file in the config path (default: `storage/config`) of your PhotoPrism instance, and change the configuration as needed:

!!! warning ""
    The configuration file **must** be named `vision.yml` using the `.yml` extension, **not** `.yaml`. Files with the `.yaml` extension will be ignored by PhotoPrism.

=== "Example 1: Using a pre-installed Model"

    This example uses the pre-installed `kosmos-2` model for generating captions. It does not require Ollama.

    !!! tip "Available pre-installed Models"
        The Vision service also provides additional pre-installed models, such as `vit-gpt2` and `blip` for image captioning, as well as `nsfw_image_detector` for NSFW content detection. You can enable these models by updating the `Name` field in your `vision.yml` configuration.
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

## Step 3: Restart PhotoPrism

After saving the `vision.yml`, restart your PhotoPrism instance:

```bash
docker compose stop photoprism
docker compose up -d
``` 

You can now proceed to [Generating Captions and Labels](../caption-generation.md#generating-captions), where you will find further information and usage examples.

[Learn more ›](../caption-generation.md#generating-captions)

## Troubleshooting

### GPU Performance Issues

If you're using the [Vision Service](https://github.com/photoprism/photoprism-vision) with Ollama enabled (`OLLAMA_ENABLED=true`), you may experience GPU VRAM management issues over time. The same VRAM degradation symptoms and solutions apply when Ollama is used through the Vision Service proxy.

Detailed troubleshooting tips can be found in the [Caption Generation](../caption-generation.md#gpu-performance-issues) documentation.

[Learn more ›](../caption-generation.md#gpu-performance-issues)