class Insertion:
    def insertion_sort(arr):
        for i in range (1, len(arr)):
            key = arr[i]

            while arr[i-1] > key and i>0:
                arr[i], arr[i-1] = arr[i-1], arr[1]
                i = i-1
            
            return arr