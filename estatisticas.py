import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

class Estatistica():
    """
        Esta classe é responsável por tratar os dados armazenados em log e gerar gráficos
        mostrando estatísticas relevantes ao jogo.
    """    
    def __init__(self):
        self.source = open('log\\log.txt')
        self.sessions = []
        self.moves = []
        self.valid_cmd = 0
        self.repeat_cmd = 0
        self.command_error = 0
        
    def getStatistics(self):
        """
            Lê o arquivo de log e disponibiliza os dados necessários para gerar os gráficos
            com matplotlib.
        """
        
        with self.source as source:
            for i, line in enumerate(source):
                
                if line.find('NEW SESSION') > -1:
                    newSession = []
                    continue
                elif line.find('END SESSION') > -1:
                    self.sessions.append(newSession)
                    continue

                newSession.append(line)
                
        for session in self.sessions:
            for line in session:
                
                if line == '\n':
                    continue
                
                try:
                    m = re.search(r'Key (\d) pressed', line)
                    key = m.group(0).replace('Key', '').replace('pressed', '').strip()
                    if line.find("Repeated Command") > -1:
                        self.repeat_cmd += 1
                except AttributeError:
                    m = re.search(r'Key \w pressed', line)
                    print(m)
                    key = m.group(0).replace('Key', '').replace('pressed', '').strip()
                    
                self.moves.append(key)
    
        for move in self.moves:
            
            if move.isnumeric():
                if int(move) > 0:
                    self.valid_cmd += 1
                else:
                    self.command_error += 1
            
            elif move.isalpha():
                self.command_error += 1
            

    def plotMoves(self):
        """
            Plota um gráfico de frequencia de uso dos números usados no jogo.
        """
        
        xlist = [i for i in range(1,10)]
        count = np.zeros(9, dtype=np.int32)
        
        for num in self.moves:
            if num.isalpha():
                continue
            else:
                iNum = int(num)
                if iNum == 0:
                    continue
            count[iNum - 1] += 1
            
        plt.figure(num=0, dpi=120)
        plt.title("Frequência de uso")
        plt.xticks(xlist)
        plt.bar(xlist, count)
        plt.show()

    def plotCommands(self):
        """
            Plota um gráfico de validade dos comandos recebidos.
        """
        
        x= [0, 1, 2]
        xlist = ['Comando válido', 'Comando repetido', 'Comando inválido']
        count = [self.valid_cmd, self.repeat_cmd, self.command_error]        

        f = plt.figure(num=1, dpi=120)
        plt.title("Comandos recebidos")
        plt.xticks(x, xlist)
        plt.bar(xlist, count)
        plt.show()
        
        
if __name__ == '__main__':
    stats = Estatistica()
    stats.getStatistics()
    stats.plotMoves()
    stats.plotCommands()