# I actually have this code in a jupyter notebook.

from JGE import *
from JGE2D import Model as M2D, Renderer as R2D
from JGEManual import Renderer as RM



engine = Engine()



r2d = R2D(engine)
engine.modules.append(r2d)

rm = RM(engine)
engine.modules.append(rm)



engine.start()



task = engine.scheduler.schedule(lambda: GLFW.set_window_title(engine.window, "UPS: {u}".format(u=engine.ups.get())), delay=1, interval=1)

texture = Texture.create_from_png("res/TreeTexture.png")
r2d.models.append(M2D(texture, 0, -.5))



engine.loop()



engine.end()
