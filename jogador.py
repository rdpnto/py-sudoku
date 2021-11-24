class Jogador:
    """
        Esta classe representa o jogador de Sudoku. Cada vez que o programa é 
        reiniciado, um novo nick deve ser colocado para registrar os
        tempos deste jogador
    """
    
    def __init__(self, nick, jogadas=0, tentativas=0, melhorTempo=-1):
        self.nick = nick                        # Nome do jogador no jogo.
        self.jogadas = jogadas                  # Quantidade de movimentos feitos
        self.tentativas = tentativas            # Quantidade de tentativas que o jogador fez.
        self.melhorTempo = melhorTempo          # Melhor tempo registrado pelo jogador.
        
        