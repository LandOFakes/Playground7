import random
 
 class Die:
     def __init__(self):
         # Seed the random number generator to ensure consistency in testing
         random.seed(0)
 
     def roll(self):
         # Roll the die (returns a value between 1 and 6)
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
 
 class PigGame:
     def __init__(self, player1_name, player2_name):
         self.die = Die()
         self.player1 = Player(player1_name)
         self.player2 = Player(player2_name)
         self.current_player = self.player1
 
     def switch_turn(self):
         if self.current_player == self.player1:
             self.current_player = self.player2
         else:
             self.current_player = self.player1
 
     def play_turn(self):
         while True:
             print(f"{self.current_player.name}'s Turn:")
             print(f"Turn score: {self.current_player.turn_score}")
             print(f"Total score: {self.current_player.score}")
             action = input("Roll (r) or Hold (h)? ")
 
             if action.lower() == 'r':
                 roll = self.die.roll()
                 print(f"Rolled: {roll}")
 
                 if roll == 1:
                     print(f"{self.current_player.name} rolled a 1! No points for this turn.")
                     self.current_player.reset_turn()
                     self.switch_turn()
                     break
                 else:
                     self.current_player.turn_score += roll
             elif action.lower() == 'h':
                 self.current_player.hold()
                 self.switch_turn()
                 break
 
     def check_winner(self):
         if self.player1.score >= 100:
             return self.player1
         elif self.player2.score >= 100:
             return self.player2
         return None
 
     def play_game(self):
         while True:
             self.play_turn()
             winner = self.check_winner()
             if winner:
                 print(f"{winner.name} wins with {winner.score} points!")
                 break
 
 if __name__ == "__main__":
     player1_name = input("Enter name for Player 1: ")
     player2_name = input("Enter name for Player 2: ")
     
     game = PigGame(player1_name, player2_name)
     game.play_game()

