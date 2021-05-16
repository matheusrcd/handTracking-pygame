from cv2 import cv2
import os

import HandTracking as htm
import pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand Tracking Game")

FPS = 30
GRAVITY = 0.5
VEL = [10, 0.1]

RED_RECTANGLE_IMAGE = pygame.image.load(os.path.join("Assets", "red_rectangle.png"))
CLAW_IMAGE = pygame.image.load(os.path.join("Assets", "red_claw.png"))

def draw_window(claw, rectangle):
    WIN.fill((255, 255, 255))
    WIN.blit(CLAW_IMAGE, (claw.x, claw.y))
    WIN.blit(RED_RECTANGLE_IMAGE, (rectangle.x, rectangle.y))
    
    pygame.display.update()


def main():
    claw = pygame.Rect(400, 0, 128, 128)
    rectangle = pygame.Rect(400, 200, 32, 32)
    ground = pygame.Rect(0, 500, 900, 3)

    clock = pygame.time.Clock()
    cap = cv2.VideoCapture(0)
    detector = htm.HandDetector()
    
    run = True
    while run:
        clock.tick(FPS)
        success, img = cap.read()
        img = detector.findHands(img, draw=True)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            claw.x = (900- 1.6* (lmList[9][1]))
            claw.y = lmList[9][2]
        
            #print("X 9: "+ str(lmList[9][2]) + ", X 0: " + str(lmList[0][2]))
            if claw.colliderect(rectangle):    
                if lmList[12][2] in range(lmList[9][2]+5, lmList[0][2]-5):
                    rectangle.x = claw.x +48
                    rectangle.y = claw.y+85
                    VEL[1] =0

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if rectangle.colliderect(ground):
            rectangle.y = HEIGHT - 30
        else:
            rectangle.y += VEL[1]
            VEL[1] += GRAVITY

                                  
        draw_window(claw, rectangle)
        
    pygame.quit()


if __name__ == "__main__":
    main()