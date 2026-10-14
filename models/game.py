from models.card import Card, HealCard, MonsterCard, ShieldCard
from models.deck import Deck
from models.player import Player


class Game:
    def __init__(self, player: Player, deck: Deck) -> None:
        self.player = player
        self.deck = deck
        self.can_skip = True
        self.score = 0
        self.end_reason: str | None = None
        self.carried_card: Card | None = None

    def create_room(self) -> list[Card] | None:
        required_cards = 3 if self.carried_card is not None else 4
        if len(self.deck.play_deck) < required_cards:
            self.deck.play_deck.clear()  # Bỏ hết các lá cuối cùng thì có nên cộng điểm không nhỉ
            self.carried_card = None
            return None

        if self.carried_card is not None:
            room = [
                self.carried_card,
                *self.deck.play_deck[:3],
            ]  # * là dấu giải nén để các lá được chọn nằm cùng cấp với carried card
            del self.deck.play_deck[
                :3
            ]  # Đơn giản hơn là for _ in range(3): self.deck.play_deck.remove(0)
            self.carried_card = None
        else:
            room = self.deck.play_deck[:4]
            del self.deck.play_deck[:4]
        return room

    def handle_action(self, actions: list[int], room: list[Card]) -> bool:
        if not actions:
            if not self.can_skip:
                raise ValueError("Không thể bỏ qua hai room liên tiếp.")
            self.deck.play_deck.extend(room)
            self.carried_card = None
            self.can_skip = False
            return True

        if len(actions) != 3:
            raise ValueError("Mỗi room phải chọn đúng 3 lá.")
        if len(set(actions)) != 3:
            raise ValueError("Không được chọn trùng lá.")
        if any(action not in range(len(room)) for action in actions):
            raise ValueError("Vị trí lá bài không hợp lệ.")

            # # Chuyển actions thành set để tìm kiếm với tốc độ O(1)
            # actions_set = set(actions)

            # self.carried_card = next(
            #     (card for index, card in enumerate(room) if index not in actions_set),
            #     # None,
            # )

        self.carried_card = next(
            (card for index, card in enumerate(room) if index not in actions), None
        )  # Lazy loop: Trả lại phần tử đầu tiên tìm thấy để tối ưu hiệu năng.
        self.can_skip = True
        selected_cards = [room[action] for action in actions]
        for card in selected_cards:
            if isinstance(card, HealCard):
                card.heal_player(self.player)
            elif isinstance(card, ShieldCard):
                card.shield_player(self.player)
            elif isinstance(card, MonsterCard):
                card.deal_dmg_to_player(self.player)
                self.score += card.value
                if self.player.health == 0:
                    self.end_reason = "health_depleted"
                    return False
        return True

    def gameloop(self) -> None:
        while self.player.health > 0:
            room = self.create_room()
            if room is None:
                self.end_reason = "deck_exhausted"
                break

            self.print_room(room)
            if (
                self.can_skip
                and input("Nhập 'skip' để bỏ qua room, hoặc nhấn Enter để chọn bài: ")
                .strip()
                .lower()
                == "skip"
            ):
                self.handle_action([], room)
                continue

            actions = self._read_actions(len(room))
            if not self.handle_action(actions, room):
                print("Bạn đã hết máu!")
                break

            self._print_player_status()

        self.print_summary()

    def _read_actions(self, room_size: int) -> list[int]:
        actions: list[int] = []
        while len(actions) < 3:
            try:
                action = int(input(f"Chọn vị trí lá bài (1-{room_size}): ")) - 1
            except ValueError:
                print(f"Vui lòng nhập số từ 1 đến {room_size}.")
                continue

            if action not in range(room_size):
                print("Vị trí không hợp lệ.")
                continue
            if action in actions:
                print("Bạn đã chọn lá bài này rồi.")
                continue
            actions.append(action)

        return actions

    def print_room(self, room: list[Card]) -> None:
        print("Đây là các lá trong room:")
        for index, card in enumerate(room, start=1):
            print(f"{index}. {card}")

    def _print_player_status(self) -> None:
        print(f"Máu: {self.player.health}/20 | Khiên: {self.player.shield}")

    def print_summary(self) -> None:
        if self.end_reason == "health_depleted":
            outcome = "Thua cuộc: máu đã về 0."
        else:
            outcome = "Kết thúc: không còn đủ bài để tạo room."
        print("\n--- Tổng kết ---")
        print(outcome)
        self._print_player_status()
        print(f"Điểm: {self.score}")
