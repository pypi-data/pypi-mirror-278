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
from browserstack_sdk.bstack1l1ll11l1l_opy_ import bstack1l1111l11_opy_
from browserstack_sdk.bstack1l111llll1_opy_ import RobotHandler
def bstack1ll1l1lll_opy_(framework):
    if framework.lower() == bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᆯ"):
        return bstack1l1111l11_opy_.version()
    elif framework.lower() == bstack1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᆰ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᆱ"):
        import behave
        return behave.__version__
    else:
        return bstack1ll1_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᆲ")