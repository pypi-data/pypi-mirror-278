class Quick:
    def quick_sort(arr):
        length = len(arr)
        
        if length <= 1:
             return arr
        else:
            pivot = arr.pop()

        greater = []
        lower = []

        for i in arr:
            if i > pivot:
                greater.append(i)
            else:
                lower.append(i)

        return Quick.quick_sort(lower)+[pivot]+Quick.quick_sort(greater)
    