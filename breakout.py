from tkinter import *
import random
import time

class Sprite:
    def __init__(self, game):
        self.game = game
        self.coordinates = None
    def move(self):
        pass
    def coords(self):
        return self.coordinates
     
class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Crash on Blocks")
        self.canvas = Canvas(self.tk, width=700, height=700, \
                highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 700
        self.canvas_width = 700
        self.bg = PhotoImage(file="background.gif")
        self.canvas.bind_all('<KeyPress-Up>', self.switch)
        self.canvas.bind_all('<KeyPress-Down>', self.exit)
        #수정 부분
        self.canvas.bind_all('<KeyPress-Tab>', self.act_X2)
        #-----
#        self.aboutToQuit = False
        self.running = True
        #수정 부분
        self.active_X2 = False
        #-----
        w = self.bg.width()
        h = self.bg.height()
        for x in range(0, 7):
            for y in range(0, 7):
                self.canvas.create_image(x * w, y * h, \
                        image=self.bg, anchor='nw')
        self.sprites = {}       
        self.running = True
        self.s= None
        self.score = None
   
    def switch(self,evt):
#        print(['Unpausing', 'Pausing'][self.running])
        self.running = not(self.running)

    def exit(self,evt):
#        self.aboutToQuit = True
        self.tk.destroy()

    #수정 부분
    def act_X2(self, evt):
        self.active_X2 = True
    #-----
        

    def mainloop(self ,canvas ,score):
        self.canvas = canvas
        self.collid = False
        self.score = score
        #수정 부분
        t1 = time.time()
        deactive = False
        #-----
      
        while 1:
             self.collid = False
             if ball.hit_bottom == False and paddle.started == True and self.running == True:
                  ball.draw()
                  paddle.draw()
                  if self.collid == True:
                     #아이템 적용 구간 
                     if self.active_X2 == True:
                         if deactive == False:
                             t2 = time.time()
                             self.score.hit_X2()
                             if t2 - t1 < 30:
                                 while t2 - t1 >= 30:
                                     t2 = time.time()
                             if t2 - t1 >= 30:
                                 self.active_X2 = False
                                 canvas.itemconfig(item_X2_text_1, state = 'normal')
                                 deactive = True
                         elif deactive == True:
                             self.score.hit_normal()
                     else:
                        self.score.hit_normal()
                     #-----
                        
                     a = self.s
                     del self.sprites[a]
                     canvas.itemconfig(a.image, state = 'hidden')
                  
                        
                  for sprite in self.sprites:
                       self.sprites[sprite].move()
             if len(self.sprites) == 0:
                 canvas.itemconfig(game_win_text, state = 'normal')                    
             if ball.hit_bottom ==True:
                  time.sleep(0.5)
                  canvas.itemconfig(game_over_text, state = 'normal')  
             self.tk.update_idletasks()
             self.tk.update()
             time.sleep(0.01)

class Coords:
     def __init__(self, x1=0, y1=0, x2=0, y2=0):
         self.x1 = x1
         self.y1 = y1
         self.x2 = x2
         self.y2 = y2
     
     def within_x(co1, co2):
         if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
                 or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
                 or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
                 or (co2.x2 > co1.x1 and co2.x2 < co1.x1):
             return True
         else:
             return False

     def within_y(co1, co2):
         if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
                 or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
                 or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
                 or (co2.y2 > co1.y1 and co2.y2 < co1.y1):
             return True
         else:
             return False

     def collided_left(co1, co2):
         if Coords.within_y(co1, co2):
             if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
                 return True
         return False

     def collided_right(co1, co2):
         if Coords.within_y(co1, co2):
             if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
                 return True
         return False

     def collided_top(co1, co2):
         if Coords.within_x(co1, co2):
             if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
                 return True
         return False

     def collided_bottom(y, co1, co2):
          if Coords.within_x(co1, co2):
              y_calc = co1.y2 + y
              if y_calc >= co2.y1 and y_calc <= co2.y2:
                  return True
          return False

class Ball(Sprite):
    def __init__(self, canvas, paddle, score, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.game = game
        self.photo_image = photo_image
        self.id = game.canvas.create_image(x, y, \
                image=self.photo_image, anchor='nw',state = 'normal')        
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -5
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.coordinates = Coords()
        self.hit_bottom = False
        
        
    def hit_paddle(self, pos):

         paddle_pos = self.canvas.coords(self.paddle.id)
         if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3]<= paddle_pos[3]:
                self.x += self.paddle.x
                return True
         return False

    def coords(self):
         xy = self.game.canvas.coords(self.id)
         self.coordinates.x1 = xy[0]
         self.coordinates.y1 = xy[1]
         self.coordinates.x2 = xy[0] + 40
         self.coordinates.y2 = xy[1] + 40
         return self.coordinates   
     
    def draw(self):
         co = self.coords()         
         for sprite in self.game.sprites:
             if sprite== self:
                 continue
             sprite_co = sprite.coords()
             if Coords.collided_top(co, sprite_co):
                 self.y = 3
                 self.game.collid = True
                 self.game.s = sprite                 
             if Coords.collided_bottom(self.y, co, sprite_co):
                 self.y = 3
                 self.game.collid = True
                 self.game.s = sprite
             if Coords.collided_left(co, sprite_co):
                  if self.x > 0:
                       self.x = 3
                  else:
                       self.x = -3
                  self.game.collid = True
                  self.game.s = sprite
             if Coords.collided_right(co, sprite_co):
                  if self.x >0:
                       self.x = 3
                  else:
                       self.x = -3
                  self.game.collid = True
                  self.game.s = sprite
                  
         self.game.canvas.move(self.id, self.x, self.y)
         pos = self.game.canvas.coords(self.id)
         pos2 = pos[0] + 40
         pos3 = pos[1] + 40
         pos.append(pos2)
         pos.append(pos3)
         if pos[1] <= 0:
             self.y = 3
         if pos[3] >= self.game.canvas_height:
             self.hit_bottom = True
         if self.hit_paddle(pos) == True:
             self.y = -3
         if pos[0] <= 0:
             self.x = 3
         if pos[2] >= self.game.canvas_width:
             self.x = -3

class Paddle:
    def __init__(self,canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 150, 10, fill= color)
        self.canvas.move(self.id, 300, 600)
        self.x = 0
        self.canvas_width= self.canvas.winfo_width()
        self.started = False
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Return>', self.start)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 4
        elif pos[2] >= self.canvas_width:
            self.x = -4
            
    def turn_left(self, evt):
        self.x = -4
        
    def turn_right(self, evt):
        self.x = 4
        
    def start(self,evt):
        self.started = True

class Block(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, \
                image=self.photo_image, anchor='nw',state = 'normal')
        self.coordinates = Coords(x, y, x + width, y + height)
        self.collid = True

class Score:
    def __init__(self,canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(670, 680, text=int(self.score), fill=color)

#수정 부분
    def hit_normal(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)

    def hit_X2(self):
        self.score += 2
        self.canvas.itemconfig(self.id, text=self.score)
    

class Item_X2:
    def __init__(self, game, canvas, photo_image, x, y, width, height):
        
        self.canvas = canvas
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, \
                image=self.photo_image, anchor='nw',state = 'normal')
#-----
        

    
            

g=Game()
canvas = g.canvas
score = Score(canvas,'blue')
num = canvas.create_text(630,680, text = 'score :')
paddle = Paddle(canvas,'yellow')
ball = Ball(canvas, paddle, score, g, PhotoImage(file="ball.gif"),350,350,30,30)
game_over_text = canvas.create_text(350, 350, text='Game Over', state = 'hidden')
game_win_text = canvas.create_text(350, 350, text='You Win', state = 'hidden')
#수정 부분
item_X2 = Item_X2(g, canvas, PhotoImage(file="item_X2.gif"), 20, 640, 30, 30)
item_X2_text_1 = canvas.create_text(100, 650, text='X', state = 'hidden')
item_X2_text_2 = canvas.create_text(70, 650, text='Tab키', state = 'normal')
#-----
manual= canvas.create_text(150, 680, text='방향키 ^ : 멈춤, 멈춤해제 / 방향키 v : 게임 종료')
block = []
w = 100
h = 25
k=0
a = ['block1.gif', 'block2.gif','block3.gif','block4.gif']
for x in range(0, 7):
    for y in range(0, 5):
        z=random.choice(a)
        block.append(Block(g, PhotoImage(file=z),x * w, y * h, w,h))
for t in block:
    g.sprites[t] = block[k]
    k = k+1
g.mainloop(canvas,score)





             
