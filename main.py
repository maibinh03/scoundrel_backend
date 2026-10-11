from models.deck import Deck
from models.game import Game
from models.player import Player


def main() -> None:
    player = Player()
    deck = Deck()
    Game(player, deck).gameloop()


if __name__ == "__main__":
    main()