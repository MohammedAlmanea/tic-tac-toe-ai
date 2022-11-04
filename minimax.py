from tictactoe import *

def main():
    g = Game()
    # To use minimax algorithm              -> g.play()
    # or
    # To use alpha-beta pruning algorithm   -> g.play_alpha_beta()
    
    
    g.play()
    
if __name__ == "__main__":
    main()