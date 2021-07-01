# coding=utf-8

# 冒泡排序
def bubble_sort(alist):
    for j in range(len(alist) - 1):
        for i in range(0, len(alist) - 1 - j):
            if alist[i] > alist[i + 1]:
                # 交换元素
                alist[i], alist[i + 1] = alist[i + 1], alist[i];


# 选择排序
def select_sort(alist):
    for i in range(len(alist) - 1):
        j = i + 1;
        for j in range(len(alist)):
            if alist[j] > alist[i]:
                # 交换元素
                alist[j], alist[i] = alist[i], alist[j];


# 插入排序
def insert_sort(alist):
    for i in range(1, len(alist)):
        for j in range(i, 0, -1):
            if alist[j] < alist[j - 1]:
                alist[j], alist[j - 1] = alist[j - 1], alist[j];


# 希尔排序
def shell_sort(alist):
    # 这里要用双斜杠
    gap = len(alist) // 2;
    while gap >= 1:
        for j in range(gap, len(alist)):
            i = j;
            while (i - gap) >= 0 and (alist[i] < alist[i - gap]):
                alist[i], alist[i - gap] = alist[i - gap], alist[i];
                i -= gap;
        gap //= 2;


# 快速排序
def fast_sort(array, left, right):
    if left >= right:
        return;
    low = left;
    high = right;
    key = array[low];
    while left < right:
        while left < right and array[right] > key:
            right -= 1;
        array[left] = array[right];
        while left < right and array[left] <= key:
            left += 1;
        array[right] = array[left];
    array[right] = key;
    fast_sort(array, low, left - 1);
    fast_sort(array, left + 1, high);

# 快速排序第二种写法
# 这个版本跟上个版本的不同在于分片过程不同,只用了一层循环,并且一趟就完成分片,相比之下代码要简洁的多了
def quick_sort(array, l, r):
    if l < r:
        q = partition(array, l, r)
        quick_sort(array, l, q - 1)
        quick_sort(array, q + 1, r)

def partition(array, l, r):
    x = array[r];
    i = l - 1;
    for j in range(l, r):
        if array[j] <= x:
            i += 1;
            array[i], array[j] = array[j], array[i];
    array[i + 1], array[r] = array[r], array[i+1];
    return i + 1;

# 主函数必须写在函数后面,否则无法调用
if __name__ == '__main__':
    alist = [54, 26, 93, 77, 44, 31, 44, 55, 20];
    print("原列表为：%s" % alist);
    # bubble_sort(alist);
    # select_sort(alist);
    # insert_sort(alist);
    # shell_sort(alist);
    # fast_sort(alist, 0, len(alist) - 1);
    quick_sort(alist, 0, len(alist) - 1);
    print("新列表为：%s" % alist);
