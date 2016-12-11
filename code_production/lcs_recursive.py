import time

import lcs_branch_and_bound


def lcs_recursive(list1, list2):
    if len(list1) == 0 or len(list2) == 0:
        return []
    m = len(list1) - 1
    n = len(list2) - 1

    if list1[m] == list2[n]:
        return lcs_recursive(list1[:-1], list2[:-1]) + [list1[m]]
    else:
        z1 = lcs_recursive(list1[:-1], list2)
        z2 = lcs_recursive(list1, list2[:-1])
        if len(z1) > len(z2):
            return z1
        else:
            return z2

if __name__ == '__main__':


    start = time.time()
    print("testing")
    end = time.time()
    print(end - start)


    print("Recursive Testing")
    lcs_start = time.time()
    lcs = lcs_recursive(["A","A","Q","C","D","D","A","A","A","D","A","D","E","A","A","C","D"],
                        ["A","F","A","D","A","D","E","A","A","C","D","Q","C","D","A","A","D"])
    print(lcs)
    print("Recursive took", (time.time() - lcs_start))
    bnb_start = time.time()
    lcs2 = lcs_branch_and_bound.branch_n_bound(["A", "A", "Q", "C", "D", "D", "A", "A", "A", "D", "A", "D", "E", "A", "A", "C", "D"],
                                               ["A","F","A","D","A","D","E","A","A","C","D","Q","C","D","A","A","D"])

    print(lcs2)
    print("Bnb took", (time.time() - bnb_start))



