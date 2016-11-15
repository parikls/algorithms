def switch_vairables(list_: list, i: int, j: int):
    list_[i] ^= list_[j]
    list_[j] ^= list_[i]
    list_[i] ^= list_[j]


def bubble_sort(list_: list) -> list:

    end_index = len(list_)
    while end_index > 0:
        for i in range(end_index - 1):
            if list_[i] > list_[i+1]:
                switch_vairables(list_, i, i+1)
        end_index -= 1

    return list_


def shaker_sort(list_: list) -> list:
    start_index = 0
    end_index = len(list_)

    while start_index < end_index:
        for i in range(start_index, end_index-1):
            if list_[i] > list_[i+1]:
                switch_vairables(list_, i, i+1)

        for i in range(end_index-1, start_index, -1):
            if list_[i] < list_[i-1]:
                switch_vairables(list_, i, i-1)

        start_index += 1
        end_index -= 1

    return list_


def insertion_sort(list_):
    # start from 1 index, because item under 0 index treated as `sorted`
    for i in range(1, len(list_)):
        current_pos = i
        current_value = list_[i]
        while current_pos > 0 and list_[current_pos-1] > current_value:
            switch_vairables(list_, current_pos, current_pos-1)
            current_pos -= 1

    return list_


def merge_sort(list_):

    def merge(left, right):
        merged_and_sorted = []
        while left and right:
            if left[0] <= right[0]:
                merged_and_sorted.append(left.pop(0))
            else:
                merged_and_sorted.append(right.pop(0))
        merged_and_sorted += left + right
        return merged_and_sorted

    if len(list_) == 1:
        return list_

    left, right = list_[:len(list_)//2], list_[len(list_)//2:]

    return merge(merge_sort(left), merge_sort(right))
