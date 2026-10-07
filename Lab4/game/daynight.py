import math
import pygame

CYCLE_SECONDS=30        # day -> night -> day ... every 30 s
FADE_SECONDS=1.5        # how long the darkness takes to fade in/out
NIGHT_COLOR=(6,10,35)
NIGHT_ALPHA=200         # how dark it gets (0-255)
CAR_BEAM_LEN=260        # night headlight reach for traffic
PLAYER_BEAM_LEN=150
BEAM_NEAR_W=40          # beam width at the car / at the far end
BEAM_FAR_W=120

_beams={}   # cached beam masks

def _beam(direction,length):
    key=(direction,length)
    if key not in _beams:
        s=pygame.Surface((BEAM_FAR_W,length),pygame.SRCALPHA)
        for y in range(length):
            t=y/length   # 0 at the car, 1 at the far end
            half=(BEAM_NEAR_W+(BEAM_FAR_W-BEAM_NEAR_W)*t)/2
            a=NIGHT_ALPHA*(1-t)**1.5
            # three nested widths = soft edges
            for wf,af in ((1.0,0.4),(0.8,0.7),(0.55,1.0)):
                hw=half*wf
                pygame.draw.line(s,(0,0,0,int(a*af)),(BEAM_FAR_W/2-hw,y),(BEAM_FAR_W/2+hw,y))
        _beams[key]=s if direction>0 else pygame.transform.flip(s,False,True)
    return _beams[key]

class DayNight:
    def __init__(self,width,height,fps,seconds=CYCLE_SECONDS):
        self.fps=fps
        self.cycle_frames=int(seconds*fps)
        self.fade_step=1/(FADE_SECONDS*fps)
        self.overlay=pygame.Surface((width,height),pygame.SRCALPHA)
        self.timer=0
        self.night=False
        self.dark=0.0   # 0 = full day, 1 = full night (eases between)

    def update(self):
        self.timer+=1
        if self.timer>=self.cycle_frames:
            self.timer=0
            self.night=not self.night
        target=1.0 if self.night else 0.0
        if self.dark<target: self.dark=min(target,self.dark+self.fade_step)
        elif self.dark>target: self.dark=max(target,self.dark-self.fade_step)

    def seconds_left(self):
        return math.ceil((self.cycle_frames-self.timer)/self.fps)

    def _lamps(self,screen,rect,direction):
        y=rect.bottom-9 if direction>0 else rect.top+3
        for x in (rect.x+6,rect.right-18):
            pygame.draw.ellipse(screen,(255,240,170),pygame.Rect(x,y,12,6))

    def draw(self,screen,cars,player):
        """Darkness + headlight beams (night), then the lamps themselves."""
        if self.dark>0:
            self.overlay.fill((*NIGHT_COLOR,int(NIGHT_ALPHA*self.dark)))
            for c in cars:
                b=_beam(c.direction,CAR_BEAM_LEN)
                x=c.rect.centerx-BEAM_FAR_W//2
                y=c.rect.bottom-4 if c.direction>0 else c.rect.top-CAR_BEAM_LEN+4
                self.overlay.blit(b,(x,y),special_flags=pygame.BLEND_RGBA_SUB)
            if player.visible:
                b=_beam(-1,PLAYER_BEAM_LEN)
                self.overlay.blit(b,(player.rect.centerx-BEAM_FAR_W//2,player.rect.top-PLAYER_BEAM_LEN+4),
                                  special_flags=pygame.BLEND_RGBA_SUB)
            screen.blit(self.overlay,(0,0))
        for c in cars: self._lamps(screen,c.rect,c.direction)
        if player.visible: self._lamps(screen,player.rect,-1)

    def draw_icon(self,screen,cx,cy):
        """Little sun / moon for the top bar."""
        if self.night:
            pygame.draw.circle(screen,(230,230,200),(cx,cy),8)
            pygame.draw.circle(screen,(20,20,20),(cx+4,cy-3),7)
        else:
            pygame.draw.circle(screen,(250,210,60),(cx,cy),5)
            for k in range(8):
                a=k*math.pi/4
                pygame.draw.line(screen,(250,210,60),
                                 (cx+math.cos(a)*7,cy+math.sin(a)*7),
                                 (cx+math.cos(a)*10,cy+math.sin(a)*10),2)
