import pygame

SPEED=2                 # px/frame moving forward/back (was 8, crossed the road in ~1s)
LANE_W=80
LANE_COOLDOWN=12        # frames between lane changes
INVINCIBLE_FRAMES=120   # 2 seconds at 60 FPS after respawn
BLINK_FRAMES=6          # blink toggle rate while invincible

class Player:
    def __init__(self, x, y):
        # x, y = centre of the player's start position
        self.rect=pygame.Rect(x-20,y-30,40,60)
        self.start=(x,y)
        self.color=(60,160,220)
        self.move_cooldown=0
        self.invincible=0

    def move(self, keys, min_x, max_x, min_y, max_y):
        # cooldown only limits lane changes; forward/back is never blocked by it
        can_turn=self.move_cooldown==0
        if self.move_cooldown>0:
            self.move_cooldown-=1

        left=keys[pygame.K_LEFT] or keys[pygame.K_a]
        right=keys[pygame.K_RIGHT] or keys[pygame.K_d]
        up=keys[pygame.K_UP] or keys[pygame.K_w]
        down=keys[pygame.K_DOWN] or keys[pygame.K_s]
        dx=(LANE_W if right else 0)-(LANE_W if left else 0)
        dy=(SPEED if down else 0)-(SPEED if up else 0)

        if dx and can_turn:
            nx=self.rect.x+dx
            # ignore the move at the edge instead of clamping, so the player stays centred in a lane
            if min_x<=nx<=max_x-self.rect.width:
                self.rect.x=nx
                self.move_cooldown=LANE_COOLDOWN
        if dy:
            # max_y is the lowest allowed value for rect.bottom
            self.rect.y=max(min_y,min(max_y-self.rect.height,self.rect.y+dy))

    def carry(self, dy, min_y, max_y):
        # moved along by a log; max_y is the lowest allowed value for rect.bottom
        self.rect.y=max(min_y,min(max_y-self.rect.height,self.rect.y+dy))

    def tick(self):
        if self.invincible>0:
            self.invincible-=1

    def respawn(self):
        self.rect.center=self.start
        self.move_cooldown=0
        self.invincible=INVINCIBLE_FRAMES

    @property
    def visible(self):
        # blinks off every other BLINK_FRAMES while invincible
        return not (self.invincible and (self.invincible//BLINK_FRAMES)%2==1)

    def draw(self,screen):
        if not self.visible:
            return
        # car body
        pygame.draw.rect(screen,self.color,self.rect,border_radius=8)
        # windows
        pygame.draw.rect(screen,(180,220,240),pygame.Rect(self.rect.x+6,self.rect.y+8,28,18),border_radius=4)
        # wheels
        for wx in [self.rect.x+4,self.rect.right-12]:
            for wy in [self.rect.y+4,self.rect.bottom-14]:
                pygame.draw.rect(screen,(30,30,30),pygame.Rect(wx,wy,8,10),border_radius=3)
