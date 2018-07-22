tell application "System Events"
            tell current desktop
                set picture rotation to 1 -- (0=off, 1=interval, 2=login, 3=sleep)
                set random order to true
                set pictures folder to alias "Macintosh HD:Users:ales:.walld:current:"
                set change interval to 5.0
            end tell
        end tell
