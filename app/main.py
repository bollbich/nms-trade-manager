import os
import sys
import streamlit as st
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
    
from app.state import init_state
from app.ui.sidebar import render_sidebar
from app.ui.view_tab import render_view_tab
from app.ui.manage_tab import render_manage_tab


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    favicon_path = os.path.join(root_dir, "assets", "NMSTradeManagerIcon.ico")
    logo_path = os.path.join(root_dir, "assets", "NMSTradeManagerLogo.png")

    st.set_page_config(
        page_title="NMS Trade Manager",
        layout="wide",
        page_icon=favicon_path
    )

    init_state()

    col1, col2 = st.columns([1, 4])

    with col1:
        st.image(logo_path, width=150)  # Aumenta este valor hasta que te guste

    with col2:
        st.write("##")
        st.title("NMS Trade Manager")
    render_sidebar()

    tab1, tab2 = st.tabs(["🔍 Ver", "✏️ Gestionar"])
    with tab1:
        render_view_tab()
    with tab2:
        render_manage_tab()


if __name__ == "__main__":
    main()
