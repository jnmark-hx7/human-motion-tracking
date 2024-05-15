# Importing all related library
import pygame
import cv2
from sys import exit
from pygame.locals import *
import modules.assets as assets
import modules.module as mod
import modules.pygamevideo as mod_vid
import modules.control as control_mechanics

SCREEN_FRAME = (1280,720) # 900,600
pygame.init()
camera = control_mechanics.Camera()
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode(SCREEN_FRAME)
pygame.display.set_caption('Final Year Project')


Default_color = (202,228,241)
pointer = pygame.image.load(assets.Default_Btn['cursor']).convert_alpha()
pointer = pygame.transform.rotozoom(pointer,0,0.2)
cpos = pointer.get_rect() #cursor position
# FIXED POSITION OF ASSESTS
# POS = (800,180)
F_SCALE = 0.24
F_SCALE_BTN = 1
F_SCALE_VC = 1
F_ROTATE = 0
F_pos = (1100,200)
F_POS_BACK_LM = (160,550)
F_POS_MENU_TEMP = (640,320)
F_POS_MENU_BACK = (520,535)
F_POS_MENU_LM = (780,535)

# Initialise Virtual Companion
Companion = mod.Virtual_Companion((200,360), F_ROTATE,F_SCALE_VC-0.5)

# Initialise the unique button 
HOB = mod.Button(assets.Default_Btn['HOB'], 
                        assets.Focus_Btn['HOB'],
                        (F_pos[0],F_pos[1]),F_ROTATE,F_SCALE_BTN)
SFM = mod.Button(assets.Default_Btn['SFM Exp'], 
                        assets.Focus_Btn['SFM Exp'],
                        (F_pos[0],F_pos[1]+100),F_ROTATE,F_SCALE_BTN)
UREDD = mod.Button(assets.Default_Btn['UREDD Project'], 
                        assets.Focus_Btn['UREDD Project'],
                        (F_pos[0],F_pos[1]+200),F_ROTATE,F_SCALE_BTN)
Gallery = mod.Button(assets.Default_Btn['Gallery'], 
                        assets.Focus_Btn['Gallery'],
                        (F_pos[0],F_pos[1]+300),F_ROTATE,F_SCALE_BTN)


# Converting them from orthographic projection into isometric projection
# Using equation from the internet where x: (i-j)* halves_width & y: (i+j)*halves_height
#           (0,0), (1,0)        
#           (0,1), (1,1) 
offset = (660,300) #450,250
margin = 100
tmp_width, tmp_height = 72 + margin,56 + margin
tmp_pos = []

# This is show 2 x 2 Matrix
for i in range(2):
    for j in range(2):
        calc_x = offset[0]+(i-j)*tmp_width
        calc_y = offset[1]+(i+j)*0.75*tmp_height
        merge = (calc_x,calc_y)
        tmp_pos.append(merge)

HOB_temp = mod.Template(assets.Default_Temp['HOB'],
                        assets.Focus_Temp['HOB'],
                        tmp_pos[0],F_ROTATE,F_SCALE)
SFM_temp = mod.Template(assets.Default_Temp['SFM Exp'],
                        assets.Focus_Temp['SFM Exp'],
                        tmp_pos[1],F_ROTATE,F_SCALE)
UREDD_temp = mod.Template(assets.Default_Temp['UREDD Project'],
                        assets.Focus_Temp['UREDD Project'],
                        tmp_pos[2],F_ROTATE,F_SCALE)
Gallery_temp = mod.Template(assets.Default_Temp['Gallery'],
                        assets.Focus_Temp['Gallery'],
                        tmp_pos[3],F_ROTATE,F_SCALE)


def HOB_menu():
    HOB_temp = mod.Template(assets.Default_Temp['HOB'],
                        assets.Focus_Temp['HOB'],
                        F_POS_MENU_TEMP,F_ROTATE,0.34)
    first_clicked = True                    
    while True:
        SCREEN.fill(Default_color)
        f,cpos.x,cpos.y = camera.get_position(SCREEN_FRAME[0], SCREEN_FRAME[1])
        Companion.display_template(SCREEN)

        
        Back_btn = mod.Button(assets.Default_Btn['Back'], assets.Focus_Btn['Back'],F_POS_MENU_BACK, F_ROTATE,F_SCALE_BTN-0.2)
        MoreInfo = mod.Button(assets.Default_Btn['More Info'], assets.Focus_Btn['More Info'],F_POS_MENU_LM, F_ROTATE,F_SCALE_BTN-0.2)
        Back_btn.display_Button(SCREEN,cpos)
        MoreInfo.display_Button(SCREEN,cpos)
        HOB_temp.display_template(SCREEN,cpos)
        HOB.display_Button(SCREEN,cpos)
        SFM.display_Button(SCREEN,cpos)
        UREDD.display_Button(SCREEN,cpos)
        Gallery.display_Button(SCREEN,cpos)
        SCREEN.blit(pointer,cpos)
        if Back_btn.clicked_Button(cpos) and camera.test == 'okey' :
            if first_clicked:        
                main()
                first_clicked = False
                exit()
        elif MoreInfo.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:        
                HOB_MORE_INFO()
                first_clicked = False
                exit()
        else:
            first_clicked = True
        cv2.putText(f,f'{camera.test}', (200,100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),4,cv2.LINE_AA)
        cv2.imshow('Camera Feed', f) 


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                           
        pygame.display.update()
        clock.tick(60)
# end of FUNC HOB menu 
def HOB_MORE_INFO():
    Back_btn = mod.Button(assets.Default_Btn['Back'], assets.Focus_Btn['Back'],F_POS_BACK_LM, F_ROTATE,0.6)
    video = mod_vid.Video(assets.Data['HOB'])
    video.set_size((665,448))
    video.play()
    first_clicked = True
    while True:
        
        SCREEN.blit(mod.Load_Background(assets.Interface['HOB'], SCREEN_FRAME), (0,0))
        f,cpos.x,cpos.y = camera.get_position(SCREEN_FRAME[0], SCREEN_FRAME[1])
        video.draw_to(SCREEN,(545,110))
        Back_btn.display_Button(SCREEN,cpos)
        SCREEN.blit(pointer,cpos)
        cv2.putText(f,f'{camera.test}', (200,100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),4,cv2.LINE_AA)
        cv2.imshow('Camera Feed', f)
        if Back_btn.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:        
                video.release()
                HOB_menu()
                first_clicked = False
                exit()
        else:
            first_clicked = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        pygame.display.update()
        clock.tick(60)
# -- end of FUNC HOB_MORE_INFO

def SFM_menu():

    SFM_temp = mod.Template(assets.Default_Temp['SFM Exp'],
                        assets.Focus_Temp['SFM Exp'],
                        F_POS_MENU_TEMP,F_ROTATE,0.34)
    Back_btn = mod.Button(assets.Default_Btn['Back'], assets.Focus_Btn['Back'],F_POS_MENU_BACK, F_ROTATE,F_SCALE_BTN-0.2)
    MoreInfo = mod.Button(assets.Default_Btn['More Info'], assets.Focus_Btn['More Info'],F_POS_MENU_LM, F_ROTATE,F_SCALE_BTN-0.2)
    first_clicked = True
    while True:
        SCREEN.fill(Default_color)
        f,cpos.x,cpos.y = camera.get_position(SCREEN_FRAME[0], SCREEN_FRAME[1])
        cv2.putText(f,f'{camera.test}', (200,100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),4,cv2.LINE_AA)
        cv2.imshow('Camera Feed', f) 
        Companion.display_template(SCREEN)
        Back_btn.display_Button(SCREEN,cpos)
        MoreInfo.display_Button(SCREEN,cpos)
        SFM_temp.display_template(SCREEN,cpos)
        HOB.display_Button(SCREEN,cpos)
        SFM.display_Button(SCREEN,cpos)
        UREDD.display_Button(SCREEN,cpos)
        Gallery.display_Button(SCREEN,cpos)
        SCREEN.blit(pointer,cpos)
        if Back_btn.clicked_Button(cpos) and camera.test == 'okey' :
            if first_clicked:        
                main()
                first_clicked = False
                exit()
        elif MoreInfo.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:        
                SFM_MORE_INFO()
                first_clicked = False
                exit()
        else:
            first_clicked = True     
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                        
        pygame.display.update()
        clock.tick(60)
# end of FUNC SFM Exp menu 
def SFM_MORE_INFO():
    # I am putting all the images into temp for easier navigation of the clicked button
    temp = [assets.SFM_Exp[value] for value in assets.SFM_Exp]
    count = 0 
    current_image = temp[count]
    first_clicked = True
    while True:
        f,cpos.x,cpos.y = camera.get_position(SCREEN_FRAME[0], SCREEN_FRAME[1])
        SCREEN.blit(mod.Load_Background(assets.Interface['SFM'], SCREEN_FRAME), (0,0))
        SCREEN.blit(mod.Load_Background(current_image, (720,460)), (280,131))    
        # Positioning the assets inside the surface display
        new_pos_back = (F_POS_BACK_LM[0],F_POS_BACK_LM[1]-400)
        right_pos = (1060,360)
        left_pos = (220,360)
        Back_btn = mod.Button(assets.Default_Btn['Back'], 
                            assets.Focus_Btn['Back'],
                            new_pos_back, F_ROTATE,0.6)
        Right_btn = mod.Button(assets.Default_Btn['Right'],
                            assets.Focus_Btn['Right'],
                            right_pos,F_ROTATE,0.15)
        Left_btn = mod.Button(assets.Default_Btn['Left'],
                            assets.Focus_Btn['Left'],
                            left_pos,F_ROTATE,0.15)                            

        # print(mpos)
        Back_btn.display_Button(SCREEN,cpos)
        Right_btn.display_Button(SCREEN,cpos)
        Left_btn.display_Button(SCREEN,cpos)
        SCREEN.blit(pointer,cpos)
        cv2.putText(f,f'{camera.test}', (200,100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),4,cv2.LINE_AA)
        cv2.imshow('Camera Feed', f)
        if Back_btn.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:        
                SFM_menu()
                first_clicked = False
                exit()
        elif Right_btn.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:   
                count +=1
                if count == len(temp):
                    count = 0
                else: 
                    count = count
                first_clicked = False
            # current_image = temp[count]
        elif Left_btn.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:
                count -=1
                if count == -1:
                    count = len(temp)-1
                else: 
                    count = count
                first_clicked = False
        else:
            first_clicked = True
        current_image = temp[count]
        # if the button has been not click display the current image
        # if yes change to another image
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
        pygame.display.update()
        clock.tick(60)
# -- end of FUNC SFM_MORE_INFO

def UREDD_menu():
    UREDD_temp = mod.Template(assets.Default_Temp['UREDD Project'],
                        assets.Focus_Temp['UREDD Project'],
                        F_POS_MENU_TEMP,F_ROTATE,0.34)
    first_clicked = True
    while True:
        SCREEN.fill(Default_color)
        Companion.display_template(SCREEN)
        f,cpos.x,cpos.y = camera.get_position(SCREEN_FRAME[0], SCREEN_FRAME[1])
        
        Back_btn = mod.Button(assets.Default_Btn['Back'], assets.Focus_Btn['Back'],F_POS_MENU_BACK, F_ROTATE,F_SCALE_BTN-0.2)
        MoreInfo = mod.Button(assets.Default_Btn['More Info'], assets.Focus_Btn['More Info'],F_POS_MENU_LM, F_ROTATE,F_SCALE_BTN-0.2)
        Back_btn.display_Button(SCREEN,cpos)
        MoreInfo.display_Button(SCREEN,cpos)
        UREDD_temp.display_template(SCREEN,cpos)
        HOB.display_Button(SCREEN,cpos)
        SFM.display_Button(SCREEN,cpos)
        UREDD.display_Button(SCREEN,cpos)
        Gallery.display_Button(SCREEN,cpos)
        SCREEN.blit(pointer,cpos)
        # Activity.display_Button(SCREEN,mpos)
        cv2.putText(f,f'{camera.test}', (200,100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),4,cv2.LINE_AA)
        cv2.imshow('Camera Feed', f) 
        if Back_btn.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:        
                main()
                first_clicked = False
                exit()
        elif MoreInfo.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:        
                UREDD_MORE_INFO()
                first_clicked = False
                exit()
        else:
            first_clicked = True  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                           
        pygame.display.update()
        clock.tick(60)
# end of FUNC UREDD menu
def UREDD_MORE_INFO():
    video = mod_vid.Video(assets.Data['UREDD'])
    video.set_size((665,448))
    video.play()
    first_clicked = True
    while True:
 
        SCREEN.blit(mod.Load_Background(assets.Interface['UREDD'], SCREEN_FRAME), (0,0))
        f,cpos.x,cpos.y = camera.get_position(SCREEN_FRAME[0], SCREEN_FRAME[1])
        video.draw_to(SCREEN,(545,110))
        Back_btn = mod.Button(assets.Default_Btn['Back'], assets.Focus_Btn['Back'],F_POS_BACK_LM, F_ROTATE,0.6)
        Back_btn.display_Button(SCREEN,cpos)
        SCREEN.blit(pointer,cpos)
        cv2.putText(f,f'{camera.test}', (200,100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),4,cv2.LINE_AA)
        cv2.imshow('Camera Feed', f) 
        if Back_btn.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:
                video.release()        
                UREDD_menu()
                first_clicked = False
                exit()
        else:
            first_clicked = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
                
        pygame.display.update()
        clock.tick(60)
# -- end of FUNC UREDD_MORE_INFO                                                                 

def Gallery_menu():
    Gallery_temp = mod.Template(assets.Default_Temp['Gallery'],
                        assets.Focus_Temp['Gallery'],
                        F_POS_MENU_TEMP,F_ROTATE,0.34)
    first_clicked = True
    while True:
        SCREEN.fill(Default_color)
        f,cpos.x,cpos.y = camera.get_position(SCREEN_FRAME[0], SCREEN_FRAME[1])
        Companion.display_template(SCREEN)
        
        Back_btn = mod.Button(assets.Default_Btn['Back'], assets.Focus_Btn['Back'],F_POS_MENU_BACK, F_ROTATE,F_SCALE_BTN-0.2)
        MoreInfo = mod.Button(assets.Default_Btn['More Info'], assets.Focus_Btn['More Info'],F_POS_MENU_LM, F_ROTATE,F_SCALE_BTN-0.2)
        Back_btn.display_Button(SCREEN,cpos)
        MoreInfo.display_Button(SCREEN,cpos)
        Gallery_temp.display_template(SCREEN,cpos)
        HOB.display_Button(SCREEN,cpos)
        SFM.display_Button(SCREEN,cpos)
        UREDD.display_Button(SCREEN,cpos)
        Gallery.display_Button(SCREEN,cpos)
        SCREEN.blit(pointer,cpos)
        cv2.putText(f,f'{camera.test}', (200,100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),4,cv2.LINE_AA)
        cv2.imshow('Camera Feed', f)

        
        if Back_btn.clicked_Button(cpos) and camera.test == 'okey' :
            if first_clicked:        
                main()
                first_clicked = False
                exit()
        elif MoreInfo.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:        
                Gallery_MORE_INFO()
                first_clicked = False
                exit()
        else:
            first_clicked = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                             
        pygame.display.update()
        clock.tick(60)
# end of FUNC Gallery menu
def Gallery_MORE_INFO():
    Gallery_animations = mod.Animation(assets.Gallery,True)
    Back_btn = mod.Button(assets.Default_Btn['Back'], assets.Focus_Btn['Back'],F_POS_BACK_LM, F_ROTATE,0.6)
    first_clicked = True
    while True:
        current_image = Gallery_animations.update(0.05)
        f,cpos.x,cpos.y = camera.get_position(SCREEN_FRAME[0], SCREEN_FRAME[1])
        SCREEN.fill(Default_color)
        SCREEN.blit(mod.Load_Background(assets.Interface['Gallery'], SCREEN_FRAME), (0,0))
        SCREEN.blit(mod.Load_Background(current_image, (665,448)), (545,110))
        Back_btn.display_Button(SCREEN,cpos)
        SCREEN.blit(pointer,cpos)
        
  
        if Back_btn.clicked_Button(cpos) and camera.test == 'okey':
            if first_clicked:        
                Gallery_menu()
                first_clicked = False
                exit()
        else:
            first_clicked = True        
        # Visualization of camera feedback
        cv2.putText(f,f'{camera.test}', (200,100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),4,cv2.LINE_AA)
        cv2.imshow('Camera Feed', f) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
        pygame.display.update()
        clock.tick(60)
# -- end of FUNC Gallery_MORE_INFO 

# Main Function
def main():
    first_clicked = True
    while True:

        SCREEN.fill(Default_color)
        # The implementations of the real-time camera capture
        # has been converted into Camera class
        # camera [lowercase c] is the object of the Camera class
        # hence only extracting following attributes:
        #   f = camera frames
        #   cpos.x = the position of MIDDLE_FINGER_MCP of x
        #   cpos.y = the position of MIDDLE_FINGER_MCP of y
        f,cpos.x,cpos.y = camera.get_position(SCREEN_FRAME[0], SCREEN_FRAME[1])


        HOB.display_Button(SCREEN,cpos)
        SFM.display_Button(SCREEN,cpos)
        UREDD.display_Button(SCREEN,cpos)
        Gallery.display_Button(SCREEN,cpos)

        Companion.display_template(SCREEN)
        HOB_temp.display_template(SCREEN,cpos)
        SFM_temp.display_template(SCREEN,cpos)
        UREDD_temp.display_template(SCREEN,cpos)
        Gallery_temp.display_template(SCREEN,cpos)
        SCREEN.blit(pointer,cpos)

        # The Events handlers for onclick event is active when the hand gesture 'okey' portray
        if HOB.clicked_Button(cpos) or HOB_temp.clicked_Template(cpos) and camera.test == 'okey' :
            if first_clicked:        
                HOB_menu()
                first_clicked = False
                exit()
        elif SFM.clicked_Button(cpos) or SFM_temp.clicked_Template(cpos) and camera.test == 'okey':
            if first_clicked:        
                SFM_menu()
                first_clicked = False
                exit()

        elif UREDD.clicked_Button(cpos) or UREDD_temp.clicked_Template(cpos) and camera.test == 'okey':
            if first_clicked:        
                UREDD_menu()
                first_clicked = False
                exit()

        elif Gallery.clicked_Button(cpos) or Gallery_temp.clicked_Template(cpos) and camera.test == 'okey':
            if first_clicked:        
                Gallery_menu()
                first_clicked = False
                exit()
        else:
            first_clicked = True
        
        # cv2.putText(f,f'open', (200,100),
        #                        cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),4,cv2.LINE_AA)
        
        # Display camera feedback on the screen
        # cv2.imshow('Camera Feed', f) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False     
        pygame.display.update()
        clock.tick(60)
# end of main function
print(camera.cursor_x)
print(camera.cursor_y)
if __name__ == '__main__':
    main()

camera.stop_camera()
pygame.quit()
cv2.destroyAllWindows()