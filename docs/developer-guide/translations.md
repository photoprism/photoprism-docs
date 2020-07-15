# Translations

PhotoPrism uses [gettext](https://en.wikipedia.org/wiki/Gettext) for localizing frontend and backend.
It's around since the 90s and probably the most widely adopted standard for translating user interfaces.
 
A human readable, English string like `File not found` is used as message id ("msgid") for 
finding a matching translation ("msgstr"), and used as default whenever there is no translation for 
the current locale.

Messages may optionally contain placeholders for dynamically inserted numbers or names,
e.g. `Found %{n} files`.

For creating and maintaining translation files, we strongly recommend [Poedit](https://poedit.net/download).
Download is free for Mac, Windows and Linux. It's source code can be obtained on [GitHub](https://github.com/vslavik/poedit),
they probably also wouldn't mind getting some more stars.

## Frontend ##

All files required for localization can be found in `frontend/src/locales/`. The main file, containing only untranslated
default messages, is `translations.pot`.

Individual `*.po` files contain the localized message strings for each language, e.g. `de.po` for German.
You can open, edit and save them with Poedit to update existing translations. 

To add a new translation, open `translations.pot`, click on "Create New Translation" at the bottom, select
the language, and start translating by going down the list. 
When done, save the translation in the same directory using the language locale as file name.

If you have a working development environment in place:

Run `npm run gettext-compile` in the `frontend/` directory after saving the `*.po` file with Poedit.
This will create a json file containing all existing translations. Then build the frontend using
`npm run build` or keep 

```
npm run watch
```

running in the background to automatically recompile JS and CSS whenever there
are changes. Lastly, make sure `photoprism` is running and open the Web UI in a supported browser. Changing the
language in Settings automatically triggers a reload.

To extract new or changed text needing translation from `*.js` and `*.vue` source, run 
```
npm run gettext-extract
```
in the `frontend/` directory. This will update the POT file `translations.pot`. You can now update the 
list of message ids in existing translations by clicking on "Catalogue" > "Update from POT File..." 
in the Poedit app menu.

!!! note
    A binary `*.mo` ("machine object") file will be automatically saved along with every `*.po` file. 
    You won't be able to open those in a text editor, but please include them in git commits or when sending
    translations via email. The compiled `translations.json` file is not required in pull requests though 
    and often causes merge conflicts.
    
## Backend ##

Backend translations were added more recently. Technical log messages should always be in English to 
avoid ambiguities and (even slightly) wrong translations. Only asynchronous confirmation messages and 
certain API responses need to be translated to provide a consistent user experience.

Files required for localization can be found in `assets/locales/`. The main file, containing only untranslated
default messages, is `messages.pot`.

Individual `default.po` files in sub directories contain the localized message strings for each language, e.g. 
`de/default.po` for German. You can open, edit and save them with Poedit to update existing translations. Please
also commit and push the automatically created, binary `*.mo` files.

To add a new translation, open `messages.pot`, click on "Create New Translation" at the bottom, select
the language, and start translating by going down the list. 
When done, create a directory for the new language and save the translation as `default.po`,
just like the existing examples.

The POT file `assets/locales/messages.pot` will be automatically updated when 
running `go generate` in `internal/i18n/` or `make generate` in the main project directory.
Note that this will only work when there is gettext installed like it is the case
in our development Docker image.
You can then update the list of message ids in existing translations by clicking on 
"Catalogue" > "Update from POT File..." in the Poedit app menu.
