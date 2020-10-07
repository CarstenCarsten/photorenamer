import sys
import wx
import wx.lib.inspection
from os import listdir, rename
from os.path import isfile, join


class RenamerPanel(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        self.menuheight = 20
        self.spacing = 50
        self.current_image = 0
        self.oldpictures = list()

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
        )

        # This is the place for the menu
        self.oldname = wx.StaticText(self, label='IMG_20131230_154006.jpg',
            pos=(0,self.GetSize().GetHeight()-self.menuheight),
            name='oldname')

        self.newname = wx.StaticText(self, label='2013_12_30_description.jpg',
            pos=(self.oldname.GetPosition().Get()[0]+self.oldname.GetSize().GetWidth()+self.spacing, self.GetSize().GetHeight()-self.menuheight),
            name='newname')

        self.description = wx.TextCtrl(self, value='description',
            pos=(self.newname.GetPosition().Get()[0]+self.newname.GetSize().GetWidth()+self.spacing, self.GetSize().GetHeight()-self.menuheight),
            name='description',
            style = wx.TE_PROCESS_ENTER,
            id=2)

        # Key downs are send to onKeyPress
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_IDLE,self.onIdle)
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter, id = 2)

        self.resize = False

    def onEnter(self,event):
        new_filename_label = self.newname.GetLabel()
        description = str(self.description.GetValue())
        new_filename = new_filename_label[0:10]  + '_' + description + new_filename_label[-4:]
        print('renaming [' + self.oldpictures[self.current_image] + '] to [' + new_filename + ']')
        rename(self.oldpictures[self.current_image], new_filename)
        self._next_file()

    def onSize(self, event):
        self.resize = True

    def onIdle(self, event):
        if self.resize:
            self.resize = False
            self._update_menuitems()
            self._update_bitmap()

    # reads raw image data into the local variable
    def _load_image(self, filename):
        self.oldname.SetLabel(filename)
        self.newname.SetLabel(filename[4:8] + '_' + filename[8:10]  + '_' + filename[10:12] + filename[-4:])
        self.description.SetSelection(-1,-1)
        self.image = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        self.resize = True
    
    # updates the staticbitmap in the UI
    def _update_bitmap(self):
        image_width = self.image.GetSize().GetWidth()
        image_height = self.image.GetSize().GetHeight()
        w2h_image = image_width/image_height
        window_width = self.GetSize().GetWidth()
        window_height = self.GetSize().GetHeight() - self.menuheight

        target_width = window_width
        target_height = window_width / w2h_image

        if target_height > window_height:
            diff = target_height - window_height
            target_width -= diff * w2h_image
            target_height = window_height

        scaledImage = self.image.Scale(target_width,
            target_height, wx.IMAGE_QUALITY_HIGH)
        bitmap = scaledImage.ConvertToBitmap()
        self.staticBitmap.SetBitmap(bitmap)

    def _update_menuitems(self):
        self.oldname.SetPosition((0, self.GetSize().GetHeight()-self.menuheight))
        self.newname.SetPosition((self.oldname.GetPosition().Get()[0]+self.oldname.GetSize().GetWidth()+self.spacing, self.GetSize().GetHeight()-self.menuheight))
        self.description.SetPosition((self.newname.GetPosition().Get()[0]+self.newname.GetSize().GetWidth()+self.spacing, self.GetSize().GetHeight()-self.menuheight))

    def _iterate_folder(self,mypath = '.'):
        self.oldpictures = list([f for f in listdir(mypath) if isfile(join(mypath, f)) and 
            f.lower().endswith('.jpg') and
            f[4:8].isdigit() and
            f[8:10].isdigit() and
            f[10:12].isdigit() and
            int(f[4:8]) > 1900 and
            int(f[4:8]) < 2100 and
            int(f[8:10]) > 0 and
            int(f[8:10]) <= 12 and
            int(f[10:12]) > 0 and
            int(f[10:12]) <= 31])
        self.current_image = 0
        self._next_file(False)
    
    def _next_file(self, increment=True):
        if increment:
            self.current_image += 1
        if len(self.oldpictures) <= self.current_image:
            wx.MessageBox('No more files')
            wx.CallAfter(frame.Close)
        else:
            self._load_image(self.oldpictures[self.current_image])

app = wx.App()
frame = wx.Frame(None, -1, 'Image Renamer', size = (500  , 500))

renamerPanel = RenamerPanel(frame,-1)
renamerPanel._iterate_folder('.')

frame.Show(1)

#wx.lib.inspection.InspectionTool().Show()

app.MainLoop()
print('Main loop over')