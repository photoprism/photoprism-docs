# Offloading AI Tasks to a Central Vision API Service

When hosting multiple PhotoPrism instances, you can offload AI tasks (image classification, face detection, NSFW detection) to a central Vision API service. This significantly reduces memory requirements on client instances, as they no longer need to load TensorFlow models into memory.

!!! info ""
    For additional models and advanced features, see the dedicated [Vision Service](../../developer-guide/vision/service/index.md) instead.

## Step 1: Set Up the Vision API Server

Add these environment variables to the Vision API server's `docker-compose.yml`:

```yaml
services:
  photoprism:
    environment:
      # ... your existing configuration ...
      PHOTOPRISM_VISION_API: "true"
      PHOTOPRISM_DISABLE_FRONTEND: "true"
```

Start the server:

```bash
docker compose up -d
```

Generate an access token:

```bash
docker compose exec photoprism photoprism auth add --name=vision --scope=vision --expires=-1
```

Save the generated access token for client configuration.

## Step 2: Configure Client Instances

Add these environment variables to each client instance's `docker-compose.yml`:

```yaml
services:
  photoprism:
    environment:
      # ... your existing configuration ...
      PHOTOPRISM_VISION_URI: "https://host.name/api/v1/vision"
      PHOTOPRISM_VISION_KEY: "your-access-token"
```

Replace `host.name` with your Vision API server's hostname or IP address, and `your-access-token` with your generated access token.

Restart the client instances:

```bash
docker compose stop
docker compose up -d
```

## Related Documentation

- [Config Options: Computer Vision](../config-options.md#computer-vision)
- [Advanced Vision Service](../../developer-guide/vision/service/index.md)
- [Computer Vision Commands](../../developer-guide/vision/cli.md)
