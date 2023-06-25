from direct.showbase.ShowBase import ShowBase
from skysphere import SkySphere
from panda3d.core import loadPrcFileData


class CrystalQuest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.set_background_color(0, 0, 0)  # Set background color to black

        self.sky_sphere = SkySphere(self)

        # Set fullscreen resolution
        width, height = 1920, 1080
        #Change resolution 
        loadPrcFileData("", "win-size" + str(width) + " " + str(height))
        #make full screen
        loadPrcFileData("", "fullscreen t")

        self.sky_sphere.run()


app = CrystalQuest()
app.run()
