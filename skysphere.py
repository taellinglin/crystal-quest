import random
from panda3d.core import Geom, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomTriangles, Texture
from panda3d.core import Vec3, Point3, TransformState, NodePath, PandaNode, GeomNode
from panda3d.core import Shader, ShaderAttrib, Filename, TextureStage, SamplerState
from pathlib import Path
import math

class SkySphere:
    def __init__(self, base):
        self.base = base
        self.skybox = NodePath("skybox")
        self.texture_path = self.get_random_skysphere_texture()

        self.generate_skybox()

    def get_random_skysphere_texture(self):
        texture_dir = Path("./skyspheres")
        texture_files = list(texture_dir.glob("*.jpg"))
        if texture_files:
            return random.choice(texture_files)
        return None
    
    def generate_skybox(self):
        if self.texture_path:
            # Load texture
            texture = self.base.loader.loadTexture(str(self.texture_path))
            texture.setWrapU(Texture.WM_repeat)
            texture.setWrapV(Texture.WM_clamp)

            # Create sky sphere geometry
            format = GeomVertexFormat.getV3t2()
            vdata = GeomVertexData("skybox", format, Geom.UH_static)
            vdata.setNumRows(24)
            vertex = GeomVertexWriter(vdata, "vertex")
            texcoord = GeomVertexWriter(vdata, "texcoord")

            # Define sky sphere vertices and UV coordinates
            segments = 32
            rings = 16
            for i in range(rings + 1):
                v = i / rings
                phi = (v - 0.5) * math.pi

                for j in range(segments + 1):
                    u = j / segments
                    theta = u * 2.0 * math.pi

                    x = math.cos(theta) * math.cos(phi)
                    y = math.sin(theta) * math.cos(phi)
                    z = math.sin(phi)

                    vertex.addData3f(x, y, z)
                    texcoord.addData2f(u, v)

            # Define sky sphere triangles
            prim = GeomTriangles(Geom.UH_static)
            for i in range(rings):
                for j in range(segments):
                    v0 = i * (segments + 1) + j
                    v1 = v0 + segments + 1
                    v2 = v0 + 1
                    v3 = v1 + 1

                    prim.addVertices(v0, v2, v1)
                    prim.addVertices(v2, v3, v1)
            prim.closePrimitive()

            geom = Geom(vdata)
            geom.addPrimitive(prim)

            node = GeomNode("skysphere")
            node.addGeom(geom)

            # Create sky sphere node path
            self.skysphere = self.base.render.attachNewNode(node)
            self.skysphere.setShaderAuto()
            self.skysphere.setDepthWrite(False)

            # Apply texture to sky sphere
            self.skysphere.setTexture(texture, 1)


    def update(self, task):
        self.skybox.setPos(self.base.camera.getPos(self.base.render))
        self.skybox.setHpr(self.base.camera.getHpr(self.base.render))

        return task.cont

    def run(self):
        self.base.taskMgr.add(self.update, "update_task")
