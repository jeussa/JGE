import numpy as np
from OpenGL import GL

from JGE import Console
from JGEMath import Matrix4



# =========
# = Model =
# =========
class Model:

    def __init__(self, texture, x, y, roll = 0, scale_x = 1, scale_y = 1, invert_y = True):
        self.texture = texture
        self.x = x
        self.y = y
        self.roll = roll
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.invert_y = invert_y
    

    # = Generate Translation Matrix =
    def generate_translation_matrix(self):
        matrix = Matrix4.create()

        matrix = Matrix4.rotate(matrix, self.roll, 0, 0, 1)
        matrix = Matrix4.translate(matrix, self.x, self.y, 0)
        matrix = Matrix4.scale(matrix, self.scale_x, self.scale_y, 1)

        return matrix



# ============
# = Renderer =
# ============
class Renderer:

    def __init__(self, engine):
        self.engine = engine
        self.models = []

        self.vao = None
        self.vbo = None
        self.shader = None
    
    
    # = On Enable =
    def on_enable(self):
        # Create VAO
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)

        GL.glBufferData(GL.GL_ARRAY_BUFFER, np.array([
            -.5, .5, -.5, -.5, .5, .5, .5, -.5
        ], np.float32), GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, False, 0, 0)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

        # Load Shader
        self.shader = [GL.glCreateProgram()]

        for program in [["lib/JGE2D.vs.glsl", GL.GL_VERTEX_SHADER], ["lib/JGE2D.fs.glsl", GL.GL_FRAGMENT_SHADER]]:
            input = open(program[0], 'r')

            id = GL.glCreateShader(program[1])
            GL.glShaderSource(id, input.read())
            GL.glCompileShader(id)

            input.close()

            if GL.glGetShaderiv(id, GL.GL_COMPILE_STATUS) == GL.GL_FALSE:
                Console.error("Failed to compile shader !")
                Console.error(GL.glGetProgramInfoLog(id))
                raise ValueError("Failed to compile shader !")

            self.shader.append(id)
        
        GL.glAttachShader(self.shader[0], self.shader[1])
        GL.glAttachShader(self.shader[0], self.shader[2])

        GL.glLinkProgram(self.shader[0])

        if GL.glGetProgramiv(self.shader[0], GL.GL_LINK_STATUS) == GL.GL_FALSE:
            raise ValueError("Failed to link shader programs !")
        
        self.uv_InvertY = GL.glGetUniformLocation(self.shader[0], "in_InvertY")
        self.uv_ObjPos = GL.glGetUniformLocation(self.shader[0], "in_ObjPos")

    

    # = On Loop =
    def on_loop(self):
        if not self.models:
            return
        
        # Prepare
        GL.glUseProgram(self.shader[0])
        GL.glBindVertexArray(self.vao)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glEnableVertexAttribArray(0)
        GL.glBindAttribLocation(self.shader[0], 0, "in_Vector")

        # Render
        for model in self.models:
            GL.glActiveTexture(GL.GL_TEXTURE0)
            GL.glBindTexture(GL.GL_TEXTURE_2D, model.texture.handle)

            GL.glUniformMatrix4fv(self.uv_ObjPos, 1, False, np.matrix.flatten(model.generate_translation_matrix()))
            GL.glUniform1f(self.uv_InvertY, 1 if model.invert_y else 0)

            GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, 4)

        # Cleanup
        GL.glUseProgram(0)
        GL.glDisableVertexAttribArray(0)
        GL.glBindVertexArray(0)
    

    # = On Disable =
    def on_disable(self):
        if self.vbo is not None:
            GL.glDeleteBuffers(1, [self.vbo])
            self.vbo = None
        
        if self.vao is not None:
            GL.glDeleteVertexArrays(1, [self.vao])
            self.vao = None
        
        if self.shader is not None:
            GL.glUseProgram(0)

            GL.glDetachShader(self.shader[0], self.shader[1])
            GL.glDetachShader(self.shader[0], self.shader[2])

            GL.glDeleteShader(self.shader[1])
            GL.glDeleteShader(self.shader[2])
            GL.glDeleteProgram(self.shader[0])

            self.shader = None
