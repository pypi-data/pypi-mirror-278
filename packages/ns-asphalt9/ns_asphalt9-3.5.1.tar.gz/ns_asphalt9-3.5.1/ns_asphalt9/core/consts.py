from .screenshot import save_screen

# Pages
# 空页面
empty = "empty"
# 游戏加载
loading_game = "loading_game"
# 比赛加载
loading_race = "loading_race"
# 寻车加载
loading_carhunt = "loading_carhunt"
# 手柄激活
connect_controller = "connect_controller"
# 手柄已连接
connected_controller = "connected_controller"
# 多人主页
multi_player = "multi_player"
# 多人一
world_series = "world_series"
# 多人二
trial_series = "trial_series"
# 生涯任务开始页
career_start = "career_start"
# 寻车
carhunt = "carhunt"
# 通行证寻车
legendary_hunt = "legendary_hunt"
# 购买票
tickets = "tickets"
# 选车
select_car = "select_car"
# 车辆详情
car_info = "car_info"
# 匹配中
searching = "searching"
# 比赛中
racing = "racing"
# 降级
demoted = "demoted"
# 升级
promoted = "promoted"
# 断开连接
disconnected = "disconnected"
# 无连接
no_connection = "no_connection"
# 俱乐部奖励
club_reward = "club_reward"
# 通行证任务完成
vip_reward = "vip_reward"
# 比赛结果
race_results = "race_results"
# 比赛成绩
race_score = "race_score"
# 比赛奖励
race_reward = "race_reward"
# 里程碑奖励
milestone_reward = "milestone_reward"
# 连接错误
connect_error = "connect_error"
# 升星
star_up = "star_up"
# 离线模式
offline_mode = "offline_mode"
# 系统错误
system_error = "system_error"
# 服务错误
server_error = "server_error"
# switch 主页
switch_home = "switch_home"
# 比赛中菜单页
game_menu = "game_menu"
# 抽卡页面
card_pack = "card_pack"
# 购买确认页
confirm_buy = "confirm_buy"
# 限时赛事
limited_series = "limited_series"
# 俱乐部申请
club = "club"
# 每日赛事
daily_events = "daily_events"
# 没匹配到对手
no_opponents = "no_opponents"
# 生涯
career = "career"
# 大奖赛
grand_prix = "grand_prix"
# 通行证页
legend_pass = "legend_pass"
# 无多人
no_mp = "no_mp"
# error code
error_code = "error_code"
# 选择用户
select_user = "select_user"
# 分屏页面
split_screen = "split_screen"
# 野兽年
custom_event = "custom_event"
# 睡眠页面
sleep_mode = "sleep_mode"
# 通行证寻车加载页
legendary_hunt_loading = "legendary_hunt_loading"
# 金币购买页
credits_shop = "credits_shop"

# 键盘与手柄映射
KEY_MAPPING = {
    "6": "MINUS",
    "7": "PLUS",
    "[": "CAPTURE",
    "]": "HOME",
    "i": "X",
    "j": "Y",
    "l": "A",
    "k": "B",
    "s": "DPAD_DOWN",
    "w": "DPAD_UP",
    "a": "DPAD_LEFT",
    "d": "DPAD_RIGHT",
    "1": "L",
    "2": "ZL",
    "9": "ZR",
    "8": "R",
    "c": save_screen,
}

car_hunt_zh = "寻车"
mp1_zh = "多人一"
mp2_zh = "多人二"
mp3_zh = "多人三"
career_zh = "生涯"
mp_zh = "多人"
free_pack_zh = "免费抽卡"
prix_pack_zh = "大奖赛抽卡"
legendary_hunt_zh = "传奇寻车"
restart = "重启"
shop_notify = "商店通知"
custom_event_zh = "自定义"


class Mode:
    car_hunt = "CAR HUNT"
    legendary_hunt = "LEGENDARY HUNT"
    world_series = "WORLD SERIES"
    limited_series = "LIMITED SERIES"
    trial_series = "TRIAL SERIES"
    custom_event = "CUSTOM EVENT"


modes_zh = {
    Mode.car_hunt: car_hunt_zh,
    Mode.legendary_hunt: legendary_hunt_zh,
    Mode.world_series: mp1_zh,
    Mode.limited_series: mp_zh,
    Mode.trial_series: mp_zh,
    Mode.custom_event: custom_event_zh,
}

modes_zh_page_mapping = {
    car_hunt_zh: carhunt,
    legendary_hunt_zh: legendary_hunt,
    mp1_zh: world_series,
    mp2_zh: limited_series,
    mp3_zh: limited_series,
    custom_event_zh: custom_event,
}


bronze = "BRONZE"
silver = "SILVER"
gold = "GOLD"
platinum = "PLATINUM"

divisions_zh = {bronze: "青铜", silver: "白银", gold: "黄金", platinum: "铂金"}
divisions_sort = [
    divisions_zh[bronze],
    divisions_zh[silver],
    divisions_zh[gold],
    divisions_zh[platinum],
]


class TaskStatus:
    default = ""
    start = "start"
    done = "done"


# 可以执行任务分发的页面
TASK_DISPATCH_PAGES = {
    world_series,
    limited_series,
    trial_series,
    carhunt,
    card_pack,
    legend_pass,
    legendary_hunt,
    daily_events,
    multi_player,
    grand_prix,
    career,
    custom_event,
    career_start,
}
