def range_sum(start,end):
    sum_res = 0
    for i in range(start,end):
        sum_res+=i
    return sum_res

if __name__ =="__main__":
    print(range_sum(1,10))