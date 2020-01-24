# Testing PhotoPrism with our demo image

For a quick test, you can start a demo that comes with pre-indexed photos:

```
docker run -p 2342:2342 -d --name demo photoprism/demo
```

After running the command, open http://localhost:2342/ in a Web browser.
It may take a few seconds to become available.

To stop and remove the container:

```
docker rm -f demo
```

It's the same image we use for [demo.photoprism.org](https://demo.photoprism.org/).
