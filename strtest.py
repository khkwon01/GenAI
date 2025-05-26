import streamlit as st


def main():
  """ test... """
  st.title("Askme Web app")

  st.text("테스트 페이지입니다.")

  html = """
  <div style="background-color:blue:padding:10px;">
  <h1 stype="color:yellow">테스트 페이지</h1>
  """

  st.markdown(html, unsafe_allow_html=True)
  st.write("테스트 페이지...")

  st.sidebar.image("", width=300)

if __name__ == "__main__":
  main()
