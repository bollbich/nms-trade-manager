import streamlit as st
from app.storage import save_json
from app.services import new_station_id, find_station, upsert_station, delete_station

DATA_DIR = "data"


def render_manage_tab():
    col_nav, col_edit = st.columns([1, 2])

    st.session_state.stations.sort(key=lambda x: x["sistema"].lower())

    # =========================
    # NAVEGACIÓN
    # =========================
    with col_nav:
        st.subheader("Estaciones")

        stations = st.session_state.stations

        search = st.text_input(
            "🔎 Buscar estación",
            placeholder="Sistema o estación"
        )

        if search:
            search_l = search.lower()
            stations = [
                s for s in stations
                if search_l in s["sistema"].lower()
                   or search_l in s["estacion"].lower()
            ]

        options = ["✨ CREAR NUEVA"] + [
            f"{s['sistema']} | {s['estacion']}"
            for s in stations
        ]

        selected = st.radio("Seleccionar", options)

        if selected == "✨ CREAR NUEVA":
            if st.session_state.editing_id is not None:
                st.session_state.editing_id = None
                st.session_state.temp_buy = []
                st.session_state.temp_sell = []
                st.rerun()
        else:
            station = next(
                s for s in st.session_state.stations
                if f"{s['sistema']} | {s['estacion']}" == selected
            )
            if st.session_state.editing_id != station["id"]:
                st.session_state.editing_id = station["id"]
                st.session_state.temp_buy = list(station["compra"])
                st.session_state.temp_sell = list(station["venta"])
                st.rerun()

    # =========================
    # EDITOR
    # =========================
    with col_edit:
        current = find_station(
            st.session_state.stations,
            st.session_state.editing_id
        )

        sistema = st.text_input("Sistema", value=current["sistema"] if current else "")
        estacion = st.text_input("Estación", value=current["estacion"] if current else "")

        economia_list = st.session_state.econ_master
        economia = st.selectbox(
            "Economía",
            economia_list,
            index=economia_list.index(current["economia"]) if current else 0
        )

        st.divider()

        # =========================
        # ITEMS
        # =========================
        if st.session_state.items_master:
            c1, c2, c3 = st.columns([2, 1, 1])

            item = c1.selectbox("Item", st.session_state.items_master)
            pct = c2.number_input("% Precio", step=0.1, format="%.1f")

            if c3.button("⬇️ Vende"):
                if not any(i["item"] == item for i in st.session_state.temp_buy):
                    st.session_state.temp_buy.append({"item": item, "pct": pct})
                    st.session_state.temp_buy.sort(key=lambda x: x["item"].lower())
                    st.rerun()

            if c3.button("⬆️ Compra"):
                if not any(i["item"] == item for i in st.session_state.temp_sell):
                    st.session_state.temp_sell.append({"item": item, "pct": pct})
                    st.session_state.temp_sell.sort(key=lambda x: x["item"].lower())
                    st.rerun()

        b_col, s_col = st.columns(2)

        with b_col:
            st.caption("🛒 Venden")
            for i, x in enumerate(st.session_state.temp_buy):
                if st.button(f"❌ {x['item']} ({x['pct']}%)", key=f"b{i}"):
                    st.session_state.temp_buy.pop(i)
                    st.rerun()

        with s_col:
            st.caption("📈 Compran")
            for i, x in enumerate(st.session_state.temp_sell):
                if st.button(f"❌ {x['item']} ({x['pct']}%)", key=f"s{i}"):
                    st.session_state.temp_sell.pop(i)
                    st.rerun()

        st.divider()

        # =========================
        # ACCIONES
        # =========================
        # GUARDAR
        if st.button("💾 GUARDAR", type="primary"):
            if not sistema or not estacion:
                st.warning("Sistema y estación son obligatorios")
                return

            station = {
                "id": st.session_state.editing_id or new_station_id(),
                "sistema": sistema,
                "estacion": estacion,
                "economia": economia,
                "compra": st.session_state.temp_buy,
                "venta": st.session_state.temp_sell
            }

            upsert_station(st.session_state.stations, station)
            save_json(f"{DATA_DIR}/nms_stations.json", st.session_state.stations)

            st.success("Guardado correctamente")
            st.session_state.editing_id = station["id"]
            st.rerun()
        # DUPLICAR
        if st.session_state.editing_id:
            if st.button("📄 DUPLICAR"):
                original = find_station(
                    st.session_state.stations,
                    st.session_state.editing_id
                )

                nueva = {
                    "id": new_station_id(),
                    "sistema": original["sistema"],
                    "estacion": f"{original['estacion']} (copia)",
                    "economia": original["economia"],
                    "compra": list(original["compra"]),
                    "venta": list(original["venta"]),
                }

                st.session_state.stations.append(nueva)
                save_json(f"{DATA_DIR}/nms_stations.json", st.session_state.stations)

                # Pasar a editar la copia
                st.session_state.editing_id = nueva["id"]
                st.session_state.temp_buy = list(nueva["compra"])
                st.session_state.temp_sell = list(nueva["venta"])

                st.rerun()
        # BORRAR
        if st.session_state.editing_id:
            if st.button("🗑️ BORRAR", type="secondary"):
                st.session_state.stations = delete_station(
                    st.session_state.stations,
                    st.session_state.editing_id
                )
                save_json(f"{DATA_DIR}/nms_stations.json", st.session_state.stations)

                st.session_state.editing_id = None
                st.session_state.temp_buy = []
                st.session_state.temp_sell = []
                st.rerun()
