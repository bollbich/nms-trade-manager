import streamlit as st
from app.storage import save_json
from app.services import export_database, import_database

DATA_DIR = "data"


def render_sidebar():
    st.sidebar.header("⚙️ Configuración Maestra")

    # ======================
    # ITEMS
    # ======================
    with st.sidebar.expander("📦 Items"):
        # Añadir
        with st.form("add_item", clear_on_submit=True):
            val = st.text_input("Nuevo item")
            if st.form_submit_button("Añadir"):
                if val and val not in st.session_state.items_master:
                    st.session_state.items_master.append(val.strip())
                    st.session_state.items_master.sort(key=str.lower)
                    save_json(f"{DATA_DIR}/nms_items.json", st.session_state.items_master)
                    st.rerun()
        # Borrar
        item = st.selectbox("Eliminar item", ["---"] + st.session_state.items_master)
        if st.button("🗑️ Eliminar Item") and item != "---":
            # Protección: no borrar items en uso
            used = any(
                item in [i['item'] for i in s["compra"] + s["venta"]]
                for s in st.session_state.stations
            )

            if used:
                st.warning(f"El item '{item}' está en uso por una o más estaciones.")
            else:
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

    from app.services import export_database, import_database
    from app.storage import save_json

    # ======================
    # BACKUP / RESTORE
    # ======================
    with st.sidebar.expander("💾 Importar / Exportar"):
        # EXPORTAR
        export_json = export_database(
            st.session_state.stations,
            st.session_state.items_master,
            st.session_state.econ_master
        )

        st.download_button(
            label="⬇️ Exportar base de datos",
            data=export_json,
            file_name="nms_trade_backup.json",
            mime="application/json"
        )

        st.divider()

        # IMPORTAR
        uploaded = st.file_uploader(
            label="Seleccionar archivo de respaldo",
            type="json",
            key="db_uploader"
        )

        if uploaded:
            try:
                content = uploaded.read().decode("utf-8")
                st.session_state["_import_preview"] = import_database(content)
                st.success("Archivo válido. Listo para importar.")

            except Exception as e:
                st.session_state["_import_preview"] = None
                st.error(f"Archivo inválido: {e}")

        if st.session_state.get("_import_preview"):
            if st.button("⚠️ Actualizar base de datos", type="primary"):
                stations, items, economies = st.session_state["_import_preview"]

                st.session_state.stations = stations
                st.session_state.items_master = items
                st.session_state.econ_master = economies

                save_json("data/nms_stations.json", stations)
                save_json("data/nms_items.json", items)
                save_json("data/nms_economies.json", economies)

                st.session_state["_import_preview"] = None
                st.success("Base de datos actualizada correctamente")
                st.rerun()
