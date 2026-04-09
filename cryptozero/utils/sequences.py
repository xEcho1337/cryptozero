def find_repeating_subsequences(stream):
    """
    Find the most common repeating subsequences (ngrams) in a stream.

    Credits: https://stackoverflow.com/questions/69170602/how-do-i-find-repeating-sequences-in-a-list

    :param stream: iterable of values
    :return: list of (subsequence, count) or None if no repetition
    """
    results = []

    for size in range(5, 1, -1):
        if len(stream) < size:
            results.append(None)
            continue

        subsequences = (
            tuple(stream[i:i + size])
            for i in range(len(stream) - size + 1)
        )

        counter = Counter(subsequences)
        most_common = counter.most_common(1)

        if most_common and most_common[0][1] > 1:
            results.append(most_common[0])
        else:
            results.append(None)

    return results


def find_repeating_length(stream, min_size=2, max_size=5):
    n = len(stream)

    for size in range(max_size, min_size - 1, -1):
        if n < size:
            continue

        subsequences = (
            tuple(stream[i:i + size])
            for i in range(n - size + 1)
        )

        counter = Counter(subsequences)
        most_common = counter.most_common(1)

        if most_common and most_common[0][1] > 1:
            return most_common[0][1]

    return None
