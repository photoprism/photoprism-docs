# PhotoPrism Vision Service

PhotoPrism® can be extended with a powerful, external service for advanced computer vision tasks like generating descriptive captions and labels for your entire photo library. This service, **PhotoPrism Vision**, acts as a flexible bridge between your main PhotoPrism instance and various AI models.

This guide provides a technical deep-dive for developers who want to understand, set up, and potentially extend the Vision service.

!!! info "Technologies Used"
    The Vision service is built with Python using the Flask web framework. It leverages popular machine learning libraries like PyTorch and Hugging Face Transformers for running local models, and can also integrate with external AI providers like Ollama.

## Architecture

The Vision service is designed to be a decoupled microservice. This architecture allows for flexibility and scalability, as the computationally intensive AI tasks can be offloaded to a separate, potentially more powerful, machine with a dedicated GPU.

The data flow is as follows:

1.  **PhotoPrism** selects a photo that needs processing. It sends a request containing a thumbnail of the image and the desired model information to the Vision service's REST API.
2.  **PhotoPrism Vision** receives the request. Based on the specified model, it routes the request to the appropriate processor:
    *   **Local Processor:** If a built-in model (like Kosmos-2) is requested, the service uses PyTorch and Transformers to load the model locally and process the image.
    *   **Ollama Processor:** If an Ollama model is requested, the service forwards the image and a prompt to the Ollama API endpoint.
3.  **The AI Model** (either local or on Ollama) analyzes the image and generates the result (a caption or a list of labels).
4.  **PhotoPrism Vision** formats the result into a standardized JSON response and sends it back to the main PhotoPrism instance.
5.  **PhotoPrism** receives the JSON response and saves the new metadata to its database.

![Vision Architecture Diagram](https://dl.photoprism.app/img/diagrams/photoprism-vision-ollama.svg){ class="w100" }

---

## Development Environment Setup

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
    export OLLAMA_HOST="http://192.168.1.123:11434"
    ```
5.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Run the Flask Development Server:**
    ```bash
    flask --app app run --debug --host=0.0.0.0 --port=5000
    ```    The `--debug` flag enables auto-reloading whenever you save a change in the code, and `--host=0.0.0.0` makes the service accessible from other machines on your network, such as your main PhotoPrism instance.

---

## Configuration (`vision.yml`)

The interaction between PhotoPrism and the Vision service is controlled by a `vision.yml` file located in your main PhotoPrism `storage/config` directory.

!!! warning "Important: File Extension"
    The configuration file **must** be named `vision.yml` with the `.yml` extension, **not** `.yaml`. Files with the `.yaml` extension will be ignored by PhotoPrism and could cause the Vision service to appear non-functional.

The file consists of a list of `Models` and a `Thresholds` section.

!!! example "`storage/config/vision.yml`"
    ```yaml
    Models:
    - Type: caption
      Resolution: 720
      Name: "llava-phi3:latest"
      Prompt: |
        Write a journalistic caption that is informative and briefly describes the most important visual content in up to 3 sentences.
      Service:
        Uri: "http://192.168.1.100:5000/api/v1/vision/caption"
        FileScheme: data
        RequestFormat: vision
        ResponseFormat: vision

    - Type: labels
      Resolution: 720
      Name: "minicpm-v:latest"
      Service:
        Uri: "http://192.168.1.100:5000/api/v1/vision/labels"
        FileScheme: base64
        RequestFormat: ollama
        ResponseFormat: ollama

    Thresholds:
      Confidence: 50
    ```

*   **`Type`**: The task to perform. Can be `caption` or `labels`.
*   **`Resolution`**: The longest edge of the thumbnail (in pixels) to be sent for analysis. Higher values may yield better results but increase processing time and network traffic.
*   **`Name`**: The name of the model to use. For Ollama, this is the model tag (e.g., `llava-phi3:latest`). For built-in models, it's the model identifier (e.g., `kosmos-2`).
*   **`Version`**: (Optional) Used for built-in models, typically `latest`.
*   **`Prompt`**: (Optional) A custom prompt to send to the AI model. If omitted, a default prompt will be used.
*   **`Service`**: A block defining how to communicate with the service.
    *   **`Uri`**: The full API endpoint of the Vision service.
    *   **`FileScheme`**: How the image data is sent. `data` (default) sends the raw thumbnail binary. `base64` sends it as a Base64-encoded string, which is required by some APIs like Ollama's.
    *   **`RequestFormat`**: The JSON structure of the request. `vision` is for the PhotoPrism Vision API. `ollama` sends a request directly compatible with the Ollama API.
    *   **`ResponseFormat`**: The expected JSON structure of the response. `vision` or `ollama`.
*   **`Thresholds`**:
    *   **`Confidence`**: A value from 0-100. Generated labels with a confidence score below this threshold will be discarded.

---

## API Endpoints

The PhotoPrism Vision service exposes a simple REST API.

#### Main Endpoints

*   `POST /api/v1/vision/caption`: Generates a caption for an image.
*   `POST /api/v1/vision/labels`: Generates labels for an image.
*   `POST /api/v1/vision/nsfw`: Checks an image for not-safe-for-work content (using built-in models).

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

---

## Code Structure

For developers looking to contribute, the codebase is structured as follows:

*   **`app.py`**: The main Flask application. It handles routing, request parsing, and calls the appropriate processor.
*   **`processor.py`**: Defines the abstract `ImageProcessor` base class. Any new integration (local or remote) must implement this interface.
*   **`local_processor.py`**: Implements the processor for the built-in Hugging Face models (Kosmos-2, BLIP, etc.). It manages downloading, caching, and running these models using PyTorch.
*   **`ollama_processor.py`**: Implements the processor for the Ollama integration. It acts as a client, formatting requests and forwarding them to an Ollama instance.
*   **`api.py`**: Contains the Pydantic models used for request/response validation and serialization.
*   **`utils.py`**: Helper functions, for instance, for image loading and encoding.

---

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