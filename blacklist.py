# coding=utf-8
blacklistwords = ['whose', 'became', 'nowhere', 'fifty', 'ten', 'did', 'mostly', 'once', 'rather', 'are', 'thereby',
                  'out', 'my', 'together', 'whereupon', 'thus', 'anyhow', 'often', 're', 'someone', 'while', 'become',
                  'being', 'never', 'from', 'which', 'ourselves', 'thereupon', 'via', 'ltd', 'we', 'alone', 'neither',
                  'two', 'elsewhere', 'fill', 'might', 'itself', 'most', 'also', 'such', 'becomes', 'whereas',
                  'between', 'couldnt', 'she', 'has', 'whenever', 'again', 'call', 'everywhere', 'next', 'about',
                  'yours', 'the', 'no', 'throughout', 'none', 'six', 'back', 'behind', 'a', 'formerly', 'besides',
                  'get', 'his', 'their', 'them', 'will', 'any', 'seemed', 'below', 'although', 'do', 'by', 'because',
                  'serious', 'show', 'wherein', 'yourself', 'becoming', 'too', 'last', 'some', 'since', 'latter',
                  'done', 'further', 's', 'sometimes', 'thence', 'hasnt', 'inc', 'third', 'anywhere', 'now', 'sometime',
                  'every', 'at', 'seeming', 'am', 'beforehand', 'here', 'be', 'top', 'eg', 'could', 'whither', 'mine',
                  'bill', 'describe', 'its', 'etc', 'take', 'twelve', 'herself', 'if', 'latterly', 'move', 'though',
                  'whoever', 'up', 'anyway', 'very', 'must', 'themselves', 'namely', 'well', 'else', 'hereafter',
                  'mill', 'almost', 'fifteen', 'five', 'hereupon', 'one', 'three', 'fire', 'due', 'there', 'otherwise',
                  'i', 'per', 'ours', 'beside', 'past', 'ever', 'towards', 'me', 'nor', 'several', 'why', 'what',
                  'hundred', 'whatever', 'cant', 'former', 'our', 'nevertheless', 'hers', 'put', 'would', 'across',
                  'moreover', 'somewhere', 'before', 'full', 'everything', 'as', 'thereafter', 'can', 'herein', 'those',
                  'whereby', 'to', 'us', 'without', 'co', 'much', 'among', 'found', 'is', 'enough', 'whether', 'along',
                  'upon', 'only', 'seems', 'either', 'all', 'something', 'indeed', 'bottom', 'see', 'within', 'many',
                  'cannot', 'into', 'therein', 'first', 'eight', 'four', 'ie', 'toward', 'anyone', 'may', 'who',
                  'meanwhile', 'was', 'whom', 'same', 'but', 'already', 'except', 'nothing', 'during', 'over', 'cry',
                  'whence', 'least', 'computer', 'through', 'hereby', 'hence', 'or', 'other', 'whole', 'him',
                  'anything', 'been', 'himself', 'less', 'with', 'where', 'more', 'noone', 'side', 'give', 'seem', 'he',
                  'whereafter', 'you', 'your', 'twenty', 'under', 'each', 'find', 'beyond', 'yourselves', 'few', 'her',
                  'both', 'con', 'part', 'on', 'ago', 'for', 'have', 'thin', 'till', 'keep', 'always', 'against',
                  'when', 'not', 'it', 'nine', 'yet', 'please', 'so', 'they', 'un', 'empty', 'than', 'others', 'front',
                  'how', 'these', 'in', 'then', 'thru', 'nobody', 'even', 'perhaps', 'thick', 'detail', 'eleven',
                  'this', 'made', 'of', 'myself', 'that', 'had', 'onto', 'name', 'wherever', 'forty', 'go', 'sincere',
                  'everyone', 'down', 'system', 'off', 'own', 'should', 'still', 'sixty', 'were', 'around', 'de',
                  'however', 'interest', 'until', 'somehow', 'therefore', 'above', 'and']


def get_blacklist():
    """
    Return black listed words
    :return: blacklistwords
    """
    return blacklistwords
