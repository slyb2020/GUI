import wx
import time


class MyProgressGauge(wx.Window):
    """ This class provides a visual alternative for wx.Gauge."""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=(-1, 30)):
        """ Default class constructor. """

        wx.Window.__init__(self, parent, id, pos, size, style=wx.BORDER_NONE)

        self._value = 0
        self._steps = 19
        self._pos = 0
        self._current = 0
        self._gaugeproportion = 0.4
        self._startTime = time.time()

        self._bottomStartColour = wx.GREEN
        rgba = self._bottomStartColour.Red(), self._bottomStartColour.Green(), \
               self._bottomStartColour.Blue(), self._bottomStartColour.Alpha()
        self._bottomEndColour = self.LightColour(self._bottomStartColour, 30)
        self._topStartColour = self.LightColour(self._bottomStartColour, 80)
        self._topEndColour = self.LightColour(self._bottomStartColour, 40)

        self._background = wx.Brush(wx.WHITE, wx.BRUSHSTYLE_SOLID)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def StartAlarm(self):
        self._bottomStartColour = wx.RED
        self._bottomEndColour = self.LightColour(self._bottomStartColour, 30)
        self._topStartColour = self.LightColour(self._bottomStartColour, 80)
        self._topEndColour = self.LightColour(self._bottomStartColour, 40)
        self.Refresh()

    def StopAlarm(self):
        self._bottomStartColour = wx.GREEN
        self._bottomEndColour = self.LightColour(self._bottomStartColour, 30)
        self._topStartColour = self.LightColour(self._bottomStartColour, 80)
        self._topEndColour = self.LightColour(self._bottomStartColour, 40)
        try:
            self.Refresh()
        except:
            pass

    def OnEraseBackground(self, event):
        """ Handles the wx.EVT_ERASE_BACKGROUND event for ProgressGauge. """
        pass

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(self._background)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()
        xsize, ysize = self.GetClientSize()
        interval = xsize / float(self._steps)
        self._pos = interval * self._value
        status = self._current / (self._steps - int((self._gaugeproportion * xsize / interval)))
        if status % 2 == 0:
            increment = 1
        else:
            increment = -1
        self._value = self._value + increment
        self._current = self._current + 1
        self.DrawProgress(dc, xsize, ysize, increment)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRADIENTINACTIVECAPTION)))
        dc.DrawRectangle(self.GetClientRect())

    def LightColour(self, colour, percent):
        end_colour = wx.WHITE
        rd = end_colour.Red() - colour.Red()
        gd = end_colour.Green() - colour.Green()
        bd = end_colour.Blue() - colour.Blue()
        high = 100
        i = percent
        r = colour.Red() + ((i * rd * 100) / high) / 100
        g = colour.Green() + ((i * gd * 100) / high) / 100
        b = colour.Blue() + ((i * bd * 100) / high) / 100
        return wx.Colour(r, g, b)

    def DrawProgress(self, dc, xsize, ysize, increment):
        interval = self._gaugeproportion * xsize
        gc = wx.GraphicsContext.Create(dc)
        clientRect = self.GetClientRect()
        gradientRect = wx.Rect(*clientRect)
        x, y, width, height = clientRect
        x, width = self._pos, interval
        gradientRect.SetHeight(gradientRect.GetHeight() / 2)
        topStart, topEnd = self._topStartColour, self._topEndColour
        rc1 = wx.Rect(x, y, width, height / 2)
        path1 = self.GetPath(gc, rc1, 8)
        br1 = gc.CreateLinearGradientBrush(x, y, x, y + height / 2, topStart, topEnd)
        gc.SetBrush(br1)
        gc.FillPath(path1)  # draw main
        path4 = gc.CreatePath()
        path4.AddRectangle(x, y + height / 2 - 8, width, 8)
        path4.CloseSubpath()
        gc.SetBrush(br1)
        gc.FillPath(path4)

        gradientRect.Offset((0, gradientRect.GetHeight()))

        bottomStart, bottomEnd = self._bottomStartColour, self._bottomEndColour

        rc3 = wx.Rect(x, y + height / 2, width, height / 2)
        path3 = self.GetPath(gc, rc3, 8)
        br3 = gc.CreateLinearGradientBrush(x, y + height / 2, x, y + height, bottomStart, bottomEnd)
        gc.SetBrush(br3)
        gc.FillPath(path3)  # draw main

        path4 = gc.CreatePath()
        path4.AddRectangle(x, y + height / 2, width, 8)
        path4.CloseSubpath()
        gc.SetBrush(br3)
        gc.FillPath(path4)

    def GetPath(self, gc, rc, r):
        """ Returns a rounded GraphicsPath. """

        x, y, w, h = rc
        path = gc.CreatePath()
        path.AddRoundedRectangle(x, y, w, h, r)
        path.CloseSubpath()
        return path

    def Pulse(self):
        """ Updates the gauge with a new value. """
        self.Refresh()


class MyLogoutGauge(MyProgressGauge):
    """ This class provides a visual alternative for wx.Gauge."""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=(-1, 30)):
        """ Default class constructor. """
        wx.Window.__init__(self, parent, id, pos, size, style=wx.BORDER_NONE)
        self._value = 0
        self._steps = 1000
        self._pos = 0
        self._current = 0
        self._gaugeproportion = 0.4
        self._startTime = time.time()

        self._bottomStartColour = wx.GREEN
        rgba = self._bottomStartColour.Red(), self._bottomStartColour.Green(), \
               self._bottomStartColour.Blue(), self._bottomStartColour.Alpha()
        self._bottomEndColour = self.LightColour(self._bottomStartColour, 30)
        self._topStartColour = self.LightColour(self._bottomStartColour, 80)
        self._topEndColour = self.LightColour(self._bottomStartColour, 40)

        self._background = wx.Brush(wx.WHITE, wx.BRUSHSTYLE_SOLID)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
