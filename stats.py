# префиксные суммы для анализа средней глубины партий


def build_prefix(games):
    # строит массив накопленных сумм длин партий
    prefix = [0]
    for length in games:
        prefix.append(prefix[-1] + length)
    return prefix


def average_in_range(prefix, start, end):
    # средняя длина за диапазон партий за O(1)
    total = prefix[end] - prefix[start]
    return total / (end - start)
