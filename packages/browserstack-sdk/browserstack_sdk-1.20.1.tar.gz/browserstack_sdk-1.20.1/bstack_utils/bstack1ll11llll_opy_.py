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
import re
from bstack_utils.bstack1l1l111ll_opy_ import bstack1llll1ll111_opy_
def bstack1llll1llll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒃ")):
        return bstack1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᒄ")
    elif fixture_name.startswith(bstack1ll1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒅ")):
        return bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᒆ")
    elif fixture_name.startswith(bstack1ll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒇ")):
        return bstack1ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᒈ")
    elif fixture_name.startswith(bstack1ll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᒉ")):
        return bstack1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᒊ")
def bstack1llll1ll1ll_opy_(fixture_name):
    return bool(re.match(bstack1ll1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᒋ"), fixture_name))
def bstack1llll1l111l_opy_(fixture_name):
    return bool(re.match(bstack1ll1_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᒌ"), fixture_name))
def bstack1llll1lll1l_opy_(fixture_name):
    return bool(re.match(bstack1ll1_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᒍ"), fixture_name))
def bstack1llll1l1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᒎ")):
        return bstack1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᒏ"), bstack1ll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᒐ")
    elif fixture_name.startswith(bstack1ll1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᒑ")):
        return bstack1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᒒ"), bstack1ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᒓ")
    elif fixture_name.startswith(bstack1ll1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᒔ")):
        return bstack1ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᒕ"), bstack1ll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᒖ")
    elif fixture_name.startswith(bstack1ll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒗ")):
        return bstack1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᒘ"), bstack1ll1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᒙ")
    return None, None
def bstack1llll1ll1l1_opy_(hook_name):
    if hook_name in [bstack1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᒚ"), bstack1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᒛ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llll1l11ll_opy_(hook_name):
    if hook_name in [bstack1ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᒜ"), bstack1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᒝ")]:
        return bstack1ll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᒞ")
    elif hook_name in [bstack1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᒟ"), bstack1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᒠ")]:
        return bstack1ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᒡ")
    elif hook_name in [bstack1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᒢ"), bstack1ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᒣ")]:
        return bstack1ll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᒤ")
    elif hook_name in [bstack1ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᒥ"), bstack1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᒦ")]:
        return bstack1ll1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᒧ")
    return hook_name
def bstack1llll1l11l1_opy_(node, scenario):
    if hasattr(node, bstack1ll1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᒨ")):
        parts = node.nodeid.rsplit(bstack1ll1_opy_ (u"ࠦࡠࠨᒩ"))
        params = parts[-1]
        return bstack1ll1_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᒪ").format(scenario.name, params)
    return scenario.name
def bstack1llll1lll11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll1_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᒫ")):
            examples = list(node.callspec.params[bstack1ll1_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᒬ")].values())
        return examples
    except:
        return []
def bstack1llll1l1l11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llll1l1l1l_opy_(report):
    try:
        status = bstack1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᒭ")
        if report.passed or (report.failed and hasattr(report, bstack1ll1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᒮ"))):
            status = bstack1ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᒯ")
        elif report.skipped:
            status = bstack1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᒰ")
        bstack1llll1ll111_opy_(status)
    except:
        pass
def bstack1ll1l11l1l_opy_(status):
    try:
        bstack1llll1l1lll_opy_ = bstack1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᒱ")
        if status == bstack1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᒲ"):
            bstack1llll1l1lll_opy_ = bstack1ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᒳ")
        elif status == bstack1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᒴ"):
            bstack1llll1l1lll_opy_ = bstack1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᒵ")
        bstack1llll1ll111_opy_(bstack1llll1l1lll_opy_)
    except:
        pass
def bstack1llll1ll11l_opy_(item=None, report=None, summary=None, extra=None):
    return