from typing import Dict
import random
from sam_utilities import validate_list_input, display_list

class Action:
    def is_stronger_then(self, action: 'Action') -> bool | None:
        pass

class Rock(Action):
    def is_stronger_then(self, action: 'Action'):
        if isinstance(action, Paper):
            return False
        if isinstance(action, Rock):
            return None
        if isinstance(action, Scissors):
            return True

class Paper(Action):
    def is_stronger_then(self, action: 'Action'):
        if isinstance(action, Paper):
            return None
        if isinstance(action, Rock):
            return True
        if isinstance(action, Scissors):
            return False

class Scissors(Action):
    def is_stronger_then(self, action: 'Action'):
        if isinstance(action, Paper):
            return True
        if isinstance(action, Rock):
            return False
        if isinstance(action, Scissors):
            return None


actions = {
    "rock": Rock(),
    "paper": Paper(),
    "scissors": Scissors(),
}

running = True

while running:
    action = validate_list_input(actions.keys(), f"Choose one of the following actions: {display_list(actions.keys())} ", "That input is invalid please try again")
    print(f"You choose {action}")
    computer_action = random.choice(list(actions.keys()))
    print(f"Computer choose {computer_action}")

    strength = actions[action].is_stronger_then(actions[computer_action])

    if strength == True:
        print("You won")
    elif strength == None:
        print("No one won")
    else:
        print("Computer won")

    play_again = validate_list_input(["yes", "no"], f"Want to play again? Choose {display_list(["yes", "no"])}", "That is an invalid input, please try again.")
    if play_again == "no":
        running = False
        break
