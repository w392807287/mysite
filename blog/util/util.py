import numpy as np
import jieba
import hashlib
import re
import farmhash
import jieba.analyse


class SimHash:
    REX_CH = re.compile(u'[\u4e00-\u9fa5]+')  # 中文
    REX_EN = re.compile('[A-Za-z]+')  # 英文
    REX_CH_EN = re.compile(u'\w')    #中文或者英文
    cut_func = jieba.cut

    @classmethod
    def hash2bin(cls, hash):
        d = ''
        for i in hash:
            try:
                if int(i) > 7:
                    d = d + '1'
                else:
                    d = d + '0'
            except ValueError:
                d = d + '1'
        return d

    @classmethod
    def hash_bin(cls, s):
        h = hashlib.md5(s.encode()).hexdigest()
        return cls.hash2bin(h)

    @classmethod
    def hist(cls, cut):
        _cut = {x: 0 for x in set(cut)}
        for i in cut:
            _cut[i] += 1
        return {cls.hash64(k): v / len(cut) for k, v in _cut.items()}

    @classmethod
    def simhash(cls, s, RE=None, cut_func=None):
        if RE:
            REX = RE
        else:
            REX = cls.REX_CH_EN
        if not cut_func:
            cut_func = cls.cut_func

        cut = [x for x in cut_func(s) if re.match(REX, x)]

        ver = [[v * (int(x) if int(x) > 0 else -1) for x in k] for k, v in cls.hist(cut).items()]
        ver = np.array(ver)
        ver_sum = ver.sum(axis=0)
        sim = ''.join(['1' if x > 0 else '0' for x in ver_sum])
        return sim

    @classmethod
    def hash64(cls, s):
        try:
            aa = bin(farmhash.hash64(s))[2:]
            ac = '0' * (64 - len(aa)) + aa
            return ac
        except:
            return None

    @staticmethod
    def haiming(s1, s2):
        x = 0
        for i in zip(s1, s2):
            if i[0] != i[1]:
                x += 1
        return x

