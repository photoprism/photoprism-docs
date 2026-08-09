# Ollama Models

We recommend choosing a [vision model](https://ollama.com/search?c=vision) that balances speed, accuracy, and reliability. Three families meet these criteria and can be recommended — [Gemma 4](https://ollama.com/library/gemma4), [Qwen3-VL](https://ollama.com/library/qwen3-vl), and [Qwen 3.5](https://ollama.com/library/qwen3.5):

| Model        | Use Case                                                   | Notes                                                                                                                               |
|--------------|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| **Gemma 4**  | Standard caption and label generation in English           | Light, reliable JSON output; good default. Not a good choice for a non-English library — see [Language Support](#language-support). |
| **Qwen3-VL** | Advanced vision and reasoning tasks (OCR, complex prompts) | Best subject coverage in our benchmark when the prompt asks for a label count. Use an `-instruct` tag.                              |
| **Qwen 3.5** | A lighter alternative for captions and labels              | Strong results on the built-in prompt at less than half the prompt tokens of Qwen3-VL. No `-instruct` tag needed.                   |

[**Gemma 4**](https://ollama.com/library/gemma4) is very consistent in terms of performance, with errors occurring rarely. However, it is less suitable for long/complex prompts and captions. We recommend using the [standard variant](https://ollama.com/library/gemma4/tags), `gemma4:latest` (currently aliases `gemma4:e4b`), for most [use cases](#gemma-4-labels). The smaller [`gemma4:e2b`](https://ollama.com/library/gemma4/tags) variant is noticeably faster and actually returns *more* labels per photo, at slightly lower subject coverage — a good choice when speed and label count matter more than picking the single best subject. If you already have [Gemma 3](https://ollama.com/library/gemma3) configured, it continues to work fine — Gemma 4 is a drop-in replacement that runs at similar latency (around 2 seconds for label generation on an NVIDIA RTX 4060 in our testing).

Where Gemma 4 loses ground is identifying a subject it is unsure about: it guesses confidently instead of staying general. In our benchmark both variants labeled a cheetah a *leopard* in every language tested and on every run, captioned a penguin colony as *seals*, and read a ski jumper as a snowboarder. If your library is heavy on wildlife or other uncommon subjects, that is the reason to try Qwen3-VL or Qwen 3.5 at a comparable size.

[**Qwen3-VL**](https://ollama.com/library/qwen3-vl) tends to be somewhat less predictable and consistent in the [smaller `2b` and `4b` variants](https://ollama.com/library/qwen3-vl/tags), where performance and error rates can vary widely [unless controlled as shown in the examples](#qwen3-vl-labels) below. The standard `qwen3-vl:latest` (`8b`) version generally works well without major adjustments. Label generation on an NVIDIA RTX 4060 typically takes [2–3 seconds](#qwen3-vl-labels), roughly comparable to [Gemma 4](#gemma-4-labels).

[**Qwen 3.5**](https://ollama.com/library/qwen3.5) is the lighter of the two Qwen options and needs no special tag: `qwen3.5:4b` already behaves like an instruct build, producing captions in about a second and keeping multi-word label names near zero. On the built-in label prompt it reached the highest subject coverage of any self-hosted model we measured, and it encodes a 720 px image into fewer than half the prompt tokens Qwen3-VL uses, which makes it noticeably cheaper on a metered endpoint. Qwen3-VL still pulls ahead once the prompt asks for a [label count](#qwen3-vl-labels), so pick Qwen 3.5 for a light, low-cost setup and Qwen3-VL when subject coverage matters most. Note the [`2b` and `9b` tiers](https://ollama.com/library/qwen3.5/tags) both scored well below `4b` on labels — bigger is not better here.

A community variant, [`frob/qwen3.5-instruct:4b`](https://ollama.com/frob/qwen3.5-instruct), is a capable alternative that uses the same Options profile as `qwen3-vl:4b-instruct` (see [below](#qwen3-vl-labels)) and delivers similar latency. Measured head to head against the official [`qwen3.5:4b`](https://ollama.com/library/qwen3.5) on the same images, it tracks its base model closely — same family, size and quantization, with 7 of 16 label sets identical and the remaining differences cosmetic. Either is a reasonable choice; the official library model is the simpler one to keep up to date. As with any Qwen-family model, it requires the strict options and "AT MOST N labels" prompt shape — without them it will over-generate and truncate the JSON response.

Performance also depends on your hardware, and the ranking can change with it. Our figures come from a single NVIDIA RTX 4060, so treat them as a starting point rather than a verdict and try the candidates on your own machine. One reason the order shifts: what an image costs in prompt tokens varies more than fivefold between model families, so a machine that is slow to encode the image — no GPU, layers offloaded to system RAM, or a GPU without flash attention — penalizes a model with a heavy vision encoder such as Qwen3-VL far more than a light one such as Gemma 4, even where the two are close on a fast GPU.

If you generate both captions and labels, use the same model for both, so that Ollama doesn't need to swap models between requests.

!!! tldr ""
    Without GPU acceleration, Ollama models will be significantly slower, taking anywhere from 10 seconds to over a minute to complete. This may be acceptable if you only want to process a few pictures or are willing to wait.

!!! warning "Disable Reasoning for Thinking Models"
    Many current vision models — the Qwen3.5 family, `qwen3-vl:*`, `frob/qwen3.5-instruct:4b`, and others — are **thinking (reasoning) models**. With reasoning enabled, recent Ollama versions emit it into the result: captions begin with text such as *"The user wants a concise description of the provided image…"* and label JSON fails to parse. **Set `Service.Think: "false"`** for these models (as shown in the examples below) to turn reasoning off — on PhotoPrism [260601](https://github.com/photoprism/photoprism/releases/tag/260601-a7d098548) and earlier it is required to keep their reasoning out of captions and labels. Later releases disable Ollama reasoning by default, so there it is a safety net rather than a requirement; it stays harmless everywhere, which is why the examples always include it. Re-enable reasoning only intentionally with `Service.Think: "true"`.

!!! tip "For Qwen3-VL, Use an `-instruct` Tag as Well"
    `Service.Think: "false"` keeps reasoning **out of the output**. It does not stop a reasoning build from *generating* it, so most of the cost remains. Measured on `qwen3-vl:4b` with reasoning off: about 414 output tokens and 6.6 seconds for a twelve-word caption, where [`qwen3-vl:4b-instruct`](https://ollama.com/library/qwen3-vl/tags) produced a longer caption in about 1.2 seconds using 24 tokens. The reasoning build also returned 21% multi-word label names against 0% for the instruct build. Treat the flag as a correctness guard and the tag as the performance choice — they are two separate decisions.

    This applies to Qwen3-VL specifically. `qwen3.5:4b` needs no `-instruct` tag: on its plain tag it already answered in about a second using 21 output tokens, with under 2% multi-word label names. Gemma 4 is not a reasoning model and is unaffected either way.

## Language Support

For languages other than English, keep the base instructions in English and add the desired language (e.g., "Respond in German"). This method works for both caption and label prompts, and holds better than translating the instructions themselves.

!!! warning "Verify Labels and Captions Separately"
    A model can honor the requested language for **captions** and silently ignore it for **labels**. In our testing, `gemma4:e2b` returned correct Arabic and Hebrew captions while returning English labels on *every* request, German included — with no error and nothing in the log.

    Answering in the right script also does not mean answering correctly. One 4B model produced fluent Hebrew that named the wrong subject, captioning a photo of an elephant as "the lion crushes the birds".

    So check both model types, and check the **content** rather than just the alphabet. Generate a handful of pictures with `photoprism vision run -m labels --count 1 --force` and `-m caption`, and read the results.

Support varies widely by model and does not follow size or general quality. Hosted models handled German, Arabic, and Hebrew far better than any self-hosted model we measured that fits in 8 GB of VRAM. Of the self-hosted options, Gemma 4 was the weakest for non-English **labels**, despite being our recommended English default — so a non-English library is one of the cases where it is worth testing [Qwen3-VL](#qwen3-vl-labels) or a [cloud model](ollama-cloud.md) instead.

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

For other languages, keep the base instructions in English and add the desired language (e.g., "Respond in German"), then verify the result as described under [Language Support](#language-support).

!!! tldr ""
    When tuning prompts, keep them as short as possible. Overly long prompts can increase hallucinations and latency.

## Configuration Examples

The following drop-in examples can be specified in your `vision.yml` file, which is located in the config directory (default: `storage/config`). [Learn more ›](index.md#visionyml-reference).

!!! tldr "How Many Labels to Expect"
    Self-hosted models under-generate when the prompt does not state a count. In our benchmark, models that fit in 8 GB of VRAM returned one to four labels per image with the built-in prompt, where hosted models volunteered seven to twelve. If you want more, ask for a count explicitly — see the [Qwen3-VL label example](#qwen3-vl-labels) below.

### Gemma 4: Labels

```yaml
Models:
- Type: labels
  Model: gemma4:latest
  Engine: ollama
  Run: auto
  Service:
    Uri: http://ollama:11434/api/generate
    Think: "false"
```

Why this works:

- **Engine:** Applies suitable **Resolution**, **Format**, **Prompt** and **Options** defaults (720 px thumbnails, JSON prompts for labels). Specifying a custom prompt is not required.
- **Run:** `auto` allows manual, after indexing, and scheduled runs ￫ [Run Modes](index.md#run-modes).
- **Model:** `gemma4:latest` currently aliases `gemma4:e4b` and returned about three labels per photo with graded topicality in our benchmark, with the best subject coverage of the two variants. Switch to `gemma4:e2b` if you prefer speed and a slightly larger label set — it averaged four to five labels per photo at marginally lower coverage.

### Gemma 4: Caption

```yaml
Models:
- Type: caption
  Model: gemma4:latest
  Engine: ollama
  Run: auto
  Prompt: >
    Create a caption with exactly one sentence in the active voice that
    describes the main visual content. Begin with the main subject and
    clear action. Avoid text formatting, meta-language, and filler words.
  Service:
    Uri: http://ollama:11434/api/generate
    Think: "false"
```

Why this works:

- **Engine:** Uses 720 px thumbnails and applies suitable **Format**, **Prompt** and **Options** defaults. Specifying a [custom prompt](#caption-prompts) is not required, but possible.
- **Run:** `auto` allows manual, after indexing, and scheduled runs ￫ [Run Modes](index.md#run-modes).
- **Prompt:** Uses the built-in [default prompt](#caption-prompts). For other languages, see [Language Support](#language-support).

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
    Think: "false"
```

Why this works:

- **Model:** [`qwen3-vl:4b-instruct`](https://ollama.com/library/qwen3-vl/tags) is a lightweight version of Qwen3-VL. You can alternatively try [`frob/qwen3.5-instruct:4b`](https://ollama.com/frob/qwen3.5-instruct) (a community variant that uses the same options profile and measured very close to the official `qwen3.5:4b`), [`huihui_ai/qwen3-vl-abliterated:4b-instruct`](https://ollama.com/huihui_ai/qwen3-vl-abliterated), [`qwen3-vl:latest`](https://ollama.com/library/qwen3-vl), or other [variants](https://ollama.com/search?c=vision&q=qwen3-vl).
- **Engine:** Applies suitable **Resolution**, **Format**, and **Options** defaults.
- **Run:** `on-demand` allows manual, metadata worker, and scheduled jobs ￫ [Run Modes](index.md#run-modes).
- **Prompt:** Ensures low latency, prevents repetition, and controls the type and number of labels returned. For other languages, see [Language Support](#language-support).
- **`Return AT MOST 3 labels`:** A deliberate cap, and the reason the strict options do not run away. It is also restrictive: in our benchmark `qwen3-vl:4b-instruct` returned about three labels per image under this prompt, rising to about ten when asked for a range of 8-15, with subject coverage going from 75% to 97%. If you want richer labels, raise the cap — and expect roughly two to three times the latency.
- **`single-word noun in canonical singular form`:** Keep this instruction in any custom prompt. PhotoPrism currently reduces a multi-word label to a single token and usually keeps the wrong one — `ferris wheel` is stored as *Ferris*, `amusement park` as *Park* ([photoprism#5773](https://github.com/photoprism/photoprism/issues/5773)).
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
    Think: "false"
```

Why this works:

- **Model:** Using [`qwen3-vl:4b-instruct`](https://ollama.com/library/qwen3-vl/tags) for both labels and captions avoids time-consuming Ollama model swaps. You can alternatively try [`frob/qwen3.5-instruct:4b`](https://ollama.com/frob/qwen3.5-instruct) (a community variant that uses the same options profile and measured very close to the official `qwen3.5:4b`), [`huihui_ai/qwen3-vl-abliterated:4b-instruct`](https://ollama.com/huihui_ai/qwen3-vl-abliterated), [`qwen3-vl:latest`](https://ollama.com/library/qwen3-vl), or other [variants](https://ollama.com/search?c=vision&q=qwen3-vl).
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
