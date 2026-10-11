import random

from models.card import Card, HealCard, MonsterCard, ShieldCard


class Deck:
    def __init__(self) -> None:
        #Card = Value + suit, loop tạo bộ bài sẽ là: 4 lần (4 suits) loops từ 2 đến 14 (Từ 2 đến Ace)
        self.full_deck_value: list[int] = [value for value in range(2, 15)]
        self.suits: list[str] = ["Cơ", "Rô", "Tép", "Bích"]
        self.play_deck: list[Card] = []
        for suit in self.suits:
            for value in self.full_deck_value:
                if value >= 11 and suit in ["Cơ", "Rô"]:
                    continue
                if suit == "Cơ":
                    card = HealCard(value, suit)
                elif suit == "Rô":
                    card = ShieldCard(value, suit)
                else:
                    card = MonsterCard(value, suit)
                self.play_deck.append(card)
        self.shuffle_deck()

    def shuffle_deck(self) -> None:
        random.shuffle(self.play_deck)

    def remove_card(self, card: Card) -> None:
        self.play_deck.remove(card)