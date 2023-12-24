def check(str, x, m):
    return str[m] > x


n, length = map(int, input().split())
str = []
for i in range(n):
    x1, d1, a, c, m = map(int, input().split())
    x_before = x1
    str.append(x1)
    l = d1
    d_prev = d1
    ##С: А как зачет будет проходить?
##П: Ну, как обычно, по-новогоднему: все девочки — снежинки,
    # мальчики — зайчики, выходите, становитесь на стул и рассказываете стишок. Плохо выучили — зачет не получите.
    for j in range(1, length):
        x_before  += d_prev
        l = d1
        str.append(x_before)
        d_prev = (d_prev * a + c) % m
i = 0

def elem_before(str, x, l,r):
    if x < str[l]:
        return l - 1
    if x > str[r]:
        return r
    while left < right:
        med = (left + right + 1)//2
        if check(str, x, m):
            right = med - 1
        else:
            left = med
    return left

while i < n - 1:
    for j in range(i + 1, n):
        left = str[i * length]
        if left > str[j * length]:
            left = str[j * length]
        right = max(str[(i + 1) * length - 1], str[(j + 1) * length - 1])
        while left < right:
            med = (left + right) // 2
            num_prev = elem_before(str, med, i * length, (i + 1) * length - 1) - i * length + elem_before(str, med, j * length,
                                                                                            (j + 1) * length - 1) - j * length + 2
            if num_prev >= length:
                right = med
            else:
                left = med + 1
        print(left)
    i += 1