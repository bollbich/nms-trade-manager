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

    st.dataframe(
        df[["sistema", "estacion", "economia", "Compra", "Venta"]],
        use_container_width=True,
        hide_index=True
    )
