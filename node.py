# узел дерева решений
# лист хранит имя животного, внутренний узел хранит вопрос


class Node:
    def __init__(self, text):
        self.text = text
        self.yes = None
        self.no = None
        self.asked = 0    # сколько раз вопрос задавался
        self.success = 0  # сколько раз после него угадали

    def is_animal(self):
        # лист не имеет потомков
        return self.yes is None

    def success_rate(self):
        if self.asked == 0:
            return 0
        return self.success / self.asked


def animal(name):
    # создает лист с названием животного
    return Node(name)


def question(text, yes, no):
    # создает внутренний узел с двумя ветками
    node = Node(text)
    node.yes = yes
    node.no = no
    return node
