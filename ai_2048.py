import game_2048
from timeit import default_timer as timer


def minimax_ai(w, h):

    print("NOT IMPLEMENTED YET")


# World -> World (??)
# Wrapper for running the random AI
# Activates the random moves
def random_ai(w, h):
    max_scores = []
    attempts = int(input("How many attempts should the AI complete? (Integer answer required) "))
    up_huh = input("Allow tilting upwards in random choices? (N/y) ")
    start = timer()
    print("\n")
    print("** PROCESSING **")
    print("\n")
    if up_huh == "y":
        while attempts > 0:
            max_scores.append(game_2048.main(w, h, 1))
            attempts -= 1
            print(attempts)
    else:
        while attempts > 0:
            max_scores.append(game_2048.main(w, h, 1))
            attempts -= 1
            print(attempts)
    print(max_scores)
    print("Max score achieved:", max(max_scores))
    elapsed = timer() - start
    print(elapsed, "seconds elapsed")
    max_scores.sort()
    print("The AI's scores were: ", max_scores)


def main():
    print("Welcome to Jake Levi's 2048 AI Launcher")
    h = int(input("Height of board: "))
    w = int(input("Width of board: "))

    # AI SELECTION
    print("Which AI would you like to use?")
    print("\t NO AI - (0)")
    print("\t Random - (1)")
    print("\t Minimax (NOT IMPLEMENTED YET) - (2)")
    ai = input("> ")
    if ai == "0":
        game_2048.main(w, h)
    elif ai == "1":
        random_ai(w, h)
    elif ai == "2":
        minimax_ai(w, h)


main()
