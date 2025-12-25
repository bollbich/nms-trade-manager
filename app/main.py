import streamlit as st
from app.state import init_state
from app.ui.sidebar import render_sidebar
from app.ui.view_tab import render_view_tab
from app.ui.manage_tab import render_manage_tab


def main():
    st.set_page_config(
        page_title="NMS Trade Manager",
        layout="wide",
        page_icon="🪐"
    )

    init_state()

    st.title("🪐 NMS Trade Manager")
    render_sidebar()

    tab1, tab2 = st.tabs(["🔍 Ver", "✏️ Gestionar"])
    with tab1:
        render_view_tab()
    with tab2:
        render_manage_tab()


if __name__ == "__main__":
    main()
