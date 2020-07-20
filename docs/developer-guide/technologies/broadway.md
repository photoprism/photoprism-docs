[Broadway](https://developer.gnome.org/gtk3/stable/gtk-broadway.html) is a display server for using [GTK+](https://www.gtk.org/) applications in a web browser like Chrome or Firefox. It is based on HTML5 and [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API). GTK (originally GIMP Toolkit) is a GUI toolkit used by many Linux desktop applications like [Darktable](https://www.darktable.org/), [Gimp](https://www.gimp.org/) and [RawTherapee](https://rawtherapee.com/). Obviously this technology is ideal for editing images in the browser, at least when the connection is fast enough.

## Docker Configuration ##

```Dockerfile
# Configure broadwayd (HTML5 display server)
RUN apt-get update && apt-get install libgtk-3-bin
ENV GDK_BACKEND broadway
ENV BROADWAY_DISPLAY :5
EXPOSE 8080
CMD broadwayd -p 8080 -a 0.0.0.0 :5
```

When this is configured, all you need to do is open http://localhost:8080 in a browser and start any GTK application in the same container (broadwayd must be running). It should be displayed instantly, otherwise the screen is white, but you shouldn't see an error.

## Screenshot ##

![Darktable in Chrome via Broadway](https://pbs.twimg.com/media/DrvRwPjX4AAnhR1.jpg:large)