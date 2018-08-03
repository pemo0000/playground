import wx

class UI(wx.Frame): 
   preferences = {
           'Default': {'darkSquareColor':'grey', 'lightSquareColor':'white', 'homeSquareColor':'red', 'targetSquareColor':'orange', 'captureSquareColor':'green'},
           'FEN':     {'darkSquareColor':'grey'}
                  }
   boardWidth = 400
   boardHeigth = boardWidth
   sizeStatusbar = 65
            
   def __init__(self, parent, title, boardsize): 
      self.boardsize = boardsize
      self.rectangleSize = UI.boardWidth / self.boardsize
      super(UI, self).__init__(parent, title = "Ich dreh durch! ;-)", size = (UI.boardWidth, UI.boardHeigth + UI.sizeStatusbar))  
      self.InitUI() 
         
   def InitUI(self): 
      self.CreateStatusBar()
      self.SetStatusText("This is the statusbar")
      # Setting up the menu.
      filemenu= wx.Menu()
      menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
      menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

      # Creating the menubar.
      menuBar = wx.MenuBar()
      menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
      self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
      self.Bind(wx.EVT_PAINT, self.OnPaint) 
      self.Centre() 
      self.Show(True)

      # Events.
      self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
      self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
      
      # Drawing test images.
      bmp = wx.Bitmap("p40.png")
      wx.StaticBitmap(self, bitmap=bmp, pos=(58,55))
      bmp1 = wx.Bitmap("P40.png")
      wx.StaticBitmap(self, bitmap=bmp1, pos=(205,201))
		
   def OnPaint(self, e): 
      x = 0
      y = 0
      dc = wx.PaintDC(self) 
      for i in range(0, self.boardsize):
          for j in range(0, self.boardsize):
              if i & 1 == j & 1:
                  dc.SetBrush(wx.Brush(wx.Colour(UI.preferences["Default"]["lightSquareColor"])))
                  dc.DrawRectangle(x, y, self.rectangleSize, self.rectangleSize) 
              else:
                  dc.SetBrush(wx.Brush(wx.Colour(UI.preferences["Default"]["darkSquareColor"])))
                  dc.DrawRectangle(x, y, self.rectangleSize, self.rectangleSize) 
              x = x + self.rectangleSize - 1 
          x = 0
          y = y + self.rectangleSize - 1

   def OnAbout(self,e):
      # Create a message dialog box
      dlg = wx.MessageDialog(self, " Maybe the Ultimate Chess Playground. \n Developped by E8 under strong code and design control of E1.", "About Ultimate Chess Playground", wx.OK)
      dlg.ShowModal()
      dlg.Destroy()

   def OnExit(self,e):
       self.Close(True)

