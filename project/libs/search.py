def search(my_list, value):
    for i in range(0, len(my_list)):
        if my_list[i] == value:
            index = i
            break

    return index
