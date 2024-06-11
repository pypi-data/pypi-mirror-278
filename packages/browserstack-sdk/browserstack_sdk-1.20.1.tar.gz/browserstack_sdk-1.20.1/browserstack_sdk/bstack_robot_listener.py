# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11_opy_ = 7
def bstack1ll1_opy_ (bstack11l1l1l_opy_):
    global bstack1lll11l_opy_
    bstack111111l_opy_ = ord (bstack11l1l1l_opy_ [-1])
    bstack1111_opy_ = bstack11l1l1l_opy_ [:-1]
    bstack1l111ll_opy_ = bstack111111l_opy_ % len (bstack1111_opy_)
    bstack1llllll1_opy_ = bstack1111_opy_ [:bstack1l111ll_opy_] + bstack1111_opy_ [bstack1l111ll_opy_:]
    if bstack1l11111_opy_:
        bstack11ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack111l11_opy_ + bstack111111l_opy_) % bstack11_opy_) for bstack111l11_opy_, char in enumerate (bstack1llllll1_opy_)])
    else:
        bstack11ll111_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack111l11_opy_ + bstack111111l_opy_) % bstack11_opy_) for bstack111l11_opy_, char in enumerate (bstack1llllll1_opy_)])
    return eval (bstack11ll111_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l111llll1_opy_ import RobotHandler
from bstack_utils.capture import bstack1l1111l111_opy_
from bstack_utils.bstack11lll11l11_opy_ import bstack11lllllll1_opy_, bstack11lll1ll1l_opy_, bstack1l1111l1l1_opy_
from bstack_utils.bstack1ll11ll1ll_opy_ import bstack1lllll1l1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll1llll1l_opy_, bstack1ll11l1l11_opy_, Result, \
    bstack1l111lll11_opy_, bstack1l111lllll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ൥"): [],
        bstack1ll1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭൦"): [],
        bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ൧"): []
    }
    bstack1l111ll11l_opy_ = []
    bstack1l1111l1ll_opy_ = []
    @staticmethod
    def bstack11lll1l1ll_opy_(log):
        if not (log[bstack1ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ൨")] and log[bstack1ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ൩")].strip()):
            return
        active = bstack1lllll1l1_opy_.bstack11llllll1l_opy_()
        log = {
            bstack1ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ൪"): log[bstack1ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ൫")],
            bstack1ll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ൬"): bstack1l111lllll_opy_().isoformat() + bstack1ll1_opy_ (u"࡛ࠧࠩ൭"),
            bstack1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ൮"): log[bstack1ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ൯")],
        }
        if active:
            if active[bstack1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨ൰")] == bstack1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ൱"):
                log[bstack1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ൲")] = active[bstack1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭൳")]
            elif active[bstack1ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ൴")] == bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹ࠭൵"):
                log[bstack1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ൶")] = active[bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ൷")]
        bstack1lllll1l1_opy_.bstack111ll1111_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l1111111l_opy_ = None
        self._1l111l1lll_opy_ = None
        self._11llll1lll_opy_ = OrderedDict()
        self.bstack11lllll11l_opy_ = bstack1l1111l111_opy_(self.bstack11lll1l1ll_opy_)
    @bstack1l111lll11_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11ll1lllll_opy_()
        if not self._11llll1lll_opy_.get(attrs.get(bstack1ll1_opy_ (u"ࠫ࡮ࡪࠧ൸")), None):
            self._11llll1lll_opy_[attrs.get(bstack1ll1_opy_ (u"ࠬ࡯ࡤࠨ൹"))] = {}
        bstack11lll1111l_opy_ = bstack1l1111l1l1_opy_(
                bstack11lll1l11l_opy_=attrs.get(bstack1ll1_opy_ (u"࠭ࡩࡥࠩൺ")),
                name=name,
                bstack1l111ll1ll_opy_=bstack1ll11l1l11_opy_(),
                file_path=os.path.relpath(attrs[bstack1ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧൻ")], start=os.getcwd()) if attrs.get(bstack1ll1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨർ")) != bstack1ll1_opy_ (u"ࠩࠪൽ") else bstack1ll1_opy_ (u"ࠪࠫൾ"),
                framework=bstack1ll1_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪൿ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll1_opy_ (u"ࠬ࡯ࡤࠨ඀"), None)
        self._11llll1lll_opy_[attrs.get(bstack1ll1_opy_ (u"࠭ࡩࡥࠩඁ"))][bstack1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪං")] = bstack11lll1111l_opy_
    @bstack1l111lll11_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11lll1ll11_opy_()
        self._1l1111ll11_opy_(messages)
        for bstack11lllll1ll_opy_ in self.bstack1l111ll11l_opy_:
            bstack11lllll1ll_opy_[bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪඃ")][bstack1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ඄")].extend(self.store[bstack1ll1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩඅ")])
            bstack1lllll1l1_opy_.bstack11llll111l_opy_(bstack11lllll1ll_opy_)
        self.bstack1l111ll11l_opy_ = []
        self.store[bstack1ll1_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪආ")] = []
    @bstack1l111lll11_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11lllll11l_opy_.start()
        if not self._11llll1lll_opy_.get(attrs.get(bstack1ll1_opy_ (u"ࠬ࡯ࡤࠨඇ")), None):
            self._11llll1lll_opy_[attrs.get(bstack1ll1_opy_ (u"࠭ࡩࡥࠩඈ"))] = {}
        driver = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ඉ"), None)
        bstack11lll11l11_opy_ = bstack1l1111l1l1_opy_(
            bstack11lll1l11l_opy_=attrs.get(bstack1ll1_opy_ (u"ࠨ࡫ࡧࠫඊ")),
            name=name,
            bstack1l111ll1ll_opy_=bstack1ll11l1l11_opy_(),
            file_path=os.path.relpath(attrs[bstack1ll1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩඋ")], start=os.getcwd()),
            scope=RobotHandler.bstack1l111ll1l1_opy_(attrs.get(bstack1ll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪඌ"), None)),
            framework=bstack1ll1_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪඍ"),
            tags=attrs[bstack1ll1_opy_ (u"ࠬࡺࡡࡨࡵࠪඎ")],
            hooks=self.store[bstack1ll1_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬඏ")],
            bstack11lll1l1l1_opy_=bstack1lllll1l1_opy_.bstack11lll11ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll1_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤඐ").format(bstack1ll1_opy_ (u"ࠣࠢࠥඑ").join(attrs[bstack1ll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧඒ")]), name) if attrs[bstack1ll1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨඓ")] else name
        )
        self._11llll1lll_opy_[attrs.get(bstack1ll1_opy_ (u"ࠫ࡮ࡪࠧඔ"))][bstack1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨඕ")] = bstack11lll11l11_opy_
        threading.current_thread().current_test_uuid = bstack11lll11l11_opy_.bstack1l111l1ll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll1_opy_ (u"࠭ࡩࡥࠩඖ"), None)
        self.bstack1l111l1l1l_opy_(bstack1ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ඗"), bstack11lll11l11_opy_)
    @bstack1l111lll11_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11lllll11l_opy_.reset()
        bstack1l111l1l11_opy_ = bstack1l111111ll_opy_.get(attrs.get(bstack1ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ඘")), bstack1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ඙"))
        self._11llll1lll_opy_[attrs.get(bstack1ll1_opy_ (u"ࠪ࡭ࡩ࠭ක"))][bstack1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧඛ")].stop(time=bstack1ll11l1l11_opy_(), duration=int(attrs.get(bstack1ll1_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪග"), bstack1ll1_opy_ (u"࠭࠰ࠨඝ"))), result=Result(result=bstack1l111l1l11_opy_, exception=attrs.get(bstack1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨඞ")), bstack11lll1lll1_opy_=[attrs.get(bstack1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩඟ"))]))
        self.bstack1l111l1l1l_opy_(bstack1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫච"), self._11llll1lll_opy_[attrs.get(bstack1ll1_opy_ (u"ࠪ࡭ࡩ࠭ඡ"))][bstack1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧජ")], True)
        self.store[bstack1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩඣ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l111lll11_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11ll1lllll_opy_()
        current_test_id = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨඤ"), None)
        bstack1l111l11l1_opy_ = current_test_id if bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩඥ"), None) else bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫඦ"), None)
        if attrs.get(bstack1ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧට"), bstack1ll1_opy_ (u"ࠪࠫඨ")).lower() in [bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪඩ"), bstack1ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧඪ")]:
            hook_type = bstack1l11111ll1_opy_(attrs.get(bstack1ll1_opy_ (u"࠭ࡴࡺࡲࡨࠫණ")), bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫඬ"), None))
            hook_name = bstack1ll1_opy_ (u"ࠨࡽࢀࠫත").format(attrs.get(bstack1ll1_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩථ"), bstack1ll1_opy_ (u"ࠪࠫද")))
            if hook_type in [bstack1ll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨධ"), bstack1ll1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨන")]:
                hook_name = bstack1ll1_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃࠧ඲").format(bstack11llll11ll_opy_.get(hook_type), attrs.get(bstack1ll1_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧඳ"), bstack1ll1_opy_ (u"ࠨࠩප")))
            bstack1l1111l11l_opy_ = bstack11lll1ll1l_opy_(
                bstack11lll1l11l_opy_=bstack1l111l11l1_opy_ + bstack1ll1_opy_ (u"ࠩ࠰ࠫඵ") + attrs.get(bstack1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨබ"), bstack1ll1_opy_ (u"ࠫࠬභ")).lower(),
                name=hook_name,
                bstack1l111ll1ll_opy_=bstack1ll11l1l11_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1ll1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬම")), start=os.getcwd()),
                framework=bstack1ll1_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬඹ"),
                tags=attrs[bstack1ll1_opy_ (u"ࠧࡵࡣࡪࡷࠬය")],
                scope=RobotHandler.bstack1l111ll1l1_opy_(attrs.get(bstack1ll1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨර"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l1111l11l_opy_.bstack1l111l1ll1_opy_()
            threading.current_thread().current_hook_id = bstack1l111l11l1_opy_ + bstack1ll1_opy_ (u"ࠩ࠰ࠫ඼") + attrs.get(bstack1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨල"), bstack1ll1_opy_ (u"ࠫࠬ඾")).lower()
            self.store[bstack1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ඿")] = [bstack1l1111l11l_opy_.bstack1l111l1ll1_opy_()]
            if bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪව"), None):
                self.store[bstack1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫශ")].append(bstack1l1111l11l_opy_.bstack1l111l1ll1_opy_())
            else:
                self.store[bstack1ll1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧෂ")].append(bstack1l1111l11l_opy_.bstack1l111l1ll1_opy_())
            if bstack1l111l11l1_opy_:
                self._11llll1lll_opy_[bstack1l111l11l1_opy_ + bstack1ll1_opy_ (u"ࠩ࠰ࠫස") + attrs.get(bstack1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨහ"), bstack1ll1_opy_ (u"ࠫࠬළ")).lower()] = { bstack1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨෆ"): bstack1l1111l11l_opy_ }
            bstack1lllll1l1_opy_.bstack1l111l1l1l_opy_(bstack1ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ෇"), bstack1l1111l11l_opy_)
        else:
            bstack11lllll111_opy_ = {
                bstack1ll1_opy_ (u"ࠧࡪࡦࠪ෈"): uuid4().__str__(),
                bstack1ll1_opy_ (u"ࠨࡶࡨࡼࡹ࠭෉"): bstack1ll1_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨ්").format(attrs.get(bstack1ll1_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ෋")), attrs.get(bstack1ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩ෌"), bstack1ll1_opy_ (u"ࠬ࠭෍"))) if attrs.get(bstack1ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫ෎"), []) else attrs.get(bstack1ll1_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧා")),
                bstack1ll1_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨැ"): attrs.get(bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧෑ"), []),
                bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧි"): bstack1ll11l1l11_opy_(),
                bstack1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫී"): bstack1ll1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ු"),
                bstack1ll1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ෕"): attrs.get(bstack1ll1_opy_ (u"ࠧࡥࡱࡦࠫූ"), bstack1ll1_opy_ (u"ࠨࠩ෗"))
            }
            if attrs.get(bstack1ll1_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪෘ"), bstack1ll1_opy_ (u"ࠪࠫෙ")) != bstack1ll1_opy_ (u"ࠫࠬේ"):
                bstack11lllll111_opy_[bstack1ll1_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ෛ")] = attrs.get(bstack1ll1_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧො"))
            if not self.bstack1l1111l1ll_opy_:
                self._11llll1lll_opy_[self._11lll11lll_opy_()][bstack1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪෝ")].add_step(bstack11lllll111_opy_)
                threading.current_thread().current_step_uuid = bstack11lllll111_opy_[bstack1ll1_opy_ (u"ࠨ࡫ࡧࠫෞ")]
            self.bstack1l1111l1ll_opy_.append(bstack11lllll111_opy_)
    @bstack1l111lll11_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11lll1ll11_opy_()
        self._1l1111ll11_opy_(messages)
        current_test_id = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫෟ"), None)
        bstack1l111l11l1_opy_ = current_test_id if current_test_id else bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭෠"), None)
        bstack1l1111ll1l_opy_ = bstack1l111111ll_opy_.get(attrs.get(bstack1ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ෡")), bstack1ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭෢"))
        bstack11llll1l11_opy_ = attrs.get(bstack1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ෣"))
        if bstack1l1111ll1l_opy_ != bstack1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ෤") and not attrs.get(bstack1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ෥")) and self._1l1111111l_opy_:
            bstack11llll1l11_opy_ = self._1l1111111l_opy_
        bstack1l11111l1l_opy_ = Result(result=bstack1l1111ll1l_opy_, exception=bstack11llll1l11_opy_, bstack11lll1lll1_opy_=[bstack11llll1l11_opy_])
        if attrs.get(bstack1ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ෦"), bstack1ll1_opy_ (u"ࠪࠫ෧")).lower() in [bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ෨"), bstack1ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ෩")]:
            bstack1l111l11l1_opy_ = current_test_id if current_test_id else bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ෪"), None)
            if bstack1l111l11l1_opy_:
                bstack11llll1ll1_opy_ = bstack1l111l11l1_opy_ + bstack1ll1_opy_ (u"ࠢ࠮ࠤ෫") + attrs.get(bstack1ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭෬"), bstack1ll1_opy_ (u"ࠩࠪ෭")).lower()
                self._11llll1lll_opy_[bstack11llll1ll1_opy_][bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭෮")].stop(time=bstack1ll11l1l11_opy_(), duration=int(attrs.get(bstack1ll1_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ෯"), bstack1ll1_opy_ (u"ࠬ࠶ࠧ෰"))), result=bstack1l11111l1l_opy_)
                bstack1lllll1l1_opy_.bstack1l111l1l1l_opy_(bstack1ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ෱"), self._11llll1lll_opy_[bstack11llll1ll1_opy_][bstack1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪෲ")])
        else:
            bstack1l111l11l1_opy_ = current_test_id if current_test_id else bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪෳ"), None)
            if bstack1l111l11l1_opy_ and len(self.bstack1l1111l1ll_opy_) == 1:
                current_step_uuid = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭෴"), None)
                self._11llll1lll_opy_[bstack1l111l11l1_opy_][bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭෵")].bstack1l111l1111_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll1_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ෶"), bstack1ll1_opy_ (u"ࠬ࠶ࠧ෷"))), result=bstack1l11111l1l_opy_)
            else:
                self.bstack1l11111l11_opy_(attrs)
            self.bstack1l1111l1ll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll1_opy_ (u"࠭ࡨࡵ࡯࡯ࠫ෸"), bstack1ll1_opy_ (u"ࠧ࡯ࡱࠪ෹")) == bstack1ll1_opy_ (u"ࠨࡻࡨࡷࠬ෺"):
                return
            self.messages.push(message)
            bstack1l111l11ll_opy_ = []
            if bstack1lllll1l1_opy_.bstack11llllll1l_opy_():
                bstack1l111l11ll_opy_.append({
                    bstack1ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ෻"): bstack1ll11l1l11_opy_(),
                    bstack1ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ෼"): message.get(bstack1ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ෽")),
                    bstack1ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ෾"): message.get(bstack1ll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ෿")),
                    **bstack1lllll1l1_opy_.bstack11llllll1l_opy_()
                })
                if len(bstack1l111l11ll_opy_) > 0:
                    bstack1lllll1l1_opy_.bstack111ll1111_opy_(bstack1l111l11ll_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1lllll1l1_opy_.bstack1l1111llll_opy_()
    def bstack1l11111l11_opy_(self, bstack1l111ll111_opy_):
        if not bstack1lllll1l1_opy_.bstack11llllll1l_opy_():
            return
        kwname = bstack1ll1_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭฀").format(bstack1l111ll111_opy_.get(bstack1ll1_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨก")), bstack1l111ll111_opy_.get(bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧข"), bstack1ll1_opy_ (u"ࠪࠫฃ"))) if bstack1l111ll111_opy_.get(bstack1ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩค"), []) else bstack1l111ll111_opy_.get(bstack1ll1_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬฅ"))
        error_message = bstack1ll1_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧฆ").format(kwname, bstack1l111ll111_opy_.get(bstack1ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧง")), str(bstack1l111ll111_opy_.get(bstack1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩจ"))))
        bstack1l1111lll1_opy_ = bstack1ll1_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣฉ").format(kwname, bstack1l111ll111_opy_.get(bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪช")))
        bstack11lll111l1_opy_ = error_message if bstack1l111ll111_opy_.get(bstack1ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬซ")) else bstack1l1111lll1_opy_
        bstack11lll11l1l_opy_ = {
            bstack1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨฌ"): self.bstack1l1111l1ll_opy_[-1].get(bstack1ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪญ"), bstack1ll11l1l11_opy_()),
            bstack1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨฎ"): bstack11lll111l1_opy_,
            bstack1ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧฏ"): bstack1ll1_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨฐ") if bstack1l111ll111_opy_.get(bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪฑ")) == bstack1ll1_opy_ (u"ࠫࡋࡇࡉࡍࠩฒ") else bstack1ll1_opy_ (u"ࠬࡏࡎࡇࡑࠪณ"),
            **bstack1lllll1l1_opy_.bstack11llllll1l_opy_()
        }
        bstack1lllll1l1_opy_.bstack111ll1111_opy_([bstack11lll11l1l_opy_])
    def _11lll11lll_opy_(self):
        for bstack11lll1l11l_opy_ in reversed(self._11llll1lll_opy_):
            bstack11lll1llll_opy_ = bstack11lll1l11l_opy_
            data = self._11llll1lll_opy_[bstack11lll1l11l_opy_][bstack1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩด")]
            if isinstance(data, bstack11lll1ll1l_opy_):
                if not bstack1ll1_opy_ (u"ࠧࡆࡃࡆࡌࠬต") in data.bstack11lll11111_opy_():
                    return bstack11lll1llll_opy_
            else:
                return bstack11lll1llll_opy_
    def _1l1111ll11_opy_(self, messages):
        try:
            bstack1l11111111_opy_ = BuiltIn().get_variable_value(bstack1ll1_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢถ")) in (bstack11lll111ll_opy_.DEBUG, bstack11lll111ll_opy_.TRACE)
            for message, bstack11lll1l111_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪท"))
                level = message.get(bstack1ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩธ"))
                if level == bstack11lll111ll_opy_.FAIL:
                    self._1l1111111l_opy_ = name or self._1l1111111l_opy_
                    self._1l111l1lll_opy_ = bstack11lll1l111_opy_.get(bstack1ll1_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧน")) if bstack1l11111111_opy_ and bstack11lll1l111_opy_ else self._1l111l1lll_opy_
        except:
            pass
    @classmethod
    def bstack1l111l1l1l_opy_(self, event: str, bstack11llll1111_opy_: bstack11lllllll1_opy_, bstack1l111lll1l_opy_=False):
        if event == bstack1ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧบ"):
            bstack11llll1111_opy_.set(hooks=self.store[bstack1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪป")])
        if event == bstack1ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨผ"):
            event = bstack1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪฝ")
        if bstack1l111lll1l_opy_:
            bstack1l11111lll_opy_ = {
                bstack1ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭พ"): event,
                bstack11llll1111_opy_.bstack11lllll1l1_opy_(): bstack11llll1111_opy_.bstack1l111l111l_opy_(event)
            }
            self.bstack1l111ll11l_opy_.append(bstack1l11111lll_opy_)
        else:
            bstack1lllll1l1_opy_.bstack1l111l1l1l_opy_(event, bstack11llll1111_opy_)
class Messages:
    def __init__(self):
        self._11llll1l1l_opy_ = []
    def bstack11ll1lllll_opy_(self):
        self._11llll1l1l_opy_.append([])
    def bstack11lll1ll11_opy_(self):
        return self._11llll1l1l_opy_.pop() if self._11llll1l1l_opy_ else list()
    def push(self, message):
        self._11llll1l1l_opy_[-1].append(message) if self._11llll1l1l_opy_ else self._11llll1l1l_opy_.append([message])
class bstack11lll111ll_opy_:
    FAIL = bstack1ll1_opy_ (u"ࠪࡊࡆࡏࡌࠨฟ")
    ERROR = bstack1ll1_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪภ")
    WARNING = bstack1ll1_opy_ (u"ࠬ࡝ࡁࡓࡐࠪม")
    bstack11llllll11_opy_ = bstack1ll1_opy_ (u"࠭ࡉࡏࡈࡒࠫย")
    DEBUG = bstack1ll1_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭ร")
    TRACE = bstack1ll1_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧฤ")
    bstack11llllllll_opy_ = [FAIL, ERROR]
def bstack11llll11l1_opy_(bstack1l111111l1_opy_):
    if not bstack1l111111l1_opy_:
        return None
    if bstack1l111111l1_opy_.get(bstack1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬล"), None):
        return getattr(bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ฦ")], bstack1ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩว"), None)
    return bstack1l111111l1_opy_.get(bstack1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪศ"), None)
def bstack1l11111ll1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬษ"), bstack1ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩส")]:
        return
    if hook_type.lower() == bstack1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧห"):
        if current_test_uuid is None:
            return bstack1ll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ฬ")
        else:
            return bstack1ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨอ")
    elif hook_type.lower() == bstack1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ฮ"):
        if current_test_uuid is None:
            return bstack1ll1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨฯ")
        else:
            return bstack1ll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪะ")