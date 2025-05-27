import streamlit as st
from PIL import Image, ImageEnhance

def main():
  """ test... """
  st.title("Askme Web app")

  # st.text("테스트 페이지입니다.")

  html = """
  <div style="background-color:blue:padding:10px;">
  <h1 stype="color:yellow">테스트 페이지</h1>
  </div>
  """

  st.markdown(html, unsafe_allow_html=True)
  # st.write("테스트 페이지...")

  st.sidebar.image("assets/hw.png", width=300)
  img = st.sidebar.file_uploader("파일 올려주세요. (jpg, png or jpeg)", type=["jpg", "png", "jpeg"])

  if img is not None:
    img = Image.open(img)

    if st.sidebar.button("이미지 미리보기"):
        st.sidebar.image(img, width=300)

  menulist = ["Guide", "Q&A", "etc"]
  choice = st.sidebar.selectbox("매뉴 선택", menulist)

  if choice == "Guide":
    st.subheader("Guide for migration")
    migtype = st.sidebar.radio("데이터베이스", ["MySQL", "AWS RDS", "AWS Mariadb"])
  elif choice == "Q&A":
    st.subheader("Q&A")
  elif choice == "etc":
    st.subheader("기타")
    crate = st.slider("Contrast", 0.5, 5.0)
    enhan = ImageEnhance.Contrast(img)
    newimg = enhan.enhance(crate)
    st.image(newimg, width=600, use_column_width=True)

  if st.sidebar.button("생성자"):
    st.sidebar.subheader("페이지 생성")
    st.sidebar.markdown("by Author's kkh")
    st.sidebar.markdown("[khkwon01@gmail.com](mailto:khkwon01@gmail.com)")
    st.sidebar.text("All Rights (2025)")

if __name__ == "__main__":
  main()
