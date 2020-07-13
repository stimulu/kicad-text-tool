# kicad-text-tool
A plugin to add text using system fonts on your PCB

## Disclaimer
This is very much a work in progress.  
This has only been tested on Linux.  
You need freetype on your system.
This is slow. It varies from font to font, and with the length of the text.  
This is so slow you may want to stop it. There is no way to do that and keep your unsaved modifications. Save your work before starting the plugin. And start by testing a font with one or two char.

## Installation 
Clone or unzip this repository in a KiCad plugin folder :  

- On linux :
   - `/usr/share/kicad/scripting/plugins/`
   - `~/.kicad/scripting/plugins`
   - `~/.kicad_plugins/`
- On macOS :
   - `/Applications/kicad/Kicad/Contents/SharedSupport/scripting/plugins`
   - `~/Library/Application Support/kicad/scripting/plugins`
   
## Usage
In the app menu `Tools > External plugin` click `Add new text`.  

## Licence
MIT
