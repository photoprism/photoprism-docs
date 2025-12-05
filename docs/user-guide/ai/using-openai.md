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
  - Type: labels
    Model: gpt-5-mini
    Engine: openai
    Run: auto
    Options:
      MaxOutputTokens: 1024 # optional: change token limit
    Service:
      Key: ${OPENAI_API_KEY}
  - Type: caption
    Model: gpt-5-nano
    Engine: openai
    Run: auto
    Options:
      Detail: low           # optional: default is low
      MaxOutputTokens: 512  # optional: change token limit
    Service:
      Key: ${OPENAI_API_KEY}
```

Recommendations:

- Keep the `Model` name exactly as published by OpenAI. The default model is `gpt-5-mini`.
- `Service.Key` can be omitted if `OPENAI_API_KEY` / `_FILE` is set in the environment. You can optionally set `Service.Org` and `Service.Project` when your account requires them for accounting purposes.
- PhotoPrism evaluates models from the bottom of the list up, so putting the OpenAI entries after the others ensures OpenAI is chosen first, leaving other models as backups.

!!! tldr ""
    By default, PhotoPrism uses the OpenAI Responses API endpoint at `https://api.openai.com/v1/responses` with a single 720 px thumbnail (`detail: low`). It can be changed by setting a custom `Service.Url`.

## Usage Tips

### Model Run Modes

To avoid unnecessary API requests and costs, especially when [testing your configuration](#performing-test-runs), set `Run: manual` and [run the models manually](cli.md#run-vision-models) via `photoprism vision run -m caption` or `photoprism vision run -m labels`. `Run: auto` will automatically run a model once indexing is complete to prevent slowdowns during indexing or importing. This option also [allows manual](cli.md#run-vision-models) and [scheduled invocations](../../getting-started/config-options.md#computer-vision).

[Learn more ›](index.md#run-modes)

### Replacing Existing Labels

If you want to remove existing labels from the built-in image classification model, run the command `photoprism vision reset -m labels -s image` in [a terminal](../../getting-started/docker-compose.md#opening-a-terminal) before you regenerate all labels with OpenAI using the following command:

```
photoprism vision run -m labels
```

[Learn more ›](cli.md#reset-vision-data)

### Generating Custom Labels

You may override the default `System` or `Prompt` instructions in your [`vision.yml`](index.md#visionyml-reference) configuration to customize the generated labels to your needs:

- **System:** You are a PhotoPrism vision model. Emit JSON that matches the provided schema and keep label names short, singular nouns.
- **Prompt:** Analyze the image and return label objects with name, confidence (0-1), and topicality (0-1).

Keep prompts short and **retain the JSON schema reminder** for labels. For **other languages**, keep the base prompt in English and add the desired language (e.g., "Respond in German"). This method works for both caption and label prompts.

Example:

```yaml
Models:
  - Type: labels
    Model: gpt-5-mini
    Engine: openai
    Run: auto
    Prompt: >
      Analyze the image and return up to 3 label objects with
      German singular name, confidence (0-1), and topicality (0-1).
```

### Changing the Caption Prompt

If you want longer captions, **other languages**, or need **domain-specific** descriptions, you may override the default `System` or `Prompt` instructions in your [`vision.yml`](index.md#visionyml-reference) configuration:

- **System:** You are a PhotoPrism vision model. Return concise, user-friendly captions that describe the main subjects accurately.
- **Prompt:** Provide exactly one sentence describing the key subject and action in the image. Avoid filler words and technical jargon.

Example:

```yaml
Models:
  - Type: caption
    Model: gpt-5-mini
    Engine: openai
    Run: auto
    Prompt: >
      Provide one or two German sentences describing the key subject and
      action in the image. Avoid filler words and technical jargon.
```

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
