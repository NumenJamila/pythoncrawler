import nltk
import jieba.analyse

# from . import bigram_tagger, cfg
from .commonutils import stringNotContainsChinese
from nltk.corpus import brown


brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
     ])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)

cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"

class NPExtractor(object):
    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        matches = []
        for t in tags:
            if t[1] == "NNP" or t[1] == "NNI":
                # if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
        return matches

    @staticmethod
    def extractKeywords(sentence: str, top=3, filterwords=None) -> set:
        """
        提取一段不包含中文字符串的关键词，返回前 top 个词
        filterwords 为过滤词，通过 nltk 提取的关键词中如果
        含有过滤词，则不返回这个词
        :type top: int
        """
        np_extractor = NPExtractor(sentence)
        result = np_extractor.extract()  # result 为 list集合
        keywords = set()
        number = 0

        for word in result:
            if number > top:
                break
            if filterwords:
                isAdd = True
                for filterword in filterwords:
                    if str(word).find(filterword) == -1:
                        isAdd = False
                        break
                if isAdd:
                    keywords.add(word)
                    number += 1
            else:
                keywords.add(word)
                number += 1
        return keywords


def extractTagFiles(tagkeyword: dict, info_dict: dict, filterwords=None):
    """
    提取 会议 Tag 字段算法
    :param tagkeyword: 关键词映射，关键词 → Tag
    :param info_dict: 会议信息字典
    :param filterwords: 会议 Tag 过滤词
    """
    tagString = info_dict.get("tag")
    if tagString is None:
        # 会议信息未归类尝试获取会议中文名
        conferenceName = info_dict.get("cnName")
        # 没有中文名测试获取英文名
        if conferenceName is None:
            conferenceName = info_dict.get("enName")

        # 会议名称不为None
        if conferenceName is not None:
            isFind = False
            # 检查会议名称是否包含关键词集中某个关键词，
            # 如果包含可以根据这个关键词对会议进行归类
            # 如果不包含关键词集中的任一关键词则判断会议名称是中文还是英文
            # 如果是中文采用结巴分词进行关键词提取
            # 如果是英文则采用NLTK生成关键词
            for k, v in tagkeyword.items():
                if str(conferenceName).find(k) != -1:
                    isFind = True
                    info_dict["tag"] = v
                    break
            if not isFind:
                # 会议名称为英文
                if stringNotContainsChinese(conferenceName):
                    keywords = NPExtractor.extractKeywords(conferenceName, filterwords=filterwords)
                    info_dict["tag"] = ",".join(keywords)
                else:
                    jieba.analyse.set_stop_words(r"setconfig/crawler/stop_words.txt")
                    keywords = jieba.analyse.extract_tags(conferenceName, 5)
                    info_dict["tag"] = ",".join(keywords)
