board = []
bot_is_white=0
def init_board():
	for i in range(0, 8):
		board.append([])
		for j in range(0, 8):
			board[i].append(-1)

def read_board():
	global bot_is_white
	global board
	board_file = open("board_file", 'r')
	line = board_file.readline()
	bot_is_white=ord(line[0]) - 48
	line = board_file.readline().split(' ')
	while(line[0]!=''):
		piece = line[0]
		position = line[1]
		i = 8 - (ord(position[1]) - 48)
		j = ord(position[0]) - 97
		board[i][j]=int(piece)
		line =  board_file.readline().split(' ')


# get moves
def possible_moves(i, j, piece):
	code = get_code(piece)
	col = get_col(piece)
	if code == 5:  # for pawn
		return pawn_movelist(i, j, col)
	elif code == 4:
		return rook_movelist(i, j, col)
	elif code == 3:
		return knight_movelist(i, j, col)
	elif code == 2:
		return bishop_movelist(i, j, col)
	elif code == 1:
		return queen_movelist(i, j, col)
	else:
		return []

def pawn_movelist(i, j, col):
	movelist = []
	if col == 1:
		if board[i - 1][j] == -1:
			movelist.append(((i - 1, j),(i,j)))
			if (i == 6 and board[i - 2][j] == -1):
				movelist.append(((i - 2, j),(i,j)))
		if (j > 0):
			if get_col(board[i - 1][j - 1]) == 0:
				movelist.append(((i - 1, j - 1),(i,j)))
		if (j < 7):
			if get_col(board[i - 1][j + 1]) == 0:
				movelist.append(((i - 1, j + 1),(i,j)))
	else:
		if board[i + 1][j] == -1:
			movelist.append(((i + 1, j),(i,j)))
			if (i == 1 and board[i + 2][j] == -1):
				movelist.append(((i + 2, j),(i,j)))
		if (j > 0):
			if get_col(board[i + 1][j - 1]) == 1:
				movelist.append(((i + 1, j - 1),(i,j)))
		if (j < 7):
			if get_col(board[i + 1][j + 1]) == 1:
				movelist.append(((i + 1, j + 1),(i,j)))
	return movelist

def rook_movelist(i, j, col):
	movelist = []
	temp_j = j - 1
	if col == 1:
		col = 0
	else:
		col = 1
	while (temp_j >= 0 and board[i][temp_j] == -1):
		movelist.append(((i, temp_j),(i,j)))
		temp_j -= 1
	if (temp_j >= 0 and get_col(board[i][temp_j]) == col ):  # kill
		movelist.append(((i, temp_j),(i,j)))
	# for right direction
	temp_j = j + 1
	while (temp_j < 8 and board[i][temp_j] == -1):
		movelist.append(((i, temp_j),(i,j)))
		temp_j += 1
	if (temp_j < 8 and get_col(board[i][temp_j]) == col ):  # kill
		movelist.append(((i, temp_j),(i,j)))
	# for down
	tempi = i + 1
	while tempi < 8 and board[tempi][j] == -1:
		movelist.append(((tempi, j),(i,j)))
		tempi += 1
	if (tempi < 8 and get_col(board[tempi][j]) == col):  # kill
		movelist.append(((tempi, j),(i,j)))
	# for up
	tempi = i - 1
	while tempi >= 0 and board[tempi][j] == -1:
		movelist.append(((tempi, j),(i,j)))
		tempi -= 1
	if (tempi >= 0 and get_col(board[tempi][j]) == col ):  # kill
		movelist.append(((tempi, j),(i,j)))
	return movelist


def bishop_movelist(i, j, col):
	movelist = []
	if col == 1:
		col = 0
	else:
		col = 1
	# for north east
	tempi = i - 1
	temp_j = j + 1
	while (tempi >= 0 and temp_j < 8 and board[tempi][temp_j] == -1):
		movelist.append(((tempi, temp_j),(i,j)))
		tempi -= 1
		temp_j += 1
	if (tempi >= 0 and temp_j < 8 and get_col(board[tempi][temp_j]) == col):  # kill
		movelist.append(((tempi, temp_j),(i,j)))
	# for north west
	tempi = i - 1
	temp_j = j - 1
	while (tempi >= 0 and temp_j >= 0 and board[tempi][temp_j] == -1):
		movelist.append(((tempi, temp_j),(i,j)))
		tempi -= 1
		temp_j -= 1
	if (tempi >= 0 and temp_j >= 0 and get_col(board[tempi][temp_j]) == col):  # kill
		movelist.append(((tempi, temp_j),(i,j)))
	# south east
	tempi = i + 1
	temp_j = j + 1
	while (tempi < 8 and temp_j < 8 and board[tempi][temp_j] == -1):
		movelist.append(((tempi, temp_j),(i,j)))
		tempi += 1
		temp_j += 1
	if (tempi < 8 and temp_j < 8 and get_col(board[tempi][temp_j]) == col):  # kill
		movelist.append(((tempi, temp_j),(i,j)))
	# south west
	tempi = i + 1
	temp_j = j - 1
	while (tempi < 8 and temp_j >= 0 and board[tempi][temp_j] == -1):
		movelist.append(((tempi, temp_j),(i,j)))
		tempi += 1
		temp_j -= 1
	if (tempi < 8 and temp_j >= 0 and get_col(board[tempi][temp_j]) == col):  # kill
		movelist.append(((tempi, temp_j),(i,j)))
	return movelist


def get_code(piece):
	return piece % 10

def get_col(piece):
	if piece == -1:
		return -1
	if piece > 5:
		return 1
	else:
		return 0

def is_protected(move):
	ans = 0
	if bot_is_white:
		ppiece = board[move[0][0]][move[0][1]]
		board[move[0][0]][move[0][1]]=board[move[1][0]][move[1][1]]
		board[move[1][0]][move[1][1]]=-1
		next_black_movelist = black_movelist()
		final_black_movelist = []
		for x in next_black_movelist:
			if board[x[1][0]][x[1][1]]==5:
				curi=x[1][0]
				curj=x[1][1]
				fini=x[0][0]
				finj=x[0][1]
				if curj!=finj:
					final_black_movelist.append(x[0])
			else:
				final_black_movelist.append(x[0])
		if (move[0][0],move[0][1]) in final_black_movelist:
			ans=1
		board[move[1][0]][move[1][1]]=board[move[0][0]][move[0][1]]
		board[move[0][0]][move[0][1]]=ppiece
	else:
		ppiece = board[move[0][0]][move[0][1]]
		board[move[0][0]][move[0][1]]=board[move[1][0]][move[1][1]]
		board[move[1][0]][move[1][1]]=-1
		next_black_movelist = white_movelist()
		final_black_movelist = []
		for x in next_black_movelist:
			if board[x[1][0]][x[1][1]]==15:
				curi=x[1][0]
				curj=x[1][1]
				fini=x[0][0]
				finj=x[0][1]
				if curj!=finj:
					final_black_movelist.append(x[0])
			else:
				final_black_movelist.append(x[0])
		if (move[0][0],move[0][1]) in final_black_movelist:
			ans=1
		board[move[1][0]][move[1][1]]=board[move[0][0]][move[0][1]]
		board[move[0][0]][move[0][1]]=ppiece
	return ans

def white_movelist(): # working
	movelist = []
	for i in range(0, 8):
		for j in range(0, 8):
			if board[i][j]>9:
				movelist.extend(possible_moves(i,j,board[i][j]))
	return movelist

def black_movelist():
	movelist = []
	for i in range(0, 8):
		for j in range(0, 8):
			if board[i][j]<9:
				movelist.extend(possible_moves(i,j,board[i][j]))
	return movelist

def make_black_move():
	olist = white_movelist() # returns opponent move, fromTowhere
	mlist = black_movelist()
	olist2 = [] # opponents attacking movelist
	for move in olist:
		if board[move[1][0]][move[1][1]]==15:
			curi=move[1][0]
			curj=move[1][1]
			fini=move[0][0]
			finj=move[0][1]
			if curj!=finj:
				olist2.append(move[0])
		else:
			olist2.append(move[0])
	for i in range(0,8):
		for j in range(0,8):
			if board[i][j]==15:
				if j<1:
					olist2.append((i-1,j+1))
				elif j>6:
					olist2.append((i-1,j-1))
				else:
					olist2.append((i-1,j+1))
					olist2.append((i-1,j-1))
	#print("black olist2",olist2)
	#print("black mlist",mlist)
	# basic move prio , ( when a piece simply moves )
	prio = []
	for i in range(0,len(mlist)):
		prio.append(0)
	moveno=0
	for move in mlist: #( add priority to basic moves )
		if board[move[1][0]][move[1][1]]==5:  					# mover is a pawn
			prio[moveno]+=20+(10*(move[0][0]))
			if move[1][1]==1:
				prio[moveno]+=20
			curi=move[1][0]
			curj=move[1][1]
			fini=move[0][0]
			finj=move[0][1]
			if fini==7: # if pawn is promoted
				prio[moveno]+=9999
			if curj!=finj: # its diagonal move
				if board[move[0][0]][move[0][1]]==12: # enemey bishop dies
					if is_protected(move):
						prio[moveno]+=200
					else:
						prio[moveno]+=200
				elif board[move[0][0]][move[0][1]]==14: # enemy rook dies
					prio[moveno]+=9999
				elif board[move[0][0]][move[0][1]]==15: # enemy pawn dies
					if is_protected(move):
						prio[moveno]+=150
					else:
						prio[moveno]+=250
			# if pawn threats
			if move[0][0]<7:
				next_movelist = possible_moves(move[0][0],move[0][1],board[move[1][0]][move[1][1]])
				for nextmove in next_movelist:
					curi=nextmove[1][0]
					curj=nextmove[1][1]
					fini=nextmove[0][0]
					finj=nextmove[0][1]
					if curj!=finj:
						if board[nextmove[0][0]][nextmove[0][1]]==14: # enemy rook dies
							prio[moveno]+=100  # pawn threats rook
				# if pawn threats end
			# if pawns move is under threat
			if move[0] in olist2:
				prio[moveno]-=150
			# if pawns move is under threat ends
			# if current position of pawn is under threat
			if move[1] in olist2:
				if move[0] not in olist2:
					prio[moveno]+=140
			# if current position of pawn is under threat ends

		elif board[move[1][0]][move[1][1]]==4: # mover is a rook
			prio[moveno]+=10
			if board[move[0][0]][move[0][1]]>9: # its enemy piece ,, our rook can kill
				if board[move[0][0]][move[0][1]]==12: # enemey bishop dies
					if is_protected(move):
						prio[moveno]-=350
					else:
						prio[moveno]+=350
				elif board[move[0][0]][move[0][1]]==14: # enemy rook dies
					prio[moveno]+=999
				elif board[move[0][0]][move[0][1]]==15: # enemy pawn dies
					if is_protected(move):
						prio[moveno]-=999
					else:
						prio[moveno]+=150
			# if rook threats in his next move
			next_movelist = possible_moves(move[0][0],move[0][1],board[move[1][0]][move[1][1]])
			for nextmove in next_movelist:
				if board[nextmove[0][0]][nextmove[0][1]]==12: # rook will threat enemy bishop
					prio[moveno]+=200
				elif board[nextmove[0][0]][nextmove[0][1]]==14: # our rook will threat enemy rook ( do not move this)
					prio[moveno]-=999
				elif board[nextmove[0][0]][nextmove[0][1]]==15: # rook will threat enemy pawn
					prio[moveno]+=150
			# if rook threats end
			# if rook move is under threat
			if move[0] in olist2:
				prio[moveno]-=900
			# if rook move is under threat ends

			# if current position of rook is under threat
			if move[1] in olist2:
				if move[0] not in olist2:
					prio[moveno]+=350
			# if current position of rook is under threat ends

		elif board[move[1][0]][move[1][1]]==2: # mover is a bishop
			prio[moveno]+=10
			if board[move[0][0]][move[0][1]]==12: # enemy bishop dies
				prio[moveno]+=999
			elif board[move[0][0]][move[0][1]]==14: # enemy rook dies
					prio[moveno]+=99999
			elif board[move[0][0]][move[0][1]]==15: # enemy pawn dies
					prio[moveno]+=150
			#if bisohp threats in his next move
			next_movelist = possible_moves(move[0][0],move[0][1],board[move[1][0]][move[1][1]])
			for nextmove in next_movelist:
				if board[nextmove[0][0]][nextmove[0][1]]==2: # bishop will threat enemy bishop
					prio[moveno]-=100
				elif board[nextmove[0][0]][nextmove[0][1]]==4: # our bishop will threat enemy rook ( do not move this)
					prio[moveno]+=200 
				elif board[nextmove[0][0]][nextmove[0][1]]==5: # bishop will threat enemy pawn
					prio[moveno]+=50
			# if bhisop threats in his next move ends
			# if bisho move is under threat
			if move[0] in olist2:
				prio[moveno]-=900
			# if bishop move is under threat ends

			# if current position of bishop is under threat
			if move[1] in olist2:
				if move[0] not in olist2:
					prio[moveno]+=150
			# if current position of bishiop is under threat ends
		moveno+=1
	moveno = 0
	maxmoveno = 0
	maxprio = -99999
	for x in prio:
		if x>maxprio:
			maxprio=x
			maxmoveno=moveno
		moveno+=1
	move = mlist[maxmoveno]
	curi=move[1][0]
	curj=move[1][1]
	fini=move[0][0]
	finj=move[0][1]
	ans=chr(curj + 97)+chr(8 - curi + 48)
	ans+=chr(finj+97)+chr(8-fini+48)
	print(ans)

def make_white_move():
	olist = black_movelist() # returns opponent move, fromTowhere
	mlist = white_movelist()
	olist2 = [] # opponents attacking movelist
	for move in olist:
		if board[move[1][0]][move[1][1]]==5:
			curi=move[1][0]
			curj=move[1][1]
			fini=move[0][0]
			finj=move[0][1]
			if curj!=finj:
				olist2.append(move[0])
		else:
			olist2.append(move[0])
	for i in range(0,8):
		for j in range(0,8):
			if board[i][j]==5:
				if j<1:
					olist2.append((i+1,j+1))
				elif j>6:
					olist2.append((i+1,j-1))
				else:
					olist2.append((i+1,j+1))
					olist2.append((i+1,j-1))
	#print("whites olist2",olist2)
	#print("whites mlist",mlist)
	# basic move prio , ( when a piece simply moves )
	prio = []
	for i in range(0,len(mlist)):
		prio.append(0)
	moveno=0
	for move in mlist: #( add priority to basic moves )
		if board[move[1][0]][move[1][1]]==15:  					# mover is a pawn
			prio[moveno]+=20+(10*(8-move[0][0]))
			if move[1][1]==6:
				prio[moveno]+=20
			curi=move[1][0]
			curj=move[1][1]
			fini=move[0][0]
			finj=move[0][1]
			if fini==0: # if pawn is promoted
				prio[moveno]+=9999
			if curj!=finj: # its diagonal move
				if board[move[0][0]][move[0][1]]==2: # enemey bishop dies
					prio[moveno]+=200
				elif board[move[0][0]][move[0][1]]==4: # enemy rook dies
					prio[moveno]+=999
				elif board[move[0][0]][move[0][1]]==5: # enemy pawn dies
					prio[moveno]+=150
			# if pawn threats
			if move[0][0]>0:
				next_movelist = possible_moves(move[0][0],move[0][1],board[move[1][0]][move[1][1]])
				for nextmove in next_movelist:
					curi=nextmove[1][0]
					curj=nextmove[1][1]
					fini=nextmove[0][0]
					finj=nextmove[0][1]
					if curj!=finj:
						if board[nextmove[0][0]][nextmove[0][1]]==4: # enemy rook dies
							prio[moveno]+=100  # pawn threats rook
			# if pawn threats end
			# if pawns move is under threat
			if move[0] in olist2:
				prio[moveno]-=150
			# if pawns move is under threat ends
			# if current position of pawn is under threat
			if move[1] in olist2:
				if move[0] not in olist2:
					prio[moveno]+=140
			# if current position of pawn is under threat ends

		elif board[move[1][0]][move[1][1]]==14: # mover is a rook
			prio[moveno]+=10
			if board[move[0][0]][move[0][1]]<9: # its enemy piece ,, our rook can kill
				if board[move[0][0]][move[0][1]]==2: # enemey bishop dies
					if is_protected(move):
						prio[moveno]-=550
					else:
						prio[moveno]+=200
				elif board[move[0][0]][move[0][1]]==4: # enemy rook dies
					prio[moveno]+=999
				elif board[move[0][0]][move[0][1]]==5: # enemy pawn dies
					if is_protected(move):
						prio[moveno]-=250
					else:
						prio[moveno]+=350
			# if rook threats in his next move
			next_movelist = possible_moves(move[0][0],move[0][1],board[move[1][0]][move[1][1]])
			for nextmove in next_movelist:
				if board[nextmove[0][0]][nextmove[0][1]]==2: # rook will threat enemy bishop
					prio[moveno]+=100
				elif board[nextmove[0][0]][nextmove[0][1]]==4: # our rook will threat enemy rook ( do not move this)
					prio[moveno]-=9999
				elif board[nextmove[0][0]][nextmove[0][1]]==5: # rook will threat enemy pawn
					prio[moveno]+=150
			# if rook threats end
			# if rook move is under threat
			if move[0] in olist2:
				prio[moveno]-=900
			# if rook move is under threat ends

			# if current position of rook is under threat
			if move[1] in olist2:
				if move[0] not in olist2:
					prio[moveno]+=350
			# if current position of rook is under threat ends

		elif board[move[1][0]][move[1][1]]==12: # mover is a bishop
			prio[moveno]+=10
			if board[move[0][0]][move[0][1]]==2:
				prio[moveno]+=40
			elif board[move[0][0]][move[0][1]]==4: # enemy rook dies
					prio[moveno]+=999
			elif board[move[0][0]][move[0][1]]==5: # enemy pawn dies
					prio[moveno]+=60
			#if bisohp threats in his next move
			next_movelist = possible_moves(move[0][0],move[0][1],board[move[1][0]][move[1][1]])
			for nextmove in next_movelist:
				if board[nextmove[0][0]][nextmove[0][1]]==2: # bishop will threat enemy bishop
					prio[moveno]-=100
				elif board[nextmove[0][0]][nextmove[0][1]]==4: # our bishop will threat enemy rook ( do not move this)
					prio[moveno]+=100 
				elif board[nextmove[0][0]][nextmove[0][1]]==5: # bishop will threat enemy pawn
					prio[moveno]+=50
			# if bhisop threats in his next move ends
			# if bisho move is under threat
			if move[0] in olist2:
				prio[moveno]-=9999
			# if bishop move is under threat ends

			# if current position of bishop is under threat
			if move[1] in olist2:
				if move[0] not in olist2:
					prio[moveno]+=150
			# if current position of bishiop is under threat ends
		moveno+=1
	#print("whites prio",prio)
	moveno = 0
	maxmoveno = 0
	maxprio = -99999
	for x in prio:
		if x>maxprio:
			maxprio=x
			maxmoveno=moveno
		moveno+=1
	move = mlist[maxmoveno]
	curi=move[1][0]
	curj=move[1][1]
	fini=move[0][0]
	finj=move[0][1]
	ans=chr(curj + 97)+chr(8 - curi + 48)
	ans+=chr(finj+97)+chr(8-fini+48)
	print(ans)

if __name__=="__main__":
	init_board()
	read_board()
	if bot_is_white:
		make_white_move()
	else:
		make_black_move()