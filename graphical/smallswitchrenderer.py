from PIL import Image
from PIL import ImageTk

class SmallSchematicSwitch:
    def __init__(self, root, canvas, posX, posY, rotation, normalColor, selectedColor):
        # store variables
        self.root = root
        self.canvas = canvas
        self.posX = posY
        self.posY = posY
        self.rotation = rotation
        
        self.normalColor = normalColor
        self.selectedColor = selectedColor
        self.backgroundColor = self.canvas["background"]
        
        self.closed = False
        self.selected = False
        
        # create image container with images
        self.imageContainer = {}
        self.GenerateImages()
        
        # present image on screen
        tag = self.GetImageTag()
        self.image = self.canvas.create_image(self.posX, self.posY, image=self.imageContainer[tag])
    
    def Delete(self):
        # delete image from canvas
        self.canvas.delete(self.image)
        self.image = None
        
        return
    
    def Update(self):
        # create new image
        tag = self.GetImageTag()
        
        # update image on canvas
        self.canvas.coords(self.image, self.posX, self.posY)
        self.canvas.itemconfig(self.image, image=self.imageContainer[tag])
    
    def Redraw(self):
        # delete old image
        self.canvas.delete(self.image)
        
        # create new image
        tag = self.GetImageTag()
        
        self.image = self.canvas.create_image(self.posX, self.posY, image=self.imageContainer[tag])
        
        return
    
    def SetToPosition(self, posX, posY):
        # store positioin and redraw
        self.posX = posX
        self.posY = posY
        
        self.canvas.coords(self.image, self.posX, self.posY)
        
        return
    
    def SetSelected(self, selected):
        self.selected = selected
        self.Update()
        return
    
    def SetClosed(self, closed):
        self.closed = closed
        self.Update()
        return
    
    def Move(self, dx, dy):
        # move image around
        self.posX += dx
        self.posY += dy
        
        self.canvas.coords(self.image, self.posX, self.posY)
        
        return
    
    def SetRotation(self, rotation):
        # store rotation
        self.rotation = rotation
        
        while self.rotation >= 360:
            self.rotation -= 360
        
        while self.rotation < 0:
            self.rotation += 360
        
        self.GenerateImages()
        
        self.Update()
        
        return
    
    def SetNormalColor(self, color):
        # set normal color and recreate images
        self.normalColor = color
        
        self.GenerateImages()
        
        self.Update()
        
        return
    
    def SetSelectedColor(self, color):
        # set selected color and recreate images
        self.selectedColor = color
        
        self.GenerateImages()
        
        self.Update()
        
        return
    
    def SetBackgroundColor(self, color):
        # set the background color
        if color == "none":
            self.backgroundColor = self.canvas["background"]
        else:
            self.backgroundColor = color
        
        self.GenerateImages()
        
        self.Update()
        
        return
    
    def GenerateImages(self):
        # there are four images to be created
        self._GenerateImage(self.normalColor, True, self.rotation)
        self._GenerateImage(self.normalColor, False, self.rotation)
        self._GenerateImage(self.selectedColor, True, self.rotation)
        self._GenerateImage(self.selectedColor, False, self.rotation)
        
        return
    
    def GetImageTag(self):
        # create tag for state
        tag = ""
        
        if self.selected:
            if self.closed:
                tag = "closed_" + self.selectedColor + "_" + str(self.rotation)
            else:
                tag = "open_" + self.selectedColor + "_" + str(self.rotation)
        else:
            if self.closed:
                tag = "closed_" + self.normalColor + "_" + str(self.rotation)
            else:
                tag = "open_" + self.normalColor + "_" + str(self.rotation)
        
        return tag
    
    def _GenerateImage(self, color, closed, rotation):
        # generate an actual image
        # generate the tag first
        tag = ""
        
        if closed:
            tag = "closed_" + color + "_" + str(rotation)
        else:
            tag = "open_" + color + "_" + str(rotation)
        
        # get the rgb values from color name
        r,g,b = self.root.winfo_rgb(color)
        br, bg, bb = self.root.winfo_rgb(self.backgroundColor)
        
        # load in mask
        if closed:
            filename = "img/smallSwitchClosed.png"
        else:
            filename = "img/smallSwitchOpen.png"
        
        mask = Image.open(filename)
        pix_mask = mask.load()
        
        # get size of image
        width, height = mask.size
        
        # process mask
        for x in range(width):
            for y in range(height):
                f = pix_mask[x,y][0] / 255
                a = pix_mask[x,y][3]
                red = self._MergeColors(int(br / 256), int(r / 256), f)
                green = self._MergeColors(int(bg / 256), int(g / 256), f)
                blue = self._MergeColors(int(bb / 256), int(b / 256), f)
                pix_mask[x,y] = (red, green, blue, a)
        
        # store into image container
        self.imageContainer[tag] = ImageTk.PhotoImage(mask.rotate(self.rotation, expand=True))
        
        return
    
    def _MergeColors(self, color_base, color_top, factor):
        # factor = 1 -> color 2
        result = int(color_base * (1 - factor) + color_top * factor)
        
        if result > 255:
            result = 255
        
        return result