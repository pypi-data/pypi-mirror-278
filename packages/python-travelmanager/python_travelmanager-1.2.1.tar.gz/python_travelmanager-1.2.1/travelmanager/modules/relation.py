from ..travelmanager_api import TravelManagerAPI


class Relation:
    @staticmethod
    def get(station_id, date, lhf_id=None, linie_id=None):
        params = {
            "station_id": station_id,
            "date": date,
        }
        if lhf_id:
            params["lhf_id"] = lhf_id
        if linie_id:
            params["linie_id"] = linie_id
        return TravelManagerAPI.get("relations", params)
