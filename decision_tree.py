from node import animal, question


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

    def descend(self, node, history, ask):
        # рекурсивный спуск по дереву
        # ask это функция, которая по тексту вопроса возвращает yes, no или back
        # возвращает лист дерева либо строку back, если откатились выше корня
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
        result = self.descend(child, history, ask)
        if result == "back":
            # убираем текущий вопрос из стека и задаем его заново
            history.pop()
            return self.descend(node, history, ask)
        return result

    def count_animals(self, node):
        # подсчет листьев рекурсивным обходом
        if node.is_animal():
            return 1
        return self.count_animals(node.yes) + self.count_animals(node.no)

    def all_questions(self, node):
        # собирает все внутренние узлы для сортировки
        if node.is_animal():
            return []
        return [node] + self.all_questions(node.yes) + self.all_questions(node.no)

    def sorted_questions(self):
        # сортировка выбором по убыванию доли успехов
        questions = self.all_questions(self.root)
        for i in range(len(questions)):
            best = i
            for j in range(i + 1, len(questions)):
                if questions[j].success_rate() > questions[best].success_rate():
                    best = j
            questions[i], questions[best] = questions[best], questions[i]
        return questions

    def learn(self, wrong_animal, parent, branch, name, text):
        # новый вопрос, на который для нового животного ответ да, а для неверного нет
        new_question = question(text, animal(name), wrong_animal)
        if branch == "yes":
            parent.yes = new_question
        else:
            parent.no = new_question
