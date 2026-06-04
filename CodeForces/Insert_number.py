k = int(input())
for _ in range(k):
    pair = input().split()
    n = int(pair[0]) # длина числа
    d = int(pair[1]) # дополнительная цифра
    nums = list(map(int, list(input())))
    
    done = False

    for num in nums:
        if num < d:
            ind = nums.index(num)
            nums.insert(ind, d)
            done = True
            break
        
    if not done:
        nums.append(d)

    print(int(''.join(map(str, nums))))