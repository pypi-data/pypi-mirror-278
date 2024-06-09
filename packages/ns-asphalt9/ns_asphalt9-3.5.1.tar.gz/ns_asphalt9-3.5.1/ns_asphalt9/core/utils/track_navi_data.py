import json

from .track_navi_data_update import data as updated_navi_data
from .track_navi_data_win import track_navi_data
from .track_navi_data_v2 import track_navi_data as track_navi_data_v2


def get_navi_data(name):
    navi_data = []
    data = None

    try:
        with open("navi_data.json", "r") as file:
            custom_navi_data = json.load(file)
    except Exception as e:
        custom_navi_data = {}

    # win端转换数据
    if name in track_navi_data:
        data = track_navi_data[name]
    # 根据ns端更新数据
    if name in updated_navi_data:
        data = updated_navi_data[name]
    # 第二版本数据
    if name in track_navi_data_v2:
        data = track_navi_data_v2[name]
    # 自定义数据
    if name in custom_navi_data:
        data = custom_navi_data[name]
    if data:
        if "L" not in data:
            return data
        for k in data["L"]:
            navi_data.append((k, "L", 0))
        for k in data["R"]:
            navi_data.append((k, "R", 0))

        for extra in ["LL", "RR", "B", "BB", "YY-1", "YY-2", "YY-3"]:
            if extra in data:
                for k in data[extra]:
                    if isinstance(k, str):
                        p, d = k.split("-")
                        navi_data.append((int(p), extra, int(d)))
                    else:
                        navi_data.append((k, extra, 0))

        navi_data = sorted(navi_data, key=lambda item: item[0])
    return navi_data


if __name__ == "__main__":
    navi_data = get_navi_data("CITY DASH")
    print(navi_data)
