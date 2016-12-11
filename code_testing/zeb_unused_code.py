
def branch_and_bound2(list1, list2):
    if len(list1) > len(list2):
        return branch_and_bound2(list2, list1)
    # explore 2 branches, whether the first index has solution or not
    print("branch and bound 2")
    max_lcs_length = min(len(list1), len(list2)) - 1
    lower, upper = _find_bounds(list1, list2)

    starting_solution = (1 << (max_lcs_length + 1)) - 1
    best_solution = starting_solution * 0

    best_score = max(lower-1, 0)
    # solution_index = -1
    # tracker_index = -1

    _bnb_recursive(list1, list2, starting_solution, -1, -1, 0, max_lcs_length, best_score, best_solution)

    return _get_solution(list1, list2, best_solution)


def _get_solution(list1, list2, best_solution):
    if len(list1) > len(list2):
        return _get_solution(list2, list1, best_solution)

    max_length = len(list1)
    solution = []
    for index, word in enumerate(list1):
        if best_solution & (1 << ((max_length - 1) - index)) > 0:
            solution.append(word)
    return solution


def _bnb_recursive(list1, list2, current_solution, index, tracker, current_score, max_lcs_length, best_score, best_solution):

    global upper1, upper1
    index += 1
    print(index, current_solution)
    # compute bounds of the two options
    # bounds if word at list[index] is kept

    tracker1 = _find_index_of_first(list1[index], tracker + 1, list2)
    score1 = -1
    if tracker1 != 1000000000:
        lower1, upper1 = _find_bounds(list1[index+1:], list2[tracker+1:])
        score1 = current_score + 1 + upper1

    solution2 = current_solution - (1 << (max_lcs_length - index))

    lower2, upper2 = _find_bounds(list1[index+1:], list2[tracker + 1:])
    score2 = current_score + upper2

    if index == max_lcs_length - 1:
        if score1 >= score2:
            best_score = upper1
            best_solution = current_solution
        else:
            best_score = upper2
            best_solution = current_solution
        return

    if score1 >= score2:
        if score1 > best_score:
            _bnb_recursive(list1, list2, current_solution, index, tracker1, score1, max_lcs_length, best_score, best_solution)
        if score2 > best_score:
            _bnb_recursive(list1, list2, solution2, index, tracker, score2, max_lcs_length, best_score, best_solution)
    else:
        if score2 > best_score:
            return _bnb_recursive(list1, list2, solution2, index, tracker, score2, max_lcs_length, best_score, best_solution)
        if score1 > best_score:
            _bnb_recursive(list1, list2, current_solution, index, tracker1, score1, max_lcs_length, best_score, best_solution)


def _find_sub_lcs_length(solution1, index, length):
    total = 0
    for i in range(0, index+1):
        # Bit shift to find if index is in solution
        if solution1 & (1 << (length - i)) > 0:
            total += 1
    return total


def _find_index_of_first(first, start, word_list):
    """
    Finds the first index of a characted/string in a list of strings, if the char does not exist, return 10^9

    :param first:
    :param start:
    :param word_list:
    :return:
    """

    if start > len(word_list)-1:
        return 1000000000
    for index, word in enumerate(word_list[start:]):
        if word == first:
            return start + index
    return 1000000000  # if the word is not found return a very high value
def _find_bounds(list1, list2):
    """
    See intro for details of this function.

    :param list1: The first list of strings to compare
    :param list2: The second list of strings to compare
    :return: returns two integers, the lower and upper bounds
    """
    if len(list1) > len(list2):
        return _find_bounds(list2, list1)

    list1_dict = {}
    list2_dict = {}

    # Use a dictionary (Hash table) to map occurrences of words
    for word in list1:
        if list1_dict.get(word) is None:
            list1_dict[word] = 1
        else:
            list1_dict[word] += 1

    for word in list2:
        if list2_dict.get(word) is None:
            list2_dict[word] = 1
        else:
            list2_dict[word] += 1

    combined_dict = {}
    for word, value in list1_dict.iteritems():
        if list2_dict.get(word) is None:
            continue
        else:
            combined_dict[word] = min(value, list2_dict[word])

    lower_bound = 0
    upper_bound = 0
    for word, value in combined_dict.iteritems():
        upper_bound += value
        lower_bound = max(lower_bound, value)

    return lower_bound, upper_bound
