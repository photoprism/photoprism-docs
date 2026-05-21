# Using AI Models

As an addition to the built-in TensorFlow models, PhotoPrism lets you generate captions and labels with [Ollama](using-ollama.md) and the [OpenAI API](using-openai.md). Our step-by-step guides explain how to set them up and provide tested configuration examples you can use as a starting point.

[Learn more ›](using-ollama.md)

## Model Engines

PhotoPrism currently supports the following runtimes and services:

| Engine                                                                 | Resolution | Runs        | Best For                                                                                                      |
|------------------------------------------------------------------------|------------|-------------|---------------------------------------------------------------------------------------------------------------|
| [TensorFlow](../../developer-guide/vision/tensorflow/custom-models.md) | 224 px     | Built-in    | Fast, offline default models for core features (labels, faces, NSFW)                                          |
| [Ollama](using-ollama.md)                                              | 720 px     | Self-Hosted | Good for generating quality captions & labels; a server with GPU is recommended                               |
| [OpenAI API](using-openai.md)                                          | 720 px     | Cloud       | Highest quality captions & labels, also suitable for users without a GPU; requires API key and network access |

### Performance

- **TensorFlow:** Our built-in models generally perform well on all types of hardware.
- **Ollama:** [Generating labels](ollama-models.md#gemma-3-labels) for an image on an NVIDIA RTX 4060 usually takes 1-4 seconds. The exact time varies depending on the model used and the [number of labels](ollama-models.md#qwen3-vl-labels) generated.
- **OpenAI:** Processing one image takes about 3 seconds, though this can vary by model, region, and demand.

!!! tldr ""
    Without GPU acceleration, Ollama models will be significantly slower, taking anywhere from 10 seconds to over a minute to complete. This may be acceptable if you only want to process a few pictures or are willing to wait.

## NSFW Detection

PhotoPrism can flag newly added pictures as private and reject web uploads when they contain unsafe content. Two independent config options control this:

| Config Option                                                                       | Effect                                                                                                                                                                                                                                                                  |
|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`PHOTOPRISM_DETECT_NSFW`](../../getting-started/config-options.md#computer-vision) | When `true`, photos detected as NSFW during indexing or a `photoprism vision run` are marked as **private**. When `false` (default), NSFW signals are ignored even if the underlying model returns them.                                                                |
| [`PHOTOPRISM_UPLOAD_NSFW`](../../getting-started/config-options.md#storage)         | When `false`, the **web upload** dialog rejects files that the NSFW model flags as unsafe (the rejected file is deleted before indexing). When `true` (default), uploads are accepted regardless and any NSFW flagging happens later during indexing per `DETECT_NSFW`. |

### Which Model Detects NSFW?

The model used for NSFW detection follows the same `vision.yml` mechanism as labels, captions, and faces. If no `Type: nsfw` entry is configured, PhotoPrism uses the built-in TensorFlow NSFW model. You can override it just like any other model — for example, to point at an Ollama or OpenAI endpoint trained to score NSFW content:

```yaml
Models:
  - Type: nsfw
    Model: <your-vision-model>
    Engine: ollama
    Service:
      Uri: ${OLLAMA_BASE_URL}/api/generate
```

Once the dedicated NSFW model entry is configured, it runs whenever `DETECT_NSFW` is `true` and the indexer or `photoprism vision run --models nsfw` invokes it.

### Detecting NSFW Through Label Generation

When `Type: labels` is served by Ollama or OpenAI, PhotoPrism can ask the model to include NSFW classification in the same response, avoiding a second inference pass. This shortcut is gated by **two** environment variables that must **both** be set to `true`:

- [`PHOTOPRISM_DETECT_NSFW`](../../getting-started/config-options.md#computer-vision)
- [`PHOTOPRISM_EXPERIMENTAL`](../../getting-started/config-options.md#feature-flags)

If either is `false`, the label-generation prompt does **not** ask for NSFW fields, so the LLM response cannot trigger NSFW flagging — even if NSFW signals exist in the image. The following matrix summarises the behaviour when Ollama or OpenAI is configured for labels and the user runs `photoprism vision run --models labels`:

| `DETECT_NSFW` | `EXPERIMENTAL` | Label prompt                                  | Outcome                                                                                                                                                                               |
|---------------|----------------|-----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `false`       | `false`        | Default labels prompt (no NSFW fields)        | NSFW detection does not run.                                                                                                                                                          |
| `false`       | `true`         | Default labels prompt (no NSFW fields)        | NSFW detection does not run.                                                                                                                                                          |
| `true`        | `false`        | Default labels prompt (no NSFW fields)        | NSFW detection does not run via labels; the dedicated NSFW model only runs when `nsfw` is explicitly included in the run's models (e.g. `--models labels,nsfw`).                      |
| `true`        | `true`         | NSFW-aware prompt (`nsfw`, `nsfw_confidence`) | LLM returns NSFW fields; photos above the configured threshold are flagged as private. The dedicated NSFW model still runs as a fallback when `nsfw` is included in the run's models. |

!!! tldr ""
    If you switched from TensorFlow to an Ollama or OpenAI labels model and noticed that NSFW detection stopped working, the most likely cause is that one of the two flags above is missing. Enable both `PHOTOPRISM_DETECT_NSFW=true` and `PHOTOPRISM_EXPERIMENTAL=true`, or include `nsfw` in the explicit `--models` list so the dedicated NSFW model runs alongside labels.

### NSFW Threshold

The `Thresholds.NSFW` value in `vision.yml` (default `75`, range `0-100`) controls how confident the model must be before a picture is flagged. Lower values are more aggressive; higher values are more permissive. The threshold applies to both the dedicated NSFW model and the NSFW fields returned through the label-generation prompt.

## `vision.yml` Reference

Custom AI engines, models, and run modes can be specified in a `vision.yml` file located in your config directory (default: `storage/config`). The file defines a list of models and thresholds to be used, e.g.:

!!! info ""
    If PhotoPrism can’t read your config file, make sure the file exists at the config path configured for your instance. Older installations may use `storage/settings`.
    
    Run `docker compose exec photoprism photoprism show config | grep config-path` to find out what's your configured config path.

```yaml
Models:
- Type: caption
  Model: gemma3:latest
  Engine: ollama
  Run: auto
  Options:
    Temperature: 0.05
  Service:
    Uri: http://ollama:11434/api/generate
- Type: labels
  Model: qwen3-vl:latest
  Engine: ollama
  Service:
    Uri: http://ollama:11434/api/generate
Thresholds:
  Confidence: 10
  Topicality: 0
  NSFW: 75
```

If a model type is omitted, PhotoPrism will use the built-in defaults for `labels`, `nsfw`, `face`, or `caption`. The optional `Thresholds` block can be used to filter out labels with a low probability or adjust the probability of flagging content as NSFW. 

| Field                   | Default                                | Notes                                                                              |
|-------------------------|----------------------------------------|------------------------------------------------------------------------------------|
| `Type` (required)       | —                                      | `labels`, `caption`, `face`, `nsfw`. Drives routing & scheduling.                  |
| `Model`                 | `""`                                   | Raw identifier override; precedence: `Service.Model` → `Model` → `Name`.           |
| `Name`                  | derived from type/version              | Display name; lower-cased by helpers.                                              |
| `Version`               | `latest` (non-OpenAI)                  | OpenAI payloads omit version.                                                      |
| `Engine`                | inferred from service/alias            | Aliases set formats, file scheme, resolution. Explicit `Service` values still win. |
| `Run`                   | `auto`                                 | See Run modes table below.                                                         |
| `Default`               | `false`                                | Keep one per type for TensorFlow fallbacks.                                        |
| `Disabled`              | `false`                                | Registered but inactive.                                                           |
| `Resolution`            | 224 (TensorFlow) / 720 (Ollama/OpenAI) | Thumbnail edge in px; TensorFlow models default to 224 unless you override.        |
| `System` / `Prompt`     | engine defaults / empty                | Override prompts per model.                                                        |
| `Format`                | `""`                                   | Response hint (`json`, `text`, `markdown`).                                        |
| `Schema` / `SchemaFile` | engine defaults / empty                | Inline vs file JSON schema (labels).                                               |
| `TensorFlow`            | engine defaults / empty                | Local TF model info (paths, tags).                                                 |
| [`Options`](#options)   | engine defaults / empty                | Sampling/settings merged with engine defaults.                                     |
| [`Service`](#service)   | engine defaults / empty                | Remote endpoint config (see below).                                                |

### Run Modes

| Value           | When it runs                                                     | Recommended use                                |
|-----------------|------------------------------------------------------------------|------------------------------------------------|
| `auto`          | TensorFlow defaults during index; external via metadata/schedule | Leave as-is for most setups.                   |
| `manual`        | Only when explicitly invoked (CLI/API)                           | Experiments and diagnostics.                   |
| `on-index`      | During indexing + manual                                         | Fast built-in models only.                     |
| `newly-indexed` | Metadata worker after indexing + manual                          | External/Ollama/OpenAI without slowing import. |
| `on-demand`     | Manual, metadata worker, and scheduled jobs                      | Broad coverage without index path.             |
| `on-schedule`   | Scheduled jobs + manual                                          | Nightly/cron-style runs.                       |
| `always`        | Indexing, metadata, scheduled, manual                            | High-priority models; watch resource use.      |
| `never`         | Never executes                                                   | Keep definition without running it.            |

!!! tldr ""
    For performance reasons, `on-index` is only supported for the built-in TensorFlow models.

### Options

Adjusts model parameters, such as temperature and top-p, as well as other constraints, when using [Ollama](using-ollama.md) or [OpenAI](using-openai.md):

| Option             | Engines        | Default             | Description                                                                             |
|--------------------|----------------|---------------------|-----------------------------------------------------------------------------------------|
| `Temperature`      | Ollama, OpenAI | engine default      | Controls randomness with a value between `0.01` and `2.0`; not used for OpenAI's GPT-5. |
| `TopK`             | Ollama         | engine default      | Limits sampling to the top K tokens to reduce rare or noisy outputs.                    |
| `TopP`             | Ollama, OpenAI | engine default      | Nucleus sampling; keeps the smallest token set whose cumulative probability ≥ `p`.      |
| `MinP`             | Ollama         | engine default      | Drops tokens whose probability mass is below `p`, trimming the long tail.               |
| `TypicalP`         | Ollama         | engine default      | Keeps tokens with typicality under the threshold; combine with TopP/MinP for flow.      |
| `TfsZ`             | Ollama         | engine default      | Tail free sampling parameter; lower values reduce repetition.                           |
| `Seed`             | Ollama         | random per run      | Fix for reproducible outputs; unset for more variety between runs.                      |
| `NumKeep`          | Ollama         | engine default      | How many tokens to keep from the prompt before sampling starts.                         |
| `RepeatLastN`      | Ollama         | engine default      | Number of recent tokens considered for repetition penalties.                            |
| `RepeatPenalty`    | Ollama         | engine default      | Multiplier >1 discourages repeating the same tokens or phrases.                         |
| `PresencePenalty`  | OpenAI         | engine default      | Increases the likelihood of introducing new tokens by penalizing existing ones.         |
| `FrequencyPenalty` | OpenAI         | engine default      | Penalizes tokens in proportion to their frequency so far.                               |
| `PenalizeNewline`  | Ollama         | engine default      | Whether to apply repetition penalties to newline tokens.                                |
| `Stop`             | Ollama, OpenAI | engine default      | Array of stop sequences (e.g., `["\\n\\n"]`).                                           |
| `Mirostat`         | Ollama         | engine default      | Enables Mirostat sampling (`0` off, `1/2` modes).                                       |
| `MirostatTau`      | Ollama         | engine default      | Controls surprise target for Mirostat sampling.                                         |
| `MirostatEta`      | Ollama         | engine default      | Learning rate for Mirostat adaptation.                                                  |
| `NumPredict`       | Ollama         | engine default      | Ollama-specific max output tokens; synonymous intent with `MaxOutputTokens`.            |
| `MaxOutputTokens`  | Ollama, OpenAI | engine default      | Upper bound on generated tokens; adapters raise low values to defaults.                 |
| `ForceJson`        | Ollama, OpenAI | engine default      | Forces structured output when enabled.                                                  |
| `SchemaVersion`    | Ollama, OpenAI | derived from schema | Override when coordinating schema migrations.                                           |
| `CombineOutputs`   | OpenAI         | engine default      | Controls whether multi-output models combine results automatically.                     |
| `Detail`           | OpenAI         | engine default      | Controls OpenAI vision detail level (`low`, `high`, `auto`).                            |
| `NumCtx`           | Ollama, OpenAI | engine default      | Context window length (tokens).                                                         |
| `NumThread`        | Ollama         | runtime auto        | Caps CPU threads for local engines.                                                     |
| `NumBatch`         | Ollama         | engine default      | Batch size for prompt processing.                                                       |
| `NumGpu`           | Ollama         | engine default      | Number of GPUs to distribute work across.                                               |
| `MainGpu`          | Ollama         | engine default      | Primary GPU index when multiple GPUs are present.                                       |
| `LowVram`          | Ollama         | engine default      | Enable VRAM-saving mode; may reduce performance.                                        |
| `VocabOnly`        | Ollama         | engine default      | Load vocabulary only for quick metadata inspection.                                     |
| `UseMmap`          | Ollama         | engine default      | Memory map model weights instead of fully loading them.                                 |
| `UseMlock`         | Ollama         | engine default      | Lock model weights in RAM to reduce paging.                                             |
| `Numa`             | Ollama         | engine default      | Enable NUMA-aware allocations when available.                                           |

### Service

Configures the endpoint URL, method, format, and authentication for [Ollama](using-ollama.md), [OpenAI](using-openai.md), and other engines that perform remote HTTP requests:

| Field                              | Default        | Notes                                                                                          |
|------------------------------------|----------------|------------------------------------------------------------------------------------------------|
| `Uri`                              | engine default | Service endpoint URL. Empty for local models.                                                  |
| `Method`                           | `POST`         | Override only if provider needs it.                                                            |
| `Key`                              | `""`           | Bearer token; supports env expansion (OpenAI: `OPENAI_API_KEY`, Ollama: `OLLAMA_API_KEY`[^1]). |
| `Username` / `Password`            | `""`           | Injected as basic auth when `Uri` lacks userinfo.                                              |
| `Model`                            | `""`           | Endpoint-specific override; wins over model/name.                                              |
| `Org` / `Project`                  | `""`           | Organization / Project ID when using OpenAI.                                                   |
| `Think`                            | `""`           | Optional Ollama reasoning hint. Quoted `"true"` / `"false"` values are sent as JSON booleans.  |
| `RequestFormat` / `ResponseFormat` | engine default | Explicit values win over engine defaults.                                                      |
| `FileScheme`                       | engine default | Controls image transport e.g. `data` or `base64`.                                              |
| `Disabled`                         | `false`        | Disables the endpoint without removing the model.                                              |

!!! tldr ""
    **Authentication:** All credentials and identifiers support `${ENV_VAR}` expansion. `Service.Key` sets `Authorization: Bearer <token>`; `Username`/`Password` injects HTTP basic authentication into the service URI when it is not already present. When `Service.Key` is empty, PhotoPrism defaults to `OPENAI_API_KEY` (OpenAI engine) or `OLLAMA_API_KEY`[^1] (Ollama engine), also honoring their `_FILE` counterparts.
 
[^1]: Available since the [March 5, 2026 release](../../release-notes.md#march-5-2026).
