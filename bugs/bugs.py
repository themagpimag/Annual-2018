from random import randint as rand

WIDTH = W = 640
HEIGHT = H = 480
TITLE = "Babbage vs Bugs"

P = [(0,1,240), (-1,0,112), (0,1,32), (1,0,224), (0,1,32), (-1,0,224)]
F = [lambda x, y : 0, 
	 lambda x, y : y<1, 
	 lambda x, y : y==1, 
	 lambda x, y : y>1, 
	 lambda x, y : x&1, 
	 lambda x, y : (x^y)&1, 
	 lambda x, y : 1]

class Bug(Actor):
	def __init__(s, pos, kind):
		super().__init__("blank", pos)

		s.kind = kind
		s.life = kind*2
		s.time = 0

	def update(s):
		s.time -= 1
		s.x += P[state.pc0][0]
		s.y += P[state.pc0][1]

		c = s.collidelist(state.beams[0])
		if c >= 0:
			state.beams[0][c].h = 1

			s.life -= 1	
			if s.life == 0:
				state.score += s.kind*10

			s.time = 5

		if rand(0, 399) == 0:
			state.beams[1].append(Beam(s.pos, 3))

		s.image="bug"+("s" if s.time>0 else str(s.kind))+str(state.pc1>>3&3)

class Star(Actor):
	def __init__(s):
		super().__init__("star", (rand(0, W-1), rand(0, H-1)))

		s.v = rand(1, 3)

	def update(s):
		s.y -= s.v

		if s.y < 0:
			s.x = rand(0, W-1)
			s.y += H

class Beam(Actor):
	def __init__(s, pos, v):
		super().__init__("beam", pos)

		s.v = v
		s.h = 0

	def update(s):
		s.y += s.v

class Player(Actor):
	def __init__(s):
		super().__init__("blank", (W/2, H-64))

		s.time0 = 0
		s.time1 = 0
		s.life = 5

	def update(s):
		s.time0 -= 1
		s.time1 -= 1

		dx = (3 if keyboard.right else 0)-(3 if keyboard.left else 0)

		s.x = max(32, min(W-32, s.x+dx))

		c = s.collidelist(state.beams[1])
		if c >= 0 and s.time0 < 0:
			state.beams[1][c].h = 1

			s.life -= 1
			s.time0 = 5

		if keyboard.space and s.time1 < 0:
			state.beams[0].append(Beam(s.pos, -5))
			s.time1 = 15

		s.image = "bab"+("s" if s.life > 0 and s.time0 > 0 else str(state.pc1>>4&1))

class State:
	def __init__(s):
		s.bugs = []
		s.beams = ([], [])
		s.stars = [Star() for s in range(30)]

		s.player = Player()

		s.score = 0
		s.space = 0

		s.wave = 0

	def update(s):
		if len(s.bugs) == 0:
			for y in range(3):
				for x in range(7):
					s.bugs.append(Bug((W/2+x*60-180, y*60-180), 2 if F[min(s.wave, 6)](x, y) else 1))

			s.pc0 = 0
			s.pc1 = 0
			s.wave += 1

		for a in s.all():
			a.update()

		s.bugs = [b for b in s.bugs if b.life > 0]

		s.beams = ([b for b in s.beams[0] if b.y > -64 and not b.h],
				   [b for b in s.beams[1] if b.y < H+64 and not b.h])

		s.pc1 += 1
		if s.pc1 == P[s.pc0][2]:
			s.pc0 = 2 if s.pc0==5 else s.pc0+1
			s.pc1 = 0

	def all(s):
		return s.stars+s.beams[0]+s.beams[1]+s.bugs+[s.player]

	def over(s):
		return s.player.life <= 0 or len(s.bugs) and max([b.y for b in s.bugs]) > s.player.y - 50

state = State()

def update():
	global state

	if state.over():
		if keyboard.space and not state.space:
			state = State()
	else:
		state.update()

	state.space = keyboard.space

def draw():
	screen.clear()    

	for a in state.all():
		a.draw()

	for i in range(state.player.life):
		screen.blit("life", (6+i*32, H-26))

	screen.draw.text(str(state.score), bottomright=(W-8, H-3), fontname="consola", fontsize=20)

	if state.over():
		screen.blit("dark", (0, 0))
		screen.draw.text("GAME OVER", center=(W/2, H/2), fontname="consola", fontsize=100)
