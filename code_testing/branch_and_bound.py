""" This modules implements longest common subsequence with a branch and bound approach
    Created by Edward Beeching 09/11/2016 """

def find_bounds(list1, list2):
    if len(list1) > len(list2):
        return find_bounds(list2, list1)

    list1_dict = {}
    list2_dict = {}

    # Use a dictionary (Hash table) to map occurances of words
    for word in list1:
        if list1_dict.get(word) == None:
            list1_dict[word] = 1
        else:
            list1_dict[word] += 1

    for word in list2:
        if list2_dict.get(word) == None:
            list2_dict[word] = 1
        else:
            list2_dict[word] += 1

    combined_dict = {}
    for word, value in list1_dict.iteritems():
        if list2_dict.get(word) == None:
            continue
        else:
            combined_dict[word] = min(value, list2_dict[word])

    lower_bound = 0
    upper_bound = 0
    for word, value in combined_dict.iteritems():
        upper_bound += value
        lower_bound = max(lower_bound, value)

    return lower_bound, upper_bound




if __name__ == '__main__':
    print("Branch and Bound Testing")
    lb, ub = find_bounds(["g","a","e","b","c","e","e"],["e","e","f","g","d"])
    file1 = open("../corpus-adv_preprocessed/g0pA_taskb_adv_preprocessed.txt")
    file2 = open("../corpus-adv_preprocessed/orig_taska_adv_preprocessed.txt")

    words1 = file1.read().split()
    words2 = file2.read().split()
    # lb, ub = find_bounds(["g", "a", "e", "b", "c", "e", "e"], ["e", "e", "f", "g", "d"])
    lb, ub = find_bounds(words1, words2)

    print(lb , ub)