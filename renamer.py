import sys
import wx
import wx.lib.inspection

class RenamerPanel(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        self.menuheight = 100

        # Create an empty image, as a placeholder when no image is loaded
        # The raw image data is stored in the image variable if you rescale,
        # you need the rawdata
        self.image = wx.Image(250, 250, clear=True)
        bitmap = self.image.ConvertToBitmap()
        self.staticBitmap = wx.StaticBitmap(self,
            -1,
            bitmap,
            (0, 0),
            (-1, -1)
#            (parent.GetSize().GetWidth(),parent.GetSize().GetHeight()-self.menuheight)
        )

        # This is the place for the menu
        self.oldname = wx.StaticText(self, label='IMG_20131230_154006.jpg')
        self.newname = wx.StaticText(self, label='2013_12_30_siegessaeule.jpg')
        self.description = wx.TextCtrl(self, value='textctrl0',
            pos=(0,parent.GetSize().GetHeight()-self.menuheight))


        # Key downs are send to onKeyPress
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_IDLE,self.onIdle)

        self.resize = False
        print('Init done')
    
    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        print(keycode)
        if keycode == wx.WXK_SPACE:
            print("you pressed the spacebar!")
#            self._load_image('IMG_20131230_154006.jpg')
        elif keycode == wx.WXK_F12:
            print("you pressed F12")
#            self._update_bitmap()
        event.Skip()

    def onSize(self, event):
        self.resize = True

    def onIdle(self, event):
        if self.resize:
            print('Resizing')
            self.resize = False
            self._update_bitmap()
            self._update_menuitems()

    # reads raw image data into the local variable
    def _load_image(self, filename):
        self.image = wx.Image(filename, wx.BITMAP_TYPE_ANY)
    
    # updates the staticbitmap in the UI
    def _update_bitmap(self):
        scaledImage = self.image.Scale(self.Parent.GetSize().GetWidth(),
            self.Parent.GetSize().GetHeight()-self.menuheight, wx.IMAGE_QUALITY_HIGH)
        bitmap = scaledImage.ConvertToBitmap()
#        size = self.staticBitmap.GetSize()
#        print(size)
#        self.staticBitmap.SetSize((size.GetWidth(), size.GetHeight()))
        self.staticBitmap.SetBitmap(bitmap)

    def _update_menuitems(self):
        height = self.GetParent().GetSize().GetHeight()
        x,_ = self.description.GetPosition()
        print(height)
        self.description.SetPosition((x,height-self.menuheight))

app = wx.App()
frame = wx.Frame(None, -1, 'Image Renamer', size = (500  , 500))

renamerPanel = RenamerPanel(frame,-1)
renamerPanel._load_image('IMG_20131230_154006.jpg')

frame.Show(1)


wx.lib.inspection.InspectionTool().Show()

app.MainLoop()
