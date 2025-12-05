# Ollama Models

We recommend choosing a [vision model](https://ollama.com/search?c=vision) that balances speed, accuracy, and reliability. Two models that meet these criteria and that we can recommend are [Gemma 3](https://ollama.com/library/gemma3) and [Qwen3-VL](https://ollama.com/library/qwen3-vl):

| Model        | Use Case                                                   | Notes                                                                                     |
|--------------|------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| **Gemma 3**  | Standard caption and label generation                      | Light, reliable JSON output; good default.                                                |
| **Qwen3-VL** | Advanced vision and reasoning tasks (OCR, complex prompts) | Better visual grounding and multi-language support; available in many sizes and variants. |

[**Gemma 3**](https://ollama.com/library/gemma3) is very consistent in terms of performance, with errors occurring rarely. However, it is less suitable for long/complex prompts and captions. We recommend using the [standard variant](https://ollama.com/library/gemma3/tags), `gemma3:latest`, for most [use cases](#gemma-3-labels).

[**Qwen3-VL**](https://ollama.com/library/qwen3-vl) tends to be somewhat less predictable and consistent in the [smaller `2b` and `4b` variants](https://ollama.com/library/qwen3-vl/tags), where performance and error rates can vary widely [unless controlled as shown in the examples](#qwen3-vl-labels) below. The standard `qwen3-vl:latest` (`8b`) version generally works well without major adjustments. One drawback is slightly lower performance compared to Gemma 3 on an NVIDIA RTX 4060, with [label generation taking 2–3 seconds](#qwen3-vl-labels) versus [1–2 seconds](#gemma-3-labels).

Performance also depends on your hardware, so e.g., [Qwen3-VL variants](https://ollama.com/search?q=qwen3-vl) might outperform Gemma 3 when running on Apple Silicon or NVIDIA Blackwell GPUs. Our recommendation is therefore to test both models to see which one works best for you. If you generate both captions and labels, stick with this model so that Ollama doesn't need to swap models between requests.

!!! tldr ""
    Without GPU acceleration, Ollama models will be significantly slower, taking anywhere from 10 seconds to over a minute to complete. This may be acceptable if you only want to process a few pictures or are willing to wait.

## Temperature, TopK, and TopP

Specifying the `Temperature`, `TopK`, and `TopP` [options](index.md#options) when using Ollama models allows you to control the randomness and creativity of generative [large-language models](https://en.wikipedia.org/wiki/Large_language_model):

| Parameter   | Effect on Output                           | When to Use                                    |
|-------------|--------------------------------------------|------------------------------------------------|
| Temperature | Adjusts overall randomness                 | Control creativity without limiting vocabulary |
| TopK        | Restricts choices to most probable tokens  | Prevent rare or irrelevant tokens              |
| TopP        | Adapts vocabulary size based on confidence | Dynamic control over diversity                 |

### Combining Techniques

These methods can be combined to fine-tune the output further. For instance:

- **Temperature + TopK:** adjust randomness while choosing the most probable tokens.
- **Temperature + TopP:** control creativity with temperature and adaptively limit tokens.

You can additionally specify **MinP** to cut off tokens with very low probability, which are typically rare labels and odd phrasings that you don't want for classification.

## Caption Prompts

With most models, the following should generate concise captions with exactly one sentence:

> Create a caption with exactly one sentence in the active voice that describes the main visual content. Begin with the main subject and clear action. Avoid text formatting, meta-language, and filler words.

**Example:** *A sleek pool extends over a dramatic cliffside overlooking turquoise waters.*

For detailed captions, try this prompt, which should generate up to three sentences:

> Write a descriptive caption in 3 sentences or fewer that captures the essence of the visual content. Avoid text formatting, meta-language, and filler words. Do not start captions with phrases such as "This image", "The picture", or "Here are". Begin with the subject(s), then describe the surroundings, and finally add atmosphere (e.g., time of day). If possible, include the subject's gender and general age group.

**Example:** *A gray cat with a fluffy coat is lounging on a cushion, its eyes closed in a peaceful slumber. The background features a blurred view of trees and a blue sky, suggesting it's daytime. The cat's relaxed posture and the serene outdoor setting create a tranquil and cozy atmosphere.*

For other languages, keep the base instructions in English and add the desired language (e.g., "Respond in German"). This method works for both caption and label prompts.

!!! tldr ""
    When tuning prompts, keep them as short as possible. Overly long prompts can increase hallucinations and latency.

## Configuration Examples

The following drop-in examples can be specified in your `vision.yml` file, which is located in the `storage/config` directory. [Learn more ›](index.md#visionyml-reference).

### Gemma 3: Labels

```yaml
Models:
- Type: labels
  Model: gemma3:latest
  Engine: ollama
  Run: auto
  Service:
    Uri: http://ollama:11434/api/generate
```

Why this works:

- **Engine:** Applies suitable **Resolution**, **Format**, **Prompt** and **Options** defaults (720 px thumbnails, JSON prompts for labels). Specifying a custom prompt is not required.
- **Run:** `auto` allows manual, after indexing, and scheduled runs ￫ [Run Modes](index.md#run-modes).

### Gemma 3: Caption

```yaml
Models:
- Type: caption
  Model: gemma3:latest
  Engine: ollama
  Run: auto
  Prompt: >
    Create a caption with exactly one sentence in the active voice that
    describes the main visual content. Begin with the main subject and
    clear action. Avoid text formatting, meta-language, and filler words.
  Service:
    Uri: http://ollama:11434/api/generate
```

Why this works:

- **Engine:** Uses 720 px thumbnails and applies suitable **Format**, **Prompt** and **Options** defaults. Specifying a [custom prompt](#caption-prompts) is not required, but possible.
- **Run:** `auto` allows manual, after indexing, and scheduled runs ￫ [Run Modes](index.md#run-modes).
- **Prompt:** Uses the built-in [default prompt](#caption-prompts). For other languages, keep the base instructions in English and add the desired language (e.g., "Respond in German").

### Qwen3-VL: Labels

```yaml
Models:
- Type: labels
  Model: qwen3-vl:4b-instruct
  Engine: ollama
  Run: on-demand
  Prompt: |
    Analyze the image and return JSON label objects with name, confidence (0-1), and topicality (0-1):
    - Return AT MOST 3 labels.
    - Each label name MUST be a single-word noun in canonical singular form.
    - Do NOT repeat the same label name more than once.
    - Do NOT add any fields other than name, confidence, topicality.
    - Do NOT output any text before or after the JSON.
  Options:
    Seed: 3407           # model default, see https://github.com/QwenLM/Qwen3-VL
    Temperature: 0.01    # low randomness, fewer hallucinations
    TopK: 40             # consider only top ~40 tokens
    TopP: 0.9            # cut off tail of distribution
    MinP: 0.05           # drop rare tokens
    TypicalP: 1.0        # effectively off
    RepeatLastN: 128     # look back to prevent repetition
    RepeatPenalty: 1.2   # penalty to avoid simple loops
    NumPredict: 512      # prevent runaway output
  Service:
    Uri: http://ollama:11434/api/generate
```

Why this works:

- **Model:** [`qwen3-vl:4b-instruct`](https://ollama.com/library/qwen3-vl/tags) is a lightweight version of Qwen3-VL. You can alternatively try [`huihui_ai/qwen3-vl-abliterated:4b-instruct`](https://ollama.com/huihui_ai/qwen3-vl-abliterated), [`qwen3-vl:latest`](https://ollama.com/library/qwen3-vl), or other [variants](https://ollama.com/search?c=vision&q=qwen3-vl).
- **Engine:** Applies suitable **Resolution**, **Format**, and **Options** defaults.
- **Run:** `on-demand` allows manual, metadata worker, and scheduled jobs ￫ [Run Modes](index.md#run-modes).
- **Prompt:** Ensures low latency, prevents repetition, and controls the type and number of labels returned. For other languages, keep the base instructions in English and add the desired language (e.g., "Respond in German").
- **Seed:** Ensures stable labels. Our example uses the [instruct model variant](https://github.com/QwenLM/Qwen3-VL?tab=readme-ov-file#instruct-models) default.
- **Temperature, TopP,** and **TopK:** Picks high-probability, common words, not creative synonyms.
- **MinP:** Cuts off very low-probability tokens, which are typically those rare labels and odd phrasings you don’t want for classification.
- **RepeatLastN** and **RepeatPenalty:** Ensures that labels are unique by penalizing repetition.
- **NumPredict:** Limits the maximum number of output tokens to prevent infinite repetition.

### Qwen3-VL: Caption

```yaml
Models:
- Type: caption
  Model: qwen3-vl:4b-instruct
  Engine: ollama
  Run: on-schedule
  System: You are an image captioning assistant.
  Prompt: |
    Write one or two concise sentences that describe the main subject, key actions, and setting of the image:
    - Describe only what is clearly visible in the image; do not invent names, ages, or backstories.
    - Use natural, fluent language without bullet points or lists.
    - Do NOT start with phrases like "The image shows" or "In this picture".
    - Do NOT mention camera settings, image quality, filters, or art style unless they are essential to understanding the content.
    - Do NOT include quotation marks around the caption.
    - Respond with the caption text only, and nothing else.
  Options:
    Seed: 3407           # model default, see https://github.com/QwenLM/Qwen3-VL
    Temperature: 0.25    # reduce randomness for fewer hallucinations
    TopK: 20             # matches the model's default
    TopP: 0.8            # matches the model's default
    MinP: 0.05           # cut very low-probability, odd tokens
    TypicalP: 1.0        # effectively disabled; TopP/MinP dominate
    RepeatLastN: 64      # short history for 1–2 sentences
    RepeatPenalty: 1.1   # penalty to avoid loops without harming fluency
    NumPredict: 128      # prevent runaway output
  Service:
    Uri: http://ollama:11434/api/generate
```

Why this works:

- **Model:** Using [`qwen3-vl:4b-instruct`](https://ollama.com/library/qwen3-vl/tags) for both labels and captions avoids time-consuming Ollama model swaps. You can alternatively try [`huihui_ai/qwen3-vl-abliterated:4b-instruct`](https://ollama.com/huihui_ai/qwen3-vl-abliterated), [`qwen3-vl:latest`](https://ollama.com/library/qwen3-vl), or other [variants](https://ollama.com/search?c=vision&q=qwen3-vl).
- **Engine:** Applies suitable **Resolution**, **Format**, and **Options** defaults.
- **Run:** `on-schedule` allows manual and scheduled jobs ￫ [Run Modes](index.md#run-modes).
- **System:** Tells the model to describe images in natural language.
- **Prompt:** Asks for one or two sentences describing the subject, actions, and setting while banning meta phrases such as "The image shows...", lists, and extra commentary. This pushes the model toward clean alt-text-style captions that can be displayed directly in UIs without further processing. Guidelines such as "describe only what is clearly visible" and "do not invent names/ages/backstories" prevent the model from hallucinating brands, story details, or emotions, keeping captions factual and safe for automated use.
- **Seed:** Gives stable, reproducible captions for the same image + prompt, which is useful for indexing and re-generating captions in a media library scenario. If you want more variety per refresh, simply drop or randomize the seed.
- **Temperature** and **MinP:** Removes the long tail of very low-probability tokens (weird words, broken fragments) and keeps token choices close to the most likely ones. Together, this yields simple, high-confidence captions rather than imaginative paraphrases.
- **TopK** and **TopP:** Ensures stability and lower hallucination risk in a captioning context.
- **RepeatPenalty** and **RepeatLastN:** Discourages repetition without affecting normal phrasing.
- **NumPredict:** High enough for 1–2 sentences, but low enough to avoid rambling.

## Usage Tips

### Model Run Modes

To avoid unnecessary API requests, especially when [testing your configuration](#performing-test-runs), set `Run: manual` and [run the models manually](cli.md#run-vision-models) via `photoprism vision run -m caption` or `photoprism vision run -m labels`. `Run: auto` will automatically run a model once indexing is complete to prevent slowdowns during indexing or importing. This option also [allows manual](cli.md#run-vision-models) and [scheduled invocations](../../getting-started/config-options.md#computer-vision).

[Learn more ›](index.md#run-modes)

### Replacing Existing Labels

If you want to remove existing labels from the built-in image classification model, run the command `photoprism vision reset -m labels -s image` in [a terminal](../../getting-started/docker-compose.md#opening-a-terminal) before you regenerate all labels with Ollama using the following command:

```
photoprism vision run -m labels
```

[Learn more ›](cli.md#reset-vision-data)

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
