import streamlit as st


def main():
  """ test... """
  st.title("Askme Web app")

  st.text("테스트 페이지입니다.")

  html = """
  <div style="background-color:blue:padding:10px;">
  <h1 stype="color:yellow">테스트 페이지</h1>
  </div>
  """

  st.markdown(html, unsafe_allow_html=True)
  st.write("테스트 페이지...")

  st.sidebar.image("assets/hw.png", width=300)
  img = st.sidebar.file_uploader("파일 올려주세요. (jpg, png or jpeg)", type=["jpg", "png", "jpeg"])


if __name__ == "__main__":
  main()
