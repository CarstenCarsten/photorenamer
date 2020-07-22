import sys
import wx

class RenamerPanel(wx.Panel):

    @property
    def file_name(self):
        return self._file_name
    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, value):
        self._image = value

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.resized = False
        self.Bind(wx.EVT_SIZE,self.OnSize)
        self.Bind(wx.EVT_IDLE,self.OnIdle)

    def OnSize(self,event):
        self.resized = True

    def OnIdle(self,event):
        if self.resized:
            if self.image:
                panelSize = self.GetSize()
                print(panelSize)
                bitmap = self.image.Scale(panelSize.GetWidth(), panelSize.GetHeight(), wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                wx.StaticBitmap(self, -1, bitmap, (0, 0), (bitmap.GetWidth(), bitmap.GetHeight()))
                self.resized = False

    def loadImage(self, file_name):
        self.file_name = file_name
        try:
            self.image = wx.Image(self.file_name, wx.BITMAP_TYPE_ANY)
        except:
            print('Could not read image')
            sys.exit()
        bitmap = self.image.Scale(100, 100, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
#        wx.StaticBitmap(self, -1, bitmap, (0, 0), (bitmap.GetWidth(), bitmap.GetHeight()))
#        wx.StaticText(self, label='Meinlabel')
#        wx.TextCtrl(self, value='textctrl0')
        self.resized = True

app = wx.App()

frame = wx.Frame(None, -1, 'Image Renamer', size = (400, 300))

renamerPanel = RenamerPanel(frame,-1)
frame.Show(1)

renamerPanel.loadImage('IMG_20131230_154006.jpg')

app.MainLoop()
