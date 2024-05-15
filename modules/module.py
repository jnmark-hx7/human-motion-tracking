import pygame
from pygame.locals import *
import modules.assets as assets


def Load_Background(FILENAME,FRAME):
    output = pygame.image.load(FILENAME)
    output = pygame.transform.scale(output,FRAME)
    return output
#end of Func Load_Background
        
class Button:
    def __init__(self,  default_image, # Default Images
                        focus_image,   # Focus Images
                        pos,           # Position of the object
                        rotation,      # Rotation of the certain angle 
                        scale          # Scaling value
                        ):
        self.image = pygame.image.load(default_image) # Read an default image
        self.f_image = pygame.image.load(focus_image) # Reading an focus image
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        # Rescale the images to fit to the display surface
        self.rescale = pygame.transform.rotozoom(self.image,rotation,scale)
        self.f_rescale = pygame.transform.rotozoom(self.f_image,rotation,scale)

        self.rect_pos = self.rescale.get_rect(center = (self.x_pos,self.y_pos))
        self.f_rect_pos = self.f_rescale.get_rect(center=(self.x_pos,self.y_pos))

    
    def display_Button(self, surface,mouse_pos):
        # Display the image loaded into the Button class
        if mouse_pos[0] in range(self.rect_pos.left, self.rect_pos.right) and mouse_pos[1] in range(self.rect_pos.top, self.rect_pos.bottom):
            
            self.f_rect_pos.x = self.rect_pos.x - 10
            surface.blit(self.f_rescale,self.f_rect_pos)
        else:
            surface.blit(self.rescale,self.rect_pos)
    
    def clicked_Button(self,mouse_pos):
        if mouse_pos[0] in range(self.rect_pos.left, self.rect_pos.right) and mouse_pos[1] in range(self.rect_pos.top, self.rect_pos.bottom):
            return True
        else:
            return False
# -- end of Class Button

class Template:
    def __init__(self, default_image,focus_image, pos,rotation, scale):
        self.image = pygame.image.load(default_image) # Read an default image
        self.f_image = pygame.image.load(focus_image) # Reading an focus image
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        # Rescale the images to fit to the display surface
        self.rescale = pygame.transform.rotozoom(self.image,rotation,scale)
        self.f_rescale = pygame.transform.rotozoom(self.f_image,rotation,scale)

        self.rect_pos = self.rescale.get_rect(center = (self.x_pos,self.y_pos))
        self.f_rect_pos = self.f_rescale.get_rect(center=(self.x_pos,self.y_pos))   

    def display_template(self,surface, mouse_pos):
        if mouse_pos[0] in range(self.rect_pos.left, self.rect_pos.right) and mouse_pos[1] in range(self.rect_pos.top, self.rect_pos.bottom):
            self.f_rect_pos.x = self.rect_pos.x -10
            surface.blit(self.f_rescale,self.f_rect_pos)   
        else:
            surface.blit(self.rescale,self.rect_pos)

    def clicked_Template(self,mouse_pos):
        if mouse_pos[0] in range(self.rect_pos.left, self.rect_pos.right) and mouse_pos[1] in range(self.rect_pos.top, self.rect_pos.bottom):
            return True
        else:
            return False
# -- end of Class Template

# import modules.control as control

class Virtual_Companion:
    def __init__(self, pos,rotation, scale):
        self.VC_Animate = Animation(assets.Virtual_Companion,True)
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.scale = scale
        self.rotation = rotation
        # self.face = control.Camera()

        # Dialogue box of the virtual companion
        self.Dialgue_box = Animation(assets.Speech,True)
        
    def get_frame(self):
        current_image = self.VC_Animate.update(0.1)
        image = pygame.image.load(current_image)
        rescale = pygame.transform.rotozoom(image,self.rotation,self.scale)
        rect_pos = rescale.get_rect(center = (self.x_pos,self.y_pos))
        return rescale,rect_pos

    def get_dialouge(self):
        current_dialogue = self.Dialgue_box.update(0.003)
        image = pygame.image.load(current_dialogue)
        rescale = pygame.transform.rotozoom(image,self.rotation,self.scale+0.2)
        rect_pos = rescale.get_rect(center = (self.x_pos, self.y_pos-190))
        return rescale, rect_pos


    def display_template(self,surface):
        render_image,render_pos = self.get_frame()
        
        surface.blit(Load_Background(assets.Render['shadow'],(400,100)),(-5,425))
        surface.blit(render_image,render_pos)
        
        # Output boolean if face detected or not
        # output = self.face.Face_detection()
        render_dialouge, render_d_pos = self.get_dialouge()
        surface.blit(render_dialouge,render_d_pos)    
        # if output == True:
        #     render_dialouge, render_d_pos = self.get_dialouge()
        #     surface.blit(render_dialouge,render_d_pos)
# -- end of Virtual Companion

class Animation:
    def __init__(self,Frame,condition):
        # Calculate how many picture for animation
        # Set count start from zero
        # current image start from count zero
        self.temp = [Frame[value] for value in Frame]
        self.count = 0
        self.current_image = self.temp[self.count]
        self.is_animating = condition

    def update(self,speed):
        if self.is_animating == True:
            self.count += speed
            if self.count >= len(self.temp):
                self.count = 0
            else:
                self.count = self.count
        self.current_image = self.temp[int(self.count)] 
        return self.current_image 
        # setting condition for self loop
        # The speed of the picture transition
        # condition when the count picture reach limit

# -- end of Animation
