# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class TextToolDialog
###########################################################################

class TextToolDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Text Tool", pos = wx.DefaultPosition, size = wx.Size( 581,250 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.Size( 510,250 ), wx.DefaultSize )

		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gbSizer1.SetMinSize( wx.Size( 510,250 ) )
		font_listChoices = []
		self.font_list = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, font_listChoices, wx.CB_SORT )
		self.font_list.SetSelection( 1 )
		gbSizer1.Add( self.font_list, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.size_spin = wx.SpinCtrlDouble( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 1, 400, 12.000000, 0.1 )
		self.size_spin.SetDigits( 1 )
		gbSizer1.Add( self.size_spin, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.text_field = wx.TextCtrl( self, wx.ID_ANY, u"KiCad", wx.DefaultPosition, wx.DefaultSize, wx.TE_DONTWRAP )
		gbSizer1.Add( self.text_field, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		layer_listChoices = []
		self.layer_list = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 130,-1 ), layer_listChoices, wx.LB_EXTENDED|wx.LB_MULTIPLE )
		gbSizer1.Add( self.layer_list, wx.GBPosition( 0, 3 ), wx.GBSpan( 6, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.add_button = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.add_button, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.size_status = wx.StaticText( self, wx.ID_ANY, u"pt (3.88 mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.size_status.Wrap( -1 )

		gbSizer1.Add( self.size_status, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		gbSizer1.AddGrowableCol( 0 )
		gbSizer1.AddGrowableRow( 5 )

		self.SetSizer( gbSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_close )
		self.size_spin.Bind( wx.EVT_TEXT, self.on_size_change )
		self.add_button.Bind( wx.EVT_BUTTON, self.run )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def on_close( self, event ):
		event.Skip()

	def on_size_change( self, event ):
		event.Skip()

	def run( self, event ):
		event.Skip()


