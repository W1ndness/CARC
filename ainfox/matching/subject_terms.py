from nltk.corpus import wordnet as wn
import jieba.analyse


def path_similarity(a, b, threshold=0.8):
    a_extracted = jieba.analyse.extract_tags(a)
    b_extracted = jieba.analyse.extract_tags(b)


if __name__ == '__main__':
    a = wn.synsets("兴趣", lang='cmn')
    b = wn.synsets("方向", lang='cmn')
    print(a)
    print(b)
    for i in a:
        for j in b:
            print(j.wup_similarity(i))
            print(j.lowest_common_hypernyms(i))