# NSFW Detection

PhotoPrism can automatically flag pictures as **private** when an image-classification model considers them unsafe for work, and can also reject such files at the **web upload** stage so they never enter the index. NSFW detection is opt-in and disabled by default; it is mainly intended to help operators of public or shared instances keep adult content out of their library without having to review every upload by hand.

## Configuration Options

Two independent config options govern the runtime behaviour. Both are off by default:

| Config Option                                                                       | Effect                                                                                                                                                                                                                                                                  |
|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`PHOTOPRISM_DETECT_NSFW`](../../getting-started/config-options.md#computer-vision) | When `true`, photos detected as NSFW during indexing or a `photoprism vision run` are marked as **private**. When `false` (default), NSFW signals are ignored even if the underlying model returns them.                                                                |
| [`PHOTOPRISM_UPLOAD_NSFW`](../../getting-started/config-options.md#storage)         | When `false`, the **web upload** dialog rejects files that the NSFW model flags as unsafe (the rejected file is deleted before indexing). When `true` (default), uploads are accepted regardless and any NSFW flagging happens later during indexing per `DETECT_NSFW`. |

The two options are independent: you can reject uploads without flagging existing imports, flag existing imports without policing uploads, or both.

## Which Model Detects NSFW?

The model used for NSFW detection follows the same [`vision.yml`](index.md#visionyml-reference) mechanism as labels, captions, and faces. If no `Type: nsfw` entry is configured, PhotoPrism uses the built-in TensorFlow NSFW model. You can override it just like any other model — for example, to point at an Ollama or OpenAI endpoint trained to score NSFW content:

```yaml
Models:
  - Type: nsfw
    Model: <your-vision-model>
    Engine: ollama
    Service:
      Uri: ${OLLAMA_BASE_URL}/api/generate
```

Once the dedicated NSFW model entry is configured, it runs whenever `PHOTOPRISM_DETECT_NSFW` is `true` and the indexer or `photoprism vision run --models nsfw` invokes it.

!!! info ""
    The built-in TensorFlow NSFW model is small and fast and ships with every PhotoPrism image. There is no need to configure an LLM-based replacement unless you want to.

### Using a Labels Model

When `Type: labels` is served by [Ollama](using-ollama.md) or the [OpenAI API](using-openai.md), PhotoPrism can ask the model to include NSFW classification in the same response, avoiding a second inference pass. This shortcut is **experimental** and gated by two environment variables that must **both** be set to `true`:

- [`PHOTOPRISM_DETECT_NSFW`](../../getting-started/config-options.md#computer-vision)
- [`PHOTOPRISM_EXPERIMENTAL`](../../getting-started/config-options.md#feature-flags)

If either is `false`, the label-generation prompt will not ask for NSFW fields, so the LLM response cannot trigger NSFW flagging — even if an image contains NSFW content. The following matrix summarizes the behavior when Ollama or OpenAI is configured for labels and the user runs `photoprism vision run --models labels`:

| Detect NSFW | Experimental | Labels Prompt                                 | Outcome                                                                                                                                                                               |
|-------------|--------------|-----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `false`     | `false`      | Default labels prompt (no NSFW fields)        | NSFW detection does not run.                                                                                                                                                          |
| `false`     | `true`       | Default labels prompt (no NSFW fields)        | NSFW detection does not run.                                                                                                                                                          |
| `true`      | `false`      | Default labels prompt (no NSFW fields)        | NSFW detection does not run via labels; the dedicated NSFW model only runs when `nsfw` is explicitly included in the run's models (e.g. `--models labels,nsfw`).                      |
| `true`      | `true`       | NSFW-aware prompt (`nsfw`, `nsfw_confidence`) | LLM returns NSFW fields; photos above the configured threshold are flagged as private. The dedicated NSFW model still runs as a fallback when `nsfw` is included in the run's models. |

!!! tldr ""
    If you switched from TensorFlow to an Ollama or OpenAI labels model and noticed that NSFW detection stopped working, the most likely cause is that one of the two flags above is missing. Enable both `PHOTOPRISM_DETECT_NSFW=true` and `PHOTOPRISM_EXPERIMENTAL=true`, or include `nsfw` in the explicit `--models` list so the dedicated NSFW model runs alongside labels.

## NSFW Threshold

The `Thresholds.NSFW` value in [`vision.yml`](index.md#visionyml-reference) controls how confident the model must be before a picture is flagged. The threshold accepts an integer between `0` and `100` and defaults to `75`. Lower values are more aggressive (more pictures flagged); higher values are more permissive. The threshold applies to both the dedicated NSFW model and the NSFW fields returned through the label-generation prompt.

```yaml
Thresholds:
  NSFW: 75
```

## Running NSFW Detection Manually

To re-evaluate the existing library after enabling or tuning NSFW detection, run the vision worker with the `nsfw` model in [a terminal](../../getting-started/docker-compose.md#opening-a-terminal):

```bash
docker compose exec photoprism photoprism vision run --models nsfw
```

Add `--force` to override existing `private` flags, and restrict the run to a subset of the library by appending a search filter (same syntax as the `--vision-filter` config option), for example:

```bash
docker compose exec photoprism photoprism vision run --models nsfw --force public:true
```

[Learn more ›](cli.md#run-vision-models)
