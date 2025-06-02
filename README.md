# fSpy Blender Addon - Next Generation

## Introduction

This is a **FORK** of [official fSpy importer addon for Blender](https://github.com/stuffmatic/fSpy-Blender).

## User Manual

### Install Addon

1. Download the latest stable version of this plugin in Release page of this repository.
1. Open the preferences window by selecting `Preferences` from the `Edit` menu in Blender.
1. Select the `Add-ons` tab and press the button with "V" icon at top-right corner. In expanded menu, click `Install from Disk...`.
1. In pop-up window, select your downloaded zip file, and click `Install from Disk` button.
1. Locate the `fSpy Importer` in the add-on list and enable it by pressing the checkbox.

> [!WARNING]  
> If you're using Safari, make sure you __download the add-on by right clicking and choosing "Download Linked File"__. This prevents the downloaded file from getting unzipped automatically.

### Addon Usage

#### Import Camera

Once the add-on is installed and activated, fSpy project files can be imported by selecting `fSpy (.fspy)` from the `File > Import` menu. This will create a camera with the same name as the imported project file.

When importing fSpy project file, there are some options listed hereinafter can be configured at the right side panel in import window.

* `Update Existing Import`: If checked, any previously created camera with a name matching the project filename will be updated. If unchecked, a new camera will be created on each import. 
* `Import Background Image`: If checked, the image from the fSpy project file will be used as the background image for the Blender camera.

#### Switch between Multiple Cameras

For each this plugin imported fSpy camera, you can get a panel called `fSpy` in camera data properties window. In this panel, you can see some properties of this imported camera, such as its corresponding image resolution.

If you are using multiple cameras with different reference image sizes, you can quickly switch from one render resolution to another using the `Set Render Resolution` button in this panel.

## Differences with Official

The official fSpy plugin looks like it hasn't been updated in a long time (although all features are functional, it's okay without an update). It's still working but not good with contemporary Blender. So I create this fork to make it use latest Blender LTS suggested solution.

I don't want to take any place of official fSpy Blender addon, so I add a `NG` suffix meaning "next generation". And this fork will not be merged into upstream repository (I mean I will not open any PR in upstream repository).

I COULD upload this plugin into official Blender extension gallery so that everyone can install it more convenient, but I will NOT do that because most of these code are not done by myself and this behavior may be seen as less ethical, even though it is allowed by the license.

## Lifetime Principle

This addon has entirely different support strategy with official fSpy Blender addon.

This plugin only supports Blender LTS version. I will only update this plugin once Blender release next LTS version, except there are some fatal issues in addon. Because this is a tiny addon and I do not have so much time on it. However, all version adaption PRs are welcomed.

Once a new LTS version is released for Blender, the old version is no longer supported. All new features and bug fixes (including those that are fatal) will only be accessible in the new Blender LTS.

The obvious truth is that I can't serve this addon immortally. I'll try to keep updating this addon as long as I'm still using Blender. If that day comes, I will archive this repository to tell you explicitly.

## Test Instruction

Navigate to the root of this repository, and execute `python3 test/test.py` directly.

## Build Instruction

Navigate to the root of this repository, then enter `fspy_blender_ng` directory, open command line prompt and execute `blender --command extension build` directly. You will find `fspy_blender_ng-x.x.x.zip` in your work directory. That's the final release package.
