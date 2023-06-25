from panda3d.core import Vec3

class Camera:
    def __init__(self, base, skybox):
        self.base = base
        self.skybox = skybox
        self.setup_camera()

    def setup_camera(self):
        self.base.disableMouse()
        self.base.camera.setPos(Vec3(0, 0, 0))
        self.base.camera.reparentTo(self.skybox)
