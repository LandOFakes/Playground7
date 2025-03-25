import time
import random

# Die class for simulating dice rolls
class Die:
    def roll(self):
        return random.randint(1, 6)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_score = 0

    def reset_turn(self):
        self.turn_score = 0

    def add_turn_score(self):
        self.score += self.turn_score

    def hold(self):
        self.add_turn_score()
        self.reset_turn()

class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def make_move(self):
        # Strategy: If the computer's score is less than 100, it will hold if the score is greater than 25
        hold_threshold = min(25, 100 - self.score)
        if self.turn_score >= hold_threshold:
            self.hold()
            return 'h'
        else:
            return 'r'

class PlayerFactory:
    def create_player(self, player_type, name):
        if player_type == 'human':
            return Player(name)
        elif player_type == 'computer':
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type. Choose 'human' or 'computer'.")

class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def check_time(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 60:
            print("Time's up!")
            return True
        return False

    def play_game(self):
        while True:
            if self.check_time():
                winner = self.game.check_winner()
                if winner:
                    print(f"{winner.name} wins with {winner.score} points!")
                break
            self.game.play_turn()
            winner = self.game.check_winner()
            if winner:
                print(f"{winner.name} wins with {winner.score} points!")
                break

class PigGame:
    def __init__(self, player1_type, player2_type, player1_name, player2_name):
        self.die = Die()
        player_factory = PlayerFactory()
        self.player1 = player_factory.create_player(player1_type, player1_name)
        self.player2 = player_factory.create_player(player2_type, player2_name)
        self.current_player = self.player1

    def switch_turn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play_turn(self):
        print(f"{self.current_player.name}'s Turn:")
        print(f"Turn score: {self.current_player.turn_score}")
        print(f"Total score: {self.current_player.score}")
        
        if isinstance(self.current_player, ComputerPlayer):
            action = self.current_player.make_move()
        else:
            action = input("Roll (r) or Hold (h)? ")

        if action.lower() == 'r':
            roll = self.die.roll()
            print(f"Rolled: {roll}")

            if roll == 1:
                print(f"{self.current_player.name} rolled a 1! No points for this turn.")
                self.current_player.reset_turn()
                self.switch_turn()
            else:
                self.current_player.turn_score += roll
        elif action.lower() == 'h':
            self.current_player.hold()
            self.switch_turn()

    def check_winner(self):
        if self.player1.score >= 100:
            return self.player1
        elif self.player2.score >= 100:
            return self.player2
        return None

if __name__ == "__main__":
    player1_type = input("Enter type for Player 1 (human/computer): ").lower()
    player2_type = input("Enter type for Player 2 (human/computer): ").lower()
    player1_name = input("Enter name for Player 1: ")
    player2_name = input("Enter name for Player 2: ")

    game = PigGame(player1_type, player2_type, player1_name, player2_name)

    # Use TimedGameProxy if the timed argument is passed
    timed_game = input("Do you want a timed game? (y/n): ").lower()
    if timed_game == 'y':
        timed_proxy = TimedGameProxy(game)
        timed_proxy.play_game()
    else:
        game.play_game()

