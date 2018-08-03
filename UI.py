import wx

class UI(wx.Frame):

    app = wx.App(False)
    frame = wx.Frame(None, title="Draw on Panel")
    panel = wx.Panel(frame)

    def __init__(self, parent, title): 
        #boardsize = 8 
        #boardWidth = 400
        #boardHeigth = boardWidth
        #sizeStatusbar = 70
        #rectangleSize = boardWidth / boardsize

        # Setting up the menu.
        filemenu= wx.Menu()
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        #self.SetMenuBar(UI.frame)  # Adding the MenuBar to the Frame content.
        #self.Bind(wx.EVT_PAINT, self.OnPaint) 
        #self.Centre() 
        #self.Show(True)

    def on_paint(event):
        dc = wx.PaintDC(event.GetEventObject())
        dc.Clear()

        boardsize = 8
        x = 0
        y = 0
        for i in range(0, boardsize):
            for j in range(0, boardsize):
                if i & 1 == j & 1:
                    dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
                    dc.DrawRectangle(x, y, 50, 50) 
                else:
                    dc.SetBrush(wx.Brush(wx.Colour(155,155,155)))
                    dc.DrawRectangle(x, y, 50, 50) 
                x = x + 49
            x = 0
            y = y + 49

    bmp = wx.Bitmap('k40.png')
    wx.StaticBitmap(panel, bitmap=bmp, pos=(5,5))
    
    panel.Bind(wx.EVT_PAINT, on_paint)
    frame.Show(True)
    app.MainLoop()
