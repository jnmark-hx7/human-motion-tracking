import cv2
import control 

# # List of function
# def BGR2RGB_Conversion(img,model):
#         # To improve performance, optionally mark the image as not writeable
#         # to  pass by reference
#         image = cv2.cvtColor(cv2.flip(img,1), cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
#         image.flags.writeable = False                  # Image is not writeable
#         results = model.process(image)                 # Processing the feedback of object detected
#         image.flags.writeable = True                   # Image is now writeable
#         image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)  # COLOR CONVERSION RGB 2 BGR
        
#         return image,results
# # ----- end of FUNC: BGR2RGB_Conversion
# class Face_Detection:
#     def __init__(self):
#         self.mp_holistic = mp.solutions.holistic
#         self.mp_drawing = mp.solutions.drawing_utils
#         self.holi = self.mp_holistic.Holistic(
#                             min_detection_confidence = 0.5,
#                             min_tracking_confidence = 0.5)
        
#     # end of --init--
    
#     def FACE_MESH_Annotation(self,frame):
#         image,results = BGR2RGB_Conversion(frame,self.holi)
#         if results.face_landmarks:
#             # This is drawing utility of drawing annotation of the face mesh for detected face
#             self.mp_drawing.draw_landmarks(  image,
#                                         results.face_landmarks,
#                                         self.mp_holistic.FACEMESH_CONTOURS,
#                                         self.mp_drawing.DrawingSpec(color = (80,110,10), 
#                                                                thickness = 1, circle_radius = 1),
#                                         self.mp_drawing.DrawingSpec(color = (80,256,121), 
#                                                                thickness = 1, circle_radius = 1))

#         return image,results
# # ---- end of FUNC : FACE_MESH_Annotaion


# curr_camera = 0
# cap = cv2.VideoCapture(curr_camera)
face = control.Camera()
while True:
    # # Read the camera feedback
    # success, frame = cap.read()
    # Error handling if there are no camera detected
    # if not success:
    #     print("Ignoring empty camera frame")
    #     break
    # Getting the generated face mesh for face detection purposes
    output = face.Face_detection()
    print(output)
    
    # Camera output of detected faces, output
    # cv2.putText(image,f'{output}', (200,100),
    #                            cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),4,cv2.LINE_AA)
    
    # cv2.imshow('Camera Feed', image)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    # --> end of while loop
# Destroy gracefully all running background application after this
face.stop_camera()
cv2.destroyAllWindows()