from PIL import Image
from PIL import ImageTk

class LargeControlSwitch:
    def __init__(self, root, canvas, posX, posY, rotation, lineOffColor, lineOnColor):
        # store variables
        self.root = root
        self.canvas = canvas
        self.posX = posY
        self.posY = posY
        self.rotation = rotation
        
        self.lineOffColor = lineOffColor
        self.lineOnColor = lineOnColor
        self.backgroundColor = self.canvas["background"]
        
        self.isClosed = False
        self.isBlocked = False
        self.isLine1On = False
        self.isLine2On = False
        self.isClicked = False
        
        # create image container with images
        self.imageContainer = {}
        
        # present image on screen
        self.image = self.canvas.create_image(self.posX, self.posY, image=self.GetImage())
        self.canvas.tag_bind(self.image, '<ButtonPress-1>', self.OnClick)
        self.canvas.tag_bind(self.image, '<ButtonRelease-1>', self.OnRelease)
        
        # external on click callback
        self.extOnClickCallback = None
    
    def Delete(self):
        # delete image from canvas
        self.canvas.delete(self.image)
        self.image = None
        
        return
    
    def Update(self):
        # update image on canvas
        self.canvas.coords(self.image, self.posX, self.posY)
        self.canvas.itemconfig(self.image, image=self.GetImage())
    
    def Redraw(self):
        # delete old image
        self.canvas.delete(self.image)
        
        # create new image
        self.image = self.canvas.create_image(self.posX, self.posY, image=self.GetImage())
        
        return
    
    def OnClick(self, event):
        # update image to clicked
        self.isClicked = True
        self.Update()
        
        # call external callback function
        if not self.isBlocked:
            if self.extOnClickCallback:
                self.extOnClickCallback(not self.isClosed)
        
        return
    
    def OnRelease(self, event):
        # reset image
        self.isClicked = False
        self.Update()
        
        return
    
    def SetToPosition(self, posX, posY):
        # store positioin and redraw
        self.posX = posX
        self.posY = posY
        
        self.canvas.coords(self.image, self.posX, self.posY)
        
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
        
        self.Update()
        
        return
    
    def SetLineOnColor(self, color):
        # set normal color and recreate images
        self.lineOnColor = color
        
        self.Update()
        
        return
    
    def SetLineOffColor(self, color):
        # set selected color and recreate images
        self.lineOffColor = color
        
        self.Update()
        
        return
    
    def SetBackgroundColor(self, color):
        # set new background color
        if color == "none":
            self.backgroundColor = self.canvas["background"]
        else:
            self.backgroundColor = color
        
        self.Update()
        
        return
    
    def SetBlocked(self, isBlocked):
        # set blocked state
        self.isBlocked = isBlocked
        
        self.Update()
        
        return
    
    def SetClosed(self, isClosed):
        # set state of switch
        self.isClosed = isClosed
        
        self.Update()
        
        return
    
    def SetLineOn(self, line, onOff):
        # store status of line
        if line == 1:
            self.isLine1On = onOff
        elif line == 2:
            self.isLine2On = onOff
        
        self.Update()
        
        return
    
    def GetImage(self):
        # generate tag
        status = ""
        blocked = ""
        l1color = ""
        l2color = ""
        
        if self.isClosed:
            status = "closed_"
        else:
            status = "open_"
        
        if self.isBlocked:
            blocked = "blocked_"
        else:
            blocked = "unblocked_"
        
        l1color = self._GetLineColor(self.isLine1On)
        l2color = self._GetLineColor(self.isLine2On)
        
        tag = status + blocked + l1color + "_" + l2color + "_" + self.backgroundColor + "_" + str(self.rotation)
        
        # check if tag is in imageContainer
        if tag in self.imageContainer.keys():
            return self.imageContainer[tag]
        
        # create new image
        self.imageContainer[tag] = self._GenerateImage()
        
        return self.imageContainer[tag]
    
    def _GenerateImage(self):
        # start by getting the right mask
        filename = ""
        
        if self.isClosed:
            filename = "img/largeSwitchClosed.png"
        else:
            filename = "img/largeSwitchOpen.png"
        
        # get the colors
        l1color = self._GetLineColor(self.isLine1On)
        l2color = self._GetLineColor(self.isLine2On)
        
        # get rgb values from color names
        l1r, l1g, l1b = self.root.winfo_rgb(l1color)
        l1r = int(l1r / 256)
        l1g = int(l1g / 256)
        l1b = int(l1b / 256)
        
        l2r, l2g, l2b = self.root.winfo_rgb(l2color)
        l2r = int(l2r / 256)
        l2g = int(l2g / 256)
        l2b = int(l2b / 256)
        
        bgr, bgg, bgb = self.root.winfo_rgb(self.backgroundColor)
        bgr = int(bgr / 256)
        bgg = int(bgg / 256)
        bgb = int(bgb / 256)
        
        # load in mask and overlay
        mask = mask = Image.open(filename)
        pix_mask = mask.load()
        
        width, height = mask.size
        
        if self.isBlocked:
            overlay = Image.open("img/largeSwitchBlocked.png")
            pix_overlay = overlay.load()
        else:
            overlay = Image.new("RGBA", (width, height), color=(0,0,0,0))
            pix_overlay = overlay.load()
        
        # create new image and fill with background color
        base = Image.new(mode="RGB", size = (width, height), color=(bgr, bgg, bgb))
        pix_base = base.load()
        
        # add colors from mask to base
        for x in range(width):
            for y in range(height):
                f1 = pix_mask[x,y][0] / 255
                f2 = pix_mask[x,y][1] / 255
                f3 = pix_overlay[x,y][3] / 255
                
                red =   self._MergeColors(pix_base[x,y][0], l1r, f1)
                green = self._MergeColors(pix_base[x,y][1], l1g, f1)
                blue =  self._MergeColors(pix_base[x,y][2], l1b, f1)
                
                pix_base[x,y] = (red, green, blue)
                
                red =   self._MergeColors(pix_base[x,y][0], l2r, f2)
                green = self._MergeColors(pix_base[x,y][1], l2g, f2)
                blue =  self._MergeColors(pix_base[x,y][2], l2b, f2)
                
                pix_base[x,y] = (red, green, blue)
                
                red =   self._MergeColors(pix_base[x,y][0], pix_overlay[x,y][0], f3)
                green = self._MergeColors(pix_base[x,y][1], pix_overlay[x,y][1], f3)
                blue =  self._MergeColors(pix_base[x,y][2], pix_overlay[x,y][2], f3)
                
                pix_base[x,y] = (red, green, blue)
        
        return ImageTk.PhotoImage(base.rotate(self.rotation, expand=True))
    
    def _MergeColors(self, color_base, color_top, factor):
        # factor = 1 -> color 2
        result = int(color_base * (1 - factor) + color_top * factor)
        
        if result > 255:
            result = 255
        
        return result
    
    def _GetLineColor(self, onOff):
        # return line color from status
        if self.isClicked:
            if self.isBlocked:
                return "red"
            else:
                return "green"
        else:
            if onOff:
                return self.lineOnColor
            else:
                return self.lineOffColor
        
        return self.lineOffColor