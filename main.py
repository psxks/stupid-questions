import sys, pygame

from scripts.utils import Animation, Tileset, load_image
from scripts.player import Player
from scripts.tilemap import Tilemap
from scripts.ui import SkillsUI, BuffUI
from scripts.buff import *
from scripts.shaders import Shader

class Game():
    def __init__(self):
        pygame.init()
        
        self.font = pygame.font.SysFont('data/texts/BoutiqueBitmap9x9_1.9.ttf', 24)
        self.screen = pygame.display.set_mode((960, 540), pygame.OPENGL | pygame.DOUBLEBUF)
        
        self.main_shader = Shader('shader', 'shader')

        self.display_width, self.display_height = 320, 180
        
        self.display = pygame.Surface((self.display_width, self.display_height))
        
        self.main_surf = pygame.Surface((self.display_width, self.display_height))
        self.decoration_surf = pygame.Surface((self.display_width, self.display_height))
        self.ui_surf = pygame.Surface((960, 540))
        
        self.clock = pygame.time.Clock()
        self.movement = [False, False]
              
        self.current_zoom = 1.0
        self.target_zoom = 1.0
              
        self.animations = {
            'player/idle': Animation('data/assets/Animations/Player/idle/anim1.png', img_dur=30),
            'player/edge_idle': Animation('data/assets/Animations/Player/idle/anim2.png', img_dur=30),
            'player/run': Animation('data/assets/Animations/Player/walk/anim1.png', img_dur=6),
            'player/jump': Animation('data/assets/Animations/Player/jump/anim1.png', img_dur=7, loop=False),
            'player/wall_slide': Animation('data/assets/Animations/Player/slide/anim1.png'),
            'player/fall': Animation('data/assets/Animations/Player/fall/anim1.png'),
            'player/land': Animation('data/assets/Animations/Player/land/anim1.png', img_dur=10, loop=False),
            'player/levitation': Animation('data/assets/Animations/Player/levitation/anim1.png', img_dur=10),
            'player/levitation_start': Animation('data/assets/Animations/Player/levitation/anim2.png', img_dur=10, loop=False),
            'player/levitation_end': Animation('data/assets/Animations/Player/levitation/anim3.png', img_dur=10, loop=False)
        }
        
        self.player = Player(self, (50, 50), (8, 15))
        
        self.tileset = Tileset("data/assets/map_tiles/test_map/tileset.png", 16).load_tileset()
                
        self.tilemap = Tilemap(self, tile_size=16)
        
        self.level = 'test'
        self.load_level(self.level)
        
        self.ui = {
            'switch': SkillsUI(50,50, load_image('data/assets/spells/form_1.png'), load_image('data/assets/spells/form_2.png'), 400, 475, 2 , 'Q'),
            'spell_1': SkillsUI(50,50, load_image('data/assets/spells/paralysed.png'), load_image('data/assets/spells/time_stop.png'), 460, 475, 10, 'E'),
            'spell_2': SkillsUI(50,50, load_image('data/assets/spells/x2_speed.png'), load_image('data/assets/spells/x2_speed_2.png'), 520, 475, 10, 'F'),
        }
        
        pygame.display.set_caption('stupid-questions')
        
        self.t = 0
        self.button_conditions = {'switch': False, 'spell_1': False, 'spell_2': False}
        
    def load_level(self, level_name):
        self.tilemap.load('data/levels/' + level_name + '.json')
        
        self.player.pos = [40, 4]
        self.player.air_time = 0
        
        self.scroll = [0, 0]

    def run(self):
        
        while True:
            self.t += self.clock.get_time() / 1000
            
            
            if 'X2Gravity' in self.player.buffs or 'X2Speed' in self.player.buffs:
                self.target_zoom = 1.05
            else:
                self.target_zoom = 1.0     
            
            self.current_zoom += (self.target_zoom - self.current_zoom) * 0.1
            
            
            self.ui_surf.fill((0,0,255))
            self.main_surf.fill((198, 183, 190))
            self.decoration_surf.fill((0, 0, 0))
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            mpos = pygame.mouse.get_pos()
            
            self.tilemap.render(
                self.main_surf,
                self.decoration_surf,
                self.tileset,
                offset=render_scroll,
            )
            
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.main_surf, offset=render_scroll)
            
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display.blit(display_sillhouette, offset)
            
            for name, buff in self.player.buffs.items():
                buff.activate_effect()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.jump()
                        
                    if event.key == pygame.K_q and self.ui['switch'].active:
                        self.button_conditions['switch'] = True
                        self.player.form = not self.player.form
                        self.ui['switch'].active = False
                        
                    if event.key == pygame.K_e and self.ui['spell_1'].active:
                        self.button_conditions['spell_1'] = True
                        if self.player.form:
                            self.player.buffs['Stun'] = Buff('Stun', 3, StunEffect, self.player, load_image('data/assets/spells/paralysed.png'))
                        else:
                            self.player.buffs['TimeStop'] = Buff('TimeStop', 3, TimeStopEffect, self.player, load_image('data/assets/spells/time_stop.png'))
                        self.ui['spell_1'].active = False
                            
                    if event.key == pygame.K_f and self.ui['spell_2'].active:
                        self.button_conditions['spell_2'] = True
                        if self.player.form:
                            self.player.buffs['X2Speed'] = Buff('X2Speed', 1.5, X2SpeedEffect, self.player, load_image('data/assets/spells/x2_speed.png'))
                        else:
                            self.player.buffs['X2Gravity'] = Buff('X2Gravity', 1.7, X2GravityEffect, self.player, load_image('data/assets/spells/x2_speed_2.png'))
                        self.ui['spell_2'].active = False
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                       self.button_conditions['switch'] = False
                    if event.key == pygame.K_e:
                        self.button_conditions['spell_1'] = False
                    if event.key == pygame.K_f:
                        self.button_conditions['spell_2'] = False
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                        
            zoomed_size = (int(self.main_surf.get_width() * self.current_zoom), int(self.main_surf.get_height() * self.current_zoom))
            offset_x = (self.main_surf.get_width() - zoomed_size[0]) // 2
            offset_y = (self.main_surf.get_height() - zoomed_size[1]) // 2

            zoomed_main_surf = pygame.transform.smoothscale(self.main_surf, zoomed_size)
            self.display.blit(zoomed_main_surf, (offset_x, offset_y))

            self.decoration_surf.set_colorkey((0, 0, 0))
            zoomed_decoration_surf = pygame.transform.smoothscale(self.decoration_surf, zoomed_size)
            self.display.blit(zoomed_decoration_surf, (offset_x, offset_y))
            
            img = self.font.render(str(int(self.clock.get_fps())), True, (1, 1, 1))
            self.ui_surf.blit(img, (930, 10))
        
            for name, obj in self.ui.items():
                obj.form = self.player.form
                state = 'pressed' if (name in self.button_conditions and self.button_conditions[name]) else mpos
                obj.render(self.ui_surf, state)
            
            for name, obj in self.player.buffs.items():
                render = obj.ui.render(self.ui_surf, list(self.player.buffs).index(name))
                if render is not None:
                    self.player.buffs.pop(render)
                    break
            
            self.ui_surf.set_colorkey((0,0,255))
                
            screen_surface = pygame.transform.scale(self.display, self.screen.get_size())
            screen_surface.blit(self.ui_surf, (0,0))
            
            self.main_shader.render(screen_surface, self.t, True if 'X2Gravity' in self.player.buffs else False,
                                    True if 'X2Speed' in self.player.buffs else False)
            
            pygame.display.flip()
            self.clock.tick(60)
            
if __name__ == "__main__":
    Game().run()