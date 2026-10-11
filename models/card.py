from models.player import Player


class Card:
    def __init__(self, value: int, suit: str) -> None:
        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        rank = {
            11: "J",
            12: "Q",
            13: "K",
            14: "A",
        }.get(self.value, str(self.value))
        return f"{rank} {self.suit}"


class HealCard(Card):
    def __init__(self, value: int, suit: str) -> None:
        super().__init__(value, suit)

    def heal_player(self, player: Player) -> None:
        player.health = min(player.max_health, player.health + self.value)

class ShieldCard(Card):
    def __init__(self, value: int, suit: str) -> None:
        super().__init__(value, suit)

    def shield_player(self, player: Player) -> None:
        player.shield = self.value

class MonsterCard(Card):
    def __init__(self, value: int, suit: str) -> None:
        super().__init__(value, suit)

    def deal_dmg_to_player(self, player: Player) -> None:
        #Sát thương = value - khiên. Nếu value nhỏ hơn khiên thì sát thương = 0
        damage = max(0, self.value - player.shield)
        player.shield = max(0, player.shield - self.value)
        player.health = max(0, player.health - damage)