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
class RobotHandler():
    def __init__(self, args, logger, bstack11ll1l1lll_opy_, bstack11ll1lll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1l1lll_opy_ = bstack11ll1l1lll_opy_
        self.bstack11ll1lll11_opy_ = bstack11ll1lll11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l111ll1l1_opy_(bstack11ll11l1ll_opy_):
        bstack11ll11ll11_opy_ = []
        if bstack11ll11l1ll_opy_:
            tokens = str(os.path.basename(bstack11ll11l1ll_opy_)).split(bstack1ll1_opy_ (u"ࠦࡤࠨ๑"))
            camelcase_name = bstack1ll1_opy_ (u"ࠧࠦࠢ๒").join(t.title() for t in tokens)
            suite_name, bstack11ll11lll1_opy_ = os.path.splitext(camelcase_name)
            bstack11ll11ll11_opy_.append(suite_name)
        return bstack11ll11ll11_opy_
    @staticmethod
    def bstack11ll11ll1l_opy_(typename):
        if bstack1ll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ๓") in typename:
            return bstack1ll1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ๔")
        return bstack1ll1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ๕")