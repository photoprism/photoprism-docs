# Using the OpenAI API

Learn how to use PhotoPrism with OpenAI's GPT-5 models to generate high-quality captions and labels for your pictures.

## Setup

### Prerequisites

- In order to use OpenAI services, you need a valid API key, which can be configured via `OPENAI_API_KEY` or `OPENAI_API_KEY_FILE`.
- PhotoPrism must also have network access to `api.openai.com`.

### Configuration

Add the following caption and/or labels model configurations to your `vision.yml` file:

```yaml
Models:
  - Type: caption
    Model: gpt-5-nano
    Engine: openai
    Run: auto
    Options:
      Detail: low           # optional: default is low
      MaxOutputTokens: 512  # optional: change token limit
    Service:
      Key: ${OPENAI_API_KEY}
  - Type: labels
    Model: gpt-5-mini
    Engine: openai
    Run: auto
    Options:
      MaxOutputTokens: 1024 # optional: change token limit
    Service:
      Key: ${OPENAI_API_KEY}
```

Recommendations:

- Keep the model `Name` exactly as published by OpenAI so defaults apply correctly.
- `Service.Key` can be omitted if `OPENAI_API_KEY` / `_FILE` is set in the environment.
- Optional headers: set `Service.Org` and `Service.Project` when your account requires them.

!!! tldr ""
    By default, PhotoPrism uses the OpenAI Responses API endpoint at `https://api.openai.com/v1/responses` with a single 720 px thumbnail (`detail: low`).

## Usage Tips

- To avoid unexpected API costs, especially when testing new models or prompts, set `Run: manual` and [run the models manually](cli.md#run-vision-models) via `photoprism vision run -m caption` or `photoprism vision run -m labels`.
- `Run: auto` automatically runs the model after indexing is complete to prevent slowdowns during indexing or importing. It also [allows manual](cli.md#run-vision-models) and [scheduled invocations](../../getting-started/config-options.md#computer-vision).
- PhotoPrism evaluates models from the bottom of the list up, so putting the OpenAI entries after the others ensures OpenAI is chosen first, leaving other models as backups.
- When you need domain-specific wording, you may override `System` or `Prompt` in `vision.yml`; keep them short and retain the schema reminder for labels.
- For other languages, keep the base instructions in English and add the desired language (e.g., "Respond in German"). This method works for both caption and label prompts.

## Troubleshooting ##

### Verifying Your Configuration

If you encounter issues, a good first step is to verify how PhotoPrism has loaded your `vision.yml` configuration. You can do this by running: 

```bash
docker compose exec photoprism photoprism vision ls
```

This command outputs the settings for all supported and configured model types. Compare the results with your `vision.yml` file to confirm that your configuration has been loaded correctly and to identify any parsing errors or misconfigurations.

### Performing Test Runs 

The following [terminal commands](../../getting-started/docker-compose.md#opening-a-terminal) will perform a single run for the specified model type:

```bash
photoprism vision run -m labels --count 1 --force
photoprism vision run -m caption --count 1 --force
```

If output is empty, enable trace logging temporarily (`PHOTOPRISM_LOG_LEVEL=trace`) and re-run the command to inspect the request/response.
