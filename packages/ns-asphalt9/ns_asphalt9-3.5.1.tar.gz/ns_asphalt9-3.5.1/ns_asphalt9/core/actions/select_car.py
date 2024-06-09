import time

from .. import consts, globals, tasks
from ..actions import process_race
from ..controller import Buttons, pro
from ..ocr import OCR
from ..utils.count import count
from ..utils.log import logger
from ..tasks import TaskManager
from .common import get_race_mode


def world_series_reset(type=None, max_col=None):
    division = globals.DIVISION
    if not division:
        division = "青铜"
    config = globals.CONFIG["多人一"][division]
    level = config["车库等级"]
    left_count_mapping = {"青铜": 4, "白银": 3, "黄金": 2, "铂金": 1}
    pro.press_group([Buttons.DPAD_UP] * 4, 0)
    pro.press_group([Buttons.DPAD_RIGHT] * 6, 0)
    pro.press_group([Buttons.DPAD_LEFT] * 1, 0)
    pro.press_group([Buttons.DPAD_DOWN] * 1, 0)
    pro.press_group([Buttons.DPAD_LEFT] * left_count_mapping.get(level), 0)
    time.sleep(1)
    pro.press_a(2)


def default_reset(type=None, max_col=None):
    pass


def other_series_reset(type=None, max_col=None):
    if type == "段位":
        pro.press_group([Buttons.DPAD_UP] * 4, 0)
        pro.press_group([Buttons.DPAD_RIGHT] * 6, 0)
        pro.press_group([Buttons.DPAD_LEFT] * 1, 0)
        pro.press_group([Buttons.DPAD_DOWN] * 1, 0)
        pro.press_group([Buttons.DPAD_LEFT] * 4, 0)
        time.sleep(0.5)
        pro.press_a(1)
    elif type == "左上":
        if max_col is None:
            max_col = 6
        else:
            max_col = max_col + 1
        pro.press_group([Buttons.DPAD_LEFT] * max_col, 0)
        pro.press_group([Buttons.DPAD_UP] * 4, 0)
        pro.press_button(Buttons.DPAD_DOWN, 1)
    else:
        pro.press_button(Buttons.ZR, 0)
        pro.press_button(Buttons.ZL, 1)


def carhunt_reset(type=None, max_col=None):
    pro.press_button(Buttons.ZR, 0)
    pro.press_button(Buttons.ZL, 1)


def get_race_config():
    mode = get_race_mode()
    division = globals.DIVISION if globals.DIVISION else "青铜"
    logger.info(f"Get mode {mode} config.")
    config_mapping = {
        consts.mp1_zh: (globals.CONFIG["多人一"][division]["车库位置"], world_series_reset),
        consts.mp2_zh: (globals.CONFIG["多人二"]["车库位置"], other_series_reset),
        consts.mp3_zh: (globals.CONFIG["多人三"]["车库位置"], other_series_reset),
        consts.car_hunt_zh: (globals.CONFIG["寻车"]["车库位置"], other_series_reset),
        consts.legendary_hunt_zh: (globals.CONFIG["传奇寻车"]["车库位置"], other_series_reset),
        consts.custom_event_zh: (globals.CONFIG["自定义"]["车库位置"], other_series_reset),
        consts.career_zh: ([{"row": 2, "col": 4}], default_reset),
    }
    positions = [{"row": row, "col": col} for row in [1, 2] for col in [1, 2, 3]]
    config = config_mapping.get(mode, (positions, default_reset))
    return config


def move_to_position(positions, reset, mode):
    if globals.SELECT_COUNT[mode] >= len(positions):
        globals.SELECT_COUNT[mode] = 0
    if positions:
        reset_type = None
        if mode in globals.CONFIG:
            reset_type = globals.CONFIG[mode].get("复位", None)
        reset(type=reset_type, max_col=max([i["col"] for i in positions]))
        position = positions[globals.SELECT_COUNT[mode]]
        logger.info(
            f"Start try position = {position}, count = {globals.SELECT_COUNT[mode]}"
        )
        for i in range(position["row"] - 1):
            pro.press_button(Buttons.DPAD_DOWN, 0)

        for i in range(position["col"] - 1):
            pro.press_button(Buttons.DPAD_RIGHT, 0)

    time.sleep(2)


def select_car():
    # 选车
    logger.info("Start select car.")
    mode = get_race_mode()
    need_select_car = True
    if mode in [consts.car_hunt_zh, consts.legendary_hunt_zh, consts.mp1_zh]:
        need_select_car = globals.SELECT_CAR[mode]
        if mode == consts.mp1_zh:
            division = globals.DIVISION
            if not division:
                division = "青铜"
            config = globals.CONFIG["多人一"][division]
            level = config["车库等级"]
            if division != level:
                need_select_car = True
        if (
            mode == consts.car_hunt_zh
            and globals.CONFIG[consts.car_hunt_zh]["活动"] == "特殊"
        ):
            need_select_car = True
    while globals.G_RUN.is_set():
        positions, reset = get_race_config()
        logger.info(f"need_select_car = {need_select_car}")
        if need_select_car:
            move_to_position(positions, reset, mode)
        elif mode in [consts.car_hunt_zh, consts.legendary_hunt_zh]:
            pro.press_group([Buttons.A, Buttons.B], 2)
        # 进入车辆详情页
        pro.press_group([Buttons.A], 3.5)
        page = OCR.get_page()
        # 如果没有进到车辆详情页面, 重
        if page.name != consts.car_info:
            pro.press_group([Buttons.B] * 3, 2)
            TaskManager.task_enter(mode, page)
            return
        # 如果车辆详情页有段位信息，说明车库段位与实际段位不匹配
        if page.has_text("BRONZE|SILVER|GOLD|PLATINUM"):
            pro.press_b()
            need_select_car = True
            globals.DIVISION = ""
            continue
        # 判断是否有play按钮
        if not page.has_text("PLAY") and not OCR.has_play(mode):
            pro.press_b()
            globals.SELECT_COUNT[mode] += 1
            need_select_car = True
            continue
        # 判断寻车是否有票
        if (
            mode in [consts.car_hunt_zh, consts.legendary_hunt_zh]
            and globals.CONFIG[mode]["蓝币寻车"]
        ):
            ticket = OCR.get_carinfo_ticket()
            logger.info(f"Get carinfo ticket = {ticket}")
            if ticket == 0:
                # 买票
                pro.press_group([Buttons.A, Buttons.DPAD_DOWN, Buttons.A, Buttons.B], 2)
        pro.press_group([Buttons.DPAD_RIGHT] * 3, 0)
        pro.press_a()
        if mode in [consts.car_hunt_zh, consts.legendary_hunt_zh, consts.mp1_zh]:
            globals.SELECT_CAR[mode] = False
            logger.info(f"Set {mode} select_car = False")
        break
    process_race()
    if mode in [consts.car_hunt_zh, consts.legendary_hunt_zh]:
        count.race_count_inc(mode)
        globals.output_queue.put({"寻车次数": count.get_race_count(mode)})
