import cv2
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import mediapipe as mp
import math
  
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)
mp_drawing = mp.solutions.drawing_utils
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

faces = [
    (0,1,2,3),
    (4,5,6,7),
    (0,1,5,4),
    (2,3,7,6),
    (1,2,6,5),
    (4,7,3,0)
]

def draw_cube():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.0, 1.0, 1.0, 0.1)
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    glLineWidth(5)
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def get_pinch_strength(hand_landmarks):
    """Returns a value between 0 (fully open) and 1 (fully pinched)"""
    if hand_landmarks is None:
        return 0

    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]

    

    distance = math.sqrt(
        (thumb_tip.x - index_tip.x)**2 +
        (thumb_tip.y - index_tip.y)**2
    )
    

    min_dist = 0.02  
    max_dist = 0.2  
    pinch_strength = 1 - min(1, max(0, (distance - min_dist) / (max_dist - min_dist)))
    
    return pinch_strength


hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)


pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -7)
glEnable(GL_DEPTH_TEST)


rotate_x = 0
rotate_y = 0
zoom_z = -7 
zoom_speed = 0.1
last_pinch_strength = 0


last_x = None
last_y = None


clock = pygame.time.Clock()
running = True
while running:
   
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False


    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    current_pinch_strength = 0
    
    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        index_tip = hand_landmarks.landmark[8]
        frame_h, frame_w, _ = frame.shape
        cx, cy = int(index_tip.x * frame_w), int(index_tip.y * frame_h)


        current_pinch_strength = get_pinch_strength(hand_landmarks)
        
     
        pinch_change = current_pinch_strength - last_pinch_strength
        zoom_z -= pinch_change * zoom_speed * 120 
        
    
        zoom_z = max(-15, min(-0.2, zoom_z))
        
        if last_x is not None and last_y is not None:
            dx = cx - last_x
            dy = cy - last_y
            rotate_y += dx * 0.5  
            rotate_x += dy * 0.5  

        last_x, last_y = cx, cy
    else:
        last_x = last_y = None
    
    last_pinch_strength = current_pinch_strength


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, zoom_z)  
    glRotatef(rotate_x, 1, 0, 0)
    glRotatef(rotate_y, 0, 1, 0)
    draw_cube()
    
    pygame.display.flip()
    clock.tick(60)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
