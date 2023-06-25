from panda3d.core import Texture, NodePath, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom, GeomNode
from panda3d.core import VBase3, TransparencyAttrib, LVecBase3f
import random
import os

class SkySphere:
    def __init__(self, base):
        self.base = base
        self.skybox = NodePath("skybox")
        self.skybox.setBin("background", 1)
        self.skybox.setDepthWrite(0)

        # Load random skysphere texture
        sky_textures_path = "./skyspheres/"
        sky_textures = [file for file in os.listdir(sky_textures_path) if file.endswith(".jpg")]
        random_texture = random.choice(sky_textures)
        sky_texture_path = os.path.join(sky_textures_path, random_texture)
        print("Selected skysphere texture:", sky_texture_path)
        sky_texture = self.base.loader.loadTexture(sky_texture_path)
        sky_texture.setWrapU(Texture.WMClamp)
        sky_texture.setWrapV(Texture.WMClamp)

        # Create skybox geometry
        format = GeomVertexFormat.getV3()
        vdata = GeomVertexData("skybox_data", format, Geom.UHStatic)
        vdata.setNumRows(8)

        vertex = GeomVertexWriter(vdata, "vertex")
        for i in range(8):
            vertex.addData3f(LVecBase3f(-1, -1, -1))

        tris = GeomTriangles(Geom.UHStatic)
        tris.addVertices(0, 1, 2)
        tris.addVertices(1, 3, 2)
        tris.addVertices(2, 3, 4)
        tris.addVertices(3, 5, 4)
        tris.addVertices(4, 5, 6)
        tris.addVertices(5, 7, 6)
        tris.addVertices(6, 7, 0)
        tris.addVertices(7, 1, 0)
        tris.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(tris)

        node = GeomNode("skybox_geom")
        node.addGeom(geom)
        skybox_model = self.skybox.attachNewNode(node)

        # Apply skysphere texture to skybox
        skybox_model.setTexture(sky_texture)
        skybox_model.setTransparency(TransparencyAttrib.MAlpha)

        # Set up camera
        self.base.disableMouse()
        self.base.camera.setPos(0, 0, 0)
        self.base.camera.reparentTo(self.skybox)
        self.base.camLens.setNear(0.1)

    def run(self):
        self.base.run()
