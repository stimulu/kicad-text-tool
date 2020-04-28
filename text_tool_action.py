import sys
import os

if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__), "freetype/lib/win32")))
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__), "freetype/lib/win64")))

from .text_tool_gui import TextToolDialog
from .text_tool_fontpick import *
from .text_tool_draw import Text, Point

from .freetype import Face

import math
import wx
import pcbnew
import json

class TextTool(TextToolDialog):

    def __init__(self, board, action):
        super(TextTool, self).__init__(None)
        self.board = board
        self.configfilepath = ".".join(self.board.GetFileName().split('.')[:-1])+".text-tool-config"
        self.action = action

        self.fonts = load_font_list()
        for f in self.fonts:
            self.font_list.Append(f)
        
        self.load_layers()

        self.load_config()

        for l in self.layer_selections:
            self.layer_list.SetSelection(l)

        self.text_field.ChangeValue(self.text_line)
        self.font_list.SetSelection(self.font_index)
        self.size_spin.SetValue(self.current_size)


        font_size_mm = self.current_size*0.352778
        self.size_status.SetLabel("pt ("+str(round(font_size_mm, 2))+" mm)")

    def on_size_change( self, event ):
        self.current_size = self.size_spin.GetValue()
        font_size_mm = self.current_size*0.352778
        self.size_status.SetLabel("pt ("+str(round(font_size_mm, 2))+" mm)")

    def load_layers( self,  ):
        #layertable = {}
        numlayers = pcbnew.PCB_LAYER_ID_COUNT
        self.layers = []
        for i in range(numlayers):
            #layertable[i] = board.GetLayerName(i)
            if self.board.IsLayerEnabled(i) and i is not 50:
                self.layers.append(i)
                self.layer_list.Append(self.board.GetLayerName(i)+ " (" + str(i) + ")")
        
    def run( self, event ):
        self.Destroy()

        self.layer_selections = self.layer_list.GetSelections()
        self.text_line = self.text_field.GetLineText(0)
        self.font_index = self.font_list.GetSelection()
        self.font_name = self.font_list.GetString(self.font_index)
        self.current_face = Face(self.fonts[self.font_name])
        print(self.layer_selections)
        self.current_size = self.size_spin.GetValue()

        self.save_config()

        t = Text(self.text_line, self.current_face, self.current_size)

        origin = self.board.GetBoardEdgesBoundingBox().Centre()
        for l in self.layer_selections:
            zone_container = t.draw(self.board, self.layers[l], origin=origin)

    def save_config(self):
        with open(self.configfilepath, "w") as config_file:
            config_file.write(json.dumps({
                                         "layers" : self.layer_selections,
                                         "text" : self.text_line,
                                         "font_index" : self.font_index,
                                         "size" : self.current_size
                                         })) 
    def load_config(self):
        config = {}
        if os.path.isfile(self.configfilepath):
            with open(self.configfilepath, "r") as config_file:
                try:
                    config = json.loads(config_file.read())
                except Exception as e:
                    print(e)
                    pass

        self.layer_selections = config['layers'] if "layers" in config else [0]
        self.text_line = config['text'] if "text" in config else "KiCad"
        self.font_index = config['font_index'] if "font_index" in config else 10
        self.current_size = config['size'] if "size" in config else 8

    def on_close( self, event ):
        self.Destroy()
        pass

class TextToolAction( pcbnew.ActionPlugin ):
 
    def defaults( self ):
        self.name = "Text Tool"
        self.category = "Modify PCB"
        self.description = "Adds text to your PCB using system fonts"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./text_tool.png")

    def Run( self ):
        board = pcbnew.GetBoard()
        rt = TextTool(board, self)
        rt.ShowModal()

