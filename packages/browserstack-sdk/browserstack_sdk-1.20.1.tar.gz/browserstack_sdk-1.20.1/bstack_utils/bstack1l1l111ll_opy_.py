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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111l1l1l1l_opy_, bstack1l11lll11_opy_, bstack1ll1llll1l_opy_, bstack1ll1ll11_opy_, \
    bstack111l1l1l11_opy_
def bstack11llll11_opy_(bstack1llll111111_opy_):
    for driver in bstack1llll111111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11111l1ll_opy_(driver, status, reason=bstack1ll1_opy_ (u"ࠬ࠭ᒸ")):
    bstack111l1l1l1_opy_ = Config.bstack1lll11l1l1_opy_()
    if bstack111l1l1l1_opy_.bstack11ll1ll111_opy_():
        return
    bstack1111llll1_opy_ = bstack11l1lll1l_opy_(bstack1ll1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᒹ"), bstack1ll1_opy_ (u"ࠧࠨᒺ"), status, reason, bstack1ll1_opy_ (u"ࠨࠩᒻ"), bstack1ll1_opy_ (u"ࠩࠪᒼ"))
    driver.execute_script(bstack1111llll1_opy_)
def bstack1l1l1ll11l_opy_(page, status, reason=bstack1ll1_opy_ (u"ࠪࠫᒽ")):
    try:
        if page is None:
            return
        bstack111l1l1l1_opy_ = Config.bstack1lll11l1l1_opy_()
        if bstack111l1l1l1_opy_.bstack11ll1ll111_opy_():
            return
        bstack1111llll1_opy_ = bstack11l1lll1l_opy_(bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᒾ"), bstack1ll1_opy_ (u"ࠬ࠭ᒿ"), status, reason, bstack1ll1_opy_ (u"࠭ࠧᓀ"), bstack1ll1_opy_ (u"ࠧࠨᓁ"))
        page.evaluate(bstack1ll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᓂ"), bstack1111llll1_opy_)
    except Exception as e:
        print(bstack1ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢᓃ"), e)
def bstack11l1lll1l_opy_(type, name, status, reason, bstack1l1ll1l11l_opy_, bstack1l1lllllll_opy_):
    bstack11lll111l_opy_ = {
        bstack1ll1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᓄ"): type,
        bstack1ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᓅ"): {}
    }
    if type == bstack1ll1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᓆ"):
        bstack11lll111l_opy_[bstack1ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᓇ")][bstack1ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᓈ")] = bstack1l1ll1l11l_opy_
        bstack11lll111l_opy_[bstack1ll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᓉ")][bstack1ll1_opy_ (u"ࠩࡧࡥࡹࡧࠧᓊ")] = json.dumps(str(bstack1l1lllllll_opy_))
    if type == bstack1ll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᓋ"):
        bstack11lll111l_opy_[bstack1ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᓌ")][bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᓍ")] = name
    if type == bstack1ll1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᓎ"):
        bstack11lll111l_opy_[bstack1ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᓏ")][bstack1ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᓐ")] = status
        if status == bstack1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᓑ") and str(reason) != bstack1ll1_opy_ (u"ࠥࠦᓒ"):
            bstack11lll111l_opy_[bstack1ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᓓ")][bstack1ll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᓔ")] = json.dumps(str(reason))
    bstack1l11ll11l_opy_ = bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᓕ").format(json.dumps(bstack11lll111l_opy_))
    return bstack1l11ll11l_opy_
def bstack1ll11llll1_opy_(url, config, logger, bstack1ll111ll_opy_=False):
    hostname = bstack1l11lll11_opy_(url)
    is_private = bstack1ll1ll11_opy_(hostname)
    try:
        if is_private or bstack1ll111ll_opy_:
            file_path = bstack111l1l1l1l_opy_(bstack1ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᓖ"), bstack1ll1_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᓗ"), logger)
            if os.environ.get(bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᓘ")) and eval(
                    os.environ.get(bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᓙ"))):
                return
            if (bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᓚ") in config and not config[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᓛ")]):
                os.environ[bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᓜ")] = str(True)
                bstack1lll1llllll_opy_ = {bstack1ll1_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩᓝ"): hostname}
                bstack111l1l1l11_opy_(bstack1ll1_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᓞ"), bstack1ll1_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧᓟ"), bstack1lll1llllll_opy_, logger)
    except Exception as e:
        pass
def bstack1l11llll1_opy_(caps, bstack1lll1llll1l_opy_):
    if bstack1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᓠ") in caps:
        caps[bstack1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᓡ")][bstack1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᓢ")] = True
        if bstack1lll1llll1l_opy_:
            caps[bstack1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᓣ")][bstack1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᓤ")] = bstack1lll1llll1l_opy_
    else:
        caps[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ᓥ")] = True
        if bstack1lll1llll1l_opy_:
            caps[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᓦ")] = bstack1lll1llll1l_opy_
def bstack1llll1ll111_opy_(bstack1l111l1l11_opy_):
    bstack1lll1lllll1_opy_ = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᓧ"), bstack1ll1_opy_ (u"ࠫࠬᓨ"))
    if bstack1lll1lllll1_opy_ == bstack1ll1_opy_ (u"ࠬ࠭ᓩ") or bstack1lll1lllll1_opy_ == bstack1ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᓪ"):
        threading.current_thread().testStatus = bstack1l111l1l11_opy_
    else:
        if bstack1l111l1l11_opy_ == bstack1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᓫ"):
            threading.current_thread().testStatus = bstack1l111l1l11_opy_