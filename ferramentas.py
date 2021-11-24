from jogador import Jogador
from datetime import datetime
import random
import os

class Ferramentas:
    """
        Esta super classe inclui todos os métodos que podem vir a ser úteis para a
        mecânica do jogo, independente das classes criadas para o jogo específico.
    """

    def __init__(self):
        self.grid = []

    def Setup(self):
        """
            Gera um novo grid de início de partida.
        """
        
        with open('src\\sudoku.txt', 'r') as file:
            length = 0
            for line in file:
                length+= 1
                
        rand = random.randint(1, length)
        
        with open('src\\sudoku.txt') as file:
            for i, line in enumerate(file):
                if i == rand + 1:
                    l = line
                    break
        try:
            arr = l.split('], [')
        except UnboundLocalError:
            bkp = "[[0, 9, 8, 0, 1, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 2, 0, 5, 0], [0, 8, 4, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 8, 0, 9], [3, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0]]"
            arr = bkp.split('], [')
        
        for line in arr:
            
            arrLn = []
            for char in line:
                if char.isnumeric():
                    arrLn.append(int(char))
            self.grid.append(arrLn)
                    
        return self.grid
    
    def RestoreSesion(self):
        """
            Restaura a última sessão salva do jogo.
        """
        
        with open('log\\last_session.txt', 'r') as save:
            for i, line in enumerate(save):
                arrLn = []
                
                for char in line:
                    if char.isnumeric():
                        arrLn.append(int(char))
                self.grid.append(arrLn)
        
        return self.grid

    def getLastPlayer(self):
        playerName = ""
        if not os.path.exists('log\\log.txt'):
            open('log\\log.txt', 'w+')
        with open('log\\log.txt', 'r') as log:
            for i, line in enumerate(log):
                if line.find('Player') != -1:
                    playerName = line.split('Player: ')[1]
        return playerName

    def getPlayer(self, playerName):
        jogadas = 0                  # Quantidade de movimentos feitos
        tentativas = 0            # Quantidade de tentativas que o jogador fez.
        melhorTempo = None
        increment = False
        timeNew, timeEnd = None, None
        
        if not os.path.exists('log\\log.txt'):
            open('log\\log.txt', 'w+')
        
        with open('log\\log.txt', 'r+') as log:
            for i, line in enumerate(log):
                line = line.lower()
                if line == '\n':
                    continue
                
                if line.find(f'{playerName.lower()}') != -1:
                    increment = True
                    tentativas += 1
                    timeNew = datetime.strptime(line.split(']')[0][1:], "%d-%m-%Y %H:%M:%S")
                    
                elif line.find('end') != -1:
                    increment = False
                    if timeNew != None:
                        timeEnd = datetime.strptime(line.split(']')[0][1:], "%d-%m-%Y %H:%M:%S")
        
                if increment and (line.find('repeated') != -1 or line.find('valid') != -1):
                    print(line)
                    jogadas += 1
                    
                if timeNew != None and timeEnd != None:
                    if melhorTempo == None:
                        melhorTempo = (timeEnd - timeNew).total_seconds() / 60.0
                    else:
                        current = (timeEnd - timeNew).total_seconds() / 60.0
                        
                        if melhorTempo > current:
                            melhorTempo = (timeEnd - timeNew).total_seconds() / 60.0
                        
                
        
        print(f'jogador: {playerName.lower()}')
        print(f'jogadas: {jogadas}')
        print(f'tentativas: {tentativas}')

        if tentativas > 0:
            player = Jogador(playerName, jogadas, tentativas, melhorTempo)
        else:
            player = Jogador(playerName)
        
        return player
    

if __name__ == '__main__':
    Ferramentas().getPlayer('dadd123')