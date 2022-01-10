import numpy as np

import os
import platform
import sys
import time

from PIL import Image
import traceback

import glfw as GLFW
from OpenGL import GL



# ===========
# = Console =
# ===========
class Console:

    def debug(message):
        print(message)

    def error(message):
        print(message)
    
    def info(message):
        print(message)
    
    def gl_error(error, description):
        print(error)
        print(description)



# ==========
# = Engine =
# ==========
class Engine:

    def __init__(self, fps = 60):
        self.modules = []
        self.sync = Sync(fps)
        self.ups = UPS()
        self.scheduler = Scheduler()
    

    # = Start =
    def start(self):
        self.startat = time.time()

        Console.info("==========================================================================")
        Console.info("os.name == \"{a}\"".format(a=os.name))
        Console.info("sys.platform == \"{a}\"".format(a=sys.platform))
        Console.info("platform.system() == \"{a}\"".format(a=platform.system()))
        Console.info("platform.machine() == \"{a}\"".format(a=platform.machine()))
        Console.info("platform.architecture() == \"{a}\"".format(a=platform.architecture()))
        Console.info("sys.version == \"{a}\"".format(a=sys.version))
        Console.info("==========================================================================")

        # Initialize
        if not GLFW.init():
            raise ValueError("Failed to initialize GLFW !")
        GLFW.set_error_callback(Console.gl_error)

        # Load modules
        Console.info("Loading modules ...")
        self.__call_modules__("on_load")
        
        # Configure GLFW
        GLFW.default_window_hints()

        # Create window
        self.window = GLFW.create_window(800, 600, "jeussa Graphics Engine", None, None)
        if not self.window:
            raise ValueError("Failed to create GLFW window !")
        GLFW.make_context_current(self.window)

        # Clear window
        GL.glClearColor(0, .8, 0, 0)

        # Enable modules
        Console.info("Enabling modules ...")
        self.__call_modules__("on_enable")

        # Finish
        Console.info("Startup done! [{a} ms]".format(a=round((time.time()-self.startat)*1000)))
    

    # = Loop =
    def loop(self):
        Console.info("Entering loop ...")

        while not GLFW.window_should_close(self.window):
            self.sync.start()

            # Events
            GLFW.poll_events()

            # Scheduler
            self.scheduler.poll()

            # Clear buffers
            GL.glViewport(0, 0, *GLFW.get_window_size(self.window))
            GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

            # Loop modules
            self.__call_modules__("on_loop")
            
            # Update window
            GLFW.swap_buffers(self.window)

            self.ups.tick()
            self.sync.end()
        
        Console.info("Exiting loop ...")
    

    # = End =
    def end(self):
        Console.info("Disabling modules ...")
        self.__call_modules__("on_disable")

        Console.info("Stopping JGEngine ...")
        GLFW.terminate()
        Console.info("JGEngine stopped")
    

    # = Call Modules =
    def __call_modules__(self, func):
        for module in self.modules:
            if hasattr(module.__class__, func):
                attr = getattr(module.__class__, func)
                if callable(attr):
                    try:
                        attr(module)
                    except Exception:
                        traceback.print_exc()
                        self.modules.remove(module)



# =============
# = Scheduler =
# =============
class Scheduler:

    def __init__(self):
        self.tasks = []
        self.jid = 0
    

    # = Cancel =
    def cancel(self, id):
        for task in self.tasks:
            if task[0] == id:
                self.tasks.remove(task)
                return True
        return False
    

    # = Poll =
    def poll(self):
        now = time.time()
        for task in self.tasks:
            if task[2] <= now:
                try:
                    task[1]()
                    if task[4] == 0:                # End of repeat -> cancel
                        self.tasks.remove(task)
                    else:                           # Repeat
                        task[2] += task[3]
                        if task[4] > 0:
                            task[4] -= 1
                except Exception:
                    traceback.print_exc()
                    self.tasks.remove(task)
    

    # = Schedule =
    def schedule(self, func, delay, interval = -1, limit = -1):
        self.jid += 1
        self.tasks.append([
            self.jid,                   # Identifier
            func,                       # The function to be executed
            delay + time.time(),        # Time at which to execute (if < 0, don't execute)
            interval,                   # After execution, repeat after this many seconds (if <=0, don't repeat)
            limit                       # After this many executions, cancel task (if < 0, don't cancel)
        ])
        return self.jid



# ========
# = Sync =
# ========
class Sync:

    def __init__(self, cap = 60):
        self.set_cap(cap)
        self.tick_start = -1
    
    def get_cap(self):
        return self.cap
    
    def set_cap(self, cap):
        self.cap = cap
        self.tick_time = 1.0 / cap
    
    def start(self):
        self.tick_start = time.time()
    
    def end(self):
        if self.tick_start > 0:
            try:
                time.sleep(self.tick_start + self.tick_time - time.time())
            except:
                return



# ===========
# = Texture =
# ===========
class Texture:

    # = Create From PNG =
    def create_from_png(file):
        image = Image.open(file)
        return Texture.create_from_png_data(np.array(list(image.getdata()), np.uint8), image.size[0], image.size[1])
    
    def create_from_png_data(data, width, height):
        handle = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, handle)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        return Texture(handle, width, height)
    

    def __init__(self, handle, width, height):
        self.handle = handle
        self.width = width
        self.height = height
    

    # = Dispose =
    def dispose(self):
        if self.handle is None:          # Already disposed
            return
        
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glDeleteTexture(self.handle)
        self.handle = None
    

    # = Filter =
    def filter(self, min, mag):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.handle)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, min)
        GL.glTexParamteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, max)
    

    # = Generate Mipmaps =
    def generate_mipmaps(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.handle)
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)



# =======
# = UPS =
# =======
class UPS:

    def __init__(self):
        self.ups = 0
        self.reset()
    
    def get(self):
        return self.ups
    
    def reset(self):
        self.time = time.time() + 1.
        self.count = 0
    
    def tick(self):
        self.count += 1
        if time.time() >= self.time:
            self.ups = self.count
            self.reset()
