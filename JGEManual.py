from OpenGL import GL



# ============
# = Renderer =
# ============
class Renderer:

    def __init__(self, engine):
        self.engine = engine
    
    # = On Loop =
    def on_loop(self):
        GL.glColor3f(0., 0., 1.)
        GL.glPointSize(5.)
        GL.glBegin(GL.GL_POINTS)
        GL.glVertex2f(.25, 0.)
        GL.glEnd()
        GL.glFlush()
