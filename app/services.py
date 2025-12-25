import uuid


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
