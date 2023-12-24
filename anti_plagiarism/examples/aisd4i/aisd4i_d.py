
def med_search(lst1, lst2, L):
    l, r = 0, L
    half = L
    while l <= r:
        i = (l + r) // 2
        j = (2 * L + 1) // 2 - i

        if (i < L and j > 0 and lst2[j - 1] > lst1[i]):
            l = i + 1

        elif (i > 0 and j < L and lst2[j] < lst1[i - 1]):
            r = i - 1
        else:
            if (i == 0):
                return lst2[j - 1]

            if (j == 0):
                return lst1[i - 1]
            else:
                return max(lst1[i - 1], lst2[j - 1])


def generate_array(x1, d1, a, c, m, l):
    d = [0] * l
    d[0] = d1
    x = [0] * l
    x[0] = x1
    for i in range(1, l):
        d[i] = (d[i - 1] * a + c) % m
    for i in range(1, l):
        x[i] = x[i - 1] + d[i - 1]
    # print(x)
    return x
"""aaaa"""

n, k = input().split()
n = int(n)
k = int(k)
all_lists = []
for i in range(n):
    lst = [int(j) for j in input().split()]
    lst1 = generate_array(lst[0], lst[1], lst[2], lst[3], lst[4], k)
    all_lists.append(lst1)

for i in range(n):
    lst1 = all_lists[i]
    for j in range(i + 1, n):
        lst2 = all_lists[j]
        print(med_search(lst1, lst2, k))
