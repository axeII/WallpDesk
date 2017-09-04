# WallpDesk
[![Build Status](https://travis-ci.org/L3rchal/WallpDesk.svg?branch=master)](https://travis-ci.org/L3rchal/WallpDesk)

`WallpDesk` is simple lightweight os x application that only displays in menu bar. Application creates two daemons for setting wallpaper and controlling deskop files. Both are controlled with menu bar settings.

<p align="center"> 
![alt-text-1](https://imgur.com/8YKlbk2.png "title-1") ![alt-text-2](https://imgur.com/FpY5tFB.png "title-2")

Application doesn't have so far any gui so only control is via menu bar. Whole application is written in python3 using two external libraries and sqlite3.

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
![gif](https://thumbs.gfycat.com/LastingZigzagAlligator-size_restricted.gif)


### Wallpaper
Set desktop wallpaper however this chooses every hour from specific directory set via setings. Depending on time it tries to choose dark image if is later then eight pm or light if it's before eight.

Application works that first creates database and inputs images path and type (light/dark). Daemon can change wallpaper every hour or if you don't like wallpaper set new one with `Next wallpaper`. **Warnig there is 5 second delay for new wallpaper**

## Install

`python3 setup.py py2app` will build WalpDesk.app however you need for that python3, rumps, Pillow and py2app to be able build application. 


## Credits
- App icon made by [Dimi Kazak](https://www.flaticon.com/authors/dimi-kazak)
