from jieba import posseg
import math


def cos_similarity(str1, str2):
    cut_str1 = [w for w, t in posseg.lcut(str1) if 'n' in t or 'v' in t]
    cut_str2 = [w for w, t in posseg.lcut(str2) if 'n' in t or 'v' in t]

    all_words = set(cut_str1 + cut_str2)

    freq_str1 = [cut_str1.count(x) for x in all_words]
    freq_str2 = [cut_str2.count(x) for x in all_words]

    sum_all = sum(map(lambda z, y: z * y, freq_str1, freq_str2))
    sqrt_str1 = math.sqrt(sum(x ** 2 for x in freq_str1))
    sqrt_str2 = math.sqrt(sum(x ** 2 for x in freq_str2))
    return sum_all / (sqrt_str1 * sqrt_str2)
