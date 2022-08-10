Open a terminal and type `photoprism start` to start the built-in server. It will listen on [localhost:2342](http://localhost:2342/) by default, see [docker-compose.yml](https://github.com/photoprism/photoprism/blob/develop/docker-compose.yml) and [Configuration](../configuration.md).

## Frameworks ##

[Vuetify](https://vuetifyjs.com/en/getting-started/quick-start) is a powerful open-source [Material Design](https://material.io/) UI component framework for building modern single-page applications.

It is based on [VueJS](https://vuejs.org/v2/guide/), a JavaScript library that combines the best ideas from [AngularJS](https://angularjs.org/) (Google) and [React](https://reactjs.org/) (Facebook); development is community driven and the API fairly stable.

Vuetify and VueJS are initialized in [frontend/src/app.js](https://github.com/photoprism/photoprism/blob/develop/frontend/src/app.js). [Webpack](https://webpack.js.org/concepts/) is used as a module loader / bundler. It creates single, optimized JS and CSS files in the server assets public build directory from the original source code. You can find the build configuration in `frontend/webpack.config.js`.

For our docs and landing pages, we may use https://materializecss.com/ as a lightweight alternative to Vuetify.

## Components ##

Components are reusable user-interface widgets. [UI Components](components.md) contains a list of custom components. Standard components like [buttons](https://vuetifyjs.com/en/components/buttons) or [forms](https://vuetifyjs.com/en/components/forms) are well documented on [vuetifyjs.com](https://vuetifyjs.com/en/getting-started/quick-start).

## Dependencies ##

The full list of dependencies can be found in `frontend/package.json`. You need to run `npm install` in the **frontend directory** to install them (automatically happens during installation, see `Makefile`). Run `npm install -P [package name]` to add a new package (library or framework).

## Building ##

A build can be triggered by running `npm run watch` (watches for changes and re-builds when needed) or `npm run build` (single build) in the **frontend directory**. [NPM](https://www.npmjs.com/) is the default package manager that comes with [NodeJS](https://nodejs.org/en/docs/guides/), a JavaScript run-time environment that executes JavaScript code outside of a browser.

## External Resources ##
- https://web.dev/progressive-web-apps/
- https://github.com/vuejs-templates/pwa - a progressive web app template for VueJS
- https://hackernoon.com/a-progressive-web-app-in-vue-tutorial-part-1-the-vue-app-f9231b032a0b
- https://medium.com/the-web-tub/creating-your-first-vue-js-pwa-project-22f7c552fb34
- https://developers.google.com/web/fundamentals/native-hardware/fullscreen/
- https://webpack.js.org/configuration/optimization/
- https://photoswipe.com/documentation/responsive-images.html
- https://seregpie.github.io/VueWordCloud/ - Word cloud for VueJS
- https://github.com/snorpey/jpg-glitch - JPEG Glitch lib for JS
- https://stylable.io/ - scopes styles to components so they don’t “leak” and clash with other styles (not sure if this is of any use for us)
- [Building the Google Photos Web UI](https://medium.com/google-design/google-photos-45b714dfbed1) - Antin Harasymiv on Medium
- [Progressive Image Grid](https://github.com/schlosser/pig.js) - arrange images in a responsive, progressive-loading grid managed in JavaScript, see [#85](https://github.com/photoprism/photoprism/issues/85)
