# Introducing Vision Playground

Our [Vision Playground](https://github.com/photoprism/photoprism-vision) provides developers with additional computer vision models and customization options. If you are looking for an easy way to generate captions and labels for your pictures, we recommend using our [direct Ollama integration](../caption-generation.md) instead.

!!! warning "" 
    The service and its integrations are **under active development**, so the configuration, commands, and other details may change or break unexpectedly. Please keep this in mind and notify us when something doesn't work as expected. Thank you for your help in keeping this documentation updated!

## Getting Started

This guide explains how to set up the dedicated service as an AI model proxy to enhance PhotoPrism's capabilities. You can use a wide range of additional models with it, including lightweight, preconfigured models, as well as popular but more demanding large language models in combination with Ollama.

PhotoPrism also allows you to generate captions and labels with Ollama directly. A key advantage of using the dedicated vision service is greater flexibility and access to an even broader range of models, which makes it ideal for advanced users and developers.

Developers can proceed to the [Build Setup](setup.md) guide, which explains how to set up a [Vision Playground](https://github.com/photoprism/photoprism-vision) development environment.

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

Now, create a new `config/vision.yml` file or edit the existing file in [the *storage* folder](../../../getting-started/docker-compose.md#photoprismstorage) of your PhotoPrism instance, following the example below. Its absolute path from inside the container is `/photoprism/storage/config/vision.yml`:

=== "Example 1: Using an Ollama Model"

    This example uses Ollama's `llava-phi3` model for generating captions, proxied through the Vision service.

    !!! example "vision.yml"
        ```yaml
        Models:
        - Type: caption
          Resolution: 720
          Model: llava-phi3:latest
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

=== "Example 2: Using a pre-installed Model"

    This example uses the pre-installed `kosmos-2` model for generating captions. It does not require Ollama.

    !!! tip "Available pre-installed Models"
        The Vision service also provides additional pre-installed models, such as `vit-gpt2` and `blip` for image captioning, as well as `nsfw_image_detector` for NSFW content detection. You can enable these models by updating the `Model` field in your `vision.yml` configuration.
    
    !!! tip "Prompts"
        Unlike the Ollama models, pre-installed models such as `kosmos-2` interpret prompts primarily as starting instructions for generating captions, rather than as detailed, task-oriented requests.

    !!! example "vision.yml"
        ```yaml
        Models:
        - Type: caption
          Resolution: 720
          Model: kosmos-2:latest
          Prompt: "A"
          Service:
            # IMPORTANT: Replace this IP with the address of your Vision service machine.
            Uri: "http://<vision-service-ip>:5000/api/v1/vision/caption"
        
        Thresholds:
          Confidence: 10
        ```

!!! note ""
    The config file must be named `vision.yml`, not `vision.yaml`, as otherwise it won't be found and will have no effect.


## Step 3: Restart PhotoPrism

Run the following commands to restart `photoprism` and apply the new settings:

```bash
docker compose stop photoprism
docker compose up -d
```

You should now be able to use the `photoprism vision` [CLI commands](../cli.md#run-vision-models) when [opening a terminal](../../../getting-started/docker-compose.md#opening-a-terminal), e.g. `photoprism vision run -m caption` to generate captions.


## Troubleshooting

### GPU Performance Issues

If you're using the [Vision Playground](https://github.com/photoprism/photoprism-vision) with Ollama enabled (`OLLAMA_ENABLED=true`), you may experience GPU VRAM management issues over time. The same VRAM degradation symptoms and solutions apply when Ollama is used through the Vision Service proxy.

Detailed troubleshooting tips can be found in the [Caption Generation](../caption-generation.md#gpu-performance-issues) documentation.

[Learn more ›](../caption-generation.md#gpu-performance-issues)