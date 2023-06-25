from direct.showbase.ShowBase import ShowBase
from skysphere import SkySphere


class CrystalQuest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.set_background_color(0, 0, 0)  # Set background color to black

        self.sky_sphere = SkySphere(self)

        self.taskMgr.add(self.sky_sphere.update, "update_task")


app = CrystalQuest()
app.run()
