"""
there are two function to return the rank of numbers in an array
if flag == 1:   function transform() returns the ascending order
if flag == 2:   function transform_unreverse() return the descending order
"""

# utils to replace each element of the list by its rank in the list
def transform(arr):
    """
    Returns:
        the ascending order of array

    """
    sorted_list = sorted(arr,reverse=True)
    rank = 1
    sorted_rank_list = [1]
    for i in range(1, len(sorted_list)):
        if sorted_list[i] != sorted_list[i - 1]:
            rank += 1
        sorted_rank_list.append(rank)

    rank_list = []
    # zip utils returns iterator of tuple pairs of matching values in two inputss
    # dict utils casts 1nd value in tuple as key and 2nd value in tuple as value
    item_rank_dict = dict(zip(sorted_list, sorted_rank_list))

    for item in arr:
        item_rank = item_rank_dict[item]
        rank_list.append(item_rank)
    print(rank_list)
    return rank_list

def transform_unreverse(arr):
    """
    Returns:
        the descending order of array

    """
    sorted_list = sorted(arr,reverse=False)
    rank = 1
    sorted_rank_list = [1]
    for i in range(1, len(sorted_list)):
        if sorted_list[i] != sorted_list[i - 1]:
            rank += 1
        sorted_rank_list.append(rank)

    rank_list = []
    # zip utils returns iterator of tuple pairs of matching values in two inputss
    # dict utils casts 1nd value in tuple as key and 2nd value in tuple as value
    item_rank_dict = dict(zip(sorted_list, sorted_rank_list))

    for item in arr:
        item_rank = item_rank_dict[item]
        rank_list.append(item_rank)
    print(rank_list)
    return rank_list

if __name__ == "__main__":
    flag = int(sys.argv(1))
    input_array = [1,4,2,3,5,7]
    if flag == 1:
        transform(input_array)
    elif flag == 2:
        transform_unreverse(input_array)