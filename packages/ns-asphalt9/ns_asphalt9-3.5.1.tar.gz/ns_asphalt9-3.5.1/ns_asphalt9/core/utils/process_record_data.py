def filter_navi_data(data):
    # 过滤
    filtered_data = []
    skip_index = []
    for index, d in enumerate(data):
        if index in skip_index:
            continue
        if index + 1 < len(data) and data[index + 1]["timestamp"] - d["timestamp"] < 40:
            skip_index.append(index + 1)
        else:
            filtered_data.append(d)
    return filtered_data


def to_navi_data(data):
    # 合并
    merged_data = []
    result = {}
    current_event = None
    for _, d in enumerate(data):
        if current_event is None and d["event_type"] == "press":
            current_event = {
                "progress": d["progress"],
                "key": d["control_data"],
                "press_start": d["timestamp"],
                "last_timestamp": d["timestamp"],
            }

        if current_event and current_event["key"] == d["control_data"]:
            if d["timestamp"] - current_event["last_timestamp"] < 30:
                current_event["last_timestamp"] = d["timestamp"]
                continue
            else:
                current_event["press_end"] = d["timestamp"]
                current_event["down"] = (
                    current_event["press_end"] - current_event["press_start"]
                )
                merged_data.append(current_event)
                current_event = None

    for _, d in enumerate(merged_data):
        progress = d["progress"]
        if str(progress) in result:
            result[str(progress)].append({"key": d["key"], "down": d["down"]})
        elif str(progress - 1) in result:
            result[str(progress - 1)].append({"key": d["key"], "down": d["down"]})
        else:
            result[str(progress)] = [{"key": d["key"], "down": d["down"]}]

    return result


def to_record_data(data):
    result = []
    last_event = None
    for _, d in enumerate(data):
        if last_event is None:
            last_event = d

        duration = (d["timestamp"] - last_event["timestamp"]) / 1000
        if duration > 0:
            result.append(f"time.sleep({duration})\n")
        if d["event_type"] == "press":
            result.append(f"pro.press('{d['control_data']}')\n")
        if d["event_type"] == "release":
            result.append(f"pro.release('{d['control_data']}')\n")
        last_event = d

    return result
