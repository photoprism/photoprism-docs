# ⚠️ Beta Feature: Vision Service (Active Development)

> **Warning:** The PhotoPrism Vision feature is currently in **beta** and under **active development**. Configuration examples, commands, and integration details are subject to change without notice. Use with caution and expect breaking changes as the feature evolves.

# PhotoPrism Vision

PhotoPrism can automatically generate descriptive labels and captions for your photos using advanced AI models through an optional, external service called **PhotoPrism Vision**. This allows you to enrich your library's metadata without manual effort.

!!! tldr ""
    This is an advanced feature that requires you to set up and run additional services on a computer in your network. You have the choice between using simple, built-in models or more powerful, customizable models via [Ollama](https://ollama.com/).

## Choosing Your Path: Built-in Models vs. Ollama

PhotoPrism Vision offers two main approaches for generating metadata. The **built-in models** are easy to set up as they don't require any additional software and are great for generating basic captions. For higher quality results, more detailed captions, and the ability to generate **labels** (tags), we recommend the **Ollama integration**. This approach lets you use a wide variety of powerful, state-of-the-art AI models.

---

## Step 1: Set Up the PhotoPrism Vision Service

Regardless of which path you choose, you first need to set up the PhotoPrism Vision service. This service is the core of the AI integration.

1. Create a new, empty folder on the machine where you want to run the Vision service.
2. Inside this new folder, create a file named `compose.yaml`.
3. Copy and paste the following content into the file:

!!! example "`compose.yaml`"
    ```yaml
    # Docker Compose configuration for the PhotoPrism Vision service.

    services:
      photoprism-vision:
        # Pulls the latest official image from Docker Hub.
        image: photoprism/vision:latest
        restart: unless-stopped
        
        # Exposes the service on port 5000 of the host machine.
        ports:
          - "5000:5000"
        
        # It's recommended to run the container as a non-root user for security.
        user: "1000:1000"
        
        environment:
          # --- Ollama Configuration (Optional) ---
          # To use Ollama, set OLLAMA_ENABLED to "true" and provide the host URL.
          # Otherwise, you can comment out or remove these lines to only use built-in models.
          - OLLAMA_ENABLED=true
          - OLLAMA_HOST=http://192.168.1.123:11434
          
        volumes:
          # This named volume stores built-in models so they are not re-downloaded.
          - "vision-models:/app/models"
          # This named volume stores the Python virtual environment.
          - "vision-venv:/app/venv"
    
    volumes:
      vision-models:
      vision-venv:
    ```

4.  **Configure the service:**
    *If you are **not** using Ollama, you can set `OLLAMA_ENABLED=false` or simply delete the two `OLLAMA...` environment lines.
    *   If you **are** using Ollama, you **must** replace `http://192.168.1.123:11434` with the correct local network URL for your Ollama instance.

5. From the folder containing your `compose.yaml` file, run the following command to start the service:

    ```bash
    docker compose up -d
    ```

## Step 2: Set Up Ollama (if you chose this path)

If you decided to use Ollama for higher quality results, follow these steps. Otherwise, proceed to Step 3.

1. Download and install Ollama from [ollama.com](https://ollama.com/) on a suitable computer.
2. **Enable Network Access:** Ensure Ollama is accessible over your local network. For detailed instructions, see the [Ollama documentation](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-expose-ollama-on-my-network).
3. **Download AI Models:** Open a terminal and pull the models you want to use:

    ```bash
    ollama pull llava-phi3:latest
    ollama pull minicpm-v:latest
    ```

## Step 3: Configure Your Main PhotoPrism Instance

Now, you need to tell your PhotoPrism instance which models to use and how to connect to the Vision service.

1. On your main PhotoPrism server, navigate to your `storage/config` folder.
2. Create or edit the file named `vision.yml`.
3. Paste the configuration that matches your chosen path.

=== "Using Ollama"

    !!! example "`storage/config/vision.yml`"
        ```yaml
        Models:
        - Type: caption
          Resolution: 720
          Name: "llava-phi3:latest"
          Service:
            # IMPORTANT: Replace this IP with the address of your Vision service machine.
            Uri: "http://192.168.1.100:5000/api/v1/vision/caption"
            FileScheme: data
            RequestFormat: vision
            ResponseFormat: vision

        - Type: labels
          Resolution: 720
          Name: "minicpm-v:latest"
          Service:
            # IMPORTANT: Replace this IP with the address of your Vision service machine.
            Uri: "http://192.168.1.100:5000/api/v1/vision/labels"
            FileScheme: data
            RequestFormat: vision
            ResponseFormat: vision
            
        Thresholds:
          Confidence: 50
        ```
    **Important:** Replace `192.168.1.100` with the IP address of the machine running your `photoprism-vision` Docker container.

=== "Using Built-in Models"

    !!! example "`storage/config/vision.yml`"
        ```yaml
        Models:
        - Type: caption
          Resolution: 720
          # This specifies the built-in 'kosmos-2' model.
          Name: "kosmos-2"
          Version: "latest"
          Service:
            # IMPORTANT: Replace this IP with the address of your Vision service machine.
            Uri: "http://192.168.1.100:5000/api/v1/vision/caption"
            FileScheme: data
            RequestFormat: vision
            ResponseFormat: vision
        
        # Note: The built-in models do not currently support label generation.
        ```
    **Important:** You still need to replace `192.168.1.100` with the IP address of your Vision service machine.

4.  After saving your `vision.yml` file, restart your main PhotoPrism instance to apply the new configuration:

    ```bash
    # Run this in your main PhotoPrism directory
    docker compose restart photoprism
    ```

## Step 4: Start Generating

Your setup is now complete! You can start generating metadata using PhotoPrism's command-line interface. You can run these commands on your entire library or on specific albums.

#### For the Entire Library

To generate captions for **all** photos in your library, run the following command. This may take a long time depending on the size of your library and your hardware.

```bash
docker compose exec photoprism photoprism vision run --models=caption
```

To generate labels for your entire library (only works if you are using Ollama):

```bash
docker compose exec photoprism photoprism vision run --models=labels
```

#### For a Specific Album

To test the process on a smaller set of photos, you can run the commands on a specific album, for example one named "Holidays":

```bash
docker compose exec photoprism photoprism vision run --models=caption album:Holidays
```

To generate labels for the album (only works if you are using Ollama):

```bash
docker compose exec photoprism photoprism vision run --models=labels album:Holidays
```

!!! tip "Re-running and Testing"
    If you want to re-generate captions or labels for photos that already have them, add the `--force` flag to the command: `photoprism vision run --models=caption --force`. This is very useful for testing different models or prompts.

---

## Troubleshooting

### Verifying Your Configuration

If you're having trouble getting the Vision service to work, a useful first step is to verify how PhotoPrism has loaded your `vision.yml` configuration. You can do this with the `vision ls` command.

Run the following command in a terminal from your main PhotoPrism directory:

```bash
docker compose exec photoprism photoprism vision ls
```

This command will output the settings for all supported and configured model types. You can compare this output with your `vision.yml` file to ensure that your settings have been read correctly and to spot any parsing errors or misconfigurations.
