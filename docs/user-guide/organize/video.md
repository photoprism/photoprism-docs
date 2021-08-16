### Videos ###
Videos with the MPEG-4 AVC format can be played natively by most modern browsers.
PhotoPrism uses [*ffmpeg*](https://www.ffmpeg.org/documentation.html) to transcode
other common video formats to [MPEG-4 AVC](https://en.wikipedia.org/wiki/MPEG-4).
All video formats, that can be transcoded by ffmpeg are supported.

!!! info
    In case you have problems with a specific format, let us know!

!!! info
    By default PhotoPrism transcodes videos, when they are first played. This may lead to long loading times for very long or high resolution videos.
    You can use `docker-compose exec photoprism photoprism convert` to convert videos upfront.

In *Videos* you find all your videos. To play a video click :material-play:.

![Screenshot](img/video-1.png)

To play videos in fullscreen mode click :material-play: on the video or :material-movie: next to the videos title.

![Screenshot](img/video.png)

### Live photos ###
Live photos are treated as photos.
They are marked with :material-adjust: in the upper left corner.

You can filter for them using `type:live`.

![Screenshot](img/live-photo.png)

To play a live photo just hover over it.
