import pygame
import random

LANE_W=80
CAR_W=60
CAR_H=80
SPAWN_GAP=120   # min clear space (px) between a new car and the previous one in the same lane
COLORS=[(220,60,60),(220,140,40),(140,60,180),(60,180,80),(180,180,40),(60,80,200)]

class Car:
    def __init__(self, lane, y, direction, speed):
        self.lane=lane
        self.rect=pygame.Rect(lane*LANE_W+10,y,CAR_W,CAR_H)
        self.y=float(y)   # float position so fractional speeds (3.5, 4.5...) aren't truncated
        self.direction=direction  # 1=down, -1=up
        self.speed=speed
        self.color=random.choice(COLORS)

    def update(self):
        self.y+=self.direction*self.speed
        self.rect.y=round(self.y)

    def off_screen(self,height):
        return self.rect.top>height+100 or self.rect.bottom<-100

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect,border_radius=8)
        pygame.draw.rect(screen,(180,220,240),pygame.Rect(self.rect.x+8,self.rect.y+10,44,22),border_radius=4)
        for wx in [self.rect.x+6,self.rect.right-16]:
            for wy in [self.rect.y+4,self.rect.bottom-16]:
                pygame.draw.rect(screen,(30,30,30),pygame.Rect(wx,wy,10,12),border_radius=3)

def _spawn_pos(lane_idx,height):
    direction=1 if lane_idx%2==0 else -1
    y=-90 if direction==1 else height+10
    return direction,y

def lane_clear(cars,lane_idx,height):
    """True if a new car can spawn in this lane without touching/crowding another car."""
    _,y=_spawn_pos(lane_idx,height)
    zone=pygame.Rect(lane_idx*LANE_W+10,y,CAR_W,CAR_H).inflate(0,2*SPAWN_GAP)
    return not any(c.lane==lane_idx and c.rect.colliderect(zone) for c in cars)

def make_car(lane_idx,height,speed):
    direction,y=_spawn_pos(lane_idx,height)
    return Car(lane_idx,y,direction,speed)
