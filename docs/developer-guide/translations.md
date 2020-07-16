# Translations

PhotoPrism uses [gettext](https://en.wikipedia.org/wiki/Gettext) for localizing frontend and backend.
It's one most widely adopted standards for translating user interfaces.
 
Human readable messages like `File not found` are used as ids for finding matching translations, 
and used as defaults whenever there is no translation available.

Messages may optionally contain placeholders, like `Found %{n} files`, for numbers and 
other variables.

We strongly recommend [Poedit](https://poedit.net/download) for creating and updating translations.
Download is free for Mac, Windows and Linux.
It's source code can be obtained on [GitHub](https://github.com/vslavik/poedit).

## Frontend ##

Localizations can be found in `/frontend/src/locales`. The POT file, only containing message ids, 
is `translations.pot`.

`*.po` files contain localized messages for each 
[language](https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html#Usual-Language-Codes),
identified by their [two-letter locale](https://www.gnu.org/software/gettext/manual/html_node/Locale-Names.html), 
like `de.po` for German.
You can open, edit and save them with Poedit to update existing translations. 

As it doesn't seem necessary for our use case, and to reduce the amount of work, 
we don't maintain translations for dialects like `de_AT` or `pt_BR`.

To add a new translation, open `translations.pot`, click on "Create New Translation" at the bottom, select
the language, and start translating. 
When done, save the result as `*.po` file using the language locale as name.

If you have a working development environment in place:

Running `npm run gettext-compile` in the `frontend` directory compiles existing translations into 
a single `translations.json` file.

Now start a frontend build using `npm run build` or keep 

```
npm run watch
```

running in the background to automatically recompile JS and CSS whenever there
are changes. Lastly, make sure `photoprism` is running and open the Web UI in a supported browser. Changing 
language in Settings automatically triggers a reload.

To extract new or changed text needing translation from `*.js` and `*.vue` source, run 
```
npm run gettext-extract
```
in `/frontend`. This updates the POT file `translations.pot`.

Apply changes to existing translations by clicking on "Catalogue" > "Update from POT File..." 
in the Poedit app menu.

!!! note
    A binary `*.mo` (machine object) file will be automatically saved along with every `*.po` file. 
    You won't be able to open those in a text editor, but please include them in git commits or when sending
    translations via email. The compiled `translations.json` file is not required for pull requests 
    and often causes merge conflicts.
    
## Backend ##

Only asynchronous notifications and certain API responses need translation to provide a 
consistent user experience.
Technical log messages should be in English to avoid ambiguities and (even slightly) wrong translations. 

Localizations are kept in `/assets/locales`. The POT file, only containing message ids, is `messages.pot`.

`default.po` files in sub directories contain localized messages for each 
[language](https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html#Usual-Language-Codes),
identified by their [two-letter locale](https://www.gnu.org/software/gettext/manual/html_node/Locale-Names.html), 
like `de/default.po` for German. You can open, edit and save them with Poedit. Please
also commit and push binary `*.mo` files, which will be automatically created by Poedit.

To add a new translation, open `messages.pot`, click on "Create New Translation" at the bottom, select
the language, and start translating. 
When done, add a new directory for the language and save your translation as `default.po`,
just like existing examples.

The POT file `/assets/locales/messages.pot` will be automatically updated when 
running `go generate` in `/internal/i18n` or `make generate` in the main project directory.
Note that this will only work when you have gettext installed on your system.
We recommand using our latest development image as described in the developer guide.

Apply changes to existing translations by clicking on "Catalogue" > "Update from POT File..." 
in the Poedit app menu.

