#-*- coding: utf-8 -*-
import os,sys
import linecache
import curses
import time
import atexit


@atexit.register
def close_curses():
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()
	print '\nDziękuję za granie w Kveiki!'
	print '------------------------------'
	print 'Czas przechodzenia poszczególnych poziomów:'
	times.append(minutes+':'+sec)
	srednia=0
	ss=0
	sm=0
	no=1
	for i in times:
		print str(no)+': '+i
		m,s=i.split(':')
		s=float(s)
		m=int(m)
		s+=m*60
		srednia+=s
		no+=1
		ss+=s
	n=int(len(times))
	fl_srednia=float(srednia)/n
	srednia=int(srednia)/n
	m=srednia/60
	s=fl_srednia%60
	s=round(s,1)
	if s<10: sep='0'
	else: sep = ''
	print ' średnia: '+str(m)+':'+sep+str(s)
	sm=ss/60
	ss=ss%60
	sm=int(sm)
	if ss<10: sep='0'
	else: sep = ''
	print ' suma: '+str(sm)+':'+sep+str(ss)
	
	player_name = raw_input('\nTwój nick >\033[0;0;1m')
	if player_name.strip() != '':
		ranking_path = os.path.join(dirs_with_lvl[choose-1], 'ranking')
		rankfile = open(ranking_path, 'rw+')
		value = []
		print ranking_path
		for i in xrange(1,len(rankfile.readlines())+1):
			linia = linecache.getline(ranking_path,i)
			linia = linia.strip('\n')
			value.append( linia )
		rank_sorted = []
		if value != '':
			for i in xrange(0,len(value)):
				rank_sorted.append( linecache.getline(ranking_path,i) )
		value.append(str(sm)+':'+sep+str(ss)+' '+player_name)
		rank_sorted=sorted(value)
		print rank_sorted
		rankfile = open(ranking_path, 'w')
		for item in rank_sorted:
			rankfile.write(item+'\n')
		#rankfile.writelines(rank_sorted)
		rankfile.close()
		print '\033[0;0;0m'


class player:
	def __init__(self):
		self.coins = 0
		self.coinsMAX = 0
		self.finish = False
		self.restoreF = False

		for i in lvl_structure:
			try:
				self.x=lvl_structure[lvl_structure.index(i)].index('P')
				self.xL=self.x
				self.y=lvl_structure.index(i)
				self.yL=self.y
			except:
				pass

		for i in lvl_structure:
			number=i.count('C')
			self.coinsMAX+=number

		#stdscr.addstr(0,0,str(self.x)+' '+str(self.y))

	def goUP(self):
		if lvl_structure[self.y-1][self.x] != 'X':
			if lvl_structure[self.y-1][self.x] != 'D':
				if lvl_structure[self.y-1][self.x] != 'R':
					if lvl_structure[self.y-1][self.x] != 'G':
						if lvl_structure[self.y-1][self.x] != 'B':
							if lvl_structure[self.y-1][self.x] != 'Y':
								self.xL = self.x
								self.yL = self.y

								self.y-=1
								self.update()

	def goDOWN(self):
		#print lvl_structure[self.y+1][self.x] != 'X'
		if lvl_structure[self.y+1][self.x] != 'X':
			if lvl_structure[self.y+1][self.x] != 'D':
				if lvl_structure[self.y+1][self.x] != 'R':
					if lvl_structure[self.y+1][self.x] != 'G':
						if lvl_structure[self.y+1][self.x] != 'B':
							if lvl_structure[self.y+1][self.x] != 'Y':
								self.xL = self.x
								self.yL = self.y

								self.y+=1
								self.update()

	def goLEFT(self):
		if lvl_structure[self.y][self.x-1] != 'X':
			if lvl_structure[self.y][self.x-1] != 'D':
				if lvl_structure[self.y][self.x-1] != 'R':
					if lvl_structure[self.y][self.x-1] != 'G':
						if lvl_structure[self.y][self.x-1] != 'B':
							if lvl_structure[self.y][self.x-1] != 'Y':
								self.xL = self.x
								self.yL = self.y

								self.x-=1
								self.update()


	def goRIGHT(self):
		if lvl_structure[self.y][self.x+1] != 'X':
			if lvl_structure[self.y][self.x+1] != 'D':
				if lvl_structure[self.y][self.x+1] != 'R':
					if lvl_structure[self.y][self.x+1] != 'G':
						if lvl_structure[self.y][self.x+1] != 'B':
							if lvl_structure[self.y][self.x+1] != 'Y':
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

		if lvl_structure[self.y][self.x] == 'F':
			if self.coins == self.coinsMAX:
				stdscr.addstr(0,0,'Done')
				stdscr.refresh()
				self.finish = True
			else:
				self.restoreF = True

		if lvl_structure[self.y][self.x] == 'C':
			clear_char_in_structure(self.y,self.x)
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
						clear_char_in_structure(self.tmpy,self.tmpx)
						stdscr.addstr(self.tmpy+3,self.tmpx,' ', curses.color_pair(1) )
						stdscr.refresh()


def clear_char_in_structure(y,x):
	lvl_structure[y][x] = ' '


dirs_with_lvl = []
if len(sys.argv) == 2:
	lvl_set = sys.argv[1]
else:
	for i in os.listdir('.'):
		if os.path.isdir(i) == True:
			isLvlSet = False
			for j in os.listdir(os.path.join('.',i)):
				if j.endswith('.lvl'):
					isLvlSet = True
			if isLvlSet:
				dirs_with_lvl.append(i)

if len(dirs_with_lvl) == 0 and len(sys.argv) != 2:
	print "Nie znaleziono żadnych zestawów z level'ami."
	print "Nie podałeś ścieżki do zestawu. kończę..."
	exit()
if len(sys.argv) != 2:
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

winlin, wincol =  stdscr.getmaxyx()
curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_WHITE)
if os.path.exists(os.path.join(dirs_with_lvl[choose-1],'discribe')):
	discribe=open( os.path.join(dirs_with_lvl[choose-1],'discribe')).read()
	stdscr.addstr(1,1,'\n'+discribe,curses.color_pair(1))
	stdscr.refresh()
	stdscr.addstr(winlin-2,1,'\n<ENTER>', curses.color_pair(2) )
	stdscr.getch()

if sys.argv != 2:
	chosen_directory = os.listdir(dirs_with_lvl[choose-1])
else:
	chosen_directory = os.listdir(os.path.join('.',sys.argv[1]))
times=[]
for level in sorted(chosen_directory):
	if level.endswith('.lvl'):
		try:
			if sec+minutes!=0:
				times.append(minutes+':'+sec)
		except:
			pass

		start_time=time.time()
		start_time=int(start_time)

		stdscr.clear()
		stdscr.addstr(0,0,'\nLevel'+' '+str(sorted(os.listdir(dirs_with_lvl[choose-1])).index(level)+1)+' ('+level+')\n\n', curses.color_pair(5))

		file_name = os.path.join(dirs_with_lvl[choose-1],level)
		lvlfile = open(file_name)
		#Przypisanie kolorów
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # ściana, drzwi, klucz
		curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) #gracz
		curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE) # wyjście i niebieski klucz i drzwi
		curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_WHITE) # moneta, żółty klucz i drzwi
		curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK) # inf. o lvl
		curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW) # pasek na dole ekranu
		curses.init_pair(7, curses.COLOR_RED, curses.COLOR_WHITE) # czerwony klucz i drzwi
		curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_WHITE) # zielony klucz i drzwi
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
		for char in lvlfile.read():
			if char == 'X':
				stdscr.addstr( "#", curses.color_pair(1) )
			elif char == ' ':
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
			elif char == '\n':
				stdscr.addstr( "\n", curses.color_pair(1) )
				line+=1
			stdscr.refresh()

		while gracz.finish == False:
			winlin, wincol =  stdscr.getmaxyx()
			stdscr.addstr(winlin-2,0,'Monety:', curses.color_pair(6) )
			stdscr.attron(curses.A_BOLD)
			stdscr.addstr(winlin-2,9,str(gracz.coins)+'/'+str(gracz.coinsMAX))

			now_time=time.time()
			now_time=int(now_time)
			sec=now_time-start_time
			minutes=sec/60
			##stdscr.addstr(20,0,str(sec))
			##stdscr.addstr(20,5,str(sec%60))
			sec=sec%60
			sec=str(sec)
			minutes=str(minutes)
			if len(sec)==1: sep='0'
			else: sep=''
			stdscr.addstr(winlin-2,16,'Czas:', curses.color_pair(6) )
			stdscr.attron(curses.A_BOLD)
			stdscr.addstr(winlin-2,24,minutes+':'+sep+sec)
			for i in xrange(0,wincol-1):
				stdscr.addstr(winlin-1,i,' ')
				stdscr.addstr(winlin-3,i,' ')
				stdscr.addstr(winlin-4,i,' ')
				stdscr.addstr(winlin-5,i,' ')

			key = stdscr.getch()
			if key == curses.KEY_UP or key == ord('w'):	gracz.goUP()
			elif key == curses.KEY_DOWN or key == ord('s'): gracz.goDOWN()
			elif key == curses.KEY_LEFT or key == ord('a'): gracz.goLEFT()
			elif key == curses.KEY_RIGHT or key == ord('d'): gracz.goRIGHT()
			elif key == ord('q'): exit()
