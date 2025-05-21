# fSpy Blender Addon - Next Generation

## What's This?

This is a fork of official [fSpy](https://fspy.io) importer addon of [Blender](https://blender.org).

<!--
This is the official [fSpy](https://fspy.io) importer add-on for .

There are two images below show an fSpy project (top) and a matching Blender camera created by the importer (bottom).

![An example fSpy project](readme_images/help_fspy.jpg)

![A matching Blender camera](readme_images/help_blender.jpg)
-->

## Differences with Official One

This repository is still work in progress.

The official fSpy plugin looks like it hasn't been updated in a long time (although all features are functional, there could have been no updates). It's still working but not good with contemporary Blender. So I create this fork to make it have "at least" compatibility with latest LTS Blender.

I don't want to take any place of official fSpy Blender addon, so I add a `NG` suffix meaning "next generation".

<!--
# Getting started

## 1. Download the add-on

[Download the latest version](https://github.com/stuffmatic/fSpy-Blender/releases/latest) (make sure you download the file called `fSpy-Blender-x.y.z.zip`).

### ⚠️ __Important note for mac users__ ⚠️

If you're using Safari, make sure you __download the add-on by right clicking and choosing "Download Linked File"__. This prevents the downloaded file from getting unzipped automatically.

## 2. Install the add-on

Open the preferences window by selecting Preferences from the Edit menu

![Edit -> Preferences](readme_images/help_edit_preferences.png)

Select the _Add-ons_ tab and press the _Install_ button

![Install add-on](readme_images/help_addons_install.png)

Select the downloaded zip-file and press _Install Add-on from file_

![Select the zip file](readme_images/help_select_zip.png)

Locate the fSpy importer in the add-on list and enable it by pressing the checkbox.

![Enable add-on](readme_images/help_enable_addon.png)

## 3. Import an fSpy project file

Once the add-on is installed and activated, fSpy project files can be imported by selecting _fSpy_ from the _Import_ menu. This will create a camera with the same name as the imported project file.

![Import menu](readme_images/help_import_menu.png)

### Import settings

At the bottom left in the importer's file browser, there is a panel with import settings.

![Import settings](readme_images/help_import_settings.png)

__Update existing import (if any)__ - If checked, any previously created camera with a name matching the project filename will be updated. If unchecked, a new camera will be created on each import. 

__Import background image__ - If checked, the image from the fSpy project file will be used as the background image for the Blender camera.
-->

## Lifetime Principle

This addon has entirely different support strategy with official fSpy Blender addon.

This plugin only supports Blender LTS version. I will only update this plugin once Blender release next LTS version, except there are some fatal issues in addon. Because this is a tiny addon and I do not have so much time on it. However, all version adaption PRs are welcomed.

Once a new LTS version is released for Blender, the old version is no longer supported. All new features and bug fixes (including those that are fatal) will only be accessible in the new Blender LTS.

The obvious truth is that I can't serve this addon immortally. I'll try to keep updating this addon as long as I'm still using Blender. If that day comes, I will archive this repository to tell you explicitly.

## How to Test?

Navigate to the root of this repository, and execute `python3 test/test.py` directly.

## How to Pack Release?

Navigate to the root of this repository, then enter `fspy_blender_ng` directory, open command line prompt and execute `blender --command extension build` directly. You will find `fspy_blender_ng-x.x.x.zip` in your work directory. That's the final release package.
