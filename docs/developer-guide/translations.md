# Translations

!!! attention ""
    Note: Please don't use the method described here to add/edit translations anymore use [this](./translations-weblate.md) instead!

PhotoPrism uses [gettext](https://en.wikipedia.org/wiki/Gettext) for frontend and backend localization.
It is one of the most widely used standards for user interface translation:

- Human-readable messages such as `File not found` are used as identifiers to search for appropriate translations. They also serve as default values when no translation is available.
- Messages can optionally contain placeholders for numbers and other variables, for example `Found %{n} files`.

We recommend [Poedit](https://poedit.net/download) for creating and updating translations. The download is free
for Mac, Windows and Linux. The source code can be obtained on [GitHub](https://github.com/vslavik/poedit).

!!! example ""
    **If translations are missing, we pre-translate messages using services such as DeepL and Google Translate.** This can lead to grammatical errors and misunderstandings. Native speakers should check existing translations and improve them if necessary. You can use the version compare feature on GitHub to detect changes in translation files.

## Frontend ##

Localizations can be found in `/frontend/src/locales`. The POT file, only containing message ids, 
is `translations.pot`.

`*.po` files contain localized messages for each 
[language](https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html)
identified by their [locale](https://www.gnu.org/software/gettext/manual/html_node/Locale-Names.html), 
for example `de.po` for German and `pt_BR.po` for Brazilian Portuguese.
You can open, edit and save them with Poedit to update existing translations.

### Add new translation ###
- In /frontend run `npm run gettext-extract`
- Install a translation tool e.g. Poedit
- Open the `/frontend/src/locales/translations.pot` file with Poedit
- In Poedit click on "Create New Translation" at the bottom and select the language
- Now you can start translating
- When done, save your translation as `*.po` file using the language locale (e.g. `de.po`) as name
- Add the new language to the `Languages` function in  `/frontend/src/options/options.js`
- Run `npm run gettext-compile` to compile existing translations into a single `translations.json` file
- To test your translations you need to build the frontend again using `npm run build` or `npm run watch`


### Update existing translation ###
- In /frontend run `npm run gettext-extract`
- Install a translation tool e.g. Poedit
- Open the `*.po` file of your language e.g. `/frontend/src/locales/fr.po` file with Poedit
- In the Poedit menu click "Catalogue" --> "Update from POT File" --> select the `translations.pot` file from `/frontend/src/locales`
- Now you can start proofreading and adding the missing translations
- Once your done save the changes in the `*.po` file
- Run `npm run gettext-compile` to compile existing translations into a single `translations.json` file
- To test your translations you need to build the frontend again using `npm run build` or `npm run watch`

!!! example ""
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
[language](https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html)
identified by their [locale](https://www.gnu.org/software/gettext/manual/html_node/Locale-Names.html), 
for example `de/default.po` for German and `pt_BR/default.po` for Brazilian Portuguese. 
You can open, edit and save them with Poedit. Please also add and commit binary `*.mo` files, 
which will be automatically created by Poedit.


### Add new translation ###
- Run `make generate` to update `/assets/locales/messages.pot`
- Open the `/assets/locales/messages.pot` file with Poedit
- In Poedit click on "Create New Translation" at the bottom and select the language
- Now you can start translating
- When done, create a new directory (using the locale as name) and save your translation there as `default.po`

### Update existing translation ###
- Run `make generate` to update `/assets/locales/messages.pot`
- Open the `/assets/locales/fr/default.po` file with Poedit
- In the Poedit menu click "Catalogue" --> "Update from POT File" --> select the messages.pot file from /assets/locales/
- Now you can start proofreading and adding the missing translations
- Once you're done, save the changes in the default.po file

!!! example ""
    This will only work when you have gettext installed on your system. We recommend using our latest development
    image as described in the [setup instructions](setup.md).


