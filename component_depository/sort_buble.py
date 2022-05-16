def sort_buble(sm):
    for i in range(len(sm)):
        for j in range(len(sm)-i-1):
            if sm[j]>sm[j+1]:
                sm[j],sm[j+1]=sm[j+1], sm[j]

if __name__ == '__main__':
    l1 = [0,2,1,8,5,3,2,57,1]
    l2 = [9,19,2,3,4]
    l3 = [1,2,3,4,5]
    print(sort_buble(l1), l1)
    print(sort_buble(l2), l2)
    print(sort_buble(l3), l3)
