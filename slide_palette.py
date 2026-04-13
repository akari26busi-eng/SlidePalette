import streamlit as st
import color_function
import tfidf_function
import csv
from PIL import Image

# 画像ファイルの読み込み
loco_img = Image.open('logo.png')
icon_img = Image.open('icon.png')

# 設定
st.set_page_config(
    page_title="slide pallet",  # サイトのタイトル
    page_icon=icon_img,  # タブのアイコン
    layout="centered",
    initial_sidebar_state="collapsed"
)

# use_container_width 実際のレイアウトの横幅に合わせるか
st.image(loco_img, use_container_width=True)

st.write("スライドの内容を入力すると、適当な配色を提案します!  ")

# スライド内容の入力
input_text = st.text_area("スライドの内容を入力してください", placeholder="例: 環境問題について考えるスライド...")

# 配色提案ボタン
if st.button("配色を提案する"):
    if input_text.strip() == "":
        st.warning("スライド内容を入力してください。")
    else:
        # 入力テキストを形態素解析し、重要語を抽出
        processed_word = tfidf_function.Morphological_analysis(input_text)

        if len(processed_word) < 2:
            st.warning("もう少し長い文章を入力してください。")
        else:
            important_words = tfidf_function.extract_important_words([processed_word])

            # 重要語の表示
            if important_words:
                st.write("---")
                st.write("### 抽出された重要語")
                st.write(", ".join(important_words))
                st.write("---")


                # 重要語ごとに類似単語と配色を提案
                for i, word in enumerate(important_words, 1):
                    # 類似単語を取得して色を提案
                    similar_words = color_function.find_sim(word, color_function.words_li)
                    similar_words = color_function.get_unique_list(similar_words)

                    if similar_words:
                        # 提案された色を取得
                        rgb_colors, hex_colors = color_function.reco_color(similar_words)

                        # 色提案結果の表示
                        st.write(f"#### {word}")
                        color_columns = st.columns(len(hex_colors))
                        for col, hex_color in zip(color_columns, hex_colors):
                            with col:
                                st.markdown(f'<div style="width: 100px; height: 50px; background-color: {hex_color};"></div>', unsafe_allow_html=True)
                                st.write(hex_color)
                    else:
                        st.warning(f"{word} に関連する色が見つかりませんでした。")
            else:
                st.error("重要な単語を抽出できませんでした。")

# CSS

# 配色提案ボタンを中央揃えにする
button_style = """
    <style>
    div.stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

custom_css = """
<style>
/* 全体のフォントをRobotoに変更 */
body {
    font-family: 'BIZ UDP明朝 Medium';
}

/* タイトル用のカスタムフォント */
h1 {
    font-family: 'BIZ UDP明朝 Medium';
}
</style>
"""

# カスタムCSSをStreamlitに適用
st.markdown(custom_css, unsafe_allow_html=True)

# 上のスペースを隠す
HIDE_ST_STYLE = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
			        .appview-container .main .block-container{
                            padding-top: 1rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 1rem;
                        }  
                        .reportview-container {
                            padding-top: 0rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 0rem;
                        }
                        header[data-testid="stHeader"] {
                            z-index: -1;
                        }
                        div[data-testid="stToolbar"] {
                        z-index: 100;
                        }
                        div[data-testid="stDecoration"] {
                        z-index: 100;
                        }
                </style>
"""

# st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)
