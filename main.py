import ctypes
import itertools
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from pygame.locals import *


class MandelbrotViewer:

    VERTEX_SHADER = """
        #version 330
        in vec2 position;
        void main()
        {
           gl_Position = vec4(position, 0.0, 1.0);
        }
    """

    FRAGMENT_SHADER = """
        #version 330
        uniform vec2 center;
        uniform float scale;
        uniform int max_iter;
        out vec4 out_color;
        void main() {
            vec2 z = vec2(0.0, 0.0);
            vec2 c = (gl_FragCoord.xy / vec2(800, 800)) * scale + center;
            int i;
            for(i = 0; i < max_iter; ++i) {
                if((z.x*z.x + z.y*z.y) > 4.0) break;
                vec2 new_z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
                z = new_z;
            }
            float color = float(i) / float(max_iter);
            out_color = vec4(color*6, color*color, sqrt(color), 1.0);  // Original color scheme
        }
    """

    def __init__(self):
        pygame.init()
        self.display = (1280, 720)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        self.shader = self.compile_shaders()

    def compile_shaders(self):
        shader = compileProgram(compileShader(self.VERTEX_SHADER, GL_VERTEX_SHADER),
                                compileShader(self.FRAGMENT_SHADER, GL_FRAGMENT_SHADER))
        return shader

    def draw(self, shader, center, scale, max_iter):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(shader)
        glUniform2f(glGetUniformLocation(shader, "center"), center[0], center[1])
        glUniform1f(glGetUniformLocation(shader, "scale"), scale)
        glUniform1i(glGetUniformLocation(shader, "max_iter"), max_iter)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        pygame.display.flip()

    def generate_zoom_positions(self, initial_center, initial_scale, max_zoom_level, zoom_factor):
        center = list(initial_center)
        scale = initial_scale
        zoom_level = 0

        while True:
            yield center, scale
            center[0] *= zoom_factor
            center[1] *= zoom_factor
            scale *= zoom_factor

            zoom_level += 1
            if zoom_level >= max_zoom_level:
                zoom_level = 0

    def main(self):
        # Initial settings
        initial_center = [0.0, 0.0]
        initial_scale = 1.0
        initial_max_iter = 2000
        initial_zoom_modifier = 0.05

        # Parameters for the zoom effect
        max_zoom_level = 10
        zoom_factor = 0.95  # Decreased the default zoom ratio

        # Create an infinite iterator of zoom positions
        zoom_positions = itertools.cycle(
            self.generate_zoom_positions(initial_center, initial_scale, max_zoom_level, zoom_factor))

        # Initialize settings
        center = initial_center[:]
        scale = initial_scale
        max_iter = initial_max_iter
        zoom_modifier = initial_zoom_modifier

        # Generate vertices and bind to VBO
        VBO = glGenBuffers(1)
        vertices = [-1, -1, 1, -1, -1, 1, 1, 1]
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (ctypes.c_float * len(vertices))(*vertices), GL_STATIC_DRAW)
        glVertexAttribPointer(glGetAttribLocation(self.shader, "position"), 2, GL_FLOAT, GL_FALSE, 0,
                              ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glEnableClientState(GL_VERTEX_ARRAY)

        # Initialize control variables
        auto_path_follow = False
        mouse_follow = False
        mouse_last_pos = pygame.mouse.get_pos()
        arrow_keys = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        scale *= (1 - zoom_modifier * 0.1)  # Zoom in
                    elif event.button == 5:
                        scale *= (1 + zoom_modifier * 0.1)  # Zoom out
                elif event.type == pygame.KEYDOWN:
                    if event.key in arrow_keys:
                        arrow_keys[event.key] = True
                    elif event.key == pygame.K_m:
                        mouse_follow = not mouse_follow  # Toggle mouse following
                        mouse_last_pos = pygame.mouse.get_pos()  # Update last mouse position on toggle
                    elif event.key == pygame.K_p:
                        auto_path_follow = not auto_path_follow  # Toggle auto path following
                    elif event.key == pygame.K_1:
                        zoom_modifier += 0.01  # Increase zoom modifier
                    elif event.key == pygame.K_2:
                        zoom_modifier -= 0.01 if zoom_modifier > initial_zoom_modifier else 0.0  # Decrease zoom modifier, but not less than the initial value
                    elif event.key == pygame.K_r:
                        center = initial_center[:]
                        scale = initial_scale
                        max_iter = initial_max_iter
                        zoom_modifier = initial_zoom_modifier
                        mouse_follow = False
                        auto_path_follow = False
                elif event.type == pygame.KEYUP:
                    if event.key in arrow_keys:
                        arrow_keys[event.key] = False

            if mouse_follow:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos != mouse_last_pos:
                    mouse_offset = [(mouse_pos[0] - mouse_last_pos[0]) / self.display[0],
                                    (mouse_pos[1] - mouse_last_pos[1]) / self.display[1]]
                    center[0] -= mouse_offset[0] * scale
                    center[1] += mouse_offset[1] * scale  # Inverted movement direction
                    mouse_last_pos = mouse_pos

            if auto_path_follow and not mouse_follow:
                center, scale = next(zoom_positions)

            if not auto_path_follow and not mouse_follow:
                move_step = 0.01 * scale  # Movement speed now scales with the zoom level
                if arrow_keys[pygame.K_UP]:
                    center[1] += move_step  # Move up
                if arrow_keys[pygame.K_DOWN]:
                    center[1] -= move_step  # Move down
                if arrow_keys[pygame.K_LEFT]:
                    center[0] -= move_step  # Move left
                if arrow_keys[pygame.K_RIGHT]:
                    center[0] += move_step  # Move right

            zoom_modifier *= 0.99 if zoom_modifier > initial_zoom_modifier else 1.0  # Slow down zooming as we zoom in more

            self.draw(self.shader, center, scale, max_iter)
            pygame.display.flip()

if __name__ == "__main__":
    mandelbrot_viewer = MandelbrotViewer()
    mandelbrot_viewer.main()