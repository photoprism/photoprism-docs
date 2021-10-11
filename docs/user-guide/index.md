# User Guide #

Step-by-step installation instructions for our self-hosted community edition can be found
in [Getting Started](../getting-started/index.md). All you need to have installed on your
system is a Web browser and [Docker](https://store.docker.com/search?type=edition&offering=community).
It is available for Mac, Linux, and Windows.

When setup is complete, you can start [indexing your pictures](library/index.md).
Be patient, this may take a while depending on your server hardware and how many files you have.

Your [photos](organize/browse.md) and [videos](organize/video.md) will successively become visible 
in search results and other parts of the user interface. The counts in the navigation are constantly 
updated, so you can follow the progress.

In case some of your pictures are still missing after indexing has been completed,
they might be in [Review](organize/review.md) due to low quality or incomplete metadata.
You can turn this and other features off in [Settings](settings/general.md), depending on
your specific use case.

!!! note ""
    Our [stable version](../release-notes.md) and development preview now come as a single
    [multi-arch image](https://hub.docker.com/r/photoprism/photoprism) for **AMD64, ARM64, and ARMv7**.
    That means you don't need to pull from different Docker repositories anymore. We recommend updating your existing
    `docker-compose.yml` config based on [our examples](https://dl.photoprism.org/docker/).

!!! example ""
    **This open-source project is made possible [thanks to our sponsors](https://github.com/photoprism/photoprism/blob/develop/SPONSORS.md).**
    If you enjoy using PhotoPrism, please consider backing us on [Patreon](https://www.patreon.com/photoprism)
    or [GitHub Sponsors](https://github.com/sponsors/photoprism).
    Your continued support helps us fund operating costs, provide services like satellite maps,
    and develop new features. Thank you very much! 💜