# WallpDesk
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![Build Status](https://travis-ci.org/L3rchal/WallpDesk.svg?branch=master)](https://travis-ci.org/L3rchal/WallpDesk)

`walld` application for updating files on desktop only and setting background wallpaper based on his color spectre and time.

## py2app is depreciated, meaning I had to remove gui from this project, working on new tool in swift

<!--![alt-text-1](https://imgur.com/8YKlbk2.png "title-1") ![alt-text-2](https://imgur.com/FpY5tFB.png "title-2")-->

## Features

### Desktop
Be able to controll all files on desktop with `Desktop daemon`. Able to controll via commands. So lets say I need move image to specific direcotry but my destop is too "mesy". I can use following.
```
@{command}file

e.g.:
@{mv /path/to/my/dir}image_file.jpg
```
And this will move image_file.jpg to specific directory. `wall` will set image wallpaper, `img` automaticly move image to `~/Pictures` and more. This list of commands is easy editable.

<p align="center">
  <img src="https://media.giphy.com/media/l1J9PYEhwprwlM6EE/giphy.gif">
</p>

### Wallpaper
Set desktop wallpaper however this chooses every hour from specific directory set via setings. Depending on time it tries to choose dark image if is later then eight pm or light if it's before eight.

Application works that first creates database and inputs images path and type (light/evening/dark). Daemon can change wallpaper every hour or if you don't like wallpaper set new one with `Next wallpaper`. **Warnig there is 5 second delay for new wallpaper**

## Install

Download lastest release or build application by your self. 
You will need:
* python3
* numpy
* python-opencv
* python-dateutil
* astral
* ~and py2app~

And build with `python3 setup.py py2app`-> WalpDesk.app

## To do list:
* ~Show remaining time to next wallapeer change~
* ~click on specific time -> new wallpaper~
* controll image by splitin to quaters
* new mode for changing only if mode time changes

## Credits
- App icon made by [Dimi Kazak](https://www.flaticon.com/authors/dimi-kazak)
