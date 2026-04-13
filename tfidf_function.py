from sklearn.feature_extraction.text import TfidfVectorizer
import MeCab
import re

# 形態素解析
def Morphological_analysis(row):
    # 名詞・動詞・形容詞のストップワードリスト
    stop_words = [
        # 名詞
        'こと', 'もの','とき', '時', '場合', 'ところ', 'よう', 'これ', 'それ', 'あれ', 'どれ', 'ここ', 'そこ', 'あそこ', 'ため', 'つい', 'わけ', 'TED', 'TEDx', 'TEDxAustin', 'TEDTalks', 'StoryCorpsTEDPrize', 'TEDPrize', 'ただ', 'あて', 'なら', 'すべて', 'うち', 'もと', 'なきゃ', 'みんな', '理由', '自分', '自身', '今', 'いま', '一', '十', '百', '千', '二', '三', '四', '五', '六', '七', '八', '九', '方法', 'D', '法', '事', '何', 'あと', '全て', 'まま', '話', 'なし', 'vs',
        # 動詞
        'する', 'ある', 'いる', 'なる', 'できる', '行う', '思う', '見える', '分かる', 'ない', 'なき', 'なく', 'しよう', '無い', 'し', 'くれる', 'いう', 'さ', 'やっ', 'でき', 'もらう', '見え', 'つけろ', 'みよう', 'い', 'なかろう', 'やり', 'す', '出', 'いけ', 'もっ', '対する', 'よっ', 'とっ', 'なれる', 'なさい', 'やめ', 
        # 形容詞
        'よい', '悪い', '大きい', '小さい', 'すごい', '少ない', '多い', 'いい', '良い'
    ]

    wakati = MeCab.Tagger()

    # 正規表現で不要な文字を削除
    row = re.sub(r'[0-9０-９]+', '', row)
    row = re.sub(r'[!"#$%&\'\\\\()*+,-./:;<=>?@\[\\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]', '', row)

    nodes = wakati.parseToNode(row)
    words = []

    while nodes:
        word = nodes.surface  # 単語
        pos = nodes.feature.split(',')[0]  # 品詞

        # 名詞、動詞、形容詞かつストップワードではない単語のみ抽出
        # if pos in ['名詞', '動詞', '形容詞'] and word not in stop_words:
        
        # 名詞、形容詞かつストップワードではない単語のみ抽出
        if pos in ['名詞', '形容詞'] and word not in stop_words + words:
            words.append(word)
        nodes = nodes.next
    print(words)
    if len(words) > 1:
        return words
    else:
        return ['もう少し長い文章を入力してください。']

# TFIDF 重要語抽出
def extract_important_words(corpus):
    vectorizer = TfidfVectorizer(analyzer=lambda x: x)  # 単語のリストをそのまま渡す
    X_vec = vectorizer.fit_transform(corpus)

    # 各文の重要語を抽出
    feature_names = vectorizer.get_feature_names_out()

    sorted_indices = X_vec[len(corpus)-1].toarray().argsort()[0, -2:][::-1]  # スコア上位2語を抽出
    important_words = [feature_names[idx] for idx in sorted_indices]

    return important_words