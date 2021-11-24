from datetime import datetime
import numpy as np

class Log:
    """
        Esta classe trata e armazena todas as entradas do usuário, filtrando e salvando
        os dados em arquivos específicos, de acordo com a seguinte estrutura:
            
        > log\log_moves.txt - armazena todas as ações do usuário no jogo, ou seja, um histórico 
        de todas as jogadas.
        > log\log.txt - LOG completo de todas as ações inputadas, registrando também todos erros 
        ocorrem durante o funcionamento do jogo.
        > log\last_session.txt - armazena o estado atual do jogo, para que possa ser restaurado 
        em uma futura sessão.
        
    """
    def __init__(self):
        self.moves = np.ndarray(0, dtype=np.int32)
        self.sessionStart = ""
        self.board = []
    
    def History(self, inputs, valid = True):
        datetimeObj = datetime.now()
        timestamp = datetimeObj.strftime("[%d-%m-%Y %H:%M:%S]")

        with open('log\\log.txt', 'a+') as log:
            log.write(f"{timestamp} - ")
            
            if not str(inputs).isnumeric() or inputs == '0':
                log.write("Command Error: ")
            elif not valid:
                log.write("Repeated Command: ")
            else:
                log.write("Valid Command: ")
            log.write(f"Key {inputs} pressed\n")
            
        
        self.moves = np.append(self.moves, str(inputs))
        
    def Session(self, inputs, playerName=""):
        timestamp = datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
        if playerName != "":
            logText = f"{timestamp} NEW SESSION - Player: {playerName}\n"
        else:
            logText = f"{timestamp} {inputs} SESSION\n"
        
        with open('log\\log.txt', 'a+') as log:
            log.write(logText)
            
        if inputs == "NEW":
            self.moves = np.ndarray(0, dtype=np.int32)
            self.sessionStart = timestamp
            
        elif inputs == "END":
            self.CurrentSession(self.board, True)
            
            with open('log\\log_moves.txt', 'a+') as log_moves:
                log_moves.write(f"SESSION {timestamp} MOVES: {str(self.moves)}\n")
                
    def CurrentSession(self, board, saveNow = False):
        if saveNow:
            with open('log\\last_session.txt', 'w+') as save:
                save.write(str(self.board))
        else:
            self.board = board
