k = int(input())
def zero(nums):
    nums.remove(0)
    result = 1
    for i in nums:
        result *= i
    print(result)

def not_zero(nums):
    result = min(nums) + 1
    nums.remove(min(nums))
    for i in nums:
        result *= i
    print(result)

for _ in range(k):
    n = int(input())
    nums = list(map(int, (input().split())))
    if 0 in nums:
        zero(nums)
    else:
        not_zero(nums)