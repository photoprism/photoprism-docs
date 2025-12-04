# Vision Playground Build Setup

Our [Vision Playground](https://github.com/photoprism/photoprism-vision) provides developers with additional computer vision models and customization options. If you are looking for an easy way to generate captions and labels for your pictures, we recommend using our [direct Ollama integration](../caption-generation.md) instead.

!!! tldr ""
    If you have an interest in AI and would like to run a dedicated [Vision Playground](https://github.com/photoprism/photoprism-vision), we recommend [reading the introduction](index.md) and [following the instructions](index.md#getting-started) there, as the following guide is intended for developers only. [Learn more ›](index.md)

## Overview

PhotoPrism® can be extended with a powerful, external service for advanced computer vision tasks like generating descriptive captions and labels for your entire photo library. This service, **Vision Playground**, acts as a flexible bridge between your main PhotoPrism instance and various AI models.

This guide provides a technical deep-dive for developers who want to understand, set up, and potentially extend the [Vision Playground](https://github.com/photoprism/photoprism-vision).

!!! info ""
    The Vision service is built with Python using the Flask web framework. It leverages popular machine learning libraries like PyTorch and Hugging Face Transformers for running local models, and can also integrate with external AI providers like Ollama.

## Architecture

The Vision service is designed to be a decoupled microservice. This architecture allows for flexibility and scalability, as the computationally intensive AI tasks can be offloaded to a separate, potentially more powerful, machine with a dedicated GPU.

The data flow is as follows:

1.  **PhotoPrism** selects a photo that needs processing. It sends a request containing a thumbnail of the image and the desired model information to the Vision service's REST API.
2.  **Vision Playground** receives the request. Based on the `model` name in the request body, it routes the request to the appropriate internal processor:
    *   **Local Processor:** If a pre-installed model (e.g., `kosmos-2`, `blip`, `vit-gpt2`, `nsfw_image_detector`) is requested, the service uses PyTorch and Transformers to load the model from the local `models` directory and process the image. This can be accelerated by a GPU if available on the Vision service machine.
    *   **Ollama Processor:** If the model name is not recognized as a local model, the service assumes it is an Ollama model. It forwards the image and a prompt to the configured `OLLAMA_HOST` API endpoint.
3.  **The AI Model** (either local or on Ollama) analyzes the image and generates the result (a caption or a list of labels).
4.  **Vision Playground** formats the result into a standardized JSON response and sends it back to the main PhotoPrism instance.
5.  **PhotoPrism** receives the JSON response and saves the new metadata to its database.

## Build Setup

This guide explains how to set up a local development environment to run the Vision service directly from source, allowing for easy code modification and debugging.

1.  **Prerequisites:** Ensure you have Python 3.12+ and Git installed on your system.
2.  **Clone the Repository:** First, clone the official `photoprism-vision` repository.
    ```bash
    git clone https://github.com/photoprism/photoprism-vision.git
    cd photoprism-vision/service
    ```
3.  **Create and Activate Virtual Environment:** It is highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python3.12 -m venv ./venv
    source ./venv/bin/activate
    ```
4.  **Set Environment Variables:** Configure the connection to your Ollama instance if you plan to use it. These variables are read by the application at startup.
    ```bash
    export OLLAMA_ENABLED="true"
    export OLLAMA_HOST="http://<ollama-host-ip>:11434"
    ```
5.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Run the Flask Development Server:**
    ```bash
    python -m flask --app app run --debug --host=0.0.0.0 --port=5000
    ```    The `--debug` flag enables auto-reloading whenever you save a change in the code, and `--host=0.0.0.0` makes the service accessible from other machines on your network, such as your main PhotoPrism instance.

!!! warning "" 
    The service and its integrations are **under active development**, so the configuration, commands, and other details may change or break unexpectedly. Please keep this in mind and notify us when something doesn't work as expected. Thank you for your help in keeping this documentation updated!

## Configuration

The interaction between PhotoPrism and the Vision service is controlled by a `vision.yml` file located in your main PhotoPrism `storage/config` directory.

!!! warning ""
    The configuration file **must** be named `vision.yml` with the `.yml` extension, **not** `.yaml`. Files with the `.yaml` extension will be ignored by PhotoPrism and could cause the Vision service to appear non-functional.

The file consists of a list of `Models` and a `Thresholds` section.

!!! example "`storage/config/vision.yml`"
    ```yaml
    Models:
    - Type: caption
      Model: gemma3:latest
      Prompt: Create a caption with exactly one sentence in the active voice that describes
        the main visual content. Begin with the main subject and clear action. Avoid text
        formatting, meta-language, and filler words.
      Resolution: 720
      Options:
        Temperature: 0.1
      Service:
        Uri: "http://<vision-service-ip>:5000/api/v1/vision/caption"
        FileScheme: data
        RequestFormat: vision
        ResponseFormat: vision
    - Type: labels
      Resolution: 720
      Model: kosmos-2:latest
      Service:
        Uri: "http://<vision-service-ip>:5000/api/v1/vision/caption"
        FileScheme: base64
        RequestFormat: vision
        ResponseFormat: vision
    Thresholds:
      Confidence: 50
    ```

*   **`Type`**: The task to perform. Can be `caption` or `labels`.
*   **`Resolution`**: The longest edge of the thumbnail (in pixels) to be sent for analysis. Higher values may yield better results but increase processing time and network traffic.
*   **`Model`**: Canonical model identifier used for routing, e.g., `llava-phi3:latest` for an Ollama model or `kosmos-2:latest` for a pre-installed model.
*   **`Name`**: Optional, human-readable display name. When omitted, PhotoPrism derives it from the type and model/version.
*   **`Version`**: The model version. For Ollama models, this is typically `latest`. For pre-installed models, it's also usually `latest`.
*   **`Prompt`**: (Optional) A custom prompt to send to the AI model. If omitted, a default prompt will be used.
*   **`Service`**: A block defining how to communicate with the service.
    *   **`Uri`**: The base API endpoint of the Vision service. PhotoPrism will append the appropriate path based on the task type, model, and version (e.g., `/caption/llava-phi3/latest`).
    *   **`FileScheme`**: How the image data is sent. `base64` sends it as a Base64-encoded string within the JSON payload (recommended for the Vision service). `data` sends the raw thumbnail binary, but this requires additional handling in the current Vision service implementation.
    *   **`RequestFormat`**: The JSON structure of the request. Use `vision` for the PhotoPrism Vision API format. The `ollama` format should only be used when connecting directly to Ollama, not through the Vision service.
    *   **`ResponseFormat`**: The expected JSON structure of the response. Use `vision` for the PhotoPrism Vision API format.
*   **`Thresholds`**:
    *   **`Confidence`**: A value from 0-100. Generated labels with a confidence score below this threshold will be discarded.

## API Endpoints

The PhotoPrism Vision service exposes a simple REST API.

#### Main Endpoints

*   `POST /api/v1/vision/caption/<model_name>/<model_version>`: Generates a caption for an image using the specified model.
*   `POST /api/v1/vision/labels/<model_name>/<model_version>`: Generates labels for an image using the specified model.
*   `POST /api/v1/vision/nsfw`: Checks an image for not-safe-for-work content (using pre-installed models).

!!! note "URL Construction"
    When PhotoPrism makes requests to the Vision service, it constructs the full URL by appending the task type, model name, and version to the base URI specified in `vision.yml`. For example, if the base URI is `http://<vision-service-ip>:5000/api/v1/vision` and you request a caption with model `llava-phi3` version `latest`, PhotoPrism will send the request to `http://<vision-service-ip>:5000/api/v1/vision/caption/llava-phi3/latest`.

#### Request Body

The API accepts a JSON payload with the following fields:

!!! example "Request to `/api/v1/vision/caption`"
    ```json
    {
        "id": "optional-uuid-to-track-request",
        "model": "llava-phi3",
        "version": "latest",
        "prompt": "Describe this image in a single sentence.",
        "images": [
          "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
        ]
    }
    ```

#### Response Body

The service returns a standardized JSON response:

!!! example "Response"
    ```json
    {
        "id": "optional-uuid-to-track-request",
        "model": {
            "name": "llava-phi3",
            "version": "latest"
        },
        "result": {
            "caption": "A colorful landscape with mountains and a clear blue sky."
        }
    }
    ```

## Code Structure

For developers looking to contribute, the codebase is structured as follows:

*   **`app.py`**: The main Flask application. It handles routing, request parsing, and calls the appropriate processor.
*   **`processor.py`**: Defines the abstract `ImageProcessor` base class. Any new integration (local or remote) must implement this interface.
*   **`local_processor.py`**: Implements the processor for the pre-installed Hugging Face models (Kosmos-2, BLIP, etc.). It manages downloading, caching, and running these models using PyTorch.
*   **`ollama_processor.py`**: Implements the processor for the Ollama integration. It acts as a client, formatting requests and forwarding them to an Ollama instance.
*   **`api.py`**: Contains the Pydantic models used for request/response validation and serialization.
*   **`utils.py`**: Helper functions, for instance, for image loading and encoding.


## Dependencies

### Flask

[Flask](https://flask.palletsprojects.com/en/3.0.x/) is the framework that is used for the API. It allows for API creation with Python, which is key for this application as it utilizes ML.

### PyTorch

[PyTorch](https://pytorch.org/) is key for working with the ML models to generate the outputs. It also enables GPU processing, speeding up the image processing with the models. PyTorch primarily creates and handles tensors, which are crucial for the function of the models.

### Transformers

[Transformers](https://huggingface.co/docs/transformers/en/index) is used for downloading and loading the models. In addition to this it is used in the image processing with the models.

### Pillow

[Pillow](https://pypi.org/project/pillow/) is used to take the supplied URL and convert it into the format needed to input into the models.

### pydantic

[pydantic](https://github.com/pydantic/pydantic) is used for JSON schemas, serialization and deserialization of requests and responses.

### ollama

[ollama](https://github.com/ollama/ollama) is used as integration library that connects to any given ollama instance.

### timm

[timm](https://huggingface.co/timm) is a tensorflow extension for timm models. Currently used for NSFW detection.

### huggingface_hub[hf_xet]

[xet](https://huggingface.co/blog/xet-on-the-hub) Extension used for faster downloading of huggingface models.

## Troubleshooting and CLI Commands

When developing or debugging the Vision service integration, you can use built-in CLI commands to inspect the configuration.

### Listing Loaded Models

To verify how the main PhotoPrism instance has parsed the `vision.yml` file, you can use the `vision ls` command from within the PhotoPrism container. This is particularly useful for debugging configuration issues without needing to trigger a full indexing job.

From within the development container (after running `make terminal`), use:

```bash
./photoprism vision ls
```

If you have a global `photoprism` binary, you can run:

```bash
photoprism vision ls
```

The command will output the settings for all supported and configured model types, which you can then compare with the expected settings in your `vision.yml`. This helps quickly identify typos, formatting issues, or incorrect values.