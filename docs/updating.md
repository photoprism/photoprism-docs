# Updating

Open a terminal, go to the directory in which you saved the `docker-compose.yml` file and run the following commands to update your version to the latest development snapshot:

```bash
docker-compose down
docker-compose pull photoprism
docker-compose up -d
```

Pulling a new version can take several minutes, depending on your internet connection. The final release will be smaller.
