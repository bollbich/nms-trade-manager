import streamlit as st
from app.storage import load_json

DATA_DIR = "data"


def init_state():
    st.session_state.setdefault(
        "stations",
        load_json(f"{DATA_DIR}/nms_stations.json", [])
    )

    st.session_state.setdefault(
        "items_master",
        load_json(f"{DATA_DIR}/nms_items.json", [])
    )

    st.session_state.setdefault(
        "econ_master",
        load_json(
            f"{DATA_DIR}/nms_economies.json",
            ["N/A"]
        )
    )

    st.session_state.setdefault("editing_id", None)
    st.session_state.setdefault("temp_buy", [])
    st.session_state.setdefault("temp_sell", [])
