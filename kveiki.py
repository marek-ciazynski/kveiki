#-*- coding: utf-8 -*-
import os,sys
import linecache
import curses
import time
import atexit
import signal

@atexit.register
def atclose():
	signal.signal(signal.SIGALRM,signal.SIG_IGN)
	#Wyświetlenie rankingu i wpisanie się do niego
	if not outranked:
		winlin, wincol =  stdscr.getmaxyx()
		stdscr.clear()
		stdscr.hline(0,0,' ', wincol,curses.A_REVERSE)
		stdscr.hline(winlin-1,0,' ', wincol,curses.A_REVERSE)
		stdscr.addstr(0,(wincol/2)-4,'Ranking',curses.color_pair(1))
		
		times.append(minutes+':'+sec)
		srednia=0
		ss=0
		sm=0
		for i in times:
			m,s=i.split(':')
			s=float(s)
			m=int(m)
			s+=m*60
			srednia+=s
			ss+=s
		n=int(len(times))
		fl_srednia=float(srednia)/n
		srednia=int(srednia)/n
		m=srednia/60
		s=fl_srednia%60
		s=round(s,1)
		if s<10: sep='0'
		else: sep = ''
		stdscr.addstr(winlin-1,1,'Czas',curses.color_pair(1)+curses.A_BOLD)
		stdscr.addstr(winlin-1,wincol-16,'Srednia: '+str(m)+':'+sep+str(s),curses.A_REVERSE)
		sm=ss/60
		ss=ss%60
		sm=int(sm)
		if ss<10: sep='0'
		else: sep = ''
		stdscr.addstr(winlin-1,wincol-30,'Suma: '+str(sm)+':'+sep+str(ss),curses.A_REVERSE)
		
		ranking_path = os.path.join(dirs_with_lvl[choose-1], 'ranking')
		if not os.path.exists(ranking_path):
			rankfile = open(ranking_path, 'w+')
			rankfile.close()
		rankfile = open(ranking_path, 'rw')
		value = []
		for i in xrange(1,len(rankfile.readlines())+1):
			linia = linecache.getline(ranking_path,i)
			linia = linia.strip('\n')
			value.append( linia )
		
		psep = ''
		pos = 1
		printed_new = False
		for i in value:
			psep = ''
			time.sleep(0.05)
			if not pos>=10: psep = ' '
			if stdscr.getyx()[0] == winlin-3:
				break
			elif printed_new == False and stdscr.getyx()[0] == winlin-5:
				stdscr.addstr(winlin-4,(wincol/2)-14,'...')
				stdscr.addstr(winlin-3,(wincol/2)-10,'_______________',curses.A_BOLD)
				inputY = pos+3
				inputX = (wincol/2)-10
				pos = 1
				allpos = 1
				for j in value:
					(jtime,jplayer) = j.split(' ')
					ktime = ''
					for k in jtime:
						if not (k == ':'):
							ktime = ktime+k
							stdscr.refresh()
					if float( ktime ) < float( str(sm)+str(ss) ):
						pos+=1
						allpos+=1
					else:
						allpos+=1
				stdscr.addstr(winlin-3,(wincol/2)-14,str(pos)+'. '+psep+19*' '+str(sm)+':'+sep+str(ss),curses.A_BOLD)
				if pos == allpos: your_pos = -1
				else: your_pos=pos
				printed_new = True
				break
			(itime,iplayer) = i.split(' ')
			jitime = ''
			for j in itime:
				if not (j == ':'):
					jitime = jitime+j
					stdscr.refresh()
			if float( jitime ) < float( str(sm)+str(ss) ) or printed_new:
				whchs = 19-len(iplayer)
				stdscr.addstr(pos+2,(wincol/2)-14,str(pos) + '. ' + psep + iplayer + whchs*' ' + itime)
				pos+=1
			else:
				stdscr.addstr(pos+2,(wincol/2)-14,str(pos)+'. '+psep+19*' '+str(sm)+':'+sep+str(ss),curses.A_BOLD)
				stdscr.addstr(pos+2,(wincol/2)-10,'_______________',curses.A_BOLD)
				inputY = pos+2
				inputX = (wincol/2)-10
				printed_new = True
				your_pos = pos
				pos+=1
				whchs = 19-len(iplayer)
				stdscr.addstr(pos+2,(wincol/2)-14,str(pos) + '. ' + psep + iplayer + whchs*' ' + itime)
				pos+=1
		if not printed_new:
			stdscr.addstr(pos+2,(wincol/2)-14,str(pos)+'. '+psep+19*' '+str(sm)+':'+sep+str(ss),curses.A_BOLD)
			stdscr.addstr(pos+2,(wincol/2)-10,'_______________',curses.A_BOLD)
			inputY = pos+2
			inputX = (wincol/2)-10
			if pos == 1: your_pos = 2
			else: your_pos = -1
		stdscr.refresh()
		curses.echo()
		stdscr.attron(curses.A_BOLD)
		player_name = ' '
		while player_name.find(' ') != -1 or player_name == '' or len(player_name) > 15:
			stdscr.addstr(inputY,inputX,'_______________')
			player_name = stdscr.getstr(inputY,inputX)
		whchs = 15-len(player_name)
		stdscr.addstr(inputY,inputX+len(player_name),whchs*' ')
		stdscr.hline(0,0,' ',wincol)
		if your_pos == 1:
			stdscr.addstr(0,(wincol/2)-5,'Pierwszy!!!',curses.color_pair(12)+curses.A_BOLD)
		elif your_pos == -1:
			stdscr.addstr(0,(wincol/2)-4,'Slabo :(',curses.color_pair(11)+curses.A_BOLD)
		else:
			stdscr.addstr(0,(wincol/2)-5,'Gratulacje!',curses.color_pair(2)+curses.A_BOLD)
		stdscr.refresh()
		time.sleep(1.5)
		#Zapisywanie pliku rankingu
		rank_sorted = []
		if value != '':
			for i in xrange(0,len(value)):
				rank_sorted.append( linecache.getline(ranking_path,i) )
		value.append(str(sm)+':'+sep+str(ss)+' '+player_name)
		rank_sorted=sorted(value)
		
		##for j in value
		#(vtime,vplayer) = j.split(' ')
		#ivtime = ''
		#for i in vtime:
		#	if not (i == ':'):
		#		ivtime = ivtime+i
		#		stdscr.refresh()
		#if float( ivtime ) < float( str(sm)+str(ss) ):
		#	rank_sorted.append(str(sm)+':'+sep+str(ss)+' '+player_name)
		#else:
		#	rank_sorted.append(j)
		
		rankfile = open(ranking_path, 'w')
		for item in rank_sorted:
			rankfile.write(item+'\n')
		#rankfile.writelines(rank_sorted)
		rankfile.close()

	
	curses.nocbreak()
	stdscr.keypad(0)
	curses.endwin()
	print '\nDziękuję za granie w Kveiki!'
	print '------------------------------'
	if not outranked:
		print 'Czas przechodzenia poszczególnych poziomów:'
		no=1
		for i in times:
			print str(no)+': '+i
			no+=1
		print ' średnia: '+str(m)+':'+sep+str(s)
		print ' suma: '+str(sm)+':'+sep+str(ss)
	else:
		print "\nNie przeszedłeś całego level set'u."
	print '\033[0;0;0m'


class player:
	def __init__(self):
		self.solid = ['X','R','G','B','Y','D']
		self.movable = ['C','K','r','g','b','y',' ']
		
		self.coins = 0
		self.coinsMAX = 0
		self.restoreF = False
		self.finish = False

		for i in lvl_structure:
			try:
				self.x=lvl_structure[lvl_structure.index(i)].index('P')
				self.xL=self.x
				self.y=lvl_structure.index(i)
				self.yL=self.y
			except:
				pass

		self.startx = self.x
		self.starty = self.y

		for i in lvl_structure:
			number=i.count('C')
			self.coinsMAX+=number

	def reset(self):
		stdscr.addstr(self.y+3,self.x,'@', curses.color_pair(11)+curses.A_BOLD )
		self.__init__()
		stdscr.addstr(self.y+3,self.x,'@', curses.color_pair(2)+curses.A_BOLD )
		time.sleep(0.5)
		stdscr.addstr(self.y+3,self.x,'@', curses.color_pair(2) )

	def goUP(self):
		if not lvl_structure[self.y-1][self.x] in self.solid:
			if lvl_structure[self.y-1][self.x] == 'Z':
				if (lvl_structure[self.y-2][self.x] in self.movable) and (lvl_structure[self.y-3][self.x] == ' ' or lvl_structure[self.y-2][self.x] == ' '):
					if lvl_structure[self.y-3][self.x] == ' ': set_char_in_structure(self.y-3,self.x,lvl_structure[self.y-2][self.x])
					set_char_in_structure(self.y-2,self.x,lvl_structure[self.y-1][self.x])
					set_char_in_structure(self.y-1,self.x,' ')
					for i in xrange(1,4):
						if lvl_structure[self.y-i][self.x] == ' ': stdscr.addstr(self.y+3-i,self.x,' ',curses.color_pair(1))
						elif lvl_structure[self.y-i][self.x] == 'C': stdscr.addstr(self.y+3-i,self.x,'$',curses.color_pair(4))
						elif lvl_structure[self.y-i][self.x] == 'K': stdscr.addstr(self.y+3-i,self.x,'F',curses.color_pair(1))
						elif lvl_structure[self.y-i][self.x] == 'r': stdscr.addstr(self.y+3-i,self.x,'F',curses.color_pair(7))
						elif lvl_structure[self.y-i][self.x] == 'g': stdscr.addstr(self.y+3-i,self.x,'F',curses.color_pair(8))
						elif lvl_structure[self.y-i][self.x] == 'b': stdscr.addstr(self.y+3-i,self.x,'F',curses.color_pair(3))
						elif lvl_structure[self.y-i][self.x] == 'y': stdscr.addstr(self.y+3-i,self.x,'F',curses.color_pair(4))
						elif lvl_structure[self.y-i][self.x] == 'Z': stdscr.addstr(self.y+3-i,self.x,'X',curses.color_pair(9))

					self.xL = self.x
					self.yL = self.y
					self.y-=1
					self.update()
			else:
				self.xL = self.x
				self.yL = self.y
				self.y-=1
				self.update()

	def goDOWN(self):
		if not lvl_structure[self.y+1][self.x] in self.solid:
			if lvl_structure[self.y+1][self.x] == 'Z':
				if (lvl_structure[self.y+2][self.x] in self.movable) and (lvl_structure[self.y+3][self.x] == ' ' or lvl_structure[self.y+2][self.x] == ' '):
					if lvl_structure[self.y+3][self.x] == ' ': set_char_in_structure(self.y+3,self.x,lvl_structure[self.y+2][self.x])
					set_char_in_structure(self.y+2,self.x,lvl_structure[self.y+1][self.x])
					set_char_in_structure(self.y+1,self.x,' ')
					for i in xrange(1,4):
						if lvl_structure[self.y+i][self.x] == ' ': stdscr.addstr(self.y+3+i,self.x,' ',curses.color_pair(1))
						elif lvl_structure[self.y+i][self.x] == 'C': stdscr.addstr(self.y+3+i,self.x,'$',curses.color_pair(4))
						elif lvl_structure[self.y+i][self.x] == 'K': stdscr.addstr(self.y+3+i,self.x,'F',curses.color_pair(1))
						elif lvl_structure[self.y+i][self.x] == 'r': stdscr.addstr(self.y+3+i,self.x,'F',curses.color_pair(7))
						elif lvl_structure[self.y+i][self.x] == 'g': stdscr.addstr(self.y+3+i,self.x,'F',curses.color_pair(8))
						elif lvl_structure[self.y+i][self.x] == 'b': stdscr.addstr(self.y+3+i,self.x,'F',curses.color_pair(3))
						elif lvl_structure[self.y+i][self.x] == 'y': stdscr.addstr(self.y+3+i,self.x,'F',curses.color_pair(4))
						elif lvl_structure[self.y+i][self.x] == 'Z': stdscr.addstr(self.y+3+i,self.x,'X',curses.color_pair(9))

					self.xL = self.x
					self.yL = self.y
					self.y+=1
					self.update()
			else:
				self.xL = self.x
				self.yL = self.y
				self.y+=1
				self.update()

	def goLEFT(self):
		if not lvl_structure[self.y][self.x-1] in self.solid:
			if lvl_structure[self.y][self.x-1] == 'Z':
				if (lvl_structure[self.y][self.x-2] in self.movable) and (lvl_structure[self.y][self.x-3] == ' ' or lvl_structure[self.y][self.x-2] == ' '):
					if lvl_structure[self.y][self.x-3] == ' ': set_char_in_structure(self.y,self.x-3,lvl_structure[self.y][self.x-2])
					set_char_in_structure(self.y,self.x-2,lvl_structure[self.y][self.x-1])
					set_char_in_structure(self.y,self.x-1,' ')
					for i in xrange(1,4):
						if lvl_structure[self.y][self.x-i] == ' ': stdscr.addstr(self.y+3,self.x-i,' ',curses.color_pair(1))
						elif lvl_structure[self.y][self.x-i] == 'C': stdscr.addstr(self.y+3,self.x-i,'$',curses.color_pair(4))
						elif lvl_structure[self.y][self.x-i] == 'K': stdscr.addstr(self.y+3,self.x-i,'F',curses.color_pair(1))
						elif lvl_structure[self.y][self.x-i] == 'r': stdscr.addstr(self.y+3,self.x-i,'F',curses.color_pair(7))
						elif lvl_structure[self.y][self.x-i] == 'g': stdscr.addstr(self.y+3,self.x-i,'F',curses.color_pair(8))
						elif lvl_structure[self.y][self.x-i] == 'b': stdscr.addstr(self.y+3,self.x-i,'F',curses.color_pair(3))
						elif lvl_structure[self.y][self.x-i] == 'y': stdscr.addstr(self.y+3,self.x-i,'F',curses.color_pair(4))
						elif lvl_structure[self.y][self.x-i] == 'Z': stdscr.addstr(self.y+3,self.x-i,'X',curses.color_pair(9))

					self.xL = self.x
					self.yL = self.y
					self.x-=1
					self.update()
			else:
				self.xL = self.x
				self.yL = self.y
				self.x-=1
				self.update()


	def goRIGHT(self):
		if not lvl_structure[self.y][self.x+1] in self.solid:
			if lvl_structure[self.y][self.x+1] == 'Z':
				if (lvl_structure[self.y][self.x+2] in self.movable) and (lvl_structure[self.y][self.x+3] == ' ' or lvl_structure[self.y][self.x+2] == ' '):
					if lvl_structure[self.y][self.x+3] == ' ': set_char_in_structure(self.y,self.x+3,lvl_structure[self.y][self.x+2])
					set_char_in_structure(self.y,self.x+2,lvl_structure[self.y][self.x+1])
					set_char_in_structure(self.y,self.x+1,' ')
					for i in xrange(1,4):
						if lvl_structure[self.y][self.x+i] == ' ': stdscr.addstr(self.y+3,self.x+i,' ',curses.color_pair(1))
						elif lvl_structure[self.y][self.x+i] == 'C': stdscr.addstr(self.y+3,self.x+i,'$',curses.color_pair(4))
						elif lvl_structure[self.y][self.x+i] == 'K': stdscr.addstr(self.y+3,self.x+i,'F',curses.color_pair(1))
						elif lvl_structure[self.y][self.x+i] == 'r': stdscr.addstr(self.y+3,self.x+i,'F',curses.color_pair(7))
						elif lvl_structure[self.y][self.x+i] == 'g': stdscr.addstr(self.y+3,self.x+i,'F',curses.color_pair(8))
						elif lvl_structure[self.y][self.x+i] == 'b': stdscr.addstr(self.y+3,self.x+i,'F',curses.color_pair(3))
						elif lvl_structure[self.y][self.x+i] == 'y': stdscr.addstr(self.y+3,self.x+i,'F',curses.color_pair(4))
						elif lvl_structure[self.y][self.x+i] == 'Z': stdscr.addstr(self.y+3,self.x+i,'X',curses.color_pair(9))

					self.xL = self.x
					self.yL = self.y
					self.x+=1
					self.update()
			else:
				self.xL = self.x
				self.yL = self.y
				self.x+=1
				self.update()

	def update(self):
		find = ''
		
		if self.restoreF == False:
			stdscr.addstr(self.yL+3,self.xL,' ', curses.color_pair(1) )
		else:
			self.restoreF = False
			stdscr.addstr(self.yL+3,self.xL,'^', curses.color_pair(3) )
		stdscr.addstr(self.y+3,self.x,'@', curses.color_pair(2) )
		stdscr.refresh()
		
		for i in Monsters:
			if (self.y,self.x) == (i.y,i.x):
				curses.flash()
				self.reset()

		if lvl_structure[self.y][self.x] == 'F':
			if self.coins == self.coinsMAX:
				stdscr.addstr(0,0,'Done')
				stdscr.refresh()
				self.finish = True
			else:
				self.restoreF = True

		if lvl_structure[self.y][self.x] == 'C':
			set_char_in_structure(self.y,self.x,' ')
			self.coins += 1

		if lvl_structure[self.y][self.x] == 'K': find ='D'
		elif lvl_structure[self.y][self.x] == 'r': find ='R'
		elif lvl_structure[self.y][self.x] == 'g': find ='G'
		elif lvl_structure[self.y][self.x] == 'b': find ='B'
		elif lvl_structure[self.y][self.x] == 'y': find ='Y'
		if find != '':
			self.tmpx = 0
			self.tmpy = 0
			for i in lvl_structure:
				for j in i:
					if j == find:
						self.tmpx=i.index(find)
						self.tmpy=lvl_structure.index(i)
						set_char_in_structure(self.tmpy,self.tmpx,' ')
						stdscr.addstr(self.tmpy+3,self.tmpx,' ', curses.color_pair(1) )
						stdscr.refresh()


class monster:
	def __init__(self,y,x):
		self.x = x
		self.y = y
		self.last_go = ' '
		
	def update(self):
		available=0
		if self.y>0 and len(lvl_structure[self.y-1])>self.x and lvl_structure[self.y-1][self.x] == '*':
			available+=1
		if self.x+1<len(lvl_structure[self.y]) and len(lvl_structure[self.y])>self.x+1 and lvl_structure[self.y][self.x+1] == '*':
			available+=1
		if self.y+1<len(lvl_structure) and len(lvl_structure[self.y+1])>self.x and lvl_structure[self.y+1][self.x] == '*':
			available+=1
		if self.x > 0 and len(lvl_structure[self.y])>self.x-1 and lvl_structure[self.y][self.x-1] == '*':
			available+=1

		if (self.y > 0 and len(lvl_structure[self.y-1])>self.x and lvl_structure[self.y-1][self.x] == '*') and (self.last_go != 'DOWN' or available == 1):
			lvl_structure[self.y][self.x] = '*'
			stdscr.addstr(self.y+3,self.x,' ',curses.color_pair(1) )
			self.y-=1
			lvl_structure[self.y][self.x] = 'm'
			stdscr.addstr(self.y+3,self.x,'@',curses.color_pair(11)+curses.A_BOLD )
			self.last_go = 'UP'
		elif (self.x+1<len(lvl_structure[self.y]) and len(lvl_structure[self.y])>self.x+1 and  lvl_structure[self.y][self.x+1] == '*') and (self.last_go != 'LEFT' or available == 1):
			lvl_structure[self.y][self.x] = '*'
			stdscr.addstr(self.y+3,self.x,' ',curses.color_pair(1) )
			self.x+=1
			lvl_structure[self.y][self.x] = 'm'
			stdscr.addstr(self.y+3,self.x,'@',curses.color_pair(11)+curses.A_BOLD )
			self.last_go = 'RIGHT'
		elif (self.y+1<len(lvl_structure) and len(lvl_structure[self.y+1])>self.x and lvl_structure[self.y+1][self.x] == '*') and (self.last_go != 'UP' or available == 1):
			lvl_structure[self.y][self.x] = '*'
			stdscr.addstr(self.y+3,self.x,' ',curses.color_pair(1) )
			self.y+=1
			lvl_structure[self.y][self.x] = 'm'
			stdscr.addstr(self.y+3,self.x,'@',curses.color_pair(11)+curses.A_BOLD )
			self.last_go = 'DOWN'
		elif (self.x> 0 and len(lvl_structure[self.y])>self.x-1 and lvl_structure[self.y][self.x-1] == '*') and (self.last_go != 'RIGHT' or available == 1):
			lvl_structure[self.y][self.x] = '*'
			stdscr.addstr(self.y+3,self.x,' ',curses.color_pair(1) )
			self.x-=1
			lvl_structure[self.y][self.x] = 'm'
			stdscr.addstr(self.y+3,self.x,'@',curses.color_pair(11)+curses.A_BOLD )
			self.last_go = 'LEFT'
		stdscr.refresh()
		
		if (gracz.y,gracz.x) == (self.y,self.x):
			curses.flash()
			gracz.reset()


def update_monsters(a,b):
	for monster in Monsters:
		monster.update()

def set_char_in_structure(y,x,char):
	lvl_structure[y][x] = char


dirs_with_lvl = []
for i in os.listdir('.'):
	if os.path.isdir(i) == True:
		isLvlSet = False
		for j in os.listdir(os.path.join('.',i)):
			if j.endswith('.lvl'):
				isLvlSet = True
		if isLvlSet:
			dirs_with_lvl.append(i)

print 'Wybierz zestaw'
for i in dirs_with_lvl:
	print ' '+str(dirs_with_lvl.index(i)+1)+'. '+str(i)
choose = len(dirs_with_lvl)+1
while choose > len(dirs_with_lvl) or choose == 0:
	try:
		choose=input('Numer zestawu: ')
	except:
		choose = 1

#Init curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
curses.start_color()
curses.curs_set(0)

def main_game():
	global sec
	global minutes
	global lvl_structure
	global wincol
	global winlin
	global start_time
	global Monsters
	global gracz
	global outranked
	
	#Wczytanie pliku level'u
	lvl_structure=[]
	tmp = []
	for line in xrange(1,len(open(file_name, 'rU').readlines())+1):
		tmp = []
		for char in linecache.getline(file_name, line):
			if char != '\n':
				tmp.append(char)
		lvl_structure.append(tmp)
	
	gracz = player()
	#Sprawdzanie czy level nie wystaje poza okno terminala
	lvl_sizey=len(lvl_structure)+10
	a=0
	lvl_sizex=0
	for i in xrange(0,len(lvl_structure)):
		a=len(lvl_structure[i])
		if a>lvl_sizex: lvl_sizex=a
	if lvl_sizex<50: lvl_sizex=50

	while lvl_sizex>wincol or lvl_sizey>winlin:
		stdscr.clear()
		winlin, wincol =  stdscr.getmaxyx()
		xx=(wincol/2)
		yy=winlin/2
		stdscr.addstr(yy-1,xx-7,'Powieksz okno,',curses.A_BOLD)
		stdscr.addstr(yy,xx-9,'aby rozpoczac gre!',curses.A_BOLD)
		stdscr.refresh()

	#Rysowanie poziomu
	stdscr.clear()
	stdscr.addstr(0,0,'\nLevel'+' '+str(sorted(os.listdir(dirs_with_lvl[choose-1])).index(level)+1)+' ('+level+')\n\n', curses.color_pair(5))
	
	stdscr.addstr(3,0,'')
	Monsters = []
	MonX = -1
	MonY = 0
	for char in open(file_name).read():
		MonX += 1
		if char == 'X':
			stdscr.addstr( "#", curses.color_pair(1) )
		elif char == ' ':
			stdscr.addstr( " ", curses.color_pair(1) )
		elif char == '*':
			stdscr.addstr( " ", curses.color_pair(1) )
		elif char == 's':
			stdscr.addstr( " ", curses.color_pair(2) )
		elif char == 'P':
			stdscr.addstr( "@", curses.color_pair(2) )
		elif char == 'F':
			stdscr.addstr( "^", curses.color_pair(3) )
		elif char == 'C':
			stdscr.addstr( "$", curses.color_pair(4) )
		elif char == 'D':
			stdscr.addstr( "=", curses.color_pair(1) )
		elif char == 'K':
			stdscr.addstr( "F", curses.color_pair(1) )
		elif char == 'G':
			stdscr.addstr( "=", curses.color_pair(8) )
		elif char == 'g':
			stdscr.addstr( "F", curses.color_pair(8) )
		elif char == 'R':
			stdscr.addstr( "=", curses.color_pair(7) )
		elif char == 'r':
			stdscr.addstr( "F", curses.color_pair(7) )
		elif char == 'Y':
			stdscr.addstr( "=", curses.color_pair(4) )
		elif char == 'y':
			stdscr.addstr( "F", curses.color_pair(4) )
		elif char == 'B':
			stdscr.addstr( "=", curses.color_pair(3) )
		elif char == 'b':
			stdscr.addstr( "F", curses.color_pair(3) )
		elif char == 'Z':
			stdscr.addstr( "X", curses.color_pair(9) )
		elif char == 'M':
			stdscr.addstr( "@", curses.color_pair(11)+curses.A_BOLD )
			#for i in lvl_structure:
			#	try:
			#		monX=lvl_structure[lvl_structure.index(i)].index('M')
			#		monY=lvl_structure.index(i)
			#	except:
			#		pass
			lvl_structure[MonY][MonX] = 'm'
			Monsters.append( monster(MonY,MonX) )
		elif char == '\n':
			MonY+=1
			MonX = -1
			stdscr.addstr( "\n", curses.color_pair(1) )
			line+=1
		stdscr.refresh()

	must_reset = False
	while gracz.finish == False:
		winlin, wincol =  stdscr.getmaxyx()
		stdscr.addstr(winlin-2,0,'Monety:', curses.color_pair(6) )
		stdscr.addstr(winlin-2,9,str(gracz.coins)+'/'+str(gracz.coinsMAX), curses.color_pair(10) )

		now_time=time.time()
		now_time=int(now_time)
		sec=now_time-start_time
		minutes=sec/60
		sec=sec%60
		sec=str(sec)
		minutes=str(minutes)
		if len(sec)==1: sep='0'
		else: sep=''
		stdscr.addstr(winlin-2,16,'Czas:', curses.color_pair(6) )
		stdscr.addstr(winlin-2,24,minutes+':'+sep+sec, curses.color_pair(10) )
		if (lvl_structure[gracz.y][gracz.x-1]=='Z' and lvl_structure[gracz.y][gracz.x-2] == 'C' and (lvl_structure[gracz.y-1][gracz.x-1] in gracz.solid or lvl_structure[gracz.y+1][gracz.x-1] in gracz.solid) and  lvl_structure[gracz.y-1][gracz.x-2] in gracz.solid and lvl_structure[gracz.y+1][gracz.x-2] in gracz.solid and lvl_structure[gracz.y][gracz.x-3] in gracz.solid) or (lvl_structure[gracz.y][gracz.x+1]=='Z' and lvl_structure[gracz.y][gracz.x+2] == 'C' and (lvl_structure[gracz.y-1][gracz.x+1] in gracz.solid or lvl_structure[gracz.y+1][gracz.x+1] in gracz.solid) and  lvl_structure[gracz.y-1][gracz.x+2] in gracz.solid and lvl_structure[gracz.y+1][gracz.x+2] in gracz.solid and lvl_structure[gracz.y][gracz.x+3] in gracz.solid) or (lvl_structure[gracz.y-1][gracz.x]=='Z' and lvl_structure[gracz.y-2][gracz.x] == 'C' and (lvl_structure[gracz.y-1][gracz.x-1] in gracz.solid or lvl_structure[gracz.y-1][gracz.x+1] in gracz.solid) and  lvl_structure[gracz.y-2][gracz.x-1] in gracz.solid and lvl_structure[gracz.y-2][gracz.x+1] in gracz.solid and lvl_structure[gracz.y-3][gracz.x] in gracz.solid) or (lvl_structure[gracz.y+1][gracz.x]=='Z' and lvl_structure[gracz.y+2][gracz.x] == 'C' and (lvl_structure[gracz.y+1][gracz.x-1] in gracz.solid or lvl_structure[gracz.y+1][gracz.x+1] in gracz.solid) and lvl_structure[gracz.y+2][gracz.x-1] in gracz.solid and lvl_structure[gracz.y+2][gracz.x+1] in gracz.solid and lvl_structure[gracz.y+3][gracz.x] in gracz.solid):
			must_reset = True
		if must_reset:	
			stdscr.addstr(winlin-2,39,'R - restart',curses.A_BLINK+curses.A_BOLD)
		else:
			stdscr.addstr(winlin-2,39,'R - restart',curses.A_NORMAL+curses.A_BOLD)

		for i in xrange(0,wincol-1):
			stdscr.addstr(winlin-1,i,' ')
			stdscr.addstr(winlin-3,i,' ')
			stdscr.addstr(winlin-4,i,' ')
			stdscr.addstr(winlin-5,i,' ')

		signal.signal(signal.SIGALRM,update_monsters)
		if signal.getitimer(signal.ITIMER_REAL)[0] == 0: signal.setitimer(signal.ITIMER_REAL,0.5)
		key = stdscr.getch()
		if key == curses.KEY_UP or key == ord('w'):	gracz.goUP()
		elif key == curses.KEY_DOWN or key == ord('s'): gracz.goDOWN()
		elif key == curses.KEY_LEFT or key == ord('a'): gracz.goLEFT()
		elif key == curses.KEY_RIGHT or key == ord('d'): gracz.goRIGHT()
		elif key == ord('r'):
			main_game()
			break
		elif key == ord('q'):
			outranked = True
			exit()
		#elif key == ord('f'): curses.flash()


winlin, wincol =  stdscr.getmaxyx()
curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_WHITE)
if os.path.exists(os.path.join(dirs_with_lvl[choose-1],'discribe')):
	discribe=open( os.path.join(dirs_with_lvl[choose-1],'discribe')).read()
	stdscr.addstr(1,1,'\n'+discribe,curses.color_pair(1))
	stdscr.refresh()
	stdscr.addstr(winlin-2,1,'\n<ENTER>', curses.color_pair(2) )
	stdscr.getch()

if os.path.exists(os.path.join(dirs_with_lvl[choose-1],'queue')):
	levels = open(os.path.join(dirs_with_lvl[choose-1],'queue'),'rU').readlines()
	for i in levels:
		levels[levels.index(i)] = levels[levels.index(i)].strip('\n')
else:
	levels = sorted( os.listdir(dirs_with_lvl[choose-1]) )

times=[]
outranked = False
for level in levels:
	if level.endswith('.lvl'):
		try:
			if sec+minutes!=0:
				times.append(minutes+':'+sec)
		except:
			pass
			
		start_time=time.time()
		start_time=int(start_time)

		file_name = os.path.join(dirs_with_lvl[choose-1],level)
		#Przypisanie kolorów
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # ściana, drzwi, klucz
		curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) #gracz
		curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE) # wyjście i niebieski klucz i drzwi
		curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_WHITE) # moneta, żółty klucz i drzwi
		curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK) # inf. o lvl
		curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW) # pasek na dole ekranu
		curses.init_pair(7, curses.COLOR_RED, curses.COLOR_WHITE) # czerwony klucz i drzwi
		curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_WHITE) # zielony klucz i drzwi
		curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLUE) # skrzynki
		curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK) # kuflerz i kuptuż
		curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK) # potwór oraz napis "Słabo :(" na końcu gry
		curses.init_pair(12, curses.COLOR_BLUE, curses.COLOR_BLACK) # napis "Pierwszy!!!" na końcu gry
		main_game()
