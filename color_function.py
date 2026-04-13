from statistics import mean
from gensim.models.keyedvectors import KeyedVectors
import pandas as pd

# RGBをカラーコードに変換する関数
def rgb2html(RGB):
    return "#{:02x}{:02x}{:02x}".format(*RGB)

# 無彩色を判定する関数
def is_achromatic(rgb):
    r, g, b = rgb
    return r == g == b or (abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15)


df = pd.read_csv("color_data.csv", encoding='utf-8')

# 説明変数
words_df = df['word'] 
words_li = words_df.tolist()
# 目的変数
rgb = df[['r', 'g', 'b']] 
r = rgb['r'].tolist()
g = rgb['g'].tolist()
b = rgb['b'].tolist()

code = df['colorcode'].tolist()


# rgb値を -1<x<1, -1<y<1, -1<z<1 でベクトル化 
def color_to_vec(color_li):
    r, g, b = 0, 1, 2
    color_vec = [[(color[r]/127.5 - 1), (color[g]/127.5 - 1), (color[b]/127.5 - 1)] for color in color_li]
    return color_vec


# ベクトル化下rgb値をもどす
def color_from_vec(color_vec):
    r, g, b = 0, 1, 2
    # 引数 color_vec を用いてリストを生成
    color_li = [[
        round(((color[r] + 1) * 127.5)), 
        round(((color[g] + 1) * 127.5)), 
        round(((color[b] + 1) * 127.5))
    ] for color in color_vec]
    return color_li

model = KeyedVectors.load_word2vec_format(
    './20170201/entity_vector/entity_vector.model.bin',
    binary=True
)

# 類似単語をリストで返却
def find_sim(input, words_li):
    sim_words = []
    if input in words_li:
        sim_words.append(input)
    
    # 「自然言語処理」と類似する単語を取得
    words = model.most_similar(input, topn=10000)

    for word, _ in words:
        if (word in words_li) and (len(sim_words) < 3):
            sim_words.append(word)

    print(sim_words)

    return sim_words

# 2次元のリストを重複のないリストにして返却
def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

# 類似単語からおすすめの色リストを返す（RGB値とカラーコード）
def reco_color(sim_words):
    color_li = [[r[words_li.index(word)], g[words_li.index(word)], b[words_li.index(word)]] for word in sim_words]
    # print(color_li)

    color_vec = [color_to_vec([color]) for color in color_li]  
    # print(color_vec)

    r_vec = mean(vec[0][0] for vec in color_vec)
    g_vec = mean(vec[0][1] for vec in color_vec)
    b_vec = mean(vec[0][2] for vec in color_vec)

    RGB = color_from_vec([[r_vec, g_vec, b_vec]])[0]
    # print(RGB)
    

    if is_achromatic(RGB) == False:
        color_li.append(RGB)


    color_li = get_unique_list(color_li)

    Hex_li = [rgb2html(row) for row in color_li]

    return color_li, Hex_li 