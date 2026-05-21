# Custom TensorFlow Models 

As an alternative to the [built-in model](index.md), PhotoPrism lets you configure more powerful custom TensorFlow models for image classification.
## Step 1: Mount model folder
In your compose.yaml file add a volume mount for a model folder.

!!! example "compose.yaml"
    ```yaml
    services:
      photoprism:
        ...
        volumes:
          - "./models/modelname:/opt/photoprism/assets/models/modelname"
          ...
    ```

## Step 2: Download model and labels.txt
Download a suitable TensorFlow model and the [labels.txt](https://dl.photoprism.app/tensorflow/models/labels.txt) to your configured model folder.

It should now contain the following:

- saved_model.pb
- a variables/ subfolder with variables.index and variables.data-*
- labels.txt

!!! note ""
    PhotoPrism supports TensorFlow 2 image classification models in the *SavedModel* format.

### Example Models

- [vision-transformer-tensorflow2-vit-b16-classification-v1](https://www.kaggle.com/models/spsayakpaul/vision-transformer)
- [inception-v3-tensorflow2-classification-v2](https://www.kaggle.com/models/google/inception-v3)

In our tests, the Vision Transformer model achieved the best accuracy. Inception V3 was faster and may be better suited to low-power devices; it produced more labels and had a higher error rate, but still outperformed the built-in NASNet model.

## Step 3: Configure PhotoPrism

Now, create a new `vision.yml` file in your config path (default: `storage/config`) or edit the existing file in [the *storage/config* folder](../../../getting-started/docker-compose.md#photoprismstorage) of your PhotoPrism instance, following the example below. Its absolute path from inside the container is `/photoprism/storage/config/vision.yml`:

!!! info ""
    If PhotoPrism can’t read your config file, make sure the file exists at the config path configured for your instance. Older installations may use `storage/settings`.

    Run `docker compose exec photoprism photoprism show config | grep config-path` to find out what's your configured config path.


!!! example "vision.yml"
    ```yaml
    Models:
    - Type: labels
      Model: "name:version"
      Resolution: 224
      TensorFlow:
        Output:
          Logits: true
    ```

!!! note ""
    The config file must be named `vision.yml`, not `vision.yaml`, as otherwise it won't be found and will have no effect.

## Step 4: Restart PhotoPrism

Run the following commands to restart `photoprism` and apply the new settings:

```bash
docker compose stop photoprism
docker compose up -d
```

On indexing the configured model will now be used to generate labels. Alternatively you can run the `photoprism vision run` [CLI command](../cli.md#run-vision-models) to generate labels. 

!!! note ""
    Labels produced by TensorFlow models always have the source "image"; customizing the label source is not supported yet.