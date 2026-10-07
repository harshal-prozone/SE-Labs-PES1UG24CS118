import pygame
import random
from game.player import Player,LANE_W
from game.traffic import make_car,lane_clear
from game.log import LogLane,WATER_LANE
from game.daynight import DayNight
from game.highscores import add_score,MAX_ENTRIES

LANES=8
WIDTH=LANES*LANE_W
HEIGHT=600
FPS=60
BG=(60,60,60)
WATER=(40,110,190)
TOP_BAR=30
BOTTOM_SIDEWALK=50
START_LANE=3        # must not be WATER_LANE
MAX_LIVES=3
GOLD=(255,210,60)

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.big_font=pygame.font.SysFont("monospace",44,bold=True)
        self.reset()

    def reset(self):
        # start centred in a lane (was WIDTH//2, which straddled two lanes)
        self.player=Player(START_LANE*LANE_W+LANE_W//2,HEIGHT-80)
        self.cars=[]
        self.logs=LogLane(HEIGHT)
        self.day_night=DayNight(WIDTH,HEIGHT,FPS)
        self.high_scores=[]
        self.new_rank=None      # position of this run's score in the table, if it made it
        self.recorded=False
        self.timer=0
        self.spawn_interval=50
        self.speed=3
        self.score=0
        self.lives=MAX_LIVES
        self.game_over=False
        self.won=False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def _hit(self):
        self.lives-=1
        if self.lives<=0:
            self.lives=0
            self.game_over=True
        else:
            self.player.respawn()   # back to start, 2s of invincibility

    def _record_score(self):
        self.high_scores,self.new_rank=add_score(self.score//10)
        self.recorded=True

    def update(self):
        if self.game_over or self.won: return
        self.day_night.update()
        keys=pygame.key.get_pressed()
        self.player.move(keys,0,WIDTH,0,HEIGHT-BOTTOM_SIDEWALK)
        self.player.tick()
        self.timer+=1
        if self.timer>=self.spawn_interval:
            # only spawn in road lanes whose entry is clear; if none, retry next frame
            free=[l for l in range(LANES) if l!=WATER_LANE and lane_clear(self.cars,l,HEIGHT)]
            if free:
                self.cars.append(make_car(random.choice(free),HEIGHT,self.speed))
                self.timer=0
                self.spawn_interval=max(22,self.spawn_interval-0.2)
        for c in self.cars:
            c.speed=self.speed   # same speed for every car so cars in a lane never catch up to each other
            c.update()

        # water: find the log under the player (before logs move), then move logs and carry the player
        in_water=self.player.rect.centerx//LANE_W==WATER_LANE
        carrier=self.logs.log_under(self.player.rect) if in_water else None
        self.logs.update()
        if carrier:
            self.player.carry(carrier.dy,0,HEIGHT-BOTTOM_SIDEWALK)

        if not self.player.invincible:
            drowned=in_water and carrier is None
            crashed=any(c.rect.colliderect(self.player.rect) for c in self.cars)
            if drowned or crashed:
                self._hit()
        self.cars=[c for c in self.cars if not c.off_screen(HEIGHT)]
        self.score+=1
        if self.score%300==0: self.speed=min(10,self.speed+0.5)
        if not self.game_over and self.player.rect.top<=10:
            self.won=True
        if (self.game_over or self.won) and not self.recorded:
            self._record_score()

    def _draw_heart(self,cx,cy,filled):
        color=(220,60,60) if filled else (80,80,80)
        r=5
        pygame.draw.circle(self.screen,color,(cx-r,cy-2),r)
        pygame.draw.circle(self.screen,color,(cx+r,cy-2),r)
        pygame.draw.polygon(self.screen,color,[(cx-2*r,cy),(cx+2*r,cy),(cx,cy+2*r+1)])

    def draw(self):
        self.screen.fill(BG)
        # water lane (under the lane lines)
        wx=WATER_LANE*LANE_W
        water=pygame.Rect(wx,TOP_BAR,LANE_W,HEIGHT-BOTTOM_SIDEWALK-TOP_BAR)
        pygame.draw.rect(self.screen,WATER,water)
        for y in range(water.top+10,water.bottom,40):
            for x in (wx+16,wx+46):
                pygame.draw.line(self.screen,(90,160,225),(x,y),(x+14,y),2)
        # road markings
        for i in range(LANES+1):
            pygame.draw.line(self.screen,(100,100,100),(i*LANE_W,0),(i*LANE_W,HEIGHT),2)
        for y in range(0,HEIGHT,60):
            for i in range(LANES):
                if i==WATER_LANE: continue
                pygame.draw.rect(self.screen,(200,200,100),pygame.Rect(i*LANE_W+LANE_W//2-3,y,6,30))
        # logs, then sidewalks on top so logs emerge from behind them
        self.logs.draw(self.screen)
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,HEIGHT-BOTTOM_SIDEWALK,WIDTH,BOTTOM_SIDEWALK))
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,0,WIDTH,TOP_BAR))
        for c in self.cars: c.draw(self.screen)
        self.player.draw(self.screen)
        self.day_night.draw(self.screen,self.cars,self.player)   # night overlay + headlights
        # top bar: score on the left, day/night + timer in the middle, lives on the right
        hud=pygame.Rect(0,0,WIDTH,TOP_BAR)
        pygame.draw.rect(self.screen,(20,20,20),hud)
        s=self.font.render(f"Score: {self.score//10}",True,(220,220,220))
        self.screen.blit(s,(6,4))
        label=f"{'NIGHT' if self.day_night.night else 'DAY'} {self.day_night.seconds_left()}s"
        g=self.font.render(label,True,(200,200,200))
        gx=WIDTH//2-(g.get_width()+28)//2
        self.day_night.draw_icon(self.screen,gx+10,TOP_BAR//2)
        self.screen.blit(g,(gx+28,4))
        for i in range(MAX_LIVES):
            self._draw_heart(WIDTH-18-i*30,9,i<self.lives)
        if self.game_over:
            self._msg("GAME OVER",(220,60,60))
        if self.won:
            self._msg("YOU MADE IT!",(80,220,80))
        pygame.display.flip()

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,190))
        self.screen.blit(ov,(0,0))
        cx=WIDTH//2
        def center(surf,y): self.screen.blit(surf,(cx-surf.get_width()//2,y))
        center(self.big_font.render(text,True,color),70)
        center(self.font.render(f"Score: {self.score//10}",True,(220,220,220)),135)
        if self.new_rank is not None:
            center(self.font.render("NEW HIGH SCORE!",True,GOLD),172)
        center(self.font.render("HIGH SCORES",True,(170,170,170)),225)
        for i in range(MAX_ENTRIES):
            y=265+i*32
            filled=i<len(self.high_scores)
            value=str(self.high_scores[i]) if filled else "---"
            surf=self.font.render(f"{i+1}. {value:>6}",True,
                                  GOLD if i==self.new_rank else (200,200,200) if filled else (90,90,90))
            if i==self.new_rank:
                pygame.draw.rect(self.screen,(90,70,0),pygame.Rect(cx-110,y-3,220,surf.get_height()+4),border_radius=6)
            center(surf,y)
        center(self.font.render("Press R to Restart",True,(200,200,200)),465)

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
