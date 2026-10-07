import pygame
import random
from game.player import LANE_W

WATER_LANE=4        # lane index (0-7) that is water instead of road
LOG_W=60
LOG_H=150
LOG_SPEED=3         # px/frame, constant (doesn't ramp up with car speed)
LOG_DIRECTION=-1    # -1 = logs move up (toward the goal), 1 = down
LOG_GAP_MIN=80      # clear water between logs (player is 60px tall)
LOG_GAP_MAX=160

class Log:
    def __init__(self, lane, y, direction, speed):
        self.lane=lane
        self.rect=pygame.Rect(lane*LANE_W+(LANE_W-LOG_W)//2,y,LOG_W,LOG_H)
        self.y=float(y)
        self.direction=direction
        self.speed=speed
        self.dy=0   # how far the log moved this frame (used to carry the player)

    def update(self):
        old=self.rect.y
        self.y+=self.direction*self.speed
        self.rect.y=round(self.y)
        self.dy=self.rect.y-old

    def off_screen(self,height):
        return self.rect.top>height or self.rect.bottom<0

    def draw(self,screen):
        r=self.rect
        pygame.draw.rect(screen,(120,80,40),r,border_radius=14)
        for off in (-14,0,14):   # grain
            pygame.draw.line(screen,(95,62,30),(r.centerx+off,r.top+10),(r.centerx+off,r.bottom-10),2)
        for y in (r.top+4,r.bottom-12):   # end caps
            pygame.draw.ellipse(screen,(165,120,65),pygame.Rect(r.x+6,y,r.width-12,8))

class LogLane:
    """All the logs in the water lane."""
    def __init__(self, height, lane=WATER_LANE, direction=LOG_DIRECTION, speed=LOG_SPEED):
        self.height=height
        self.lane=lane
        self.direction=direction
        self.speed=speed
        self.spawn_y=height if direction<0 else -LOG_H
        self.logs=[]
        self.gap=random.randint(LOG_GAP_MIN,LOG_GAP_MAX)
        # pre-fill so the lane already has logs when the game starts
        for _ in range(int((height+2*LOG_H)/speed)):
            self.update()

    def update(self):
        for l in self.logs: l.update()
        self.logs=[l for l in self.logs if not l.off_screen(self.height)]
        # spawn once the newest log has cleared its length + a random gap
        if not self.logs or abs(self.logs[-1].rect.y-self.spawn_y)>=LOG_H+self.gap:
            self.logs.append(Log(self.lane,self.spawn_y,self.direction,self.speed))
            self.gap=random.randint(LOG_GAP_MIN,LOG_GAP_MAX)

    def log_under(self, rect):
        """The log the rect's centre is standing on, or None (= in the water)."""
        for l in self.logs:
            if l.rect.collidepoint(rect.center):
                return l
        return None

    def draw(self,screen):
        for l in self.logs: l.draw(screen)
