from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from treys import Card, Evaluator

class PokerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20, **kwargs)

        self.evaluator = Evaluator()

        self.add_widget(Label(text="Wpisz 5 kart wspólnych:"))
        self.board_input = TextInput(hint_text='Np. Ah Ks 10d Jc 3h', multiline=False)
        self.add_widget(self.board_input)

        self.add_widget(Label(text="Gracz 1 – 2 karty:"))
        self.player1_input = TextInput(hint_text='Np. Qh Qd', multiline=False)
        self.add_widget(self.player1_input)

        self.add_widget(Label(text="Gracz 2 – 2 karty:"))
        self.player2_input = TextInput(hint_text='Np. As 9s', multiline=False)
        self.add_widget(self.player2_input)

        self.result_label = Label(text="")
        self.add_widget(self.result_label)

        self.button = Button(text="Sprawdź zwycięzcę")
        self.button.bind(on_press=self.calculate)
        self.add_widget(self.button)

    def calculate(self, instance):
        try:
            board = [Card.new(c.upper()) for c in self.board_input.text.strip().split()]
            p1 = [Card.new(c.upper()) for c in self.player1_input.text.strip().split()]
            p2 = [Card.new(c.upper()) for c in self.player2_input.text.strip().split()]
            if len(board) != 5 or len(p1) != 2 or len(p2) != 2:
                raise ValueError("Niepoprawna liczba kart.")

            s1 = self.evaluator.evaluate(board, p1)
            s2 = self.evaluator.evaluate(board, p2)

            name1 = self.evaluator.class_to_string(self.evaluator.get_rank_class(s1))
            name2 = self.evaluator.class_to_string(self.evaluator.get_rank_class(s2))

            if s1 < s2:
                winner = "Gracz 1 wygrywa!"
            elif s1 > s2:
                winner = "Gracz 2 wygrywa!"
            else:
                winner = "Remis!"

            self.result_label.text = f"[1] {name1} vs [2] {name2} → {winner}"

        except Exception as e:
            self.result_label.text = f"Błąd: {e}"

class PokerApp(App):
    def build(self):
        return PokerLayout()

if __name__ == '__main__':
    PokerApp().run()
