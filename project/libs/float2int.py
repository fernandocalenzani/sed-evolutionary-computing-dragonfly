def float2Int(x_float):
    x_int = []
    x_int.clear()

    for i in range(0, len(x_float[0][:])):
        if x_float[0][i] == 1:
            x_int.insert(i, 1)
        else:
            x_int.insert(i, 0)

    return x_int
