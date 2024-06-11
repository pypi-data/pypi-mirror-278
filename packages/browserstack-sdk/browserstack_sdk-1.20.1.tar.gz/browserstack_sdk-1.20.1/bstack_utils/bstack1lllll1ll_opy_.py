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
class bstack1l1llll1l_opy_:
    def __init__(self, handler):
        self._1llll1111ll_opy_ = None
        self.handler = handler
        self._1llll1111l1_opy_ = self.bstack1llll111l11_opy_()
        self.patch()
    def patch(self):
        self._1llll1111ll_opy_ = self._1llll1111l1_opy_.execute
        self._1llll1111l1_opy_.execute = self.bstack1llll11111l_opy_()
    def bstack1llll11111l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥᒶ"), driver_command, None, this, args)
            response = self._1llll1111ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll1_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥᒷ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll1111l1_opy_.execute = self._1llll1111ll_opy_
    @staticmethod
    def bstack1llll111l11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver