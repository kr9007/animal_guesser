# Узел дерева. Листья хранят имя животного, внутренние узлы хранят вопрос
class Node:
    def __init__(self, text):
        self.text = text
        self.yes = None
        self.no = None
        self.asked = 0    # сколько раз вопрос задавался
        self.success = 0  # сколько раз после него угадали

    def is_animal(self):
        return self.yes is None

    def success_rate(self):
        if self.asked == 0:
            return 0
        return self.success / self.asked


def animal(name):
    return Node(name)


# Создает внутренний узел с двумя ветками
def question(text, yes, no):
    node = Node(text)
    node.yes = yes
    node.no = no
    return node


# Стек для истории вопросов текущей игры
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

    def is_empty(self):
        return len(self.items) == 0


class DecisionTree:
    def __init__(self):
        self.root = question(
            "Это млекопитающее?",
            question(
                "Оно живет в доме?",
                question("Оно лает?", animal("собака"), animal("кошка")),
                question("Оно больше человека?", animal("слон"), animal("заяц")),
            ),
            question(
                "Оно умеет летать?",
                question("Оно хищник?", animal("орел"), animal("воробей")),
                question("Оно живет в воде?", animal("акула"), animal("змея")),
            ),
        )

    def descend(self, node, history):
        # Рекурсивный спуск по дереву. Возвращает лист или "back"
        if node.is_animal():
            return node
        answer = ask(node.text)
        if answer == "back":
            return "back"
        history.push((node, answer))
        if answer == "yes":
            child = node.yes
        else:
            child = node.no
        result = self.descend(child, history)
        if result == "back":
            # убираем текущий вопрос из стека и задаем его заново
            history.pop()
            return self.descend(node, history)
        return result

    # Подсчет листьев рекурсивным обходом
    def count_animals(self, node):
        if node.is_animal():
            return 1
        return self.count_animals(node.yes) + self.count_animals(node.no)

    # Собирает все внутренние узлы для сортировки
    def all_questions(self, node):
        if node.is_animal():
            return []
        return [node] + self.all_questions(node.yes) + self.all_questions(node.no)

    # Сортировка выбором по убыванию доли успехов
    def sorted_questions(self):
        questions = self.all_questions(self.root)
        for i in range(len(questions)):
            best = i
            for j in range(i + 1, len(questions)):
                if questions[j].success_rate() > questions[best].success_rate():
                    best = j
            questions[i], questions[best] = questions[best], questions[i]
        return questions

    def learn(self, wrong_animal, parent, branch, name, text):
        # Новый вопрос. Новое животное - да, неверное - нет
        new_question = question(text, animal(name), wrong_animal)
        if branch == "yes":
            parent.yes = new_question
        else:
            parent.no = new_question


tree = DecisionTree()
games = []  # длины партий для префиксных сумм


# Префиксные суммы для подсчета средней глубины партий

def build_prefix(games):
    prefix = [0]
    for length in games:
        prefix.append(prefix[-1] + length)
    return prefix


def average_in_range(prefix, start, end):
    # Среднее за диапазон партий за O(1)
    total = prefix[end] - prefix[start]
    return total / (end - start)


# Читает ответ пользователя, повторяет запрос при неверном вводе
def ask(text):
    while True:
        answer = input(text + " (да/нет/назад): ").strip().lower()
        if answer in ("да", "д"):
            return "yes"
        if answer in ("нет", "н"):
            return "no"
        if answer == "назад":
            return "back"
        print("Ответь да, нет или назад.")


def play():
    history = Stack()
    leaf = tree.descend(tree.root, history)
    while leaf == "back":
        # пользователь вернулся дальше корня, начинаем сначала
        leaf = tree.descend(tree.root, history)

    games.append(history.size())

    guess = input("Это " + leaf.text + "? (да/нет): ").strip().lower()
    correct = guess in ("да", "д")
    for question_node, answer in history.items:
        question_node.asked += 1
        if correct:
            question_node.success += 1

    if correct:
        print("Угадал!")
    else:
        # просим назвать животное и отличающий вопрос для обучения
        parent, branch = history.top()
        name = input("Кого ты загадал? ").strip()
        text = input("Задай вопрос, на который для '" + name + "' ответ да, а для '" + leaf.text + "' нет: ").strip()
        tree.learn(leaf, parent, branch, name, text)


def show_stats():
    print("Животных в базе:", tree.count_animals(tree.root))
    if games:
        prefix = build_prefix(games)
        total_games = len(games)
        print("Средняя длина всех партий:", average_in_range(prefix, 0, total_games))
        last_start = max(0, total_games - 5)
        print("Средняя длина последних партий:", average_in_range(prefix, last_start, total_games))
    print("Самые информативные вопросы (доля успехов):")
    for question_node in tree.sorted_questions():
        rate = round(question_node.success_rate(), 2)
        counts = "(" + str(question_node.success) + " из " + str(question_node.asked) + ")"
        print(" ", rate, counts, question_node.text)


while True:
    choice = input("\n1 играть, 2 статистика, 3 выход: ").strip()
    if choice == "1":
        play()
    elif choice == "2":
        show_stats()
    elif choice == "3":
        break
