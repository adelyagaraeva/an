def elem_before(line, x, left, right):
    if x < line[left]:
        return left - 1
    if x > line[right]:
        return right
    while left < right:
        med = (left + right + 1)//2
        if line[med] > x:
            right = med - 1
        else:
            left = med
    return left

n, length = map(int, input().split())
line = []
for i in range(n):
    x1, d1, a, c, m = map(int, input().split())
    x_prev = x1
    d_prev = d1
    line.append(x1)
    for j in range(1, length):
        x_prev += d_prev
        d_prev = (d_prev*a + c)%m
        line.append(x_prev)
for i in range(n - 1):
    for j in range(i + 1, n):
        left = min(line[i * length], line[j * length])
        right = max(line[(i + 1) * length - 1], line[(j + 1) * length - 1])
        while left < right:
            med = (left + right) // 2
            num_prev = elem_before(line, med, i * length, (i + 1) * length - 1) - i * length + elem_before(line, med, j * length,
                                                                                            (j + 1) * length - 1) - j * length + 2
            if num_prev < length:
                left = med + 1
            else:
                right = med
        print(left)