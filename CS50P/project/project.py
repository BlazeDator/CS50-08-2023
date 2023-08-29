import pygame, sys, random

class Debug_text:
   def __init__(self,font:pygame.font.Font, text:str="1", x:int=0, y:int=0, color:list=[255,255,255]):
      self.color = pygame.color.Color(*color)
      self.font = font
      self.surface = self.font.render(text, True, self.color)
      self.x = x
      self.y = y
      self.rect = self.surface.get_rect()
      self.rect.move_ip(self.x, self.y)

   def update(self, text:str):
      self.surface = self.font.render(text, True, self.color)

class Text(Debug_text):
   def __init__(self, font:pygame.font.Font, text:str, location:list, color:list):
      self.font = font
      self.color = pygame.color.Color(*color)
      self.surface = font.render(text, True, self.color)
      self.rect = self.surface.get_rect()
      self.rect.move_ip(*location)

class Player:
   def __init__(self, size:int=30, screen_center=(1280,720), speed:int=10, pcolor:list=[255,255,255]):
      self.surface = pygame.Surface((size,size)) 
      self.color = pygame.color.Color(*pcolor)
      self.rect = pygame.draw.circle(surface=self.surface, color=self.color, center=(self.surface.get_width()/2, self.surface.get_height()/2), radius=self.surface.get_width()/2, width=0)
      self.rect.move_ip(screen_center[0]-size, screen_center[1]-size)
      self.speed = speed
      self.size = size
      self.speed_diag = calc_diag_speed(self.speed)
      self.mov_vector = [0, 0]
      self.cooldown = False
      self.weapon_timer = 0
      self.can_move = False

   def movement(self, keys):
      if self.can_move:
         # Directionals
         if keys[pygame.K_w]:
            self.mov_vector = [0, -self.speed]
         if keys[pygame.K_s]:
            self.mov_vector = [0, self.speed]
         if keys[pygame.K_a]:
            self.mov_vector = [-self.speed, 0]
         if keys[pygame.K_d]:
            self.mov_vector = [self.speed, 0] 

         # Diagonals
         if keys[pygame.K_w] and keys[pygame.K_a]: 
            self.mov_vector = [-(self.speed_diag), -(self.speed_diag)]
         if keys[pygame.K_w] and keys[pygame.K_d]: 
            self.mov_vector = [(self.speed_diag), -(self.speed_diag)]
         if keys[pygame.K_s] and keys[pygame.K_a]: 
            self.mov_vector = [-(self.speed_diag), (self.speed_diag)]
         if keys[pygame.K_s] and keys[pygame.K_d]: 
            self.mov_vector = [(self.speed_diag), (self.speed_diag)]

         #Still
         if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
            self.mov_vector = [0, 0]

   def move(self):
      self.rect.move_ip(*self.mov_vector)

   def check_death(self, squares:list):
      for square in squares:
         if self.rect.colliderect(square.rect):
            self.mov_vector[0] = 0
            self.mov_vector[1] = 0
            self.can_move = False
            return True
      
   def center(self):
      return [self.rect.x + self.size/2, self.rect.y + self.size/2 ]

class Square(Player):
   def __init__(self, size:int=20, speed:int=5, screen_size:tuple=(1280,720), pcolor:list=[255,0,0]):
      self.surface = pygame.Surface((size,size))
      self.color = pygame.color.Color(*pcolor)
      self.surface.fill(self.color)
      self.rect = self.surface.get_rect()
      self.speed = speed
      self.size = size
      self.speed_diag = calc_diag_speed(self.speed)
      self.mov_vector = [0, 0]
      self.can_move = True

      # Spawn
      x = random.randint(5, screen_size[0]-25)
      y = random.randint(5, screen_size[1]-25)
      self.rect.move_ip(x, y)
      self.keys = {
         pygame.K_w : True,
         pygame.K_a : True,
         pygame.K_s : True,
         pygame.K_d : True
      }
   
   def mov_random(self):
      for key in self.keys:
         rnd = random.choice([True,False])
         if rnd:
            self.keys[key] = rnd
         else:
            self.keys[key] = rnd
      self.movement(self.keys)

   def mov_player(self, player:Player):
      s_x = self.rect.x
      s_y = self.rect.y
      player_x = player.rect.x
      player_y = player.rect.y
      margin = player.size/2

      self.keys = {key : False for key in self.keys}

      if s_x < player_x-margin:
         self.keys[pygame.K_d] = True
      elif s_x > player_x+margin:
         self.keys[pygame.K_a] = True
      else:
         self.keys[pygame.K_d] = False
         self.keys[pygame.K_a] = False

      if s_y < player_y-margin:
         self.keys[pygame.K_s] = True
      elif s_y > player_y+margin:
         self.keys[pygame.K_w] = True
      else:
         self.keys[pygame.K_s] = False
         self.keys[pygame.K_w] = False

      self.movement(self.keys)

   def mov_aim(self, player):
      start = pygame.math.Vector2(self.rect.x, self.rect.y)
      target = pygame.math.Vector2(player)
      distance = start.distance_to(target)
      target.scale_to_length(distance)
      target.normalize_ip()
      target[0] *= self.speed
      target[1] *= self.speed
      self.mov_vector = target

class Bullet:
   def __init__(self, size:int=5, player:list=[0,0], speed:int=20, pcolor:list=[255,255,255]):
      # Speed and Square size might make them go through without hit detection
      self.surface = pygame.Surface((size,size)) 
      self.color = pygame.color.Color(*pcolor)
      self.rect = pygame.draw.circle(surface=self.surface, color=self.color, center=(self.surface.get_width()/2, self.surface.get_height()/2), radius=self.surface.get_width()/2, width=0)
      self.rect.move_ip(player[0], player[1])
      self.speed = speed
      self.size = size
      self.speed_diag = calc_diag_speed(self.speed)
      self.mov_vector = [0, 0]
      self.timer = 0

   def aim(self, target):
      start = pygame.math.Vector2([self.rect.x, self.rect.y])
      target = pygame.math.Vector2(target)
      distance = start.distance_to(target)
      target.scale_to_length(distance)
      target.normalize_ip()
      target[0] *= self.speed
      target[1] *= self.speed
      self.mov_vector = target

   def move(self):
      self.rect.move_ip(*self.mov_vector)

   def check_kill(self, squares:list):
      for square in squares:
         if self.rect.colliderect(square.rect):
            squares.remove(square)
            return True

   def check_death(self, squares:list):
      for square in squares:
         if self.rect.colliderect(square.rect):
            return True

class Wall:
   def __init__(self, size:list[int]=[0,0], pcolor:list=[255,255,255], location:list[int]=[]):
      self.surface = pygame.Surface(size)
      self.color = pygame.color.Color(*pcolor)
      self.surface.fill(self.color)
      self.rect = self.surface.get_rect()
      self.rect.move_ip(*location)

def main():
   # Initialization
   pygame.init()
   pygame.display.set_caption("Survival Squared V0.1")
   icon = pygame.Surface((32,32))
   icon.fill((255, 0, 0))
   pygame.display.set_icon(icon)
   screen_size = 1600, 900
   screen = pygame.display.set_mode(screen_size)
   clock = pygame.time.Clock()
   max_framerate = 200
   font = pygame.font.Font('freesansbold.ttf', 32)
   game = True
   game_time = 0
   kills = 0
   deaths = 0

   # Colors
   black = [0, 0, 0]
   white = [255,255,255]
   red = [255, 0, 0]
   green = [0,255,0]
   blue = [0,0,255]
   purple = [150,20,255]
   grey= [75, 75, 75]

   # Text
   start_text = Text(font, "Press Space to start!", [(screen_size[0]-336)/2, screen_size[1]*0.1], white)
   wave_text = Text(font, "", [screen_size[0]*0.73, screen_size[1]*0.01], white)
   time_text = Text(font, "", [screen_size[0]*0.85, screen_size[1]*0.01], white)
   kills_text = Text(font, "", [screen_size[0]*0.61, screen_size[1]*0.01], white)
   deaths_text = Text(font, "", [screen_size[0]*0.49, screen_size[1]*0.01], white)

   # Walls
   wall_north = Wall(size=[screen_size[0], 900], pcolor=grey, location=[0, -895])
   wall_east = Wall(size=[900, screen_size[1]], pcolor=grey, location=[-895, 0])
   wall_south = Wall(size=[screen_size[0], 900], pcolor=grey, location=[0, screen_size[1]-5])
   wall_west = Wall(size=[900, screen_size[1]], pcolor=grey, location=[screen_size[0]-5, 0])
   
   walls = [wall_north, wall_east, wall_south, wall_west]

   # player
   player = Player(screen_center=(screen_size[0]/2, screen_size[1]/2))
   bullets:list[Bullet] = []

   # Waves
   # Order: Red, Green, Blue, Purple
   waves = [
      [25,0,0,0],
      [15,0,5,0],
      [10,0,0,10],
      [10,15,0,5],
      [20,25,5,5]
   ]
   wave_counter = 0

   # Squares
   squares_red = [Square(screen_size=screen_size, speed=7, pcolor=red) for i in range(waves[wave_counter][0])]
   squares_green = [Square(screen_size=screen_size, speed=1, pcolor=green) for i in range(waves[wave_counter][1])]
   squares_blue = [Square(screen_size=screen_size, speed=9, pcolor=blue) for i in range(waves[wave_counter][2])]
   squares_purple = [Square(screen_size=screen_size, speed=7, pcolor=purple) for i in range(waves[wave_counter][3])]
   entities = squares_red + squares_green + squares_blue + squares_purple
   safe_start(player, squares_red)
   safe_start(player, squares_green)
   safe_start(player, squares_blue)
   safe_start(player, squares_purple)

   # Timers
   delta_25_ms = 0   # 40  Ticks per second
   delta_1000_ms = 0 # 1   Tick  per second
   start = False

   # Debug Info
   show_debug = False
   def update_debug() -> list[str]:
      debug_info = [
               "Version 0.1 ",
               "Game Time: " + str(game_time) + " s",
               "Player Vector: " + str(player.mov_vector),
               str(int(clock.get_fps())) + " Max FPS: " + str(max_framerate),
               str(clock.get_time())+" ms",
               "Player X: " + str(player.rect.x),
               "Player Y: " + str(player.rect.y),
               "Delta 1s: " + str(delta_1000_ms),
               "Green Squares: " + str(len(squares_green)),
               "Killable Squares: " + str(len(squares_red)+len(squares_blue)+len(squares_purple)),
               "Mouse: " + str(pygame.mouse.get_pos()),
               "Mouse after: " + str(calc_relative_pos(player.center(), pygame.mouse.get_pos())),
               "Last Bullet:" + str(bullets[-1].mov_vector) if bullets else None,
               "Bullets: " + str(len(bullets)) if bullets else None,
               "red mv v1: " + str(squares_red[0].mov_vector) if squares_red else None,
               "red rel pos: "+ str(calc_relative_pos(squares_red[0].center(), player.center())) if squares_red else None,
               "purple mv v1: " + str(squares_purple[0].mov_vector) if squares_purple else None,
               "purple rel pos: "+ str(calc_relative_pos(squares_purple[0].center(), player.center())) if squares_purple else None

            ]
      return debug_info
   debug_info = update_debug()
   lines = len(debug_info) * 32
   debug = [Debug_text(font, y=i) for i in range(0,lines,32)]
   
   # Game Loop
   while game:  
      tick = clock.tick(max_framerate) 
      delta_25_ms += tick
      delta_1000_ms += tick

      # UI
      time_text.update("Time: " + str(game_time) + "s")
      wave_text.update("Wave: " + str(wave_counter+1) + "/" + str(len(waves)))
      kills_text.update("Kills: " + str(kills)) 
      deaths_text.update("Deaths: " + str(deaths))

      for event in pygame.event.get():
         if event.type == pygame.QUIT: sys.exit()
      
      keys = pygame.key.get_pressed()
      mouse = pygame.mouse.get_pressed()

      if keys[pygame.K_SPACE]:
         start = True
         player.can_move = True
      if keys[pygame.K_BACKSPACE]:
         player.can_move = True

      player.movement(keys)
      check_collisions(player, walls)
      
      if delta_25_ms >= 25: # 40 Tick Rate Updates
         # Player
         player.move() # Player Movement
         # Player Weapon
         if mouse[0] == True and not player.cooldown and start: 
            bullets.append(Bullet(player=player.center()))
            bullets[-1].aim(calc_relative_pos(player.center(), pygame.mouse.get_pos()))
            player.cooldown = True
         if player.cooldown:
            player.weapon_timer += 25
            if player.weapon_timer >= 250:
               player.cooldown = False
               player.weapon_timer = 0

         # Bullets
         for bullet in bullets:
            bullet.move()
            if bullet.check_death(squares_green + walls):
               bullets.remove(bullet)
            elif bullet.check_kill(squares_red) or bullet.check_kill(squares_blue) or bullet.check_kill(squares_purple):
               kills +=1
               bullets.remove(bullet)
            bullet.timer+=25
            if bullet.timer > 4500: # Despawn
               bullets.remove(bullet)

         # AI
         if start:
            for square in squares_red: # Squares Movement
               square.mov_aim(calc_relative_pos(square.center(), player.center()))
               check_collisions(square, squares_red + squares_green + squares_blue + squares_purple + walls)
               square.move()
            for square in squares_green:
               square.mov_player(player)
               check_collisions(square, squares_red + squares_green + squares_blue + squares_purple + walls, 2)
               square.move()
            for square in squares_blue:
               square.mov_aim(calc_relative_pos(square.center(), player.center()))
               check_collisions(square, squares_blue + squares_green + walls)
               square.move()
            for square in squares_purple:
               check_collisions(square, squares_red + squares_green + squares_blue + squares_purple + walls, 3)
               if square.mov_vector[0] > square.speed * 1.5:
                  square.mov_vector[0] -= 2
               if square.mov_vector[1] > square.speed * 1.5:   
                  square.mov_vector[1] -= 2
               square.move()

         # Player Death
         entities = squares_red + squares_green + squares_blue + squares_purple
         if player.check_death(entities): 
            start  = False
            deaths += 1
            if wave_counter > 0:
               wave_counter -= 1
            squares_red.clear()
            squares_green.clear()
            squares_blue.clear()
            squares_purple.clear()

         # Wave Control
         if len(squares_red)+len(squares_blue)+len(squares_purple) == 0:
            if start:
               wave_counter += 1
            if wave_counter < len(waves):
               bullets = []
               start = False
               player.can_move = False
               player.mov_vector = [0, 0]
               squares_red = [Square(screen_size=screen_size, speed=7, pcolor=red) for i in range(waves[wave_counter][0])]
               squares_green = [Square(screen_size=screen_size, speed=1, pcolor=green) for i in range(waves[wave_counter][1])]
               squares_blue = [Square(screen_size=screen_size, speed=9, pcolor=blue) for i in range(waves[wave_counter][2])]
               squares_purple = [Square(screen_size=screen_size, speed=7, pcolor=purple) for i in range(waves[wave_counter][3])]
               safe_start(player, squares_red)
               safe_start(player, squares_green)
               safe_start(player, squares_blue)
               safe_start(player, squares_purple)
            else:
               game = False
         
         delta_25_ms = 0

      if delta_1000_ms >= 1000: # 1 Tick Rate Updates
         # AI
         for square in squares_purple:
            square.mov_aim(calc_relative_pos(square.center(), player.center()))
         game_time += 1

         delta_1000_ms = 0

      
      # Background
      screen.fill(black)
      # Draw Image
      screen.blit(player.surface, player.rect)
      for bullet in bullets:
         screen.blit(bullet.surface, bullet.rect)
      for square in squares_red:
         screen.blit(square.surface, square.rect)
      for square in squares_green:
         screen.blit(square.surface, square.rect)
      for square in squares_blue:
         screen.blit(square.surface, square.rect)
      for square in squares_purple:
         screen.blit(square.surface, square.rect)
      for wall in walls:
         screen.blit(wall.surface, wall.rect)
      if not start:
         screen.blit(start_text.surface, start_text.rect)
      
      # UI
      screen.blit(time_text.surface, time_text.rect)
      screen.blit(wave_text.surface, wave_text.rect)
      screen.blit(kills_text.surface, kills_text.rect)
      screen.blit(deaths_text.surface, deaths_text.rect)

      # Framerate Control
      if keys[pygame.K_UP]:
         max_framerate += 5
      if keys[pygame.K_DOWN]:
         max_framerate -= 5

      # Cheats
      if keys[pygame.K_KP_PLUS]:
         player.cooldown = False


      # Debug  Info
      if keys[pygame.K_F3]:
         show_debug = True
      if show_debug:
         debug_info = update_debug()
         for i in range(len(debug)):
            debug[i].update(debug_info[i])
            screen.blit(debug[i].surface, debug[i].rect)
         if keys[pygame.K_F4]:
            show_debug = False  

      # Send Frame
      pygame.display.update()

   end_text = Text(font, "Congratulations!", [(screen_size[0]-272)/2, screen_size[1]*0.3], white) 
   wave_text = Text(font, "Time: " + str(game_time) + "s", [(screen_size[0]-416)/2, screen_size[1]*0.4], white)
   time_text = Text(font, "Wave: " + str(wave_counter) + "/" + str(len(waves)), [(screen_size[0]+128)/2, screen_size[1]*0.4], white)
   kills_text = Text(font, "Kills: " + str(kills), [(screen_size[0]-416)/2, screen_size[1]*0.5], white)
   deaths_text = Text(font, "Deaths: " + str(deaths), [(screen_size[0]+128)/2, screen_size[1]*0.5], white)

   # End game
   while True:
      tick = clock.tick(max_framerate) 
      for event in pygame.event.get():
         if event.type == pygame.QUIT: sys.exit()


      screen.fill(black)
      screen.blit(time_text.surface, time_text.rect)
      screen.blit(wave_text.surface, wave_text.rect)
      screen.blit(kills_text.surface, kills_text.rect)
      screen.blit(deaths_text.surface, deaths_text.rect)
      screen.blit(end_text.surface, end_text.rect)
      pygame.display.update()
      



def calc_diag_speed(speed: int) -> float:
   # return speed * 0.7071
   if speed < 0:
      raise ValueError
   try:
      v1, v1.x, v1.y = pygame.math.Vector2(), 0, 0
      v2, v2.x, v2.y = pygame.math.Vector2(), speed, speed
   except TypeError:
      raise TypeError
   else:
      return v1.distance_to(v2) / 2

def check_collisions(self:Square, squares:list[Square], multiply:int=1):
   try:
      if len(squares) < 1:
         raise ValueError
      if type(multiply) != int or multiply < 1:
         raise TypeError
      for next in squares:
         if self == next:
            pass
         elif self.rect.colliderect(next.rect):
            if self.rect.x < next.rect.x:
               self.mov_vector[0] = -self.speed*multiply
            elif self.rect.x  > next.rect.x:
               self.mov_vector[0] = self.speed*multiply
            else:
               self.mov_vector [0] = 0

            if self.rect.y  < next.rect.y:
               self.mov_vector[1] = -self.speed*multiply
            elif self.rect.y  > next.rect.y:
               self.mov_vector[1] = self.speed*multiply
            else:
               self.mov_vector[1] = 0
   except TypeError:
      raise TypeError
   except AttributeError:
      raise AttributeError
   else:
      pass

def calc_relative_pos(player:list[int], mouse:list[int]) -> list[int]:
   try:
      player[0] = mouse[0] - player[0]
      player[1] = mouse[1] - player[1]
   except TypeError:
      raise TypeError
   else:
      return player

def safe_start(player:Player, squares:list[Square]):
   try:
      for square in squares:
         if square.rect.colliderect(player.rect): 
            squares.remove(square)
   except AttributeError:
      raise AttributeError
   else:
      pass

if __name__ == "__main__":
    main()