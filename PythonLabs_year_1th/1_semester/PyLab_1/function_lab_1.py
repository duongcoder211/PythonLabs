# Функция, которую будем тестировать
def searchTarget(arr, tag):
    for i in range(0, len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == tag:
                return [i, j]
    return None





