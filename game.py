from decision_tree import DecisionTree
from stack import Stack
import stats


class Game:
    def __init__(self):
        self.tree = DecisionTree()
        self.games = []  # длины завершенных партий

    def ask(self, text):
        # читает ответ пользователя, повторяет запрос при неверном вводе
        while True:
            answer = input(text + " (да/нет/назад): ").strip().lower()
            if answer in ("да", "д"):
                return "yes"
            if answer in ("нет", "н"):
                return "no"
            if answer == "назад":
                return "back"
            print("Ответь да, нет или назад.")

    def play(self):
        # управляет одной партией
        history = Stack()
        leaf = self.tree.descend(self.tree.root, history, self.ask)
        while leaf == "back":
            # пользователь вернулся выше корня, начинаем сначала
            leaf = self.tree.descend(self.tree.root, history, self.ask)

        self.games.append(history.size())

        guess = input("Это " + leaf.text + "? (да/нет): ").strip().lower()
        correct = guess in ("да", "д")
        for question_node, answer in history:
            question_node.asked += 1
            if correct:
                question_node.success += 1

        if correct:
            print("Угадал!")
        else:
            # просим назвать животное и отличающий вопрос для обучения
            parent, branch = history.top()
            name = input("Кого ты загадал? ").strip()
            text = input(
                "Задай вопрос, на который для '" + name
                + "' ответ да, а для '" + leaf.text + "' нет: "
            ).strip()
            self.tree.learn(leaf, parent, branch, name, text)
            print("Запомнил.")

    def show_stats(self):
        # сводная статистика
        print("Животных в базе:", self.tree.count_animals(self.tree.root))
        if self.games:
            prefix = stats.build_prefix(self.games)
            total_games = len(self.games)
            print("Средняя длина всех партий:", stats.average_in_range(prefix, 0, total_games))
            last_start = max(0, total_games - 5)
            print("Средняя длина последних партий:", stats.average_in_range(prefix, last_start, total_games))
        print("Самые информативные вопросы (доля успехов):")
        for question_node in self.tree.sorted_questions():
            rate = round(question_node.success_rate(), 2)
            counts = "(" + str(question_node.success) + " из " + str(question_node.asked) + ")"
            print(" ", rate, counts, question_node.text)
