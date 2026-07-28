# Translation Guide for Authors

## Overview

This template supports translating add-ons with Crowdin.

## Crowdin Project Setup

You need a Crowdin account and an API token with permissions to manage a project.
If you wish to use the community project [Crowdin project to translate NVDA add-ons](https://crowdin.com/project/nvdaaddons):

* **Request Access:** Send a message to the [NVDA translation mailing list](https://groups.io/g/nvda-translations) (**nvda-translations@groups.io**), or in the [NVDA Add-ons Mailing List](https://groups.io/g/nvda-addons) (**nvda-addons@groups.io**), requesting an invitation to join the project as a developer.
* **API Token:** Once invited, generate an API token in your Crowdin account settings.

## GitHub Secrets and Variables

To allow the workflows to communicate with Crowdin, you must add the following secret to your GitHub repository (`Settings > Secrets and variables > Actions`):

* `CROWDIN_TOKEN`: Paste your Crowdin API token here.

Optionally, if you don't want to use the [Crowdin community project](https://crowdin.com/project/nvdaaddons), you can create repository variables from **Settings > Secrets and variables > Actions > Variables** by selecting the **Variables** tab and clicking **New repository variable**.

The following repository variables are supported:

* `CROWDIN_PROJECT_ID`: Paste the project ID of your Crowdin project.
* `L10N_UTIL_CONFIG`: The path to the YAML file containing the configuration for `l10nUtil.exe`, used by the translation scripts.
For more details, visit the [nvdaL10n repository](https://github.com/nvaccess/nvdaL10n).
* `MIN_PERCENTAGE_TRANSLATED`: Defines the minimum translation completion percentage required before a translated file is synchronized back to the repository.
The value must be between `0` and `100`.

Examples for `MIN_PERCENTAGE_TRANSLATED`:

* `50`: Import files that are at least 50% translated.
* `75`: Import files that are at least 75% translated.
* `100`: Import only fully translated files.

If `MIN_PERCENTAGE_TRANSLATED` is not defined, the workflow uses a default value of `50`.

## Infrastructure

Ensure that your repository includes the following files (provided in this template):

* **Workflows:** `.github/workflows/crowdinL10n.yml`
* **Scripts:** The `.github/scripts/` folder containing `checkTranslation.py`, `languageMappings.json`, `setOutputs.py`, and `crowdinSync.ps1`.

Documentation synchronization relies on the XLIFF support built into `l10nUtil.exe`.

The `md2xliff` command is used to generate the source XLIFF file from the English `readme.md` documentation file.
Translated XLIFF files downloaded from Crowdin are then converted back to Markdown documentation using `l10nUtil.exe xliff2md`.

## Running the Workflow

The translation workflow will be run weekly.
Also, you can run the workflow manually from GitHub or using GitHub CLI.

If you manage several add-ons, consider using different cron schedules for each repository.
Although the workflow includes a random startup delay to reduce collisions, concurrent Crowdin synchronization jobs may still occur.

Documentation and interface translations are synchronized only when their translation percentage reaches the configured `MIN_PERCENTAGE_TRANSLATED` threshold.

This validation mechanism is applied consistently to both `.po` and `.xliff` translation files.
