
import time

class Game:
    def __init__(player):
        player.initialize_game()

    def initialize_game(player):
        player.current_state = [['.','.','.'],
                              ['.','.','.'],
                              ['.','.','.']]

        # Player X always plays first
        player.player_turn = 'X'

    def draw_board(player):
        for i in range(0, 3):
            for j in range(0, 3):
                print('{}|'.format(player.current_state[i][j]), end=" ")
            print()
        print()

        # Determines if the made move is a legal move
    def is_valid(player, input_x, input_y):
        if input_x < 0 or input_x > 2 or input_y < 0 or input_y > 2:
            return False
        elif player.current_state[input_x][input_y] != '.':
            return False
        else:
            return True

            # Checks if the game has ended and returns the winner in each case
    def is_end(player):
        # Vertical win
        for i in range(0, 3):
            if (player.current_state[0][i] != '.' and
                player.current_state[0][i] == player.current_state[1][i] and
                player.current_state[1][i] == player.current_state[2][i]):
                return player.current_state[0][i]

    # Horizontal win
        for i in range(0, 3):
            if (player.current_state[i] == ['X', 'X', 'X']):
                return 'X'
            elif (player.current_state[i] == ['O', 'O', 'O']):
                return 'O'

    # Main diagonal win
        if (player.current_state[0][0] != '.' and
            player.current_state[0][0] == player.current_state[1][1] and
            player.current_state[0][0] == player.current_state[2][2]):
            return player.current_state[0][0]

    # Second diagonal win
        if (player.current_state[0][2] != '.' and
            player.current_state[0][2] == player.current_state[1][1] and
            player.current_state[0][2] == player.current_state[2][0]):
            return player.current_state[0][2]

    # Is whole board full?
        for i in range(0, 3):
            for j in range(0, 3):
                # There's an empty field, we continue the game
                if (player.current_state[i][j] == '.'):
                    return None

    # It's a tie!
        return '.'

    # Player 'O' is max, in this case AI
    def max(player):

        # Possible values for maxValue are:
        # -1 - loss
        # 0  - a tie
        # 1  - win

        # We're initially setting it to -2 as worse than the worst case:
        maxValue = -2

        input_x = None
        input_y = None

        result = player.is_end()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - a tie
        # 1  - win
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if player.current_state[i][j] == '.':
                    # On the empty field player 'O' makes a move and calls Min
                    # That's one branch of the game tree.
                    player.current_state[i][j] = 'O'
                    (m, min_i, min_j) = player.min()
                    # Fixing the maxValue value if needed
                    if m > maxValue:
                        maxValue = m
                        input_x = i
                        input_y = j
                    # Setting back the field to empty
                    player.current_state[i][j] = '.'
        return (maxValue, input_x, input_y)

        # Player 'X' is min, in this case human
    def min(player):

        # Possible values for minValue are:
        # -1 - win
        # 0  - a tie
        # 1  - loss

        # We're initially setting it to 2 as worse than the worst case:
        minValue = 2

        algo_x = None
        algo_y = None

        result = player.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if player.current_state[i][j] == '.':
                    player.current_state[i][j] = 'X'
                    (m, max_i, max_j) = player.max()
                    if m < minValue:
                        minValue = m
                        algo_x = i
                        algo_y = j
                    player.current_state[i][j] = '.'
        return (minValue, algo_x, algo_y)
    
    def play(player):
        depth = 0
        totalTime=0

        while True:
            player.draw_board()
            player.result = player.is_end()

            # Printing the appropriate message if the game has ended
            if player.result != None:
                if player.result == 'X':
                    print('The winner is X!')
                    print('Depth = ',depth)
                    print('Total time = ',totalTime)
                elif player.result == 'O':
                    print('The winner is O!')
                    print('Depth = ',depth)
                    print('Total time = ',totalTime)


                elif player.result == '.':
                    print("It's a tie!")
                    print('Depth = ',depth)
                    print('Total time = ',totalTime)



                player.initialize_game()
                return

            # If it's player's turn
            if player.player_turn == 'X':
                while True:

                    start = time.time()
                    (m, algo_x, algo_y) = player.min()
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 7)))
                    totalTime+= round(end - start, 7)
                    print('Recommended move: X = {}, Y = {}'.format(algo_x, algo_y))
                    print('Current depth = ',depth)

                    input_x = int(input('Insert the X coordinate: '))
                    input_y = int(input('Insert the Y coordinate: '))
                    print('\n')

                    (algo_x, algo_y) = (input_x, input_y)

                    if player.is_valid(input_x, input_y):
                        player.current_state[input_x][input_y] = 'X'
                        depth+=1
                        player.player_turn = 'O'
                        break
                    else:
                        print('The move is not valid! Try again.')

            # If it's AI's turn
            else:
                start = time.time()
                (m, input_x, input_y) = player.max()
                end = time.time()
                totalTime+= round(end - start, 7)

                depth+=1
                player.current_state[input_x][input_y] = 'O'
                player.player_turn = 'X'



    def max_alpha_beta(player, alpha, beta):
        maxValue = -2
        input_x = None
        input_y = None

        result = player.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if player.current_state[i][j] == '.':
                    player.current_state[i][j] = 'O'
                    (m, min_i, in_j) = player.min_alpha_beta(alpha, beta)
                    if m > maxValue:
                        maxValue = m
                        input_x = i
                        input_y = j
                    player.current_state[i][j] = '.'

                    # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                    if maxValue >= beta:
                        return (maxValue, input_x, input_y)

                    if maxValue > alpha:
                        alpha = maxValue

        return (maxValue, input_x, input_y)

    def min_alpha_beta(player, alpha, beta):

        minValue = 2

        algo_x = None
        algo_y = None

        result = player.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if player.current_state[i][j] == '.':
                    player.current_state[i][j] = 'X'
                    (m, max_i, max_j) = player.max_alpha_beta(alpha, beta)
                    if m < minValue:
                        minValue = m
                        algo_x = i
                        algo_y = j
                    player.current_state[i][j] = '.'

                    if minValue <= alpha:
                        return (minValue, algo_x, algo_y)

                    if minValue < beta:
                        beta = minValue
        return (minValue, algo_x, algo_y)

    def play_alpha_beta(player):
     depth = 0
     totalTime=0
     while True:
        player.draw_board()
        player.result = player.is_end()

        if player.result != None:
            if player.result == 'X':
                print('The winner is X!')
                print('Depth = ',depth)
                print('Total time = ',totalTime)
            elif player.result == 'O':
                print('The winner is O!')
                print('Depth = ',depth)
                print('Total time = ',totalTime)


            elif player.result == '.':
                print("It's a tie!")
                print('Depth = ',depth)
                print('Total time = ',totalTime)




            player.initialize_game()
            return

        if player.player_turn == 'X':
            
            while True:
                start = time.time()
                (m, algo_x, algo_y) = player.min_alpha_beta(-2, 2)
                end = time.time()
                print('Evaluation time: {}s'.format(round(end - start, 7)))
                totalTime+= round(end - start, 7)
                print('Recommended move: X = {}, Y = {}'.format(algo_x, algo_y))
                print('Current depth = ',depth)
                input_x = int(input('Insert the X coordinate: '))
                input_y = int(input('Insert the Y coordinate: '))
                print('\n')
                algo_x = input_x
                algo_y = input_y

                if player.is_valid(input_x, input_y):
                    player.current_state[input_x][input_y] = 'X'
                    player.player_turn = 'O'
                    depth+=1
                    break
                else:
                    print('The move is not valid! Try again.')

        else:
            start = time.time()
            (m, input_x, input_y) = player.max_alpha_beta(-2, 2)
            end = time.time()
            totalTime+= round(end - start, 7)

            print('AI plays :')
            player.current_state[input_x][input_y] = 'O'
            depth+=1
            player.player_turn = 'X'    
