#todo 是不是只要两个字符串中字母一样就可以匹配上
# def no_name(a,b):
#     if len(a) != len(b):
#         return False
#     for x in range(0,len(b)):
#         if a[0] == b[x]:
#             return no_name(utilityFunction(a,0),utilityFunction(b,x))
#     return len(b) == 0
#
# def utilityFunction(s,j):
#     ret = ['' for i in range(0,len(s))]
#     d = 0
#     for k in range(0,len(s)):
#         if k == j:
#             d = 1
#         else:
#             ret[k - d ] = s[k]
#     return ''.join(ret)

#Solution 1

# def no_name_new(a,b):
#     if len(a) != len(b):
#         return False
#     if len(a) == 0:
#         return True
#     substring_len,a_start,b_start = longgest_sub_string(a,b)
#     if substring_len == 0:
#         return False
#     a_ = utilityFunctionNew(a,a_start,substring_len)
#     b_ = utilityFunctionNew(b,b_start,substring_len)
#     return no_name_new(a_,b_)
#
#
# def longgest_sub_string(a,b):
#     result = 0
#     a_start = 0
#     b_start = 0
#     table = [[0 for i in range(len(a))] for j in range(len(b))]
#     for i in range(len(a)):
#         for j in range(len(b)):
#             if (i ==0 or j ==0) and a[i] != b[j]:
#                 table[i][j] = 0
#             elif i ==0 or j== 0:
#                 table[i][j] = 1
#                 if result < table[i][j]:
#                     result = table[i][j]
#                     a_start = i
#                     b_start = j
#             elif a[i] == b[j]:
#                 table[i][j] = table[i-1][j-1] + 1
#                 if result < table[i][j]:
#                     result = table[i][j]
#                     a_start = i - result + 1
#                     b_start = j - result + 1
#             else:
#                 pass
#     return result,a_start,b_start
#
# def utilityFunctionNew(s,j,k=1):
#     ret = s[:j] + s[j+k:]
#     return ret

#Solution 2

# def no_name_new(a,b):
#     if len(a) != len(b):
#         return False
#     if len(a) == 0:
#         return True
#     a_sub_match = [0 for _ in range(len(a))]
#     b_sub_match = [0 for _ in range(len(a))]
#     a_sub_label = [0 for _ in range(len(a))]
#     b_sub_label = [0 for _ in range(len(a))]
#     table = [[0 for i in range(len(a))] for j in range(len(b))]
#     for i in range(len(a)):
#         for j in range(len(b)):
#             if (i == 0 or j == 0) and a[i] != b[j]:
#                 table[i][j] = 0
#             elif i == 0 or j == 0:
#                 table[i][j] = 1
#                 a_start = i
#                 b_start = j
#                 a_sub_match[a_start] = table[i][j]
#                 b_sub_match[b_start] = table[i][j]
#             elif a[i] == b[j]:
#                 table[i][j] = table[i - 1][j - 1] + 1
#                 a_start = i - table[i][j] + 1
#                 b_start = j - table[i][j] + 1
#                 a_sub_match[a_start] = table[i][j]
#                 b_sub_match[b_start] = table[i][j]
#             else:
#                 pass
#     for index_a,item_a in enumerate(a_sub_match):
#         for i_ in range(item_a):
#             a_sub_label[index_a + i_] = 1
#     for index_b,item_b in enumerate(a_sub_match):
#         for j_ in range(item_b):
#             b_sub_label[index_b + j_] = 1
#     return not ((0 in a_sub_label) and (0 in b_sub_label))


#Solution3
def no_name_new(a,b):
    a_dict = {}
    b_dict = {}
    for a_ in a:
        if a_ in a_dict:
            a_dict[a_] = a_dict[a_]+1
        else:
            a_dict[a_] = 0
    for b_ in b:
        if b_ in b_dict:
            b_dict[b_] = b_dict[b_] + 1
        else:
            b_dict[b_] = 0
    for key in a_dict:
        if not key in b_dict:
            return False
        if a_dict[key] != b_dict[key]:
            return False
    return True

if __name__ == '__main__':
    a = 'abcdefgabc'
    b = 'fgabcdeabc'
    # a = input("please input a:")
    # b = input("please input b:")
    print(no_name_new(a,b))