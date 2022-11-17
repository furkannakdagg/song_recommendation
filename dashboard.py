
import streamlit as st
import spotify_search as ss
import extras
from PIL import Image

qr = Image.open('images/qr.png')
spo_png = Image.open("images/spotify.png")
error_img = Image.open("images/error.jpeg")
miuul = Image.open("images/miuul.png")

df = extras.read_data()

st.set_page_config(
    page_title="Song Recommendation",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
)


def markdown_summary(col):
    return col.markdown(f"""
    Sanatçı Adı: {art_info}

    Şarkı Adı: {song_info}

    Yayınlanma Tarihi: {release_date}

    Hassas İçerik: {explicit}

    Şarkının Spotify Linki: {song_spot}

    Sanatçının Spotify Linki: {art_spot}
    """)


st.markdown("<h1 style='text-align: center;'>Miuul Şarkı Tavsiye Sistemi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size:18px;'>Sıradaki Favori Şarkınızı Bulun! 🎸</h3>",
            unsafe_allow_html=True)
st.markdown(" ")
col1, col2, col3 = st.columns(3)
with col1:
    st.image(spo_png, width=300)

with col2:
    st.image(miuul, caption='🧠 Skills of tomorrow!', width=325)

with col3:
    col3.image(qr, width=200)
st.write(" ")

col1, col2 = st.columns(2, gap="medium")
col1.markdown("""
Aramak istediğiniz şarkıyı lütfen aşağıya yazınız 👇
""")
song_name = col1.text_input("Şarkı Adı")
artist_name = col1.text_input("Sanatçı Adı")
check = col1.checkbox("Şarkıyı Bul")

if check and (len(song_name) >= 1 or len(artist_name) >= 1):
    if ss.search_pic(song_name, artist_name) == -1:
        col2.markdown("""
                ### Eminiz ki istediğiniz şarkı şu an bir yerlerde besteleniyordur 🎶
                ### Bira ve bebek bezinizi alın, arkanıza yaslanıp yayınlanmasını bekleyip 🍻🍼
                """)
        col2.image(error_img, width=300)
    else:
        img, preview = ss.search_pic(song_name, artist_name)
        col2.markdown("## Albüm Kapağı")
        col2.image(img)
        col2.markdown("## Şarkının Ön İzlemesi")
        col2.audio(preview)
        art_info, song_info, release_date, explicit, song_spot, art_spot = ss.info(song_name, artist_name)
        markdown_summary(col1)

        st.markdown("""---""")
        st.markdown("""#### Lütfen kaç öneri getirmek istediğinizi seçin 👇""")
        st.markdown("""
            * Kaç öneri görmek istediğinizi aşağıdan seçebilirsiniz. 1 ve 10 arasında öneri seçme imkanınız bulunmaktadır. 🧐

            * Aradığınız şarkının güncelliğinin ayarını yapabilirsiniz. 5 ve 40 arasında seçim yapabilirsiniz, seçtiğiniz sürenin öncesi ve sonrası kadar arama filtrelenir. Örneğin 2000'de piyasaya sürülen bir şarkı için 20 seçerseniz, arama 1980-2020 arasında filtrelenecektir. 📅

            > **Yapacağınız değişiklikler işlem süresini etkileyecektir. İşlem, internet hızınıza göre 1-2 dakika sürebilmektedir! ⏱**
            """)

        # tickers = ["Öneri Sayısı Seç", 3, 5, 10]
        rec1, rec2 = st.columns(2)
        # selection = st.selectbox("Kaç öneri görmek istersiniz?", tickers)
        selection = rec1.number_input(label="Kaç öneri görmek istersiniz?", min_value=1, max_value=10, step=1, value=3)
        year_range = rec2.number_input(label="Belirlemek istediğiniz aralık yılı", min_value=5, max_value=40, step=1,
                                       value=10)
        # year_range = rec2.selectbox("Belirlemek istediğiniz aralık yılı", list(range(5, 21)))
        recomm = rec1.checkbox("Önerileri Getir!")
        if recomm:
            try:
                rec_song = df[(df["name"].str.contains(song_name, case=False)) &
                              (df["artists"].str.contains(artist_name, case=False))] \
                    .drop(["name", "artists"], axis=1)
                rec_song = rec_song.iloc[0].squeeze()
                song_release = rec_song["release_date"]
                filtered_df = df[(df["release_date"] < song_release + year_range)
                                 & (df["release_date"] > song_release - year_range)]
                filtered_df.drop(["name", "artists", "release_date"], axis=1, inplace=True)

                rec_list = filtered_df.corrwith(rec_song.drop(["release_date"]), axis=1, numeric_only=True) \
                    .sort_values(ascending=False).head(11)
                rec_list = rec_list[1:]
                rec_df = df.loc[rec_list.index, ["name", "artists"]]
            except:
                rec_song = ss.audio_features(song_name, artist_name)
                song_release = rec_song[2]
                filtered_df = df[(df["release_date"] < song_release + year_range)
                                 & (df["release_date"] > song_release - year_range)]
                filtered_df.drop(["name", "artists", "release_date"], axis=1, inplace=True)

                rec_list = filtered_df.corrwith(rec_song.drop([2]), axis=1, numeric_only=True) \
                    .sort_values(ascending=False).head(11)
                rec_list = rec_list[1:]
                rec_df = df.loc[rec_list.index, ["name", "artists"]]
            finally:
                if selection != "Öneri Sayısı Seç":
                    if selection <= 5:
                        rec_cols = st.columns(selection, gap="small")
                        for i in range(selection):
                            rec_name = rec_df.iloc[i, 0]
                            rec_song = rec_df.iloc[i, 1]
                            rec_img, rec_preview = ss.search_pic(rec_name, rec_song)
                            rec_cols[i].image(rec_img)
                            rec_cols[i].audio(rec_preview)
                            art_info, song_info, release_date, explicit, song_spot, art_spot = ss.info(rec_song,
                                                                                                       rec_name)
                            markdown_summary(rec_cols[i])

                    elif selection > 5:
                        # rec_list = df.corrwith(rec_song, axis=1).sort_values(ascending=False).head(selection + 1)
                        # rec_list = rec_list[1:]
                        # rec_df = df.loc[rec_list.index, ["name", "artists"]]
                        rec_cols = st.columns(5, gap="small")
                        for i in range(5):
                            rec_name = rec_df.iloc[i, 0]
                            rec_song = rec_df.iloc[i, 1]
                            rec_img, rec_preview = ss.search_pic(rec_name, rec_song)
                            rec_cols[i].image(rec_img)
                            rec_cols[i].audio(rec_preview)
                            art_info, song_info, release_date, explicit, song_spot, art_spot = ss.info(rec_song,
                                                                                                       rec_name)
                            markdown_summary(rec_cols[i])
                        rec_cols2 = st.columns(year_range - 5, gap="small")
                        for i in range(year_range - 5):
                            rec_name = rec_df.iloc[i + 5, 0]
                            rec_song = rec_df.iloc[i + 5, 1]
                            rec_img, rec_preview = ss.search_pic(rec_name, rec_song)
                            rec_cols2[i].image(rec_img)
                            rec_cols2[i].audio(rec_preview)
                            art_info, song_info, release_date, explicit, song_spot, art_spot = ss.info(rec_song,
                                                                                                       rec_name)
                            markdown_summary(rec_cols2[i])
