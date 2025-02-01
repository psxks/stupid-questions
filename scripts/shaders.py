
import moderngl, pygame
from array import array

BASE_PATH = 'shaders/'

class Shader():
    def __init__(self, vert_path, frag_path):
        
        self.vert = open(BASE_PATH + vert_path + '.vert', 'r').read()
        self.frag = open(BASE_PATH + frag_path + '.frag', 'r').read()

        self.ctx = moderngl.create_context()
        
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0,
        ]))
        
        self.program = self.ctx.program(vertex_shader=self.vert, fragment_shader=self.frag)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
    
    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA' 
        tex.write(surf.get_view('1'))
        return tex
    
    def render(self, surf, t, gravity, speed):
        frame_tex = self.surf_to_texture(surf)
        frame_tex.use(0)
        
        self.program['tex'].value = 0
        self.program['time'].value = t
        self.program['gravity'].value = gravity
        self.program['speed'].value = speed

        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
        frame_tex.release()