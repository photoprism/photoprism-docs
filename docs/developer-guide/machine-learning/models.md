# Additional Computer Vision Models

Our <https://github.com/photoprism/photoprism-vision> repository on GitHub contains supplementary computer vision models which can be accessed as [web services](#usage) by PhotoPrism and other applications. They provide a [REST API](#example-request) that accepts an image URL and returns, for example, a matching caption in response.

The currently [integrated models](#models), each with [its own endpoint](#api-endpoints), are *kosmos-2*, *blip-image-captioning large* and *vit-gpt2-image-captioning*.

!!! example ""
    Note that this has not been officially released yet and that further documentation will be added over time.

## Models

### Kosmos-2

Komsos-2 is the most accurate model of the three. It was developed by Microsoft, and this application uses the transformers implementation of the original model, as described in its [Huggingface](https://huggingface.co/microsoft/kosmos-2-patch14-224). This model was released in June 2023, and offers object detection and spatial reasoning. Kosmos-2 has very accurate accurate image captions (a .04-.1 increase in clip score when compared to the other two models offered), and is the default model used.

### VIT-GPT2

This model was released by [nlpconnect](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning). This model combined VIT and GPT-2 to create a multi-modal image captioning model. I have found this to be the least performing of the three, but your mileage may vary.

### BLIP

This model was released by [Salesforce](https://huggingface.co/Salesforce/blip-image-captioning-large) in 2022. The primary purpose for this model was to increase both image understanding and text generation using novel techniques. It has achieved a +2.8% CIDEr result, and I've found this model to be more performant than VIT-GPT2, but Kosmos-2 to be slightly better (a .4 increase in CLIP score).

## Dependencies

### Flask

[Flask](https://flask.palletsprojects.com/en/3.0.x/) is the framework that is used for the API. It allows for API creation with Python, which is key for this application as it utilizes ML.

### PyTorch

[PyTorch](https://pytorch.org/) is key for working with the ML models to generate the outputs. It also enables GPU processing, speeding up the image processing with the models. PyTorch primarily creates and handles tensors, which are crucial for the function of the models.

### Transformers

[Transformers](https://huggingface.co/docs/transformers/en/index) is used for downloading and loading the models. In addition to this it is used in the image processing with the models.

### Pillow

[Pillow](https://pypi.org/project/pillow/) is used to take the supplied URl and convert it into the format needed to input into the models.

### Hardware Acceleration Libraries

[Numpy](https://numpy.org/) could be used for further hardware acceleration. It isn't included in the application by default to save space and keep from installing unnecessary dependencies. Numpy can be configured to use the GPU for computations. PyTorch already enables GPU processing, so numpy may not make a signficant difference.

## Build Setup

Before installing the Python dependencies, please make sure that you have [Git](https://git-scm.com/downloads) and [Python 3.12+ (incl. pip)](https://www.python.org/downloads/) installed on your system, e.g. by running the following command on Ubuntu/Debian Linux:

```
sudo apt-get install -y git python3 python3-pip python3-venv python3-wheel
```

You can then install the required libraries in a virtual environment by either using the Makefiles we provide (i.e. run `make` in the main project directory or a subdirectory) or by manually running the following commands in a service directory, for example:

```bash
git clone git@github.com:photoprism/photoprism-vision.git
cd photoprism-vision/describe
python3 -m venv ./venv
. ./venv/bin/activate
./venv/bin/pip install --disable-pip-version-check --upgrade pip
./venv/bin/pip install --disable-pip-version-check -r requirements.txt
```

## Usage

Run the Python file `app.py` in the `describe` subdirectory to start the *describe* service after you have installed [the dependencies](#build-setup) (more services, e.g. for OCR and tag generation, may follow):

```bash
./venv/bin/python app.py
```

The service then listens on port 5000 by default and its API endpoints for generating captions support both `GET` and `POST` requests. It can be tested with the `curl` command (`curl.exe` on Windows) as shown in the example below:

```bash
curl -v -H "Content-Type: application/json" \
  --data '{"url":"https://dl.photoprism.app/img/team/avatar.jpg"}' \
  -X POST http://localhost:5000/api/v1/vision/describe
```

At a minimum, a valid image `url` must be specified for this. In addition, a `model` name and an `id` [can be passed](#example-request) to allow asynchronous processing of requests (the same `id` is then returned with the response). If no `id` is passed, a random UUID v4 `id` is returned with [the response](#example-response).

If your client submits `POST` requests, the request body must be [JSON-encoded](https://www.json.org/), e.g.:

```json
{
    "url": "https://dl.photoprism.app/img/team/avatar.jpg",
    "id": "3487da77-246e-4b4c-9437-67507177bcd7"
}
```

Alternatively, you can perform `GET` requests with URL-encoded query parameters, which is easier to test without an HTTP client:

> http://localhost:5000/api/v1/vision/describe?url=https%3A%2F%2Fdl.photoprism.app%2Fimg%2Fteam%2Favatar.jpg&id=3487da77-246e-4b4c-9437-67507177bcd7

### API Endpoints

#### `/api/v1/vision/describe`

This is the default endpoint of the API. An image url should be passed in with the key "url", and optionally a "model" and/or "id" value can be passsed in. The "model" key allows the user to specify which of the three models they would like to use. If no model is given, the application will default to using the kosmos-2 model.

#### `/api/v1/vision/describe/kosmos-2/patch14-224`

This is the endpoint for the Kosmos-2 model. An image url should be passed in with the key "url", and optionally a "model" and/or "id" value can be passsed in.

#### `/api/v1/vision/describe/vit-gpt2-image-captioning`

This is the endpoint for the VIT GPT-2 model. An image url should be passed in with the key "url", and optionally an "id" value can be passsed in.

#### `/api/v1/vision/describe/blip-image-captioning-large`

This is the endpoint for the BLIP model. An image url should be passed in with the key "url", and an "id" value can be passsed in.

### Example Request

`POST /api/v1/vision/describe`

```json
{
    "url": "https://images.rawpixel.com/image_png_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTA5L3Jhd3BpeGVsX29mZmljZV8yOF9mZW1hbGVfbWluaW1hbF9yb2JvdF9mYWNlX29uX2RhcmtfYmFja2dyb3VuZF81ZDM3YjhlNy04MjRkLTQ0NWUtYjZjYy1hZmJkMDI3ZTE1NmYucG5n.png",
    "model": "kosmos-2",
    "id": "b0db2187-7a09-438c-8649-a9c6c0f7b8a1"
}
```

### Example Response

```json
{
    "id": "b0db2187-7a09-438c-8649-a9c6c0f7b8a1",
    "model": {
        "name": "kosmos-2",
        "version": "patch14-224"
    },
    "result": {
        "caption": "An image of a female robot with a transparent face and blue eyes, a head with a circuit board inside and a glowing blue light on a transparent background"
    }
}
```

## Code Structure

### Model Loading and Initialization

```python
MODEL_DIR = "models"
KOSMOS_MODEL_PATH = os.path.join(MODEL_DIR, "kosmos-2-patch14-224")
VIT_MODEL_PATH = os.path.join(MODEL_DIR, "vit-gpt2-image-captioning")
BLIP_MODEL_PATH = os.path.join(MODEL_DIR, "blip-image-captioning-large")
```

This code block creates the paths for the models. This will be useful when downloading/loading the models. It uses os.path to assemble the correct path depending on if the system is Windows-based or UNIX-based.

### Downloading Models

```python
def download_model(model_name, save_path):
    if not os.path.exists(save_path):
        print(f"Downloading {model_name}...")
        if model_name == "microsoft/kosmos-2-patch14-224":
            AutoModelForVision2Seq.from_pretrained(model_name).save_pretrained(save_path)
            AutoProcessor.from_pretrained(model_name).save_pretrained(save_path)
        elif model_name == "nlpconnect/vit-gpt2-image-captioning":
            VisionEncoderDecoderModel.from_pretrained(model_name).save_pretrained(save_path)
            ViTImageProcessor.from_pretrained(model_name).save_pretrained(save_path)
            AutoTokenizer.from_pretrained(model_name).save_pretrained(save_path)
        elif model_name == "Salesforce/blip-image-captioning-large":
            BlipForConditionalGeneration.from_pretrained(model_name).save_pretrained(save_path)
            BlipProcessor.from_pretrained(model_name).save_pretrained(save_path)
        print(f"{model_name} downloaded and saved to {save_path}")
    else:
        print(f"{model_name} already exists at {save_path}")
```

Here the code is checking if the models already exist or not. If they don't exist it is downloading them, if they do it is skipping the downloading.

```python
os.makedirs(MODEL_DIR, exist_ok=True)
download_model("microsoft/kosmos-2-patch14-224", KOSMOS_MODEL_PATH)
download_model("nlpconnect/vit-gpt2-image-captioning", VIT_MODEL_PATH)
download_model("Salesforce/blip-image-captioning-large", BLIP_MODEL_PATH)
```

Here the code is downloading the models by calling the function in the previous block.

### Loading Models

```python
print("Loading models...")
kosmosModel = AutoModelForVision2Seq.from_pretrained(KOSMOS_MODEL_PATH)
kosmosProcessor = AutoProcessor.from_pretrained(KOSMOS_MODEL_PATH)

vitModel = VisionEncoderDecoderModel.from_pretrained(VIT_MODEL_PATH)
vitFeature_extractor = ViTImageProcessor.from_pretrained(VIT_MODEL_PATH)
vitTokenizer = AutoTokenizer.from_pretrained(VIT_MODEL_PATH)

blipProcessor = BlipProcessor.from_pretrained(BLIP_MODEL_PATH)
blipModel = BlipForConditionalGeneration.from_pretrained(BLIP_MODEL_PATH)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vitModel.to(device)
```

Here the models are being loaded after they have been saved. 

### Services

```python
def kosmosGenerateResponse(url):
    try:
        image = Image.open(requests.get(url, stream=True).raw)
    except Exception as e:
        return "fetchError", f"Unable to fetch image: {str(e)}"

    prompt = "<grounding>An image of"

    try:
        inputs = kosmosProcessor(text=prompt, images=image, return_tensors="pt")
        generated_ids = kosmosModel.generate(
            pixel_values=inputs["pixel_values"],
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            image_embeds=None,
            image_embeds_position_mask=inputs["image_embeds_position_mask"],
            use_cache=True,
            max_new_tokens=128,
        )

        generated_text = kosmosProcessor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        processed_text, entities = kosmosProcessor.post_process_generation(generated_text)
    except Exception as e:
        return "processingError", f"Error during processing: {str(e)}"

    return "ok", processed_text

def vitGenerateResponse(url):
    vitModel.to(device)    

    max_length = 16
    num_beams = 4
    gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

    def predict_step(url):
        image = Image.open(requests.get(url, stream=True).raw)
        images = []

        if image.mode != "RGB":
            image = image.convert(mode="RGB")

        images.append(image)

        pixel_values = vitFeature_extractor(images=images, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)

        output_ids = vitModel.generate(pixel_values, **gen_kwargs)

        preds = vitTokenizer.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]
        return preds

    processed_text = predict_step(url)  # returns prediction

    return "ok", processed_text

def blipGenerateResponse(url):
    img_url = url
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

    inputs = blipProcessor(raw_image, return_tensors="pt")

    out = blipModel.generate(**inputs)
    processed_text = blipProcessor.decode(out[0], skip_special_tokens=True)

    return "ok", processed_text
```

These are the services to generate the captions. There is a function for each model.

## API Endpoints

### Default Endpoint

```python
@app.route('/api/v1/vision/describe', methods=['POST', 'GET'])
def generateResponse():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
    elif request.method == 'GET':
        data = request.args

    url = data.get('url')
    model = data.get('model')
    id = data.get('id')

    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    if model == "kosmos-2" or not model:
        status, result = kosmosGenerateResponse(url)
        if status == "fetchError":
            return jsonify({"error": result}), 500
        elif status == "processingError":
            return jsonify({"error": result}), 500
        elif status == "ok":
            if id:
                return jsonify({"id": id, "result": {"caption": result}, "model": {"name": "kosmos-2", "version": "patch14-224"}}), 200
            return jsonify({"id": uuid.uuid4(), "result": {"caption": result}, "model": {"name": "kosmos-2", "version": "patch14-224"}}), 200
    elif model == "vit-gpt2-image-captioning":
        status, result = vitGenerateResponse(url)
        if status == "ok":
            if id:
                return jsonify({"id": id, "result": {"caption": result}, "model": {"name": model, "version": "latest"}}), 200
            return jsonify({"id": uuid.uuid4(), "result": {"caption": result}, "model": {"name": model, "version": "latest"}}), 200
        return jsonify({"error": "Error during processing"})
    elif model == "blip-image-captioning-large":
        status, result = blipGenerateResponse(url)
        if status =='ok':
            if id:
                return jsonify({"id": id, "result": {"caption": result}, "model": {"name": model, "version": "latest"}}), 200
            return jsonify({"id": uuid.uuid4(), "result": {"caption": result}, "model": {"name": model, "version": "latest"}}), 200
        return jsonify({"error": "Error during processing"})
```

This is the default endpoint. It checks to see if a model is specified, and if it is it calls the service associated with that model and returns the respose with the data. If a model isn't specified it uses kosmos-2.

### Specific Endpoints

```python
@app.route('/api/v1/vision/describe/kosmos-2/patch14-224', methods=['POST', 'GET'])
def kosmosController():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
    elif request.method == 'GET':
        data = request.args

    url = data.get('url')
    id = data.get('id')

    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    status, result = kosmosGenerateResponse(url)

    if status == "fetchError":
        return jsonify({"error": result}), 500
    elif status == "processingError":
        return jsonify({"error": result}), 500
    elif status == "ok":
        if id:
            return jsonify({"id": id, "result": {"caption": result}, "model": {"name": "kosmos-2", "version": "patch14-224"}}), 200
        return jsonify({"id": uuid.uuid4(), "result": {"caption": result}, "model": {"name": "kosmos-2", "version": "patch14-224"}}), 200

    


@app.route('/api/v1/vision/describe/vit-gpt2-image-captioning', methods=['POST', 'GET'])
def vitController():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
    elif request.method == 'GET':
        data = request.args
    
    url = data.get('url')
    id = data.get('id')

    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    status, result = vitGenerateResponse(url)

    if status == "ok":
        if id:
            return jsonify({"id": id, "result": {"caption": result}, "model": {"name": "vit-gpt2-image-captioning", "version": "latest"}}), 200
        return jsonify({"id": uuid.uuid4(), "result": {"caption": result}, "model": {"name": "vit-gpt2-image-captioning", "version": "latest"}}), 200
    
    return jsonify({"error": "Error during processing"})



@app.route('/api/v1/vision/describe/blip-image-captioning-large', methods=['POST', 'GET'])
def blipController():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
    elif request.method == 'GET':
        data = request.args

    url = data.get('url')
    id = data.get('id')

    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    status, result = blipGenerateResponse(url)

    if status == "ok":
        if id:
            return jsonify({"id": id, "result": {"caption": result}, "model": {"name": "vit-gpt2-image-captioning", "version": "latest"}}), 200
        return jsonify({"id": uuid.uuid4(), "result": {"caption": result}, "model": {"name": "vit-gpt2-image-captioning", "version": "latest"}}), 200
    
    return jsonify({"error", "Error during processing"})

```

These are the endpoints for each model. They do some error handling, run the service, and return the response.

## Contributors

We would like to thank everyone involved, especially [Aatif Dawawala](https://github.com/Aatif-Dawawala) who got things rolling and contributed much of the initial code:

- [Aatif Dawawala](https://github.com/Aatif-Dawawala)
- [Niaz Faridani-Rad](https://github.com/derneuere)

[Learn more ›](https://github.com/photoprism/photoprism-vision/graphs/contributors)
 
## Submitting Pull Requests

Follow our [step-by-step guide](https://docs.photoprism.app/developer-guide/pull-requests) to learn how to submit new features, bug fixes, and documentation enhancements.

[Learn more ›](https://docs.photoprism.app/developer-guide/pull-requests)

## License and Disclaimer

The files in the <https://github.com/photoprism/photoprism-vision> repository are licensed under the [Apache License, Version 2.0](../../license/apache.md) (the “License”).

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

[Learn more ›](../../license/apache.md)