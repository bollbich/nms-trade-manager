import uuid
import json


def export_database(stations, items, economies) -> str:
    payload = {
        "stations": stations,
        "items": items,
        "economies": economies
    }
    return json.dumps(payload, indent=4, ensure_ascii=False)


def import_database(json_str: str):
    data = json.loads(json_str)

    if not all(k in data for k in ("stations", "items", "economies")):
        raise ValueError("Formato de archivo inválido")

    if not isinstance(data["stations"], list):
        raise ValueError("stations debe ser una lista")

    if not isinstance(data["items"], list):
        raise ValueError("items debe ser una lista")

    if not isinstance(data["economies"], list):
        raise ValueError("economies debe ser una lista")

    return data["stations"], data["items"], data["economies"]


def new_station_id() -> str:
    return str(uuid.uuid4())


def find_station(stations, station_id):
    return next((s for s in stations if s["id"] == station_id), None)


def upsert_station(stations, station):
    for i, s in enumerate(stations):
        if s["id"] == station["id"]:
            stations[i] = station
            return
    stations.append(station)


def delete_station(stations, station_id):
    return [s for s in stations if s["id"] != station_id]
