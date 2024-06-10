import string


# IC
def Index_of_Coincidence(content: str, table: str):
    content = ''.join([i for i in content.lower() if i in table])
    # 统计频度(次数)
    f = [content.count(i) for i in table]
    n = len(content)
    IC = sum([f[i] * (f[i] - 1) for i in range(len(table))]) / (n * (n - 1))
    return IC


# 常规MIC计算
def Mutual_Index_of_Coincidence(content1: str, content2: str, table: str):
    # 预处理-只要（小写）字母
    content1 = ''.join([i for i in content1.lower() if i in table])
    content2 = ''.join([i for i in content2.lower() if i in table])
    # 统计频度(次数)
    f1 = [content1.count(i) for i in table]
    f2 = [content2.count(i) for i in table]
    n1 = len(content1)
    n2 = len(content2)
    MIC = sum([f1[i] * f2[i] for i in range(len(table))]) / (n1 * n2)
    return MIC


# 与字频统计规律进行MIC运算
def MIC_natural(content: str, table: str):
    # 各字母频率
    p = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06996, 0.00153, 0.00772, 0.04025,
         0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.0236, 0.0015,
         0.01974, 0.00074]
    content = ''.join([i for i in content.lower() if i in table])
    f = [content.count(i) for i in table]
    n = len(content)
    MIC = sum([p[i] * f[i] for i in range(len(table))]) / n
    return MIC


def mean(list1):
    return sum(list1) / len(list1)


def getd(enc: str, d_len_max: int, table: str):
    """
    :param enc: vigenere密文
    :param d_len_max: 密钥最大可能长度
    :return: d
    """
    d_IC = {}  # 存放d与对应分组下的IC值
    enc = ''.join([i for i in enc.lower() if i in table])  # 对enc预处理，只关注(小写)字母
    for d in range(1, d_len_max + 1):
        ICs = []
        for x in range(d):  # 按照d进行分组，求同一个ki加密的内容的IC
            tmp = [i for i in range(len(enc)) if i % d == x]
            tmp = ''.join([enc[i] for i in tmp])
            ICs.append(round(Index_of_Coincidence(tmp, table), 5))
        d_IC[d] = ICs

    # 最大筛选
    MAX_MEAN = 0
    real_d = 0
    for d in d_IC.keys():
        tmp_mean = mean(d_IC[d])
        if tmp_mean > MAX_MEAN:
            MAX_MEAN = tmp_mean
            real_d = d

    return real_d


def caesar_enc(m, g, table):
    return ''.join([table[(table.index(char) + g) % len(table)] for char in m])


# 方法二：利用真实有效的自然明文，然后与Yj计算MIC，逐一确定kj
def findkey(enc: str, d: int, table) -> str:
    enc = ''.join([i for i in enc.lower() if i in table])  # 对enc预处理，只关注(小写)字母
    natural_message = """
            Man ages all too easily, but not nature;
            The Double Ninth comes every year.
            And on this Double Ninth
            Yellow chrysanthemums on the battlefield smell exceedingly sweet.
            Every year autumn winds blow hard.
            Autumn scenery is wholly unlike spring
            And yet better:
            See the frosty sky and freezing water stretching endlessly far.
            """
    Y_ = ''.join([i for i in natural_message.lower() if i in table])
    Ys = []
    for x in range(d):  # 按照d进行分组
        tmp = [i for i in range(len(enc)) if i % d == x]
        tmp = ''.join(enc[i] for i in tmp)
        Ys.append(tmp)
    key = []

    # 用最大MIC，而非最接近0.065
    for j in range(len(Ys)):
        MAX_MIC = 0
        guess_ki = 0
        for g in range(len(table)):
            """
            对于实际的语句进行统计
            """
            tmp_MIC = Mutual_Index_of_Coincidence(Y_, caesar_enc(Ys[j], g, table), table)

            """
            利用业界总结的字母统计频率
            缺点: 换表了不好使
            """
            # tmp_MIC = MIC_natural(caesar_enc(Ys[j], g, table), table)

            if tmp_MIC > MAX_MIC:
                MAX_MIC = tmp_MIC
                guess_ki = -g % len(table)
        key.append(guess_ki)
    key = ''.join(table[i] for i in key)
    return key


# 维吉尼亚攻击
def attack(enc: str, key_len_max: int = 10, table: str = string.ascii_lowercase) -> str:
    """
    :param enc: 密文
    :param d_len_max: 密钥最大长度
    :return: 明文
    """
    d_len_max = key_len_max
    d = getd(enc, d_len_max, table)  # 密钥长度
    key = findkey(enc, d, table)
    message = VigenereDec(enc, key, table)
    print(f'{key = }')
    return message


# 维吉尼亚加密
def VigenereEnc(message: str, key: str, table: str = string.ascii_lowercase) -> str:
    message = [table.index(i) for i in message.lower() if i in table]
    key = [table.index(i) for i in key.lower() if i in table]
    d = len(key)
    enc = [table[(message[i] + key[i % d]) % len(table)] for i in range(len(message))]
    return ''.join(enc)


# 维吉尼亚解密
def VigenereDec(enc: str, key: str, table: str = string.ascii_lowercase) -> str:
    enc = [table.index(i) for i in enc.lower() if i in table]
    key = [table.index(i) for i in key.lower() if i in table]
    d = len(key)
    message = [table[(enc[i] - key[i % d]) % len(table)] for i in range(len(enc))]
    return ''.join(message)