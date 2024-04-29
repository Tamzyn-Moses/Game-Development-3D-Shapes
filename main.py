import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from pyramid import draw_pyramid
from prism import draw_prism
from cube import draw_cube

models = [draw_pyramid, draw_prism, draw_cube]
current_model = 0
translation_vectors = [(0, 0, -5)] * len(models)
rotation_angles = [(0, 0, 0)] * len(models)
scaling_factors = [(1, 1, 1)] * len(models)

class Display:
    def __init__(self):
        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glClearColor(0.9, 0.7, 0.9, 1.0)  

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.handle_keys(event.key)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPushMatrix()
            self.apply_transformations()
            models[current_model]()
            glPopMatrix()
            pygame.display.flip()
            pygame.time.wait(10)

    def handle_keys(self, key):
        global current_model, translation_vectors, rotation_angles, scaling_factors
        if key == pygame.K_SPACE:
            current_model = (current_model + 1) % len(models)
        elif key == pygame.K_LEFT:
            translation_vectors[current_model] = (translation_vectors[current_model][0] - 0.1, translation_vectors[current_model][1], translation_vectors[current_model][2])
        elif key == pygame.K_RIGHT:
            translation_vectors[current_model] = (translation_vectors[current_model][0] + 0.1, translation_vectors[current_model][1], translation_vectors[current_model][2])
        elif key == pygame.K_UP:
            translation_vectors[current_model] = (translation_vectors[current_model][0], translation_vectors[current_model][1] + 0.1, translation_vectors[current_model][2])
        elif key == pygame.K_DOWN:
            translation_vectors[current_model] = (translation_vectors[current_model][0], translation_vectors[current_model][1] - 0.1, translation_vectors[current_model][2])
        elif key == pygame.K_1:
            translation_vectors[current_model] = (translation_vectors[current_model][0], translation_vectors[current_model][1], translation_vectors[current_model][2] + 0.1)
        elif key == pygame.K_2:
            translation_vectors[current_model] = (translation_vectors[current_model][0], translation_vectors[current_model][1], translation_vectors[current_model][2] - 0.1)
        elif key == pygame.K_a:
            rotation_angles[current_model] = (rotation_angles[current_model][0] + 5, rotation_angles[current_model][1], rotation_angles[current_model][2])
        elif key == pygame.K_d:
            rotation_angles[current_model] = (rotation_angles[current_model][0] - 5, rotation_angles[current_model][1], rotation_angles[current_model][2])
        elif key == pygame.K_w:
            rotation_angles[current_model] = (rotation_angles[current_model][0], rotation_angles[current_model][1] + 5, rotation_angles[current_model][2])
        elif key == pygame.K_s:
            rotation_angles[current_model] = (rotation_angles[current_model][0], rotation_angles[current_model][1] - 5, rotation_angles[current_model][2])
        elif key == pygame.K_q:
            rotation_angles[current_model] = (rotation_angles[current_model][0], rotation_angles[current_model][1], rotation_angles[current_model][2] + 5)
        elif key == pygame.K_e:
            rotation_angles[current_model] = (rotation_angles[current_model][0], rotation_angles[current_model][1], rotation_angles[current_model][2] - 5)
        elif key == pygame.K_MINUS:
            scaling_factors[current_model] = tuple(s * 0.9 for s in scaling_factors[current_model])
        elif key == pygame.K_EQUALS:
            scaling_factors[current_model] = tuple(s * 1.1 for s in scaling_factors[current_model])

    def apply_transformations(self):
        glTranslatef(*translation_vectors[current_model])
        x_angle, y_angle, z_angle = rotation_angles[current_model]
        glRotatef(x_angle, 1, 0, 0)
        glRotatef(y_angle, 0, 1, 0)
        glRotatef(z_angle, 0, 0, 1)
        sx, sy, sz = scaling_factors[current_model]
        glScalef(sx, sy, sz)

if __name__ == "__main__":
    display = Display()
    display.main_loop()