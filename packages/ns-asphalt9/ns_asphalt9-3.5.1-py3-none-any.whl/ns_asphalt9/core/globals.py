import queue
import threading

from . import consts
from .utils.thread_lifo_queue import LIFOQueue

packet_queue = queue.Queue()

input_packet = {}

progress_data = []

input_queue = queue.Queue()
output_queue = queue.Queue()
notify_queue = queue.Queue()

frame_queue = LIFOQueue()

task_queue = queue.Queue()
video_queue = queue.Queue(maxsize=10)

# 视频设置队列
video_setting_queue = queue.Queue()

CONFIG = None

# 回放停止事件
G_REPLAY_RUN = threading.Event()
G_REPLAY_STOP = threading.Event()

G_OCR_PROGRESS = threading.Event()

# 程序运行
G_RUN = threading.Event()

#
G_OUT_WORKER = threading.Event()

# 退出循环事件
G_RACE_RUN_EVENT = threading.Event()
G_RACE_QUIT_EVENT = threading.Event()

# 是否活跃状态
NO_OPERATION_COUNT = 0

# 游戏模式
MODE = ""

# 段位
DIVISION = ""

# 选车次数
SELECT_COUNT = {
    consts.mp1_zh: 0,
    consts.mp2_zh: 0,
    consts.mp3_zh: 0,
    consts.car_hunt_zh: 0,
    consts.legendary_hunt_zh: 0,
    consts.custom_event_zh: 0,
    consts.career_zh: 0,
}
# 是否选车
SELECT_CAR = {
    consts.mp1_zh: True,
    consts.car_hunt_zh: True,
    consts.legendary_hunt_zh: True,
}

# Event
EVENT_UPDATE = False

# 比赛中
RACING = 0

#

SUPPORT_MJPG = None
