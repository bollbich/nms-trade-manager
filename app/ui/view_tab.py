import streamlit as st
import pandas as pd

def render_view_tab():
    if not st.session_state.stations:
        st.info("Base de datos vacía")
        return

    df = pd.DataFrame(st.session_state.stations)

    fmt = lambda l: ", ".join(f"{i['item']} ({i['pct']}%)" for i in l)
    df["Compra"] = df["compra"].apply(fmt)
    df["Venta"] = df["venta"].apply(fmt)

    # =========================
    # Selector de tipo de búsqueda + input
    # =========================
    tipo_busqueda = st.selectbox(
        "Buscar por:",
        options=["Sistema", "Estación", "Economía", "Compra", "Venta"]
    )
    texto_busqueda = st.text_input("Texto a buscar")

    df_filtrado = df.copy()
    if texto_busqueda:
        columna_map = {
            "Sistema": "sistema",
            "Estación": "estacion",
            "Economía": "economia",
            "Compra": "Compra",
            "Venta": "Venta"
        }
        columna = columna_map[tipo_busqueda]
        df_filtrado = df_filtrado[df_filtrado[columna].str.contains(texto_busqueda, case=False)]

    # =========================
    # Mostrar tabla
    # =========================
    st.dataframe(
        df_filtrado[["sistema", "estacion", "economia", "Compra", "Venta"]],
        use_container_width=True,
        hide_index=True
    )
