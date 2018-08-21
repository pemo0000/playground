import wx

class View(wx.Panel):
  preferences = {
          'Default': {'darkSquareColor':'grey', 'lightSquareColor':'white', 'homeSquareColor':'red', 'targetSquareColor':'orange', 'captureSquareColor':'green'},
          'FEN':     {'darkSquareColor':'grey'}
                  }
  def __init__(self, parent):
    self.parent = parent 
    super(View, self).__init__(parent)
    self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
    self.Bind(wx.EVT_SIZE, self.on_size)
    self.Bind(wx.EVT_PAINT, self.on_paint)
    self.boardsize = 8

  def on_size(self, event):
    event.Skip()
    self.Refresh()

  def on_paint(self, event):
    w, h = self.parent.GetClientSize()
    dc = wx.AutoBufferedPaintDC(self)
    dc.Clear()
    rectangleSize = min(h, w)/self.boardsize
    x=y=0
    for i in range(0,self.boardsize):
      for j in range(0,self.boardsize):
        if i & 1 != j & 1:
          dc.SetBrush(wx.Brush(wx.Colour(self.preferences["Default"]["darkSquareColor"])))
          dc.DrawRectangle(x, y, rectangleSize, rectangleSize)
        else:
          dc.SetBrush(wx.Brush(wx.Colour(self.preferences["Default"]["lightSquareColor"])))
          dc.DrawRectangle(x, y, rectangleSize, rectangleSize)
        x = x + rectangleSize - 2
      x = 0
      y = y + rectangleSize - 2

class Frame(wx.Frame):
  def __init__(self):
    super(Frame, self).__init__(None)
    self.SetTitle('strulls wx board in pemos playground')
    self.SetClientSize((500, 500))
    self.Center()
    self.view = View(self)
