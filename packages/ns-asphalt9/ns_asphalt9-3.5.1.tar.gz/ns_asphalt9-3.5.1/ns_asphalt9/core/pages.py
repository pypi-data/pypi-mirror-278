import re

from . import actions, consts, globals
from .controller import Buttons, pro
from .ocr import OCR
from .utils.decorator import cache_decorator
from .utils.log import logger
from .utils.credits import credits
from .utils.error_process import error_process


class Page:
    text = None
    name = None
    data = None
    mode = None
    hunt_car = None
    division = None
    touchdriver = None
    next_page = None

    feature = ""
    part_match = False

    action = None
    args = ()

    def __init__(self, text: str, last_page: "Page" = None) -> None:
        if last_page:
            self.mode = last_page.mode
            self.division = last_page.division
            self.touchdriver = last_page.touchdriver
            self.hunt_car = last_page.hunt_car
        self.text = text

    def parse_division(self):
        division = ""
        if self.name in [consts.world_series]:
            division = OCR.get_division()
        else:
            divisions = re.findall("BRONZE|SILVER|GOLD|PLATINUM", self.text)
            if divisions:
                division = consts.divisions_zh.get(divisions[0], "")
        return division

    def parse_common(self):
        division = self.parse_division()
        if division:
            logger.info(f"Get division {division}")

        if (
            division
            and self.name
            in [
                consts.world_series,
                consts.searching,
                consts.loading_race,
            ]
            and division != self.division
        ):
            self.division = division
            globals.SELECT_CAR[consts.mp1_zh] = True
            logger.info(f"Set mp1 select_car = True")

        modes = re.findall(
            "YEAR OF THE BEAST|LEGENDARY HUNT|CAR HUNT|WORLD SERIES|LIMITED SERIES|TRIAL SERIES",
            self.text,
        )
        if (
            modes
            and self.name not in [consts.multi_player]
            and modes[0] not in ["CAR HUNT ENENT PACK"]
        ):
            self.mode = consts.modes_zh.get(modes[0], "")
            if self.mode == consts.car_hunt_zh:
                hunt_cars = re.findall("APEX AP-0", self.text)
                if hunt_cars:
                    self.hunt_car = hunt_cars[0]

        credits.parse_text(self.text, self.name)
        error_process.parse_page(self.name)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        """计算权重"""
        match_count = 0
        if callable(cls.feature):
            feature = cls.feature()
        else:
            feature = cls.feature
        if feature:
            match_count = len(re.findall(feature, text))
            if not cls.part_match and match_count > 0:
                match_count = 10
        return match_count

    def has_text(self, identity):
        """page_text中是否包含identity"""
        if re.findall(identity, self.text):
            return True
        return False

    @property
    def dict(self) -> dict:
        return {
            "name": self.name,
            "text": self.text,
            "data": self.data,
            "mode": self.mode,
            "division": self.division,
            "touchdriver": self.touchdriver,
        }

    def call_action(self):
        if self.action:
            logger.debug(f"Call aciton func = {self.action} args = {self.args}")
            self.action(*self.args)


class Empty(Page):
    """Empty"""

    name = consts.empty


@cache_decorator("page")
class LoadingGame(Page):
    """游戏加载页"""

    name = consts.loading_game
    feature = "GAMELOFT PLAYER.*ASPHALT"
    part_match = False

    action = staticmethod(actions.loading_game)


@cache_decorator("page")
class LoadingRace(Page):
    """比赛加载页"""

    name = consts.loading_race
    feature = "LOADING RACE"
    part_match = False

    action = staticmethod(actions.process_race)


@cache_decorator("page")
class LoadingCarHunt(Page):
    """寻车加载页"""

    name = consts.loading_carhunt
    feature = "CAR HUNT.*BEST TIME"
    part_match = False

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(re.findall(cls.feature, text))
        if match_count:
            if "CAR HUNT EVENT PACK" in text:
                match_count = 0
            else:
                match_count = 10
        return match_count


@cache_decorator("page")
class LoadingLegendaryHunt(Page):
    """通行证寻车加载页"""

    name = consts.legendary_hunt_loading
    feature = "LIMITED-TIME EVENT.*LEGENDARY HUNT"
    part_match = False


@cache_decorator("page")
class ConnectController(Page):
    """连接手柄"""

    name = consts.connect_controller
    feature = "Press.*on the controller"
    part_match = False

    action = staticmethod(actions.connect_controller)


@cache_decorator("page")
class ConnectedController(Page):
    """手柄已连接"""

    name = consts.connected_controller
    feature = "Controllers"
    part_match = False

    action = staticmethod(actions.enter_game)


@cache_decorator("page")
class MultiPlayer(Page):
    """多人首页"""

    name = consts.multi_player
    feature = "WORLD SERIES|LIMITED SERIES|TRIAL SERIES"
    part_match = False

    action = staticmethod(actions.enter_series)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(set(re.findall(cls.feature, text)))
        position_count = len(re.findall("MY POSITION", text))
        if match_count >= 2 or position_count >= 2:
            match_count = 10
        return match_count


@cache_decorator("page")
class WorldSeries(Page):
    """多人一"""

    name = consts.world_series
    feature = "WORLD SERIES|MY POSITION|SERIES SCORE|NEXT MILESTONE|LEADERBOARD|PLAY"
    part_match = True
    next_page = consts.select_car

    action = staticmethod(pro.press_button)
    args = (Buttons.A, 8)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(re.findall(cls.feature, text))
        if "WORLD SERIES" in text:
            match_count += 3
        return match_count

    def parse_mode(self):
        self.mode = consts.mp1_zh


@cache_decorator("page")
class TrialSeries(Page):
    """多人二尾流"""

    name = consts.trial_series
    feature = "TRIAL SERIES|MY POSITION|SERIES SCORE|NEXT MILESTONE|LEADERBOARD|PLAY"
    part_match = True
    next_page = consts.select_car

    action = staticmethod(pro.press_button)
    args = (Buttons.A, 8)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(re.findall(cls.feature, text))
        if "TRIAL SERIES" in text:
            match_count += 3
        return match_count

    def parse_mode(self):
        self.mode = consts.mp_zh


@cache_decorator("page")
class LimitedSeries(Page):
    """多人二限时赛事"""

    name = consts.limited_series
    feature = "LIMITED SERIES|MY POSITION|SERIES SCORE|NEXT MILESTONE|LEADERBOARD|PLAY"
    part_match = True
    next_page = consts.select_car

    action = staticmethod(pro.press_button)
    args = (Buttons.A, 8)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(re.findall(cls.feature, text))
        if "LIMITED SERIES" in text:
            match_count += 3
        return match_count

    def parse_mode(self):
        self.mode = consts.mp_zh


@cache_decorator("page")
class CarHunt(Page):
    """寻车"""

    name = consts.carhunt
    # feature = "CAR HUNT:.*CAR HUNT EVENT PACK"
    # feature = "CAR HUNT EVENT PACK"
    feature = "CAR HUNT.*:.*COMPLETING"
    part_match = False
    next_page = consts.select_car

    action = staticmethod(actions.validate_ticket)
    # args = (Buttons.A, 3)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(re.findall(cls.feature, text))
        if match_count:
            if "LEGENDARY" in text:
                match_count = 0
            else:
                match_count = 10
        return match_count

    def parse_mode(self):
        self.mode = consts.car_hunt_zh


@cache_decorator("page")
class LegendaryHunt(Page):
    """通行证寻车"""

    name = consts.legendary_hunt
    feature = "LEGENDARY HUNT.*COMPLETING"
    part_match = False
    next_page = consts.select_car

    action = staticmethod(actions.validate_ticket)
    # action = staticmethod(pro.press_button)
    # args = (Buttons.A, 3)

    def parse_mode(self):
        self.mode = consts.legendary_hunt_zh


@cache_decorator("page")
class CustomEvent(Page):
    """自定义活动"""

    name = consts.custom_event
    feature = staticmethod(actions.get_feature)
    part_match = False
    next_page = consts.select_car

    action = staticmethod(pro.press_button)
    args = (Buttons.A, 5)

    def parse_mode(self):
        self.mode = consts.custom_event_zh


@cache_decorator("page")
class Tickets(Page):
    """购买票"""

    name = consts.tickets
    feature = "TICKETS"
    part_match = False


@cache_decorator("page")
class SelectCar(Page):
    """选车"""

    name = consts.select_car
    feature = "CAR SELECTION|CAR SELECT.*FOR THIS RACE"
    part_match = False

    action = staticmethod(actions.select_car)


@cache_decorator("page")
class CarInfo(Page):
    """车辆详情"""

    name = consts.car_info
    feature = "TOP SPEED|LERATION|HANDLING|NITRO|TOUCH|PLAY|SKIP|Play|Nitro"
    part_match = True

    action = staticmethod(actions.enter_race)
    #action = staticmethod(pro.press_button)
    #args = (Buttons.B, 3)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(re.findall(cls.feature, text))
        if match_count <= 2:
            match_count = 0
        return match_count


@cache_decorator("page")
class Searching(Page):
    """匹配中"""

    name = consts.searching
    feature = "SEARCHING FOR OTHER PLAYERS AND LOCATION|WAITING FOR OTHER PLAYERS"
    part_match = False

    action = staticmethod(pro.press_button)
    args = (Buttons.Y, 3)


@cache_decorator("page")
class Racing(Page):
    """比赛中"""

    name = consts.racing
    feature = "POS\.| \d/\d|DIST|\d+%|NITRO|\d+:\d+\.\d+|TOUCHORIVE|SURFING|PERFECT"
    part_match = True

    def parse_racing(self):
        position = re.findall(r"\d/\d", self.text)
        position = position[0] if position else None
        progress = re.findall(r"(\d+)%", self.text)
        progress = int(progress[0]) if progress else None

        if self.touchdriver is None:
            touchdriver = OCR.get_touchdriver()
            if touchdriver == 0:
                pro.press_button(Buttons.MINUS)
                self.touchdriver = 1
            if touchdriver == 1:
                self.touchdriver = 1

        self.data = {
            "position": position,
            "progress": progress,
        }


@cache_decorator("page")
class Demoted(Page):
    """降级"""

    name = consts.demoted
    feature = "DEMOTED"
    part_match = False

    action = staticmethod(actions.demoted)

    def parse_common(self):
        super().parse_common()
        if globals.CONFIG["模式"] == consts.mp1_zh:
            logger.info("Set mp1 select_car = True")
            globals.SELECT_CAR[consts.mp1_zh] = True
            if globals.DIVISION:
                division_index = consts.divisions_sort.index(globals.DIVISION) - 1
            else:
                division_index = 0
            self.division = consts.divisions_sort[division_index]


@cache_decorator("page")
class Promoted(Page):
    """升级"""

    name = consts.promoted
    feature = ".*LEAGUE.*END OF SEASON REWARDS"
    part_match = False

    action = staticmethod(actions.promoted)

    def parse_common(self):
        super().parse_common()
        if globals.CONFIG["模式"] == consts.mp1_zh:
            logger.info("Set mp1 select_car = True")
            globals.SELECT_CAR[consts.mp1_zh] = True
            if globals.DIVISION:
                division_index = consts.divisions_sort.index(globals.DIVISION) + 1
            else:
                division_index = 0
            self.division = consts.divisions_sort[division_index]


@cache_decorator("page")
class Disconnected(Page):
    """断开连接"""

    name = consts.disconnected
    feature = "DISCONNECTED"
    part_match = False

    action = staticmethod(pro.press_button)
    args = (Buttons.B,)


@cache_decorator("page")
class NoConnection(Page):
    """无连接"""

    name = consts.no_connection
    feature = "NO CONNECTION"
    part_match = False
    action = staticmethod(pro.press_button)
    args = (Buttons.B,)


@cache_decorator("page")
class ErrorCdoe(Page):
    """Error Code: 2124-8028"""

    name = consts.error_code
    feature = "Error Code"
    part_match = False
    action = staticmethod(pro.press_button)
    args = (Buttons.A,)


@cache_decorator("page")
class ClubReward(Page):
    """俱乐部奖励"""

    name = consts.club_reward
    feature = "YOUR CLUB ACHIEVED"
    part_match = False

    action = staticmethod(pro.press_button)
    args = (Buttons.B,)


@cache_decorator("page")
class RaceResults(Page):
    """比赛结果"""

    name = consts.race_results
    feature = "RACE RESULTS|POS\.|PLAYER|CAR NAME|NEXT"
    part_match = True
    action = staticmethod(pro.press_button)
    args = (Buttons.A,)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(re.findall(cls.feature, text))
        if "RACE RESULTS" in text:
            match_count = 10
        return match_count


@cache_decorator("page")
class RaceScore(Page):
    """比赛成绩"""

    name = consts.race_score
    feature = "WINNER|YOUR POSITION|YOUR TIME|RATING|NEXT"
    part_match = True
    action = staticmethod(pro.press_button)
    args = (Buttons.A,)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(re.findall(cls.feature, text))
        if "WINNER" in text:
            match_count = 10
        return match_count


@cache_decorator("page")
class RaceReward(Page):
    """比赛奖励"""

    name = consts.race_reward
    feature = "RACE|REWARDS|REPUTATION|TOTAL|CREDITS|NEXT"
    part_match = True
    action = staticmethod(pro.press_button)
    args = (Buttons.A,)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(re.findall(cls.feature, text))
        if match_count < 2:
            match_count = 0
        if "RACE REWARDS" in text:
            match_count = 10
        if "THESE REWARDS" in text:
            match_count = 10
        return match_count


@cache_decorator("page")
class MilestoneReward(Page):
    """里程碑奖励"""

    name = consts.milestone_reward
    feature = "CONGRATULATIONS"
    part_match = False
    action = staticmethod(pro.press_button)
    args = (Buttons.A,)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = 0
        if cls.feature in text or "BUTTON TO SKIP" in text:
            match_count = 10
        if "ADDED" in text and "BANK" in text:
            match_count = 0
        return match_count


@cache_decorator("page")
class ConnectError(Page):
    """连接错误"""

    name = consts.connect_error
    feature = "CONNECTION ERROR"
    part_match = False
    action = staticmethod(pro.press_button)
    args = (Buttons.A,)


@cache_decorator("page")
class StarUp(Page):
    """升星"""

    name = consts.star_up
    feature = "STAR|UP"
    part_match = True
    action = staticmethod(pro.press_button)
    args = (Buttons.A,)


@cache_decorator("page")
class OfflineMode(Page):
    """离线模式"""

    name = consts.offline_mode
    feature = "OFFLINE MODE"
    part_match = False
    action = staticmethod(pro.press_group)
    args = ([Buttons.DPAD_LEFT, Buttons.B], 1)


@cache_decorator("page")
class SystemError(Page):
    """系统错误"""

    name = consts.system_error
    feature = "software.*closed"
    part_match = False

    action = staticmethod(actions.system_error)


@cache_decorator("page")
class ServerError(Page):
    """服务错误"""

    name = consts.server_error
    feature = "ERROR.*ACTION"
    part_match = False
    action = staticmethod(pro.press_button)
    args = (Buttons.B,)


@cache_decorator("page")
class SwitchHome(Page):
    """switch 主页"""

    name = consts.switch_home
    feature = "\d+:\d+.*Asphalt 9: Legends"
    part_match = False

    action = staticmethod(pro.press_group)
    args = ([Buttons.A] * 3, 3)


@cache_decorator("page")
class GameMenu(Page):
    """比赛中菜单页"""

    name = consts.game_menu
    feature = "GAME MENU"
    part_match = False
    action = staticmethod(pro.press_button)
    args = (Buttons.A,)


@cache_decorator("page")
class CardPack(Page):
    """抽卡页面"""

    name = consts.card_pack
    feature = "CARD PACK LEVEL INFO"
    part_match = False

    action = staticmethod(pro.press_group)
    args = ([Buttons.B] * 2, 3)


@cache_decorator("page")
class Club(Page):
    """俱乐部申请"""

    name = consts.club
    feature = "YOUR CLUB"
    part_match = False
    action = staticmethod(pro.press_button)
    args = (Buttons.B,)


@cache_decorator("page")
class DailyEvents(Page):
    """每日赛事"""

    name = consts.daily_events
    feature = "PLAY LIMITED.*BEST WAY TO EARN CREDITS FAST"
    part_match = False

    action = staticmethod(actions.enter_carhunt)


@cache_decorator("page")
class NoOpponents(Page):
    """每日赛事"""

    name = consts.no_opponents
    feature = "NO OPPONENTS WERE FOUND"
    part_match = False
    action = staticmethod(pro.press_button)
    args = (Buttons.B,)


@cache_decorator("page")
class Career(Page):
    """生涯"""

    name = consts.career
    feature = "CHAPTER.*CAREER"
    part_match = False


@cache_decorator("page")
class GrandPrix(Page):
    """大奖赛抽卡"""

    name = consts.grand_prix
    feature = "GP Standings"
    part_match = False


@cache_decorator("page")
class LegendPass(Page):
    """通行证页"""

    name = consts.legend_pass
    feature = "ENDS IN|CURRENT TIER|GARAGE|GRANTS UP TO"
    part_match = True


@cache_decorator("page")
class VipReward(Page):
    """通行证任务完成"""

    name = consts.vip_reward
    feature = "TIER"
    part_match = False
    action = staticmethod(pro.press_button)
    args = (Buttons.B,)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        match_count = len(re.findall(cls.feature, text))
        if match_count:
            if "ENDS IN" in text:
                match_count = 0
            else:
                match_count = 10
        return match_count


@cache_decorator("page")
class NoMP(Page):
    """无多人任务(大概率是网络问题)"""

    name = consts.no_mp
    feature = "NEW MULTIPLAYER SERIES.*COMING SOON"
    part_match = False

    action = staticmethod(actions.restart)


@cache_decorator("page")
class SelectUser(Page):
    """选择用户界面"""

    name = consts.select_user
    feature = "Select a user"
    part_match = False

    action = staticmethod(pro.press_button)
    args = (Buttons.A,)


@cache_decorator("page")
class SplitScreen(Page):
    """分屏页面"""

    name = consts.split_screen
    feature = "SPLIT-SCREEN MODE.*SELECT NUMBER OF PLAYERS"
    part_match = False


@cache_decorator("page")
class ConfirmBuy(Page):
    """确认购买页面"""

    name = consts.confirm_buy
    feature = "BUY THESE"
    part_match = False

    action = staticmethod(actions.process_confirm_bug)


@cache_decorator("page")
class SleepMode(Page):
    """睡眠页面"""

    name = consts.sleep_mode
    feature = "Sleep Mode"
    part_match = False

    action = staticmethod(actions.return_game)


@cache_decorator("page")
class CareerStart(Page):
    """生涯任务"""

    name = consts.career_start
    feature = "WIN THE RACE"
    part_match = False
    next_page = consts.select_car

    action = staticmethod(pro.press_button)
    args = (Buttons.A, 6)

    def parse_mode(self):
        self.mode = consts.career_zh


@cache_decorator("page")
class CreditsShop(Page):
    """金币购买页面"""

    name = consts.credits_shop
    feature = "CREDITS"
    part_match = False

    action = staticmethod(actions.restart)

    @classmethod
    def calc_weight(cls, text: str) -> int:
        if text.count(cls.feature) >= 4:
            return 10
        return 0
