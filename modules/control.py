# Control mechanics for the GUI
from sys import exit
from pygame.locals import *

# Importing all related library
import cv2
import mediapipe as mp
import numpy as np
import pickle

# BGR2RGB_Conversion: It is a function that converting the visual media
# from BGR 2 RGB format (cond. for mediapipe pipelines) for detecting
# the hand landmark 
def BGR2RGB_Conversion(raw_img, model):
# To improve performance, optionally mark the image as not writeable
# to  pass by reference
    image= cv2.cvtColor(cv2.flip(raw_img,1), cv2.COLOR_BGR2RGB) 
    image.flags.writeable = False                  # Image is not writeable
    results = model.process(image)                 # Made Prediction
    image.flags.writeable = True                   # Image is now writeable
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)  # COLOR CONVERSION RGB 2 BGR
    return image,results
# ----- end of FUNC: BGR2RGB_Conversion


with open('modules/model_classifer.pkl', 'rb') as f:
    loaded_clf = pickle.load(f)

class Hand_Detection:
    LM_set = []
    X_set=[]
    Y_set =[]
    Z_set = [] 
    overall = []
    def __init__(self, 
                 max_num = 1,
                 min_detect = 0.5,
                 min_track = 0.5):
        self.max_num = max_num
        self.min_detect = min_detect
        self.min_track = min_track
        
        
        # Mediapipe Solutions - Hands Detection
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.test_hands = self.mp_hands.Hands(max_num_hands = self.max_num,
                                    min_detection_confidence = self.min_detect,
                                    min_tracking_confidence = self.min_track)
    # -- end of def __init__
    
    def Hand_Annotations(self, raw_img):
 
        h,w,c = raw_img.shape
        image, results = BGR2RGB_Conversion(raw_img, self.test_hands)
        # If there are hands detection, the results presence hence proceed
        # hand landmarks extraction procedure
        if results.multi_hand_landmarks:

            for hand_presence in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(image,
                                                hand_presence,
                                                self.mp_hands.HAND_CONNECTIONS)
                

            
                for idx,lm in enumerate(hand_presence.landmark):
                    rep = hand_presence.landmark[idx]
                    inst = idx # landmark of the hands, 0 - 20
                    x_value = rep.x*w
                    y_value = rep.y*h
                    z_value = rep.z

                    
                    # append all the 21 LM into their resp features_traits
                    # The expected output will shown as below:
                    # LM_set = [0 ... 20]  == 21 LM
                    # X_set, Y_set, Z_set = [n ... n = 20]
                    self.LM_set.append(inst)
                    self.X_set.append(x_value)
                    self.Y_set.append(y_value)
                    self.Z_set.append(z_value)
                    if idx >= 20:
                        temp = {'index' : self.LM_set,'x' : self.X_set,'y': self.Y_set,'z' : self.Z_set}
                        self.overall.append(temp)
                        self.LM_set = []
                        self.X_set = []
                        self.Y_set = []
                        self.Z_set = []
                         
        # only outputing the image for visual output of the hand landmark
        # on the main function
        return image, self.overall, results
    # -- end of Hand Annotations
    
# --> End class Hand_Detection
class Face_Detection:
    def __init__(self):
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.holi = self.mp_holistic.Holistic(
                            min_detection_confidence = 0.5,
                            min_tracking_confidence = 0.5)
        
    # end of --init--
    
    def FACE_MESH_Annotation(self,frame):
        image,results = BGR2RGB_Conversion(frame,self.holi)
        if results.face_landmarks:
            # This is drawing utility of drawing annotation of the face mesh for detected face
            self.mp_drawing.draw_landmarks(  image,
                                        results.face_landmarks,
                                        self.mp_holistic.FACEMESH_CONTOURS,
                                        self.mp_drawing.DrawingSpec(color = (80,110,10), 
                                                               thickness = 1, circle_radius = 1),
                                        self.mp_drawing.DrawingSpec(color = (80,256,121), 
                                                               thickness = 1, circle_radius = 1))

        return results
# ---- end of FUNC : FACE_MESH_Annotaion

# Camera Class
class Camera:
    def __init__(self):
        self.current_camera = 0
        self.cap = cv2.VideoCapture(self.current_camera)
        self.extract_input = []
        self.output_classifier = []
        self.test = 0
        self.hands = Hand_Detection() #Initialise an hand detection object
        self.face = Face_Detection()
        self.cursor_x = 0
        self.cursor_y = 0
        self.update_x = self.cursor_x
        self.update_y = self.cursor_y
    # end of --init--
    def Input_extraction(self):
        success, frame = self.cap.read()
        if not success:
            print('No Camera has detected.')
        
        image,extract,soln = self.hands.Hand_Annotations(frame)
              
        # Finding the index, coords of the finger coordinates
        for idx,value in enumerate(extract):
            extract_index = extract[idx]['index']
            extract_x = extract[idx]['x']
            extract_y = extract[idx]['y']
            extract_z = extract[idx]['z']
            merge = np.array([extract_index,extract_x, extract_y,extract_z]).flatten()
            self.output_classifier.append(merge)
            self.test =loaded_clf.predict(self.output_classifier)[-1]
            self.output_classifier = [] # dumping all the existiing data for smoother transition
            merge = []
            # Camera Capture feedback of test value
            
        return image,soln
    # end of Input_extraction
    # Cleanup memory for fast allocation
    def Face_detection(self):
        success, frame = self.cap.read()
        if not success:
            print('No Camera has detected.')

        # Getting the generated face mesh for face detection purposes
        results = self.face.FACE_MESH_Annotation(frame)
        
        if not results.face_landmarks:
            output = False
        else:
            output = True
        return output
    # end of Face_detection
    def get_position(self,SCREEN_WIDTH,SCREEN_HEIGHT):
        image,soln = self.Input_extraction()
        
        # Using the predicted `pickle` model for recognizing hand gesture
        # Hand gesture `pointer` only can move the cursor
        if soln.multi_hand_landmarks:
            for hand_presence in soln.multi_hand_landmarks:
                # Retrieve the x,y coord of index fingers
                self.cursor_x = int(hand_presence.landmark[9].x*SCREEN_WIDTH)
                self.cursor_y = int(hand_presence.landmark[9].y*SCREEN_HEIGHT)   
                   
        return image,self.cursor_x, self.cursor_y
    
    def stop_camera(self):
        return self.cap.release()
# --> End class Camera


