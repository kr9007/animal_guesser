from game import Game


def main():
    game = Game()
    while True:
        choice = input("\n1 играть, 2 статистика, 3 выход: ").strip()
        if choice == "1":
            game.play()
        elif choice == "2":
            game.show_stats()
        elif choice == "3":
            break


if __name__ == "__main__":
    main()
