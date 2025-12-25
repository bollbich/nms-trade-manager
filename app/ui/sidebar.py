import streamlit as st
from app.storage import save_json

DATA_DIR = "data"


def render_sidebar():
    st.sidebar.header("⚙️ Configuración Maestra")

    # ======================
    # ITEMS
    # ======================
    with st.sidebar.expander("📦 Items"):
        with st.form("add_item", clear_on_submit=True):
            val = st.text_input("Nuevo item")
            if st.form_submit_button("Añadir"):
                if val and val not in st.session_state.items_master:
                    st.session_state.items_master.append(val.strip())
                    st.session_state.items_master.sort(key=str.lower)
                    save_json(f"{DATA_DIR}/nms_items.json", st.session_state.items_master)
                    st.rerun()

        item = st.selectbox("Eliminar item", ["---"] + st.session_state.items_master)
        if st.button("🗑️ Eliminar Item") and item != "---":
            st.session_state.items_master.remove(item)
            save_json(f"{DATA_DIR}/nms_items.json", st.session_state.items_master)
            st.rerun()

    # ======================
    # ECONOMÍAS
    # ======================
    with st.sidebar.expander("💰 Economías", expanded=True):
        # Añadir
        with st.form("add_econ", clear_on_submit=True):
            val = st.text_input("Nueva economía")
            if st.form_submit_button("Añadir"):
                if val and val not in st.session_state.econ_master:
                    st.session_state.econ_master.append(val.strip())
                    st.session_state.econ_master.sort(key=str.lower)
                    save_json(
                        f"{DATA_DIR}/nms_economies.json",
                        st.session_state.econ_master
                    )
                    st.rerun()

        # Borrar
        econ = st.selectbox(
            "Eliminar economía",
            ["---"] + st.session_state.econ_master
        )

        if st.button("🗑️ Eliminar Economía") and econ != "---":
            # Protección: no borrar economías en uso
            used = any(
                s["economia"] == econ
                for s in st.session_state.stations
            )

            if used:
                st.warning(
                    f"La economía '{econ}' está en uso por una o más estaciones."
                )
            else:
                st.session_state.econ_master.remove(econ)
                save_json(
                    f"{DATA_DIR}/nms_economies.json",
                    st.session_state.econ_master
                )
                st.rerun()
