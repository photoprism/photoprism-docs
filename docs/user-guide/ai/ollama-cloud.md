# Ollama Cloud Setup

Learn how to use PhotoPrism with [Ollama Cloud](https://ollama.com/blog/ollama-cloud) to generate detailed captions and accurate labels for your pictures without running a local Ollama instance.

## Step 1: Get an API Key

In order to use Ollama Cloud, you need an account at [ollama.com](https://ollama.com) and a valid API key, which you can generate at <https://ollama.com/settings/keys>.

## Step 2: Configure Environment

Add the `OLLAMA_BASE_URL` and `OLLAMA_API_KEY` environment variables to the `photoprism` service in your `compose.yaml` (or `docker-compose.yml`) file, as shown in the example below.[^1]

!!! example "compose.yaml"
    ```yaml
    services:
      photoprism:
        image: photoprism/photoprism:latest
        environment:
          OLLAMA_BASE_URL: "https://ollama.com"
          OLLAMA_API_KEY: "your-api-key"
          ...
    ```

With these variables set, PhotoPrism automatically uses the Ollama Cloud endpoint for all Ollama-based models configured in your [`vision.yml`](index.md#visionyml-reference). You do not need to specify a `Service.Uri` or `Service.Key` in the model configuration, as they are resolved from the environment.

!!! info ""
    When `OLLAMA_BASE_URL` is set to `https://ollama.com`, PhotoPrism switches to cloud defaults automatically. An API key alone does not force cloud usage. Ollama Cloud model names change and are occasionally retired without notice, so we recommend setting an explicit, currently-available `Model:` in `vision.yml` — for example `minimax-m3:cloud` — and checking the [list of cloud models](https://ollama.com/search?c=cloud) if label or caption generation stops working.

## Step 3: Configure Models

Create a new `vision.yml` file in your config path (default: `storage/config`) or edit the existing file in [the *storage/config* folder](../../getting-started/docker-compose.md#photoprismstorage) of your PhotoPrism instance, following the example below.

Since the service URI is resolved from `OLLAMA_BASE_URL`, you can omit the `Service` block:

!!! example "vision.yml"
    ```yaml
    Models:
    - Type: labels
      Model: minimax-m3:cloud
      Engine: ollama
      Run: auto
      Service:
        Think: "false"
    - Type: caption
      Model: minimax-m3:cloud
      Engine: ollama
      Run: auto
      Service:
        Think: "false"
    ```

Make sure the models you configure are [available on Ollama Cloud](https://ollama.com/search?c=cloud). You can browse the [list of supported cloud models](https://ollama.com/search?c=cloud) to see which ones can be used. You do not need to pull them manually, cloud models are served remotely.

Setting `Service.Think: "false"` disables the model's reasoning output and is **recommended for captions and labels**. Many current models are thinking (reasoning) models, and recent Ollama versions emit that reasoning **by default** — without this setting it leaks into the result (captions begin with text like *"The user wants a concise description of the provided image…"* and label JSON fails to parse). Disabling it also reduces latency by not spending output tokens on internal reasoning. It is harmless for non-thinking models, so you can set it unconditionally.

Always set an explicit `Model:` for cloud use: the built-in default can lag behind Ollama Cloud's current catalog (models are occasionally retired), so pinning a currently-available model such as `minimax-m3:cloud` avoids ambiguity and keeps label and caption generation working.

[Learn more ›](ollama-models.md)

### Scheduling Options

- `Run: auto` (recommended) automatically runs the model after indexing is complete to prevent slowdowns during indexing or importing. It also [allows manual](cli.md#run-vision-models) and [scheduled invocations](../../getting-started/config-options.md#computer-vision).
- `Run: manual` disables automatic execution, allowing you to [run the model manually](cli.md#run-vision-models) via `photoprism vision run -m caption` or `photoprism vision run -m labels`.

[Learn more ›](index.md#run-modes)

### Configuration Tips

PhotoPrism evaluates models from the bottom of the list up, so placing the Ollama entries after the others ensures Ollama is chosen first while the others remain available as fallback options.

Ollama-generated captions and labels are stored with the `ollama` metadata source automatically, so you do not need to request a specific `source` field in the schema or pass `--source` to the CLI unless you want to override the default.

!!! tip "Prompt Localization"
    To generate output in other languages, keep the base instructions in English and add the desired language (e.g., "Respond in German"). This method works for both [caption](ollama-models.md#qwen3-vl-caption) and [label prompts](ollama-models.md#qwen3-vl-labels).

## Step 4: Restart PhotoPrism

Run the following commands to restart `photoprism` and apply the new settings:

```bash
docker compose stop photoprism
docker compose up -d
```

You should now be able to use the `photoprism vision` [CLI commands](./cli.md#run-vision-models) when [opening a terminal](../../getting-started/docker-compose.md#opening-a-terminal), e.g. `photoprism vision run -m caption` to generate captions, or `photoprism vision run -m labels` to generate labels.

[Learn more ›](cli.md#run-vision-models)

## Troubleshooting

### Verifying Your Configuration

If you encounter issues, a good first step is to verify how PhotoPrism has loaded your [`vision.yml`](index.md#visionyml-reference) configuration. You can do this by running:

```bash
docker compose exec photoprism photoprism vision ls
```

This command outputs the settings for all supported and configured model types. Compare the results with your [`vision.yml`](index.md#visionyml-reference) file to confirm that your configuration has been loaded correctly and to identify any parsing errors or misconfigurations.

### Performing Test Runs

The following [terminal commands](../../getting-started/docker-compose.md#opening-a-terminal) will perform a single run for the specified model type:

```bash
photoprism vision run -m labels --count 1 --force
photoprism vision run -m caption --count 1 --force
```

If you don't get the expected results or notice any errors, you can re-run the commands with trace log mode enabled to inspect the request and response:

```bash
photoprism --log-level=trace vision run -m labels --count 1 --force
photoprism --log-level=trace vision run -m caption --count 1 --force
```

[^1]: Unrelated configuration details have been omitted for brevity.
