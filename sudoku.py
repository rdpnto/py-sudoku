from ferramentas import *
from jogador import *
from logica import *
from log import *
from estatisticas import *

import os
import PIL.Image
import PIL.ImageTk
import numpy as np
from copy import deepcopy
from tkinter import *

"""
    Este programa consistem no jogo Sudoku
    
    É um jogo baseado na colocação lógica de números. O objetivo do jogo é a colocação de números 
    de 1 a 9 em cada uma das células vazias numa grade de 9x9, constituída por 3x3 subgrades chamadas
    regiões. O quebra-cabeça contém algumas pistas iniciais, que são números inseridos em algumas
    células, de maneira a permitir uma indução ou dedução dos números em células que estejam vazias.
    
    Fonte: https://pt.wikipedia.org/wiki/Sudoku
    
    Dada a descrição simples do jogo, algumas opções são escolhas do usuário:
        - Nível de dificuldade: varia de 1 a 5, 
          quão maior o nível, maior o número de lacunas no início (padrão = 3)
        - Modo de jogo: livre ou corrida contra o tempo (padrão = livre)
        
    As 91 casas do Sudoku são expressas abaixo. As posições são referidas como uma combinação de 
    um dos caracteres na margem vertical e um da margem horizontal (e.g B4), como num tabuleiro
    de xadrez
    
    Os * funcionam como lacunas (aqui todas as casas foram substituidas por lacuna para
    fins de simplicidade visual
    
      1 2 3 4 5 6 7 8 9
    A □ □ □ □ □ □ □ □ □
    B □ □ □ □ □ □ □ □ □
    C □ □ □ □ □ □ □ □ □
    D □ □ □ □ □ □ □ □ □
    E □ □ □ □ □ □ □ □ □
    F □ □ □ □ □ □ □ □ □
    G □ □ □ □ □ □ □ □ □
    H □ □ □ □ □ □ □ □ □
    I □ □ □ □ □ □ □ □ □ 

"""

# Document properties
__author__ = 'Andressa Moraes'
__copyright__ = 'Copyright_2021'
__credits__ = __author__
__license__ = 'GPL'
__version__ = '1.0.0'
__maintainer__ = __author__ # Responsável por manter o programa funcionando
__email__ = 'andressam@poli.ufrj.com'
__status__ = 'Production'


def getRecorde():
    """
        Esta função retorna o melhor tempo registrado.
        
        criar input para nome e armazenar.
        
        
        
    """
    return None
    

class create_button:
    def __init__(self, frame, x, y, root, number, board, canvas, i, j, ct):
        self.frame = frame
        self.root = root
        self.canvas = canvas
        self.number = number
        self.board = board

        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.ct = ct

        self.bt = Button(self.frame, bd=0, command=self.input, text=number, relief=SUNKEN, font=("Helvetica", 30), bg="white")

    def get_board(self):
        return self.board

    def draw_button(self):
        self.bt.bind("<Enter>", lambda _: self.bt.configure(bg="light yellow"))
        self.bt.bind("<Leave>", lambda _: self.bt.configure(bg="white"))
        self.bt.pack(expand=1, fill=BOTH)

    def draw_fixed_button(self):
        self.bt.configure(command=NONE, bg="#9ED9CC", activebackground="#9ED9CC")

        self.bt.pack(expand=1, fill=BOTH)

    def input(self):

        def onKeyPress(event=None):
            inputs = event.char
            
            if inputs in "123456789":
                inputs = int(event.char)
                
                if Logica(self.board).check(self.x, self.y, inputs):
                    Logger.log.History(inputs)
                    
                    self.bt.configure(text=inputs, bg="white")
                    self.board[self.x, self.y] = inputs

                    self.bt.bind("<Enter>", lambda _: self.bt.configure(bg="light yellow"))
                    self.bt.bind("<Leave>", lambda _: self.bt.configure(bg="white"))
                    self.root.unbind('<KeyPress>')
                    
                else:
                    Logger.log.History(inputs, False)
                    
            else:
                Logger.log.History(inputs)
                messagebox.showerror("CommandError", "Entrada inválida")
            
            Logger.log.CurrentSession(self.board)
            

        self.board[self.x, self.y] = 0
        self.bt.configure(text='', bg="#AF814D")

        self.bt.unbind("<Enter>")
        self.bt.unbind("<Leave>")
        self.root.bind('<KeyPress>', onKeyPress)
        
class Logger:
    log = Log()

def create_button_list(dim, canvas, root, board):
    frames_list = []
    canvas_id = []
    ct = 0
    width = dim // 9 - 8

    btn_list = []

    for x, i in enumerate(range(4, dim - (dim // 9), dim // 9)):
        btn_list.append([])
        for y, j in enumerate(range(4, dim - (dim // 9), dim // 9)):
            frames_list.append(Frame(root, width=width, height=width, bg="#FFDDE2"))
            frames_list[ct].propagate(False)

            num = str(board[x, y]) if board[x, y] != 0 else ''
            if num == '':
                # if num = 0, create input able button
                btn_list[x].append(create_button(frames_list[ct], x, y, root, num, board, canvas, i, j, ct))
                btn_list[x][y].draw_button()
            else:
                # if num != 0, create fixed button
                btn_list[x].append(create_button(frames_list[ct], x, y, root, num, board, canvas, i, j, ct))
                btn_list[x][y].draw_fixed_button()
            canvas_id.append(canvas.create_window(j + 5, i + 5, anchor="nw", window = frames_list[ct]))

            ct += 1
            
    return btn_list

def func_buttons(canvas1, root, back_up, board, b_lst, player):
    
    def showStats():
        stats = Estatistica()
        stats.getStatistics()
        stats.plotMoves()
        stats.plotCommands()
        
    def showLog():
        os.startfile("log\log.txt", operation="Open")
        
    timeRec = "Sem registro"
    
    if player.melhorTempo != None:
        if player.melhorTempo > 1:
            time = player.melhorTempo
            m = (time) % 60
            s = (time*60) % 60
            timeRec = "00:%02d:%02d" % (m, s)

    stats_bt = Button(root, bd=0, command=showStats, text="Estatisticas", font=("Poplar Std", 15), width=14, bg="gray")
    log_bt = Button(root, bd=0, command=showLog, text="Arquivo log", font=("Poplar Std", 15), width=14, bg="gray")
    player_lbl = Label(root, bd=0, text="Jogador(a):", font=("Courier New", 15), width=14)
    player.nick =  Label(root, bd=0, text=f"\n{player.nick}", font=("Poplar Std", 16), width=14)
    time_lbl = Label(root, bd=0, text="Melhor tempo:", font=("Courier New", 15), width=14)
    time = Label(root, bd=0, text=f"\n{timeRec}", font=("Poplar Std", 16), width=14)
    tries_lbl = Label(root, bd=0, text="Tentativas:", font=("Courier New", 15), width=14)
    tries = Label(root, bd=0, text=f"\n{player.tentativas}", font=("Poplar Std", 16), width=14)
    moves_lbl = Label(root, bd=0, text="Jogadas:", font=("Courier New", 15), width=14)
    moves = Label(root, bd=0, text=f"\n{player.jogadas}", font=("Poplar Std", 16), width=14)



    canvas1.create_window(20, 540, anchor="nw", window=log_bt)
    canvas1.create_window(20, 600, anchor="nw", window=stats_bt)
    
    canvas1.create_window(15, 60, anchor="nw", window=player_lbl)
    canvas1.create_window(15, 80, anchor="nw", window=player.nick)
    
    canvas1.create_window(15, 140, anchor="nw", window=time_lbl)
    canvas1.create_window(15, 160, anchor="nw", window=time)
        
    canvas1.create_window(15, 220, anchor="nw", window=tries_lbl)
    canvas1.create_window(15, 240, anchor="nw", window=tries)
        
    canvas1.create_window(15, 300, anchor="nw", window=moves_lbl)
    canvas1.create_window(15, 320, anchor="nw", window=moves)

    
def main():
    
    dialog = Tk()
    dialog.withdraw()

    tools = Ferramentas()
    RestoreSesion = False
    playerName = None
    
    if os.path.exists('log\\last_session.txt'):
        
        with open('log\\last_session.txt', 'r') as save:
            for i, line in enumerate(save):
                if line == '[]':
                    break
                else:
                    if messagebox.askokcancel("Restaurar ultima sessao", "Deseja retornar ao ultimo jogo salvo?"):
                        RestoreSesion = True
                break
    
    if RestoreSesion:
        board = np.array(tools.RestoreSesion())
        playerName = tools.getLastPlayer()
    else:
        board = np.array(tools.Setup())
        playerName = simpledialog.askstring(title='Sudoku', prompt='Quem está jogando? ')
    dialog.destroy()
    
    if playerName == None or playerName == "":
        playerName = "Visitante"
    
    player = tools.getPlayer(playerName)
    
    
    dimension = 700
    imgFile = "src\\bg.jpg"
    isNewSession = TRUE
    
    root = Tk()
    root.title('Sudoku')
    root.configure(bg="light gray")

    root.geometry(f"{dimension + 200}x{dimension}")
    c = Canvas(root, height=dimension, width=dimension, bg="black", bd=0, highlightthickness=0)
    
    img = PIL.Image.open(imgFile)
    img = img.resize((dimension, dimension), PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(img)
    
    b_lst = create_button_list(dimension, c, root, board)
    c.grid(row=0, column=0)

    c1 = Canvas(root, height=dimension, width=250, bg="light gray", bd=0, highlightthickness=0)
    c1.grid(row=0, column=1)
    
    backup_board = deepcopy(board)
    func_buttons(c1, root, backup_board, board, b_lst, player)
    
    Logger.log.Session("NEW", playerName)
    
    root.mainloop()
    
    Logger.log.Session("END")
    
    
if __name__ == '__main__':
    main()