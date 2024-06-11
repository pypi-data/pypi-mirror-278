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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1111ll111_opy_ as bstack1111111l1_opy_
from browserstack_sdk.bstack1l1lll111_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11lll111_opy_
class bstack1l1111l11_opy_:
    def __init__(self, args, logger, bstack11ll1l1lll_opy_, bstack11ll1lll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1l1lll_opy_ = bstack11ll1l1lll_opy_
        self.bstack11ll1lll11_opy_ = bstack11ll1lll11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1l11l11_opy_ = []
        self.bstack11ll1ll1ll_opy_ = None
        self.bstack1l1l1l11l_opy_ = []
        self.bstack11ll1l11ll_opy_ = self.bstack11lll11l1_opy_()
        self.bstack1llll11111_opy_ = -1
    def bstack1l1l11lll_opy_(self, bstack11ll1l1111_opy_):
        self.parse_args()
        self.bstack11ll1ll11l_opy_()
        self.bstack11ll1l1l1l_opy_(bstack11ll1l1111_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11ll1l11l1_opy_():
        import importlib
        if getattr(importlib, bstack1ll1_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬั"), False):
            bstack11ll1ll1l1_opy_ = importlib.find_loader(bstack1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪา"))
        else:
            bstack11ll1ll1l1_opy_ = importlib.util.find_spec(bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫำ"))
    def bstack11ll1l1ll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1llll11111_opy_ = -1
        if self.bstack11ll1lll11_opy_ and bstack1ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪิ") in self.bstack11ll1l1lll_opy_:
            self.bstack1llll11111_opy_ = int(self.bstack11ll1l1lll_opy_[bstack1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫี")])
        try:
            bstack11ll1l111l_opy_ = [bstack1ll1_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧึ"), bstack1ll1_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩื"), bstack1ll1_opy_ (u"ࠧ࠮ࡲุࠪ")]
            if self.bstack1llll11111_opy_ >= 0:
                bstack11ll1l111l_opy_.extend([bstack1ll1_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴูࠩ"), bstack1ll1_opy_ (u"ࠩ࠰ࡲฺࠬ")])
            for arg in bstack11ll1l111l_opy_:
                self.bstack11ll1l1ll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11ll1ll11l_opy_(self):
        bstack11ll1ll1ll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11ll1ll1ll_opy_ = bstack11ll1ll1ll_opy_
        return bstack11ll1ll1ll_opy_
    def bstack1ll11ll111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11ll1l11l1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l11lll111_opy_)
    def bstack11ll1l1l1l_opy_(self, bstack11ll1l1111_opy_):
        bstack111l1l1l1_opy_ = Config.bstack1lll11l1l1_opy_()
        if bstack11ll1l1111_opy_:
            self.bstack11ll1ll1ll_opy_.append(bstack1ll1_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ฻"))
            self.bstack11ll1ll1ll_opy_.append(bstack1ll1_opy_ (u"࡙ࠫࡸࡵࡦࠩ฼"))
        if bstack111l1l1l1_opy_.bstack11ll1ll111_opy_():
            self.bstack11ll1ll1ll_opy_.append(bstack1ll1_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ฽"))
            self.bstack11ll1ll1ll_opy_.append(bstack1ll1_opy_ (u"࠭ࡔࡳࡷࡨࠫ฾"))
        self.bstack11ll1ll1ll_opy_.append(bstack1ll1_opy_ (u"ࠧ࠮ࡲࠪ฿"))
        self.bstack11ll1ll1ll_opy_.append(bstack1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭เ"))
        self.bstack11ll1ll1ll_opy_.append(bstack1ll1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫแ"))
        self.bstack11ll1ll1ll_opy_.append(bstack1ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪโ"))
        if self.bstack1llll11111_opy_ > 1:
            self.bstack11ll1ll1ll_opy_.append(bstack1ll1_opy_ (u"ࠫ࠲ࡴࠧใ"))
            self.bstack11ll1ll1ll_opy_.append(str(self.bstack1llll11111_opy_))
    def bstack11ll1lll1l_opy_(self):
        bstack1l1l1l11l_opy_ = []
        for spec in self.bstack1l1l11l11_opy_:
            bstack11l1111ll_opy_ = [spec]
            bstack11l1111ll_opy_ += self.bstack11ll1ll1ll_opy_
            bstack1l1l1l11l_opy_.append(bstack11l1111ll_opy_)
        self.bstack1l1l1l11l_opy_ = bstack1l1l1l11l_opy_
        return bstack1l1l1l11l_opy_
    def bstack11lll11l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11ll1l11ll_opy_ = True
            return True
        except Exception as e:
            self.bstack11ll1l11ll_opy_ = False
        return self.bstack11ll1l11ll_opy_
    def bstack1lll111ll_opy_(self, bstack11ll1l1l11_opy_, bstack1l1l11lll_opy_):
        bstack1l1l11lll_opy_[bstack1ll1_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬไ")] = self.bstack11ll1l1lll_opy_
        multiprocessing.set_start_method(bstack1ll1_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬๅ"))
        bstack11l1ll1ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll1111lll_opy_ = manager.list()
        if bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪๆ") in self.bstack11ll1l1lll_opy_:
            for index, platform in enumerate(self.bstack11ll1l1lll_opy_[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ็")]):
                bstack11l1ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11ll1l1l11_opy_,
                                                            args=(self.bstack11ll1ll1ll_opy_, bstack1l1l11lll_opy_, bstack1ll1111lll_opy_)))
            bstack11ll1llll1_opy_ = len(self.bstack11ll1l1lll_opy_[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ่ࠬ")])
        else:
            bstack11l1ll1ll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11ll1l1l11_opy_,
                                                        args=(self.bstack11ll1ll1ll_opy_, bstack1l1l11lll_opy_, bstack1ll1111lll_opy_)))
            bstack11ll1llll1_opy_ = 1
        i = 0
        for t in bstack11l1ll1ll_opy_:
            os.environ[bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ้࡚ࠪ")] = str(i)
            if bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ๊ࠧ") in self.bstack11ll1l1lll_opy_:
                os.environ[bstack1ll1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ๋࠭")] = json.dumps(self.bstack11ll1l1lll_opy_[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ์")][i % bstack11ll1llll1_opy_])
            i += 1
            t.start()
        for t in bstack11l1ll1ll_opy_:
            t.join()
        return list(bstack1ll1111lll_opy_)
    @staticmethod
    def bstack1l1l11l1l_opy_(driver, bstack111l1l11l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫํ"), None)
        if item and getattr(item, bstack1ll1_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࠪ๎"), None) and not getattr(item, bstack1ll1_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡳࡵࡥࡤࡰࡰࡨࠫ๏"), False):
            logger.info(
                bstack1ll1_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠤ๐"))
            bstack11ll11llll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1111111l1_opy_.bstack1ll11l11ll_opy_(driver, bstack11ll11llll_opy_, item.name, item.module.__name__, item.path, bstack111l1l11l_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)