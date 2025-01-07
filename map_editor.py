import sys

import pygame

from scripts.utils import Images
from scripts.tilemap import Tilemap

RENDER_SCALE = 3.0

class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((960, 540))
        
        self.display_width = 320
        self.display_height = 180
        
        self.display = pygame.Surface((self.display_width, self.display_height))
        self.display_2 = pygame.Surface((self.display_width, self.display_height))

        self.clock = pygame.time.Clock()
        
        self.test_tileset = Images("data/assets/map_tiles/test_map/tileset.png", 16)
        self.tileset = self.test_tileset.load_tileset()
        
        self.movement = [False, False, False, False]
        
        self.tilemap = Tilemap(self, tile_size=16)
        
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        
        self.scroll = [0, 0]
        
        self.tile_list = list(self.tileset)
        self.tile_group = 0
        
        self.decorations = False
        
        self.clicking = False
        self.right_clicking = False
        
    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.render(self.display, offset=render_scroll)
            self.tilemap.render(self.display_2, offset=render_scroll)
            
            current_tile_img = self.tileset[self.tile_list[self.tile_group]].copy()
            current_tile_img.set_alpha()
            
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
            
            self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))

            if self.clicking:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'tile_id': self.tile_list[self.tile_group], 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
            
            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                    if event.button == 3:
                        self.right_clicking = True
                                                    
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                        
                    if event.key == pygame.K_a:
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        self.tile_variant = 0
                    if event.key == pygame.K_d:
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                        self.tile_variant = 0
                        
                    if event.key == pygame.K_w:
                        self.tile_group = (self.tile_group - int(self.test_tileset.tileset_image.get_width()/self.test_tileset.tile_size)) % len(self.tile_list)
                        self.tile_variant = 0
                    if event.key == pygame.K_s:
                        self.tile_group = (self.tile_group + int(self.test_tileset.tileset_image.get_width()/self.test_tileset.tile_size)) % len(self.tile_list)
                        self.tile_variant = 0                    
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()

"初音階段 - Vacant World (2013)"