#Chess Game.
#Author:- Srivats Ramaswamy
#Date:- 13/11/2019

import pygame
import sys
from pygame.locals import *
pygame.init()

def RookMove(piBord,piece,position,Pieces):
    r,c=piece['Coords']
    tr,tc=position
    move=False

    if r==tr and c!=tc:
        move=HorizontalMove(piBord,piece,position,Pieces)
    elif c==tc and r!=tr:
        move=VerticalMove(piBord,piece,position,Pieces)
    elif c!=tc and r!=tr:
        drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
    
    return move

def QueenMove(piBord,piece,position,Pieces):
    r,c=piece['Coords']
    tr,tc=position
    move=False

    if r==tr and c!=tc:
        move=HorizontalMove(piBord,piece,position,Pieces)
    elif c==tc and r!=tr:
        move=VerticalMove(piBord,piece,position,Pieces)
    elif c!=tc and r!=tr:
        move=DiagonalMove(piBord,piece,position,Pieces)
    else:
        drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
        
    return move

def BishopMove(piBord,piece,position,Pieces):
    move=DiagonalMove(piBord,piece,position,Pieces)
    return move

def KingMove(piBord,piece,position,Pieces):
    r,c=piece['Coords']
    tr,tc=position
    row=abs(int(r-tr))
    column=abs(int(c-tc))
    move=False

    if column in (2,3) and piece['Castling']==False:
        move=castling(piBord,piece,position,Pieces)
        if move==True:
            piece['Castling']=True
    if row==1 and column==0:
        move=VerticalMove(piBord,piece,position,Pieces)
        if move==True:
            piece['Castling']=True
    elif row==0 and column==1:
        move=HorizontalMove(piBord,piece,position,Pieces)
        if move==True:
            piece['Castling']=True
    elif row==1 and column==1:
        move=DiagonalMove(piBord,piece,position,Pieces)
        if move==True:
            piece['Castling']=True
    else:
        drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
        move=False
    return move

def castling(piBord,piece,position,Pieces):
    r,c=piece['Coords']
    tr,tc=position
    nr,nc=r,c
    ntr,ntc=tr,tc
    rookPresence=False
    cas=False
    v=''

    while nc!=tc:
        if nc>tc:
            nc-=1
        elif nc<tc:
            nc+=1
        v=piBord[nr][nc]
        if v=='':
            cas=True
        elif v!='':
            cas=False
            drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
            return cas
    
    if c>tc:
        ntc-=1
    elif c<tc:
        ntc+=1
    v=piBord[ntr][ntc]
    if v[1]=='R':
        rookPresence=True
    else:
        rookPresence=False
        drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
        return rookPresence
    
    if rookPresence==True:
        rook=Pieces[v]
        nr,nc=r,c
        piBord[r][c]=''
        piece['Coords']=[tr,tc]
        piBord[tr][tc]=piece['Value']
        piBord[ntr][ntc]=''
        
        if nc<tc:
            ntc=tc-1
        elif nc>tc:
            ntc=tc+1

        rook['Coords']=[ntr,ntc]
        piBord[ntr][ntc]=rook['Value']
        putBoardPieces(piBord,Pieces)
        return rookPresence

def PawnMoveUp(piBord,piece,position,Pieces):
    r,c=piece['Coords']
    tr,tc=position
    p2=piBord[tr][tc]
    piece2=searchPiece(p2,Pieces)
    move=False

    if r<tr:
        drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
    elif r>tr:    
        row=abs(int(r-tr))
        column=abs(int(c-tc))
        if (row==2 and column==0):
            if piece2==None:
                if piece['Dual-Step']==False:
                    move=enpassantPawn(piece,piBord,Pieces,position)
                    if move==True:
                        piece['Dual-Step']=True
                elif piece['Dual-Step']==True:
                    drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                    move=False
            elif piece2!=None:
                drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                move=False
        elif row==1:
            if column==0 and piece2==None:
                move=VerticalMove(piBord,piece,position,Pieces)
                if move==True:
                    piece['Dual-Step']=True
            elif column==0 and piece2!=None:
                drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                move=False
            elif column==1 and piece2!=None:
                move=DiagonalMove(piBord,piece,position,Pieces)
                if move==True:
                    piece['Dual-Step']=True
            elif column==1 and piece2==None:
                drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                move=False
            elif column not in (0,1):
                drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                move=False
        elif (row==2 and column==1) or (row==1 and column==2):
            drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
            move=False
    return move
            
def PawnMoveDown(piBord,piece,position,Pieces):
    r,c=piece['Coords']
    tr,tc=position
    p2=piBord[tr][tc]
    piece2=searchPiece(p2,Pieces)
    move=False
    
    if r>tr:
        drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
        move=False
    elif r<tr:
        row=abs(int(r-tr))
        column=abs(int(c-tc))
        if (row==2 and column==0):
            if piece2==None:
                if piece['Dual-Step']==False:
                    move=enpassantPawn(piece,piBord,Pieces,position)
                    if move==True:
                        piece['Dual-Step']=True
                elif piece['Dual-Step']==True:
                    drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                    move=False
            elif piece2!=None:
                drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                move=False
        elif row==1:
            if column==0 and piece2==None:
                move=VerticalMove(piBord,piece,position,Pieces)
                if move==True:
                    piece['Dual-Step']=True
            elif column==0 and piece2!=None:
                drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                move=False
            elif column==1 and piece2!=None:
                move=DiagonalMove(piBord,piece,position,Pieces)
                if move==True:
                    piece['Dual-Step']=True
            elif column==1 and piece2==None:
                drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                move=False
            elif column not in (0,1):
                drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                move=False
        elif (row==2 and column==1) or (row==1 and column==2):
            drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
            move=False
    return move

def EmPawnCheck(val,r,c,position,piBord,Pieces):
    tr,tc=position
    nr,nc=r,c
    Con=False

    if r==6:
        nr-=1
        nc-=1
        v=piBord[nr][nc]
        if v!='':
            if v[0]==val[0]:
                Con=False
            elif v in ('WK','BK'):
                Con=False
            else:
                Con=True
                return Con,v
        elif v=='':
            Con=False

        nr,nc=r,c
        nr-=1
        nc+=1
        v=piBord[nr][nc]
        if v!='':
            if v[0]==val[0]:
                Con=False
            elif v in ('WK','BK'):
                Con=False
            else:
                Con=True
                return Con,v 
        elif v=='':
            Con=False

    elif r==1:
        nr+=1
        nc-=1
        v=piBord[nr][nc]
        if v!='':
            if v[0]==val[0]:
                Con=False
            elif v in ('WK','BK'):
                Con=False
            else:
                Con=True
                return Con,v
        elif v=='':
	        Con=False

        nr,nc=r,c
        nr+=1
        nc+=1
        v=piBord[nr][nc]
        if v!='':
            if v[0]==val[0]:
                Con=False
            elif v in ('WK','BK'):
                Con=False
            else:
                Con=True
                return Con,v                
        elif v=='':
            Con=False
    return Con,v

def enpassantPawn(piece,piBord,Pieces,position):
    val=piece['Value']
    r,c=piece['Coords']
    tr,tc=position
    Con,v=EmPawnCheck(val,r,c,position,piBord,Pieces)
    
    if Con==True:
        if v!='':
            p=Pieces[v]
            print('p='+str(p))
            p['Elimination']=True
    piBord[r][c]=''
    piece['Coords']=[tr,tc]
    piBord[tr][tc]=val
    putBoardPieces(piBord,Pieces) 
          
    return Con

def KnightMove(piBord,piece,position,Pieces):
    r,c=piece['Coords']
    tr,tc=position
    p2=piBord[tr][tc]
    piece2=searchPiece(p2,Pieces)
    row=abs(int(r-tr))
    column=abs(int(c-tc))
    move=False

    if r==tr or c==tc:
        drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
        move=False
    else:
        if abs(int(row-column))!=1:
            drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
            move=False
        elif abs(int(row-column))==1:
            if piece2!=None:
                pv=piece['Value']
                pv2=piece2['Value']
                if pv[0]==pv2[0]:
                    drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                    move=False
                elif pv2 in ('WK','BK'):
                    drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                    move=False
                elif pv[0]!=pv2[0]:
                    move=True
            elif piece2==None:
                move=True 
    
    if move==True:
        if piece2==None:
            piBord[r][c]=''
            piece['Coords']=[tr,tc]
            piBord[tr][tc]=piece['Value']
            putBoardPieces(piBord,Pieces)
        
        elif piece2!=None:
            piece2['Elimination']=True
            piBord[r][c]=''
            piece['Coords']=[tr,tc]
            piBord[tr][tc]=piece['Value']
            putBoardPieces(piBord,Pieces)

    return move

#The User Interface

def UImain():
    fontObj=pygame.font.Font('Fonts/Gotham Nights.ttf',150)
    textSurfOb=fontObj.render('Chess',True,BLACK)
    fontObj2=pygame.font.Font('Fonts/Gotham Nights.ttf',50)
    textSurf1=fontObj2.render('Play Game',True,BLACK)
    textSurf2=fontObj2.render('Exit',True,BLACK)

    while True:
        UIS.blit(BG,(0,0))
        UIS.blit(textSurfOb,(300,100))

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos
                #print('Mousex:-'+str(mousex)+' Mousey:-'+str(mousey))
                if mousex in range(300,460) and mousey in range(190,290):
                    textSurf1=fontObj2.render('Play Game',True,WHITE)
                elif mousex not in range(300,460) and mousey not in range(190,290):
                    textSurf1=fontObj2.render('Play Game',True,BLACK)

                if mousex in range(300,360) and mousey in range(320,380):
                    textSurf2=fontObj2.render('Exit',True,WHITE)
                elif mousex not in range(300,360) and mousey not in range(320,380): 
                    textSurf2=fontObj2.render('Exit',True,BLACK)

            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                if mousex in range(300,460) and mousey in range(190,290):
                    Choice=ChoiceUI()
                    return Choice
                elif mousex in range (300,360) and mousey in range(320,380):
                    pygame.quit()
                    sys.exit()
                
            UIS.blit(textSurf1,(300,250))
            UIS.blit(textSurf2,(300,310))
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def ChoiceUI():
    fontObj1=pygame.font.Font('Fonts/Gotham Nights.ttf',100)
    text1=fontObj1.render('Choose Your Side',True,BLACK)
    fontObj2=pygame.font.Font('Fonts/Gotham Nights.ttf',50)
    text2=fontObj2.render('Black',True,BLACK)
    text3=fontObj2.render('White',True,BLACK)
    mousex,mousey=0,0
    choice=''

    while True:
        CH.blit(BG,(0,0))
        CH.blit(text1,(100,100))

        for event in pygame.event.get():
            if event.type==QUIT:
                UImain()
            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos
                #print('Mousex='+str(mousex)+' Mousey='+str(mousey))
                if mousex in range(300,360) and mousey in range(250,300):
                    text2=fontObj2.render('Black',True,WHITE)
                elif mousex not in range(300,360) and mousey not in range(250,300):
                    text2=fontObj2.render('Black',True,BLACK)
                elif mousex in range(300,360) and mousey in range(310,350):
                    text3=fontObj2.render('White',True,WHITE)
                elif mousex not in range(300,360) and mousey not in range(310,350):
                    text3=fontObj2.render('White',True,BLACK)

            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                if mousex in range(300,360) and mousey in range(250,300):
                    text2=fontObj2.render('Black',True,WHITE)
                    choice='Black'
                    return choice
                if mousex in range(300,360) and mousey in range(310,350):
                    text3=fontObj2.render('White',True,WHITE)
                    choice='White'
                    return choice

            CH.blit(text2,(300,250))
            CH.blit(text3,(300,310))
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def game(Pieces,Kings,Choice):
    
    mousex=0
    mousey=0
    x=None
    y=None
    clickCount=0
    chance=True
    stalemate=False
    blackStaleCount,whiteStaleCount=0,0
   # blackIMCount,whiteIMCount=0,0
    checkConfirmed=False,#IllegalMove=False
    Piecechk,Piecechker='',''
    CheckMate=False
    whiteCut,blackCut=[],[]
    staleFont=pygame.font.Font('Fonts/BankGothic-Regular.ttf',50)
    board=chessBoard(Choice)

    while True:
        DS.blit(BG,(0,0))
        piBord=piecesBoard(Pieces)
        putTiles(board)    
        putBoardPieces(piBord,Pieces)
        HUD(Choice)

        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYUP and event.key==K_ESCAPE):
                Controller()
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                clickCount+=1

            if (mousex<BOARDSIZE and mousey<BOARDSIZE):
                if (clickCount==1):
                    bory,borx=boardCoordinates(mousex,mousey)
                    tx,ty=tileCoordinates(borx,bory)
                    val=piBord[bory][borx]
                    piece=searchPiece(val,Pieces)
                    if piece==None:
                        drawHighlightBox(tx,ty,RED)
                        clickCount=0
                    elif piece!=None:
                        if (chance==True and val[0]=='B') or (chance==False and val[0]=='W'):
                            clickCount=0
                            drawHighlightBox(tx,ty,RED)
                        else:
                            drawHighlightBox(tx,ty,BLUE)
                elif (clickCount==2):
                    bory,borx=boardCoordinates(mousex,mousey)
                    tx,ty=tileCoordinates(borx,bory)
                    drawHighlightBox(tx,ty,GREEN)
                    position=[bory,borx]
                    move=piece['Move'](piBord,piece,position,Pieces)
                    if move==True:
                        chance=not(chance)
                        if stalemate==True:
                            if len(blackCut)==15:
                                blackStaleCount+=1
                            elif len(whiteCut)==15:
                                whiteStaleCount+=1
                    clickCount=0

            if mousex>=BOARDSIZE or mousey>=BOARDSIZE:
                clickCount=0
            
            checkConfirmed,Piecechker,Piecechk=check(piBord,Kings,Pieces)
            if checkConfirmed==True and (Piecechk=='WK' or Piecechk=='BK'):
                king=Kings[Piecechk]
                king['Castling']=True
                kr,kc=king['Coords']
                drawHighlightBox(kc*TILESIZE,kr*TILESIZE,RED)
                CheckMate=checkmate(king,Piecechker,Pieces,piBord)

            whiteCut,blackCut=CutPieces(Pieces,Choice)

            if CheckMate==True:
                clickCount=3
                print('Game Over') 
            
            if 15 in (len(whiteCut),len(blackCut)):
                stalemate=True
            
            if stalemate==True:
                staleText1=staleFont.render(str(blackStaleCount),True,BLACK)
                staleText2=staleFont.render(str(whiteStaleCount),True,WHITE)
                if len(blackCut)==15:
                    if Choice=='Black':
                        DS.blit(staleText1,(650,400))
                    elif Choice=='White':
                        DS.blit(staleText1,(650,250))
                if len(whiteCut)==15:
                    if Choice=='Black':
                        DS.blit(staleText2,(650,400))
                    elif Choice=='White':
                        DS.blit(staleText2,(650,250))

            if 50 in (blackStaleCount,whiteStaleCount):
                clickCount=3
                print('Game Over')
                
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def HUD(Choice):
    FontObj=pygame.font.Font('Fonts/BankGothic-Regular.ttf',50)
    text1=FontObj.render('BLACK',True,BLACK)
    text2=FontObj.render('WHITE',True,WHITE)

    if Choice=='White':
        DS.blit(text1,(595,30))
        DS.blit(text2,(595,500))
    elif Choice=='Black':
        DS.blit(text1,(595,500))
        DS.blit(text2,(595,30))

def Controller():
    Choice=UImain() 
    Pieces,Kings=PieceSelection(Choice,Pieces1,Kings1,Pieces2,Kings2)
    game(Pieces,Kings,Choice)

#Define all the pieces as seperate dictionaries.

WhiteRookQS1={'Value':'WRQ','Coords':[7,0],'Image':pygame.image.load('GameImages/Pieces/WhiteRook.png'),'Elimination':False,'Move':RookMove}
WhiteKnightQS1={'Value':'WKNQ','Coords':[7,1],'Image':pygame.image.load('GameImages/Pieces/WhiteKnight.png'),'Elimination':False,'Move':KnightMove}
WhiteBishopQS1={'Value':'WBQ','Coords':[7,2],'Image':pygame.image.load('GameImages/Pieces/WhiteBishop.png'),'Elimination':False,'Move':BishopMove}
WhiteQueen1={'Value':'WQ','Coords':[7,3],'Image':pygame.image.load('GameImages/Pieces/WhiteQueen.png'),'Elimination':False,'Move':QueenMove}
WhiteKing1={'Value':'WK','Coords':[7,4],'Image':pygame.image.load('GameImages/Pieces/WhiteKing.png'),'Elimination':False,'Move':KingMove,'Castling':False,'Check-Mate':False}
WhiteBishopKS1={'Value':'WBK','Coords':[7,5],'Image':pygame.image.load('GameImages/Pieces/WhiteBishop.png'),'Elimination':False,'Move':BishopMove}
WhiteKnightKS1={'Value':'WKNK','Coords':[7,6],'Image':pygame.image.load('GameImages/Pieces/WhiteKnight.png'),'Elimination':False,'Move':KnightMove}
WhiteRookKS1={'Value':'WRK','Coords':[7,7],'Image':pygame.image.load('GameImages/Pieces/WhiteRook.png'),'Elimination':False,'Move':RookMove}
WhitePawn11={'Value':'WP1','Coords':[6,0],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False,'Resurection':False}
WhitePawn21={'Value':'WP2','Coords':[6,1],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False,'Resurection':False}
WhitePawn31={'Value':'WP3','Coords':[6,2],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False,'Resurection':False}
WhitePawn41={'Value':'WP4','Coords':[6,3],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False,'Resurection':False}
WhitePawn51={'Value':'WP5','Coords':[6,4],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False,'Resurection':False}
WhitePawn61={'Value':'WP6','Coords':[6,5],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False,'Resurection':False}
WhitePawn71={'Value':'WP7','Coords':[6,6],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False,'Resurection':False}
WhitePawn81={'Value':'WP8','Coords':[6,7],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False,'Resurection':False}

BlackRookQS1={'Value':'BRQ','Coords':[0,0],'Image':pygame.image.load('GameImages/Pieces/BlackRook.png'),'Elimination':False,'Move':RookMove}
BlackKnightQS1={'Value':'BKNQ','Coords':[0,1],'Image':pygame.image.load('GameImages/Pieces/BlackKnight.png'),'Elimination':False,'Move':KnightMove}
BlackBishopQS1={'Value':'BBQ','Coords':[0,2],'Image':pygame.image.load('GameImages/Pieces/BlackBishop.png'),'Elimination':False,'Move':BishopMove}
BlackQueen1={'Value':'BQ','Coords':[0,3],'Image':pygame.image.load('GameImages/Pieces/BlackQueen.png'),'Elimination':False,'Move':QueenMove}
BlackKing1={'Value':'BK','Coords':[0,4],'Image':pygame.image.load('GameImages/Pieces/BlackKing.png'),'Elimination':False,'Move':KingMove,'Castling':False,'Check-Mate':False}
BlackBishopKS1={'Value':'BBK','Coords':[0,5],'Image':pygame.image.load('GameImages/Pieces/BlackBishop.png'),'Elimination':False,'Move':BishopMove}
BlackKnightKS1={'Value':'BKNK','Coords':[0,6],'Image':pygame.image.load('GameImages/Pieces/BlackKnight.png'),'Elimination':False,'Move':KnightMove}
BlackRookKS1={'Value':'BRK','Coords':[0,7],'Image':pygame.image.load('GameImages/Pieces/BlackRook.png'),'Elimination':False,'Move':RookMove}
BlackPawn11={'Value':'BP1','Coords':[1,0],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
BlackPawn21={'Value':'BP2','Coords':[1,1],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
BlackPawn31={'Value':'BP3','Coords':[1,2],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
BlackPawn41={'Value':'BP4','Coords':[1,3],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
BlackPawn51={'Value':'BP5','Coords':[1,4],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
BlackPawn61={'Value':'BP6','Coords':[1,5],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
BlackPawn71={'Value':'BP7','Coords':[1,6],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
BlackPawn81={'Value':'BP8','Coords':[1,7],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}

Pieces1={'BRQ':BlackRookQS1,'BKNQ':BlackKnightQS1,'BBQ':BlackBishopQS1,'BQ':BlackQueen1,'BK':BlackKing1,'BBK':BlackBishopKS1,'BKNK':BlackKnightKS1,
'BRK':BlackRookKS1,'BP1':BlackPawn11,'BP2':BlackPawn21,'BP3':BlackPawn31,'BP4':BlackPawn41,'BP5':BlackPawn51,'BP6':BlackPawn61,'BP7':BlackPawn71,'BP8':BlackPawn81,
'WRQ':WhiteRookQS1,'WKNQ':WhiteKnightQS1,'WBQ':WhiteBishopQS1,'WQ':WhiteQueen1,'WK':WhiteKing1,'WBK':WhiteBishopKS1,'WKNK':WhiteKnightKS1,'WRK':WhiteRookKS1,
'WP1':WhitePawn11,'WP2':WhitePawn21,'WP3':WhitePawn31,'WP4':WhitePawn41,'WP5':WhitePawn51,'WP6':WhitePawn61,'WP7':WhitePawn71,'WP8':WhitePawn81}

Kings1={'BK':BlackKing1,'WK':WhiteKing1}

WhiteRookQS2={'Value':'WRQ','Coords':[0,0],'Image':pygame.image.load('GameImages/Pieces/WhiteRook.png'),'Elimination':False,'Move':RookMove}
WhiteKnightQS2={'Value':'WKNQ','Coords':[0,1],'Image':pygame.image.load('GameImages/Pieces/WhiteKnight.png'),'Elimination':False,'Move':KnightMove}
WhiteBishopQS2={'Value':'WBQ','Coords':[0,2],'Image':pygame.image.load('GameImages/Pieces/WhiteBishop.png'),'Elimination':False,'Move':BishopMove}
WhiteQueen2={'Value':'WQ','Coords':[0,3],'Image':pygame.image.load('GameImages/Pieces/WhiteQueen.png'),'Elimination':False,'Move':QueenMove}
WhiteKing2={'Value':'WK','Coords':[0,4],'Image':pygame.image.load('GameImages/Pieces/WhiteKing.png'),'Elimination':False,'Move':KingMove,'Castling':False,'Check-Mate':False}
WhiteBishopKS2={'Value':'WBK','Coords':[0,5],'Image':pygame.image.load('GameImages/Pieces/WhiteBishop.png'),'Elimination':False,'Move':BishopMove}
WhiteKnightKS2={'Value':'WKNK','Coords':[0,6],'Image':pygame.image.load('GameImages/Pieces/WhiteKnight.png'),'Elimination':False,'Move':KnightMove}
WhiteRookKS2={'Value':'WRK','Coords':[0,7],'Image':pygame.image.load('GameImages/Pieces/WhiteRook.png'),'Elimination':False,'Move':RookMove}
WhitePawn12={'Value':'WP1','Coords':[1,0],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
WhitePawn22={'Value':'WP2','Coords':[1,1],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
WhitePawn32={'Value':'WP3','Coords':[1,2],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
WhitePawn42={'Value':'WP4','Coords':[1,3],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
WhitePawn52={'Value':'WP5','Coords':[1,4],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
WhitePawn62={'Value':'WP6','Coords':[1,5],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
WhitePawn72={'Value':'WP7','Coords':[1,6],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}
WhitePawn82={'Value':'WP8','Coords':[1,7],'Image':pygame.image.load('GameImages/Pieces/WhitePawn.png'),'Elimination':False,'Move':PawnMoveDown,'Dual-Step':False}

BlackRookQS2={'Value':'BRQ','Coords':[7,0],'Image':pygame.image.load('GameImages/Pieces/BlackRook.png'),'Elimination':False,'Move':RookMove}
BlackKnightQS2={'Value':'BKNQ','Coords':[7,1],'Image':pygame.image.load('GameImages/Pieces/BlackKnight.png'),'Elimination':False,'Move':KnightMove}
BlackBishopQS2={'Value':'BBQ','Coords':[7,2],'Image':pygame.image.load('GameImages/Pieces/BlackBishop.png'),'Elimination':False,'Move':BishopMove}
BlackQueen2={'Value':'BQ','Coords':[7,3],'Image':pygame.image.load('GameImages/Pieces/BlackQueen.png'),'Elimination':False,'Move':QueenMove}
BlackKing2={'Value':'BK','Coords':[7,4],'Image':pygame.image.load('GameImages/Pieces/BlackKing.png'),'Elimination':False,'Move':KingMove,'Castling':False,'Check-Mate':False}
BlackBishopKS2={'Value':'BBK','Coords':[7,5],'Image':pygame.image.load('GameImages/Pieces/BlackBishop.png'),'Elimination':False,'Move':BishopMove}
BlackKnightKS2={'Value':'BKNK','Coords':[7,6],'Image':pygame.image.load('GameImages/Pieces/BlackKnight.png'),'Elimination':False,'Move':KnightMove}
BlackRookKS2={'Value':'BRK','Coords':[7,7],'Image':pygame.image.load('GameImages/Pieces/BlackRook.png'),'Elimination':False,'Move':RookMove}
BlackPawn12={'Value':'BP1','Coords':[6,0],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False}
BlackPawn22={'Value':'BP2','Coords':[6,1],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False}
BlackPawn32={'Value':'BP3','Coords':[6,2],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False}
BlackPawn42={'Value':'BP4','Coords':[6,3],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False}
BlackPawn52={'Value':'BP5','Coords':[6,4],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False}
BlackPawn62={'Value':'BP6','Coords':[6,5],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False}
BlackPawn72={'Value':'BP7','Coords':[6,6],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False}
BlackPawn82={'Value':'BP8','Coords':[6,7],'Image':pygame.image.load('GameImages/Pieces/BlackPawn.png'),'Elimination':False,'Move':PawnMoveUp,'Dual-Step':False}

Pieces2={'BRQ':BlackRookQS2,'BKNQ':BlackKnightQS2,'BBQ':BlackBishopQS2,'BQ':BlackQueen2,'BK':BlackKing2,'BBK':BlackBishopKS2,'BKNK':BlackKnightKS2,
'BRK':BlackRookKS2,'BP1':BlackPawn12,'BP2':BlackPawn22,'BP3':BlackPawn32,'BP4':BlackPawn42,'BP5':BlackPawn52,'BP6':BlackPawn62,'BP7':BlackPawn72,'BP8':BlackPawn82,
'WRQ':WhiteRookQS2,'WKNQ':WhiteKnightQS2,'WBQ':WhiteBishopQS2,'WQ':WhiteQueen2,'WK':WhiteKing2,'WBK':WhiteBishopKS2,'WKNK':WhiteKnightKS2,'WRK':WhiteRookKS2,
'WP1':WhitePawn12,'WP2':WhitePawn22,'WP3':WhitePawn32,'WP4':WhitePawn42,'WP5':WhitePawn52,'WP6':WhitePawn62,'WP7':WhitePawn72,'WP8':WhitePawn82}

Kings2={'BK':BlackKing2,'WK':WhiteKing2}

def PieceSelection(Choice,Pieces1,Kings1,Pieces2,Kings2):
    if Choice=='Black':
        Pieces=Pieces2
        Kings=Kings2
    elif Choice=='White':
        Pieces=Pieces1
        Kings=Kings1

    return Pieces,Kings

def PrintPieces(Pieces):
    for keys in Pieces:
        p=Pieces[keys]
        print(p)
    print('---------------------------------------------------------')
    print('\n')


def chessBoard(Choice):
    board=[]
    i=0
    k=0

    for x in range(8):
        board.append([0]*8)
    
    for row in range(8):
        i=k
        for column in range(8):
            if Choice=='White':
                if i%2==0:
                    board[row][column]='00'
                    k=i
                    i=i+1
                else:
                    board[row][column]='11'
                    k=i
                    i=i+1
            elif Choice=='Black':
                if i%2==0:
                    board[row][column]='11'
                    k=i
                    i=i+1
                else:
                    board[row][column]='00'
                    k=i
                    i=i+1
    return(board)

def displayBoard(board):
    for x in range(8):
        print(board[x])
        print('\n')
    print('\n')

def piecesBoard(Pieces):
    piBord=[]

    for i in range(8):
        piBord.append(['']*8)
    
    for key in Pieces:
        p=Pieces[key]
        r,c=p['Coords']
        if p['Elimination']!=True:
            piBord[r][c]=p['Value']

    return(piBord)

def searchPiece(s,Pieces):
    if s!='':
        return(Pieces[s])
    elif s=='':
        return None
    
DS=pygame.display.set_mode((850,592))
UIS=pygame.display.set_mode((850,592)) 
CH=pygame.display.set_mode((850,592))
PG=pygame.display.set_mode((850,592))
pygame.display.set_caption('Chess')
FPSCLOCK=pygame.time.Clock()
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0,0,255)
GREEN=(0,255,0)
RED=(255,0,0)
TILESIZE=74
BOARDSIZE=592
LB=pygame.image.load('GameImages/Tiles/LightBrown.png').convert()
DB=pygame.image.load('GameImages/Tiles/DarkBrown.png').convert()
BG=pygame.image.load('GameImages/Backgrounds/Dark-Wood-Background.jpg').convert()
FPS=100
MAX_BYTES=65535

#Note:- y-axis=row and x-axis=column

def putTiles(board):
    bx=0
    by=0
    for y in range(8):
        if y>0:
            by+=TILESIZE
        bx=0
        for x in range(8):
            if board[y][x]=='00':
                DS.blit(LB,(bx,by))
            elif board[y][x]=='11':
                DS.blit(DB,(bx,by))
            bx+=TILESIZE

def putBoardPieces(piBord,Pieces):
    bx=0
    by=0

    for key in Pieces:
        p=Pieces[key]
        r,c=p['Coords']
        
        bx=c*TILESIZE
        by=r*TILESIZE

        if p['Elimination']!=True:
            DS.blit(p['Image'],(bx,by))
        
def CutPieces(Pieces,Choice):
    NS=int(TILESIZE/2)
    bElCount,wElCount=0,0
    tx=600
    wc,bc=[],[]
    bty,wty=0,0
    bposx,wposx=0,0
    
    if Choice=='White':
            bty,wty=150,450
    elif Choice=='Black':
        bty,wty=450,150

    for keys in Pieces:
        p=Pieces[keys]
        if p['Elimination']==True:
            img=pygame.transform.scale(p['Image'],(NS,NS))
            val=p['Value']
            if val[0]=='B':
                bElCount+=1
                bposx=NS*bElCount
                if int(tx+bposx)>850:
                    bty=bty+NS
                    bElCount=1
                    bposx=NS*bElCount
                DS.blit(img,(tx+bposx,bty))
                bc.append(val)

            elif val[0]=='W':
                wElCount+=1
                wposx=NS*wElCount
                if int(tx+wposx)>850:
                    wty=wty+NS
                    wElCount=1
                    wposx=NS*wElCount
                DS.blit(img,(tx+wposx,wty))
                wc.append(val)
    return wc,bc

def tileCoordinates(borx,bory):
    return(borx*TILESIZE,bory*TILESIZE)
    
def boardCoordinates(mousex,mousey):
    col=int(mousex/TILESIZE)
    row=int(mousey/TILESIZE)
    return[row,col]

def drawHighlightBox(tilex,tiley,color):
    pygame.draw.rect(DS,color,(tilex,tiley,TILESIZE,TILESIZE),4)

def VerticalMove(piBord,piece,position,Pieces):
    tr,tc=position
    r,c=piece['Coords']
    nr=0
    val=piece['Value']
    bx=tc*TILESIZE
    by=tr*TILESIZE
    v=0
    valid=False
    
    if c!=tc:
        drawHighlightBox(bx,by,RED)
        return valid
    elif c==tc:
        valid=True
        nr=r
        while nr!=tr:
            if nr<tr:
                nr+=1
            elif nr>tr:
                nr-=1
            if nr==tr:
                break
            v=piBord[nr][c]
            if v!='':
                drawHighlightBox(tc*TILESIZE,tr*TILESIZE,RED)
                valid=False
                break
            elif v=='':
                continue
        
        v=piBord[tr][tc]
        if v!='' and valid==True:
            if v[0]==val[0]:
                drawHighlightBox(bx,by,RED)
                valid=False
            elif v in ('WK','BK'):
                drawHighlightBox(bx,by,RED)
                valid=False
            elif v[0]!=val[0]:
                piece2=searchPiece(v,Pieces)
                piece2['Elimination']=True
                valid=True
               
        if valid==True:
            while r!=tr:
                piBord[r][c]=''
                if r<tr:
                    r+=1
                elif r>tr:
                    r-=1
                piBord[r][c]=piece['Value']
                piece['Coords']=[r,c]
                pygame.time.wait(120)
                putBoardPieces(piBord,Pieces)
    return valid

def HorizontalMove(piBord,piece,position,Pieces):
    tr,tc=position
    r,c=piece['Coords']
    nc=0
    val=piece['Value']
    bx=tc*TILESIZE
    by=tr*TILESIZE
    valid=False
    v=0

    if r!=tr:
        drawHighlightBox(bx,by,RED)
        return valid
    elif r==tr:
        valid=True
        nc=c
        while nc!=tc:
            if nc<tc:
                nc+=1
            elif nc>tc:
                nc-=1
            if nc==tc:
                break
            v=piBord[r][nc]
            if v!='':
                drawHighlightBox(bx,by,RED)
                valid=False
                break

        v=piBord[tr][tc]
        if v!='' and valid==True:
            if v[0]==val[0]:
                drawHighlightBox(bx,by,RED)
                valid=False
            elif v in ('WK','BK'):
                drawHighlightBox(bx,by,RED)
                valid=False
            elif v[0]!=val[0]:
                piece2=searchPiece(v,Pieces)
                piece2['Elimination']=True
                valid=True
                
        if valid==True:
            while c!=tc:
                piBord[r][c]=''
                if c<tc:
                    c+=1
                elif c>tc:
                    c-=1
                piBord[r][c]=piece['Value']
                piece['Coords']=[r,c]
                pygame.time.wait(120)
                putBoardPieces(piBord,Pieces)
    return valid

def DiagonalMove(piBord,piece,position,Pieces):
    tr,tc=position
    r,c=piece['Coords']
    nr,nc=0,0
    v=0
    val=piece['Value']
    by=tr*TILESIZE
    bx=tc*TILESIZE
    valid=False

    if abs(int(r-tr))!=abs(int(c-tc)):
        drawHighlightBox(bx,by,RED)
        return valid
    elif abs(int(r-tr))==abs(int(c-tc)):
        valid=True
        nr,nc=r,c
        while nr!=tr and nc!=tc:
            if nr<tr:
                nr+=1
            elif nr>tr:
                nr-=1
            if nc<tc:
                nc+=1
            elif nc>tc:
                nc-=1
            if nr==tr and nc==tc:
                break
            v=piBord[nr][nc]
            if v!='':
                drawHighlightBox(bx,by,RED)
                valid=False
                break
            
        v=piBord[tr][tc]
        if v!='' and valid==True:
            if v[0]==val[0]:
                drawHighlightBox(bx,by,RED)
                valid=False
            elif v in ('WK','BK'):
                drawHighlightBox(bx,by,RED)
                valid=False
            elif v[0]!=val[0]:
                piece2=searchPiece(v,Pieces)
                piece2['Elimination']=True
                
        if valid==True:
            while r!=tr or c!=tc:
                piBord[r][c]=''
                if r<tr:
                    r+=1
                elif r>tr:
                    r-=1
                if c>tc:
                    c-=1
                elif c<tc:
                    c+=1
                piBord[r][c]=piece['Value']
                piece['Coords']=[r,c]
                putBoardPieces(piBord,Pieces)
    return valid

def HorPieceCheck(k,kr,kc,piBord):
    val=k['Value']
    nr,nc=kr,kc
    con=False
    v=''

    while con==False and nc<7:
        nc+=1
        v=piBord[nr][nc]
        if v!='':
            if val[0]!=v[0]:
                if val[0]=='B':
                    if v in ('WQ','WRK','WRQ'):
                        con=True
                        break
                    elif v=='WK' and abs(int(nc-kc))==1:
                        con=True
                        break
                    else:
                        con=False
                        break
                elif val[0]=='W':
                    if v in ('BQ','BRK','BRQ'):
                        con=True
                        break
                    elif v=='BK' and abs(int(nc-kc))==1:
                        con=True
                        break
                    else:
                        con=False
                        break
            elif val[0]==v[0]:
                con=False
                break
    nr,nc=kr,kc
    while con==False and nc>0:
        nc-=1
        v=piBord[nr][nc]
        if v!='':
            if val[0]!=v[0]:
                if val[0]=='B':
                    if v in ('WQ','WRK','WRQ'):
                        con=True
                        break
                    elif v=='WK' and abs(int(nc-kc))==1:
                        con=True
                        break
                    else:
                        con=False
                        break
                elif val[0]=='W':
                    if v in ('BQ','BRK','BRQ'):
                        con=True
                        break
                    elif v=='BK' and abs(int(nc-kc))==1:
                        con=True
                        break
                    else:
                        con=False
                        break
            elif val[0]==v[0]:
                con=False 
                break
    return con,v

def VerPieceCheck(k,kr,kc,piBord):
    val=k['Value']
    con=False
    nr,nc=kr,kc

    while con==False and nr<7:
        nr+=1
        v=piBord[nr][nc]
        if v!='':
            if val[0]!=v[0]:
                if val[0]=='B':
                    if v in ('WQ','WRK','WRQ'):
                        con=True
                        break
                    elif v=='WK' and abs(int(nr-kr))==1:
                        con=True
                        break
                    else:
                        con=False
                        break
                elif val[0]=='W':
                    if v in ('BQ','BRK','BRQ'):
                        con=True
                        break
                    elif v=='BK' and abs(int(nr-kr))==1:
                        con=True
                        break
                    else:
                        con=False
                        break
            elif val[0]==v[0]:
                con=False
                break
    nr,nc=kr,kc
    while con==False and nr>0:
        nr-=1
        v=piBord[nr][nc]
        if v!='':
            if val[0]!=v[0]:
                if val[0]=='B':
                    if v in ('WQ','WRK','WRQ'):
                        con=True
                        break
                    elif v=='WK' and abs(int(nr-kr))==1:
                        con=True
                        break
                    else:
                        con=False
                        break
                elif val[0]=='W':
                    if v in ('BQ','BRK','BRQ'):
                        con=True
                        break
                    elif v=='BK' and abs(int(nr-kr))==1:
                        con=True
                        break
                    else:
                        con=False
                        break
            elif val[0]==v[0]:
                con=False
                break
    return con,v

def DiagPieceCheck(k,kr,kc,piBord,Pieces):
    val=k['Value']
    nr,nc=kr,kc
    count=0
    con=False
    v=''

    while con==False and (nc<7 and nr<7): #Condition 1
        nc+=1
        nr+=1
        v=piBord[nr][nc]
        if v!='':
            if val[0]!=v[0]:
                if val[0]=='B':
                    if v in ('WQ','WBK','WBQ'):
                        con=True
                        break
                    elif v[1]=='P':
                        p=Pieces[v]
                        if p['Move']==PawnMoveUp:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr>kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                        elif p['Move']==PawnMoveDown:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr<kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                    elif v=='WK' and (abs(int(nr-kr))==1 and abs(int(nc-kc))==1):
                        con=True
                        break
                    else:
                        con=False
                        break
                elif val[0]=='W':
                    if v in ('BQ','BBK','BBQ'):
                        con=True
                        break
                    elif v[1]=='P':
                        p=Pieces[v]
                        if p['Move']==PawnMoveUp:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr>kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                        elif p['Move']==PawnMoveDown:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr<kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                    elif v=='BK' and (abs(int(nr-kr))==1 and abs(int(nc-kc))==1):
                        con=True
                        break
                    else:
                        con=False
                        break
            elif val[0]==v[0]:
                con=False
                break
    nr,nc=kr,kc
    while con==False and (nr>0 and nc>0): #Condition 2
        nr-=1
        nc-=1
        v=piBord[nr][nc]
        if v!='':
            if val[0]!=v[0]:
                if val[0]=='B':
                    if v in ('WQ','WBK','WBQ'):
                        con=True
                        break
                    elif v[1]=='P':
                        p=Pieces[v]
                        if p['Move']==PawnMoveUp:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr>kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                        elif p['Move']==PawnMoveDown:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr<kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                    elif v=='WK' and (abs(int(nr-kr))==1 and abs(int(nc-kc))==1):
                        con=True
                        break
                    else:
                        con=False
                        break
                elif val[0]=='W':
                    if v in ('BQ','BBK','BBQ'):
                        con=True
                        break
                    elif v[1]=='P':
                        p=Pieces[v]
                        if p['Move']==PawnMoveUp:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr>kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                        elif p['Move']==PawnMoveDown:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr<kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                    elif v=='BK' and (abs(int(nr-kr))==1 and abs(int(nc-kc))==1):
                        con=True
                        break
                    else:
                        con=False
                        break
            elif val[0]==v[0]:
                con=False
                break
    nr,nc=kr,kc
    while con==False and (nr<7 and nc>0): #Condition 3
        nr+=1
        nc-=1
        v=piBord[nr][nc]
        if v!='':
            if val[0]!=v[0]:
                if val[0]=='B':
                    if v in ('WQ','WBK','WBQ'):
                        con=True
                        break
                    elif v[1]=='P':
                        p=Pieces[v]
                        if p['Move']==PawnMoveUp:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr>kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                        elif p['Move']==PawnMoveDown:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr<kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                    elif v=='WK' and (abs(int(nr-kr))==1 and abs(int(nc-kc))==1):
                        con=True
                        break
                    else:
                        con=False
                        break
                elif val[0]=='W':
                    if v in ('BQ','BBK','BBQ'):
                        con=True
                        break
                    elif v[1]=='P':
                        p=Pieces[v]
                        if p['Move']==PawnMoveUp:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr>kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                        elif p['Move']==PawnMoveDown:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr<kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                    elif v=='BK' and (abs(int(nr-kr))==1 and abs(int(nc-kc))==1):
                        con=True
                        break
                    else:
                        con=False
                        break
            elif val[0]==v[0]:
                con=False
                break
    nr,nc=kr,kc
    while con==False and (nr>0 and nc<7): #Condition 4
        nr-=1
        nc+=1
        v=piBord[nr][nc]
        if v!='':
            if val[0]!=v[0]:
                if val[0]=='B':
                    if v in ('WQ','WBK','WBQ'):
                        con=True
                        break
                    elif v[1]=='P':
                        p=Pieces[v]
                        if p['Move']==PawnMoveUp:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr>kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                        elif p['Move']==PawnMoveDown:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr<kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                    elif v=='WK' and (abs(int(nr-kr))==1 and abs(int(nc-kc))==1):
                        con=True
                        break
                    else:
                        con=False
                        break
                elif val[0]=='W':
                    if v in ('BQ','BBK','BBQ'):
                        con=True
                        break
                    elif v[1]=='P':
                        p=Pieces[v]
                        if p['Move']==PawnMoveUp:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr>kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                        elif p['Move']==PawnMoveDown:
                            if (abs(int(kr-nr))==1 and abs(int(kc-nc))==1) and nr<kr:
                                con=True
                                break
                            else:
                                con=False
                                break
                    elif v=='BK' and (abs(int(nr-kr))==1 and abs(int(nc-kc))==1):
                        con=True
                        break
                    else:
                        con=False
                        break
            elif val[0]==v[0]:
                con=False
                break
    return con,v

def KnConf(nr,nc,piBord,val):
    v=0
    conf=False
    v=piBord[nr][nc]

    if v!='':
        if val[0]!=v[0]:
            if val[0]=='B':
                if v in ('WKNK','WKNQ'):
                    conf=True
                else:
                    conf=False
            elif val[0]=='W':
                if v in ('BKNK','BKNQ'):
                    conf=True
                else:
                    conf=False
            else:
                conf=False
        elif val[0]==v[0]:
            conf=False
    return conf,v

def KnightPieceCheck(k,kr,kc,piBord):
    val=k['Value']
    con=False
    count=0
    chpiece=''

    while con==False and count<7:
        #Condition 1
        nr,nc=kr,kc
        nr+=2
        nc+=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            con,chpiece=KnConf(nr,nc,piBord,val)
            if con==True:
                break
        count+=1
        #Condition 2
        nr,nc=kr,kc
        nr-=2
        nc-=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            con,chpiece=KnConf(nr,nc,piBord,val)
            if con==True:
                break
        count+=1
        #Condition 3
        nr,nc=kr,kc
        nr-=2
        nc+=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            con,chpiece=KnConf(nr,nc,piBord,val)
            if con==True:
                break
        count+=1
        #Condition 4
        nr,nc=kr,kc
        nr+=2
        nc-=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            con,chpiece=KnConf(nr,nc,piBord,val)
            if con==True:
                break
        count+=1
        #Condition 5
        nr,nc=kr,kc
        nr+=1
        nc+=2
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            con,chpiece=KnConf(nr,nc,piBord,val)
            if con==True:
                break
        count+=1
        #Condition 6
        nr,nc=kr,kc
        nr-=1
        nc-=2
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            con,chpiece=KnConf(nr,nc,piBord,val)
            if con==True:
                break
        count+=1
        #Condition 7
        nr,nc=kr,kc
        nr+=1
        nc-=2
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            con,chpiece=KnConf(nr,nc,piBord,val)
            if con==True:
                break
        count+=1
        #Condtion 8
        nr,nc=kr,kc
        nr-=1
        nc+=2
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            con,chpiece=KnConf(nr,nc,piBord,val)
            if con==True:
                break
        count+=1
        if count>7:
            break
    return con,chpiece

def check(piBord,Kings,Pieces):
    for key in Kings:
        k=Kings[key]
        kr,kc=k['Coords']
        val=k['Value']
        checkPiece=''
        Confirm=False

        horCon,horP=HorPieceCheck(k,kr,kc,piBord)
        verCon,verP=VerPieceCheck(k,kr,kc,piBord)
        diagCon,diagP=DiagPieceCheck(k,kr,kc,piBord,Pieces)
        knCon,knP=KnightPieceCheck(k,kr,kc,piBord)

        if True in (horCon,verCon,diagCon,knCon):
            Confirm=True
            if horCon==True:
                checkPiece=horP
                break
            elif verCon==True:
                checkPiece=verP
                break
            elif diagCon==True:
                checkPiece=diagP
                break
            elif knCon==True:
                checkPiece=knP
                break
    return Confirm,checkPiece,val

def checkmate(king,Piecechker,Pieces,piBord):
    piece=Pieces[Piecechker]
    pVal=piece['Value']
    pr,pc=piece['Coords']
    pieceAttack,kingMove,pathBlock=False,False,False
    textObj=pygame.font.Font('Fonts/Gotham Nights.ttf',50)
    text1=textObj.render('CHECK MATE',True,RED)
    text2=textObj.render('CHECK',True,RED)
    con=False

    #Condition 1: Check whether the checking piece can be killed.
    pieceAttack,atckp=PieceAttacker(piece,pr,pc,piBord,Pieces)

    #Condtion 2: Check whether the king can move to an empty space.
    pa,kingMove=KingMovement(piBord,king,Pieces,atckp)
    if pa==False:
        if atckp!='':
            if atckp[0]!=pVal[0]:
                if atckp in ('BK','WK'):
                    pieceAttack=True
    #Condition 3: Check whether the path between the king and the piece can be blocked.
    #pathBlock=PathBlocker(piBord,piece,king)
    
    if pieceAttack==True and kingMove==True: #and pathBlock==True: # : 
        DS.blit(text1,(650,296))
        con=True
    elif False in (pieceAttack,kingMove):#,pathBlock 
        DS.blit(text2,(650,296))
        con=False
    return con

def PieceAttacker(piece,pr,pc,piBord,Pieces):
    horCon,horP=HorPieceCheck(piece,pr,pc,piBord)
    verCon,verP=VerPieceCheck(piece,pr,pc,piBord)
    diagCon,diagP=DiagPieceCheck(piece,pr,pc,piBord,Pieces)
    knCon,knP=KnightPieceCheck(piece,pr,pc,piBord)
    confirm=False
    v=''

    if True in (horCon,verCon,diagCon,knCon):
        confirm=False
        if horCon==True:
           v=horP
        elif verCon==True:
            v=verP
        elif diagCon==True:
            v=diagP
        elif knCon==True:
            v=knP  
    else:
        confirm=True
        
    return confirm,v

def KingMovement(piBord,king,Pieces,atckp):
    kVal=king['Value']
    kr,kc=king['Coords']
    nr,nc=kr,kc
    count=0
    con=False
    pa=False
    v=''
    at=''

    while count<=7:
        #Condition 1
        nc-=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            v=piBord[nr][nc]
            if v!='':
                if v[0]==kVal[0]:
                    con=True
                elif v[0]!=kVal[0]:
                    pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                    if pa==False:
                        con=True
                    elif pa==True:
                        con=False
                        break
            elif v=='':
                pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                if pa==False:
                    con=True
                elif pa==True:
                    con=False
                    break
        count+=1
        nr,nc=kr,kc
        #Condition 2
        nc+=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            v=piBord[nr][nc]
            if v!='':
                if v[0]==kVal[0]:
                    con=True
                elif v[0]!=kVal[0]:
                    pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                    if pa==False:
                        con=True
                    elif pa==True:
                        con=False
                        break
            elif v=='':
                pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                if pa==False:
                    con=True
                elif pa==True:
                    con=False
                    break
        count+=1
        nr,nc=kr,kc
        #Condition 3
        nr-=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            v=piBord[nr][nc]
            if v!='':
                if v[0]==kVal[0]:
                    con=True
                elif v[0]!=kVal[0]:
                    pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                    if pa==False:
                        con=True
                    elif pa==True:
                        con=False
                        break
            elif v=='':
                pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                if pa==False:
                    con=True
                elif pa==True:
                    con=False
                    break    
        count+=1
        nr,nc=kr,kc
        #Condition 4
        nr+=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            v=piBord[nr][nc]
            if v!='':
                if v[0]==kVal[0]:
                    con=True
                elif v[0]!=kVal[0]:
                    pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                    if pa==False:
                        con=True
                    elif pa==True:
                        con=False
                        break
            elif v=='':
                pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                if pa==False:
                    con=True
                elif pa==True:
                    con=False
                    break
        count+=1
        nr,nc=kr,kc
        #Condition 5
        nc-=1
        nr-=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            v=piBord[nr][nc]
            if v!='':
                if v[0]==kVal[0]:
                    con=True
                elif v[0]!=kVal[0]:
                    pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                    if pa==False:
                        con=True
                    elif pa==True:
                        con=False
                        break
            elif v=='':
                pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                if pa==False:
                    con=True
                elif pa==True:
                    con=False
                    break    
        count+=1
        nr,nc=kr,kc
        #Condition 6
        nc+=1
        nr-=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            v=piBord[nr][nc]
            if v!='':
                if v[0]==kVal[0]:
                    con=True
                elif v[0]!=kVal[0]:
                    pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                    if pa==False:
                        con=True
                    elif pa==True:
                        con=False
                        break
            elif v=='':
                pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                if pa==False:
                    con=True
                elif pa==True:
                    con=False
                    break
        count+=1
        nr,nc=kr,kc
        #Condtion 7
        nc+=1
        nr-=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            v=piBord[nr][nc]
            if v!='':
                if v[0]==kVal[0]:
                    con=True
                elif v[0]!=kVal[0]:
                    pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                    if pa==False:
                        con=True
                    elif pa==True:
                        con=False
                        break
            elif v=='':
                pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                if pa==False:
                    con=True
                elif pa==True:
                    con=False
                    break
        count+=1
        nr,nc=kr,kc
        #Condition 8
        nc+=1
        nr+=1
        if (nr<=7 and nc<=7) and (nr>=0 and nc>=0):
            v=piBord[nr][nc]
            if v!='':
                if v[0]==kVal[0]:
                    con=True
                elif v[0]!=kVal[0]:
                    pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                    if pa==False:
                        con=True
                    elif pa==True:
                        con=False
                        break
            elif v=='':
                pa,at=PieceAttacker(king,nr,nc,piBord,Pieces)
                if pa==False:
                    con=True
                elif pa==True:
                    con=False
                    break
        count+=1
        nr,nc=kr,kc
        if count>7:
            break
    return pa,con 

def PieceLocator(Pieces,piece,nr,nc,piBord):
    print('Piece Locator')
    con=False

    horCon,horP=HorPieceCheck(piece,nr,nc,piBord)
    print('horCon='+str(horCon))
    print('horP='+str(horP))
    verCon,verP=VerPieceCheck(piece,nr,nc,piBord)
    print('verrCon='+str(horCon))
    print('verP='+str(horP))
    diagCon,diagP=DiagPieceCheck(piece,nr,nc,piBord)
    print('diagCon='+str(horCon))
    print('diagP='+str(horP))
    knCon,knP=KnightPieceCheck(piece,nr,nc,piBord)
    print('knCon='+str(horCon))
    print('knP='+str(horP))
    pawnCon=PawnLocator(Pieces,piece,nr,nc,piBord)
    print('pawnCon='+str(horCon))
    print('\n')

    if True in (horCon,verCon,diagCon,knCon,pawnCon):
        con=True
    else:
        con=False
    return con

def PawnLocator(Pieces,piece,nr,nc,piBord):
    print('Pawn Locator')
    pVal=piece['Value']
    lr,lc=nr,nc
    v=''
    count=0

    while count<2:
        lr+=1
        v=piBord[lr][lc]
        if v!='':
            if v[0]!=pVal[0]:
                if v[1]=='P':
                    pawn=Pieces[v]
                    print('Pawn='+str(pawn['Value']))
                    pawnRow,pawnCol=pawn['Coords']
                    if pawn['Move']=='PawnMoveDown':
                        if pawnRow<nr:
                            if abs(int(pawnRow-nr))==1:
                                c=True
                                break
                            elif abs(int(pawnRow-nr))==2 and pawn['Dual-Step']==False:
                                c=True
                                break
                            else:
                                c=False
                                break
                    elif pawn['Move']=='PawnMoveUp':
                        if pawnRow>nr:
                            if abs(int(pawnRow-nr))==1:
                                c=True
                                break
                            elif abs(int(pawnRow-nr))==2 and pawn['Dual-Step']==False:
                                c=True
                                break
                            else:
                                c=False
                                break
            elif v[0]==pVal[0]:
                c=False
                break
    print('c='+str(c))
    return c

def PathBlocker(piBord,piece,king,Pieces):
    pr,pc=piece['Coords']
    pVal=piece['Value']
    kVal=king['Value']
    kr,kc=king['Coords']
    nr,nc=pr,pc
    con=False
    v=''

    if nr==kr and nc!=kc:
        print('Horizontally')
        while nc!=kc:
            if nc<kc:
                nc+=1
            elif nc>kc:
                nc-=1
            if nc==kc:
                con=True
                break
            c=PieceLocator(Pieces,piece,nr,nc,piBord)
            if c==True:
                con=False
                break
            elif c==False:
                con=True
    elif nr!=kr and nc==kc:
        print('Vertically')
        while nr!=kr:
            if nr<kr:
                nr+=1
            elif nr>kr:
                nr-=1
            if nr==kr:
                con=True
                break
            c=PieceLocator(Pieces,piece,nr,nc,piBord)
            if c==True:
                con=False
                break
            else:
                con=True
    elif nr!=kr and nc!=kc:
        if abs(int(pr-nr))==abs(int(pc-nc)):
            print('Diagonally')
            while nr!=kr and nc!=kc:
                if nr<kr:
                    nr+=1
                elif nr>kr:
                    nr-=1
                if nc<kc:
                    nc+=1
                elif nc>kc:
                    nc-=1
                if nr==kr or nc==kc:
                    con=True
                    break
                print('nr='+str(nr)+' nc='+str(nc))
                c=PieceLocator(Pieces,piece,nr,nc,piBord)
                if c==True:
                    con=False
                    break
                elif c==False:
                    con=True
        elif abs(int(pr-kr))!=abs(int(pc-kc)):
            con=False    
    print('\n')
    displayBoard(piBord)
    print('\n')
    return con

Controller()
