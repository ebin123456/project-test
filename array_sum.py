
def get_max_sum_list(input_list): 
    max_now = 0
    sum_now = 0
    for number in input_list: 
        sum_now = sum_now + number
        max_now = max(max_now, sum_now)
        sum_now = max(0, sum_now)  
    return max_now 

if __name__ == '__main__':
    num = [-2,1,-3,4,-1,2,1,-5,4]
    print(get_max_sum_list(num))