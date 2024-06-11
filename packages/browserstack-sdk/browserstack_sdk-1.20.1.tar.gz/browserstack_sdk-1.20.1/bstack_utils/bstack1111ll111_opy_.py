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
import json
import requests
import logging
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l1ll1l11_opy_ as bstack11l1ll11l1_opy_
from bstack_utils.bstack1111l11ll_opy_ import bstack1111l11ll_opy_
from bstack_utils.helper import bstack1ll11l1l11_opy_, bstack1l111lllll_opy_, bstack1l11lll1l_opy_, bstack11l1ll1ll1_opy_, bstack11ll111l11_opy_, bstack1111ll1ll_opy_, get_host_info, bstack11l1l1llll_opy_, bstack1l1l11llll_opy_, bstack1l111lll11_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l111lll11_opy_(class_method=False)
def _11ll111lll_opy_(driver, bstack111l1l11l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll1_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪ๖"): caps.get(bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ๗"), None),
        bstack1ll1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๘"): bstack111l1l11l_opy_.get(bstack1ll1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๙"), None),
        bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬ๚"): caps.get(bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ๛"), None),
        bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ๜"): caps.get(bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ๝"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧ๞") + str(error))
  return response
def bstack111l1lll1_opy_(config):
  return config.get(bstack1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ๟"), False) or any([p.get(bstack1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ๠"), False) == True for p in config.get(bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ๡"), [])])
def bstack1ll1ll1111_opy_(config, bstack1lll1l1ll_opy_):
  try:
    if not bstack1l11lll1l_opy_(config):
      return False
    bstack11ll1111l1_opy_ = config.get(bstack1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ๢"), False)
    if int(bstack1lll1l1ll_opy_) < len(config.get(bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๣"), [])) and config[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ๤")][bstack1lll1l1ll_opy_]:
      bstack11ll11l111_opy_ = config[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭๥")][bstack1lll1l1ll_opy_].get(bstack1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ๦"), None)
    else:
      bstack11ll11l111_opy_ = config.get(bstack1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ๧"), None)
    if bstack11ll11l111_opy_ != None:
      bstack11ll1111l1_opy_ = bstack11ll11l111_opy_
    bstack11l1ll11ll_opy_ = os.getenv(bstack1ll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ๨")) is not None and len(os.getenv(bstack1ll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ๩"))) > 0 and os.getenv(bstack1ll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭๪")) != bstack1ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧ๫")
    return bstack11ll1111l1_opy_ and bstack11l1ll11ll_opy_
  except Exception as error:
    logger.debug(bstack1ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪ๬") + str(error))
  return False
def bstack1l11l1lll_opy_(bstack11l1lll1l1_opy_, test_tags):
  bstack11l1lll1l1_opy_ = os.getenv(bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ๭"))
  if bstack11l1lll1l1_opy_ is None:
    return True
  bstack11l1lll1l1_opy_ = json.loads(bstack11l1lll1l1_opy_)
  try:
    include_tags = bstack11l1lll1l1_opy_[bstack1ll1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ๮")] if bstack1ll1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ๯") in bstack11l1lll1l1_opy_ and isinstance(bstack11l1lll1l1_opy_[bstack1ll1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ๰")], list) else []
    exclude_tags = bstack11l1lll1l1_opy_[bstack1ll1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭๱")] if bstack1ll1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ๲") in bstack11l1lll1l1_opy_ and isinstance(bstack11l1lll1l1_opy_[bstack1ll1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ๳")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦ๴") + str(error))
  return False
def bstack1lll11ll1l_opy_(config, bstack11ll11l11l_opy_, bstack11l1lllll1_opy_, bstack11l1lll11l_opy_):
  bstack11l1ll1lll_opy_ = bstack11l1ll1ll1_opy_(config)
  bstack11ll11111l_opy_ = bstack11ll111l11_opy_(config)
  if bstack11l1ll1lll_opy_ is None or bstack11ll11111l_opy_ is None:
    logger.error(bstack1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭๵"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ๶"), bstack1ll1_opy_ (u"ࠧࡼࡿࠪ๷")))
    data = {
        bstack1ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭๸"): config[bstack1ll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ๹")],
        bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭๺"): config.get(bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๻"), os.path.basename(os.getcwd())),
        bstack1ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨ๼"): bstack1ll11l1l11_opy_(),
        bstack1ll1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ๽"): config.get(bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ๾"), bstack1ll1_opy_ (u"ࠨࠩ๿")),
        bstack1ll1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ຀"): {
            bstack1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪກ"): bstack11ll11l11l_opy_,
            bstack1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧຂ"): bstack11l1lllll1_opy_,
            bstack1ll1_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ຃"): __version__,
            bstack1ll1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨຄ"): bstack1ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ຅"),
            bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨຆ"): bstack1ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫງ"),
            bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪຈ"): bstack11l1lll11l_opy_
        },
        bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ຉ"): settings,
        bstack1ll1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡉ࡯࡯ࡶࡵࡳࡱ࠭ຊ"): bstack11l1l1llll_opy_(),
        bstack1ll1_opy_ (u"࠭ࡣࡪࡋࡱࡪࡴ࠭຋"): bstack1111ll1ll_opy_(),
        bstack1ll1_opy_ (u"ࠧࡩࡱࡶࡸࡎࡴࡦࡰࠩຌ"): get_host_info(),
        bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪຍ"): bstack1l11lll1l_opy_(config)
    }
    headers = {
        bstack1ll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨຎ"): bstack1ll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ຏ"),
    }
    config = {
        bstack1ll1_opy_ (u"ࠫࡦࡻࡴࡩࠩຐ"): (bstack11l1ll1lll_opy_, bstack11ll11111l_opy_),
        bstack1ll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ຑ"): headers
    }
    response = bstack1l1l11llll_opy_(bstack1ll1_opy_ (u"࠭ࡐࡐࡕࡗࠫຒ"), bstack11l1ll11l1_opy_ + bstack1ll1_opy_ (u"ࠧ࠰ࡸ࠵࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹࠧຓ"), data, config)
    bstack11l1ll1l1l_opy_ = response.json()
    if bstack11l1ll1l1l_opy_[bstack1ll1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩດ")]:
      parsed = json.loads(os.getenv(bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪຕ"), bstack1ll1_opy_ (u"ࠪࡿࢂ࠭ຖ")))
      parsed[bstack1ll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬທ")] = bstack11l1ll1l1l_opy_[bstack1ll1_opy_ (u"ࠬࡪࡡࡵࡣࠪຘ")][bstack1ll1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧນ")]
      os.environ[bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨບ")] = json.dumps(parsed)
      bstack1111l11ll_opy_.bstack11ll111ll1_opy_(bstack11l1ll1l1l_opy_[bstack1ll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ປ")][bstack1ll1_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪຜ")])
      bstack1111l11ll_opy_.bstack11ll111l1l_opy_(bstack11l1ll1l1l_opy_[bstack1ll1_opy_ (u"ࠪࡨࡦࡺࡡࠨຝ")][bstack1ll1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ພ")])
      bstack1111l11ll_opy_.store()
      return bstack11l1ll1l1l_opy_[bstack1ll1_opy_ (u"ࠬࡪࡡࡵࡣࠪຟ")][bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫຠ")], bstack11l1ll1l1l_opy_[bstack1ll1_opy_ (u"ࠧࡥࡣࡷࡥࠬມ")][bstack1ll1_opy_ (u"ࠨ࡫ࡧࠫຢ")]
    else:
      logger.error(bstack1ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪຣ") + bstack11l1ll1l1l_opy_[bstack1ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ຤")])
      if bstack11l1ll1l1l_opy_[bstack1ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬລ")] == bstack1ll1_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧ຦"):
        for bstack11l1lll111_opy_ in bstack11l1ll1l1l_opy_[bstack1ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ວ")]:
          logger.error(bstack11l1lll111_opy_[bstack1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຨ")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤຩ") +  str(error))
    return None, None
def bstack1l11l1l1l_opy_():
  if os.getenv(bstack1ll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧສ")) is None:
    return {
        bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪຫ"): bstack1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪຬ"),
        bstack1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ອ"): bstack1ll1_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬຮ")
    }
  data = {bstack1ll1_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨຯ"): bstack1ll11l1l11_opy_()}
  headers = {
      bstack1ll1_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨະ"): bstack1ll1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪັ") + os.getenv(bstack1ll1_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣາ")),
      bstack1ll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪຳ"): bstack1ll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨິ")
  }
  response = bstack1l1l11llll_opy_(bstack1ll1_opy_ (u"࠭ࡐࡖࡖࠪີ"), bstack11l1ll11l1_opy_ + bstack1ll1_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩຶ"), data, { bstack1ll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩື"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵຸࠢࠥ") + bstack1l111lllll_opy_().isoformat() + bstack1ll1_opy_ (u"ࠪ࡞ູࠬ"))
      return {bstack1ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶ຺ࠫ"): bstack1ll1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ົ"), bstack1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧຼ"): bstack1ll1_opy_ (u"ࠧࠨຽ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦ຾") + str(error))
    return {
        bstack1ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ຿"): bstack1ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩເ"),
        bstack1ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬແ"): str(error)
    }
def bstack1l11ll1l_opy_(caps, options, desired_capabilities={}):
  try:
    bstack11l1ll1111_opy_ = caps.get(bstack1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ໂ"), {}).get(bstack1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪໃ"), caps.get(bstack1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧໄ"), bstack1ll1_opy_ (u"ࠨࠩ໅")))
    if bstack11l1ll1111_opy_:
      logger.warn(bstack1ll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨໆ"))
      return False
    if options:
      bstack11l1llllll_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack11l1llllll_opy_ = desired_capabilities
    else:
      bstack11l1llllll_opy_ = {}
    browser = caps.get(bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ໇"), bstack1ll1_opy_ (u"່ࠫࠬ")).lower() or bstack11l1llllll_opy_.get(bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧ້ࠪ"), bstack1ll1_opy_ (u"໊࠭ࠧ")).lower()
    if browser != bstack1ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫໋ࠧ"):
      logger.warn(bstack1ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ໌"))
      return False
    browser_version = caps.get(bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪໍ")) or caps.get(bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ໎")) or bstack11l1llllll_opy_.get(bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ໏")) or bstack11l1llllll_opy_.get(bstack1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭໐"), {}).get(bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ໑")) or bstack11l1llllll_opy_.get(bstack1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ໒"), {}).get(bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ໓"))
    if browser_version and browser_version != bstack1ll1_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩ໔") and int(browser_version.split(bstack1ll1_opy_ (u"ࠪ࠲ࠬ໕"))[0]) <= 94:
      logger.warn(bstack1ll1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠴࠯ࠤ໖"))
      return False
    if not options is None:
      bstack11l1lll1ll_opy_ = bstack11l1llllll_opy_.get(bstack1ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ໗"), {})
      if bstack1ll1_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪ໘") in bstack11l1lll1ll_opy_.get(bstack1ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬ໙"), []):
        logger.warn(bstack1ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥ໚"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦ໛") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l1l1lll1_opy_ = config.get(bstack1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪໜ"), {})
    bstack11l1l1lll1_opy_[bstack1ll1_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧໝ")] = os.getenv(bstack1ll1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪໞ"))
    bstack11l1llll1l_opy_ = json.loads(os.getenv(bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧໟ"), bstack1ll1_opy_ (u"ࠧࡼࡿࠪ໠"))).get(bstack1ll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ໡"))
    caps[bstack1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ໢")] = True
    if bstack1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ໣") in caps:
      caps[bstack1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ໤")][bstack1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ໥")] = bstack11l1l1lll1_opy_
      caps[bstack1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ໦")][bstack1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ໧")][bstack1ll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ໨")] = bstack11l1llll1l_opy_
    else:
      caps[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ໩")] = bstack11l1l1lll1_opy_
      caps[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ໪")][bstack1ll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ໫")] = bstack11l1llll1l_opy_
  except Exception as error:
    logger.debug(bstack1ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨ໬") +  str(error))
def bstack1111lll1l_opy_(driver, bstack11ll1111ll_opy_):
  try:
    setattr(driver, bstack1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭໭"), True)
    session = driver.session_id
    if session:
      bstack11l1llll11_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1llll11_opy_ = False
      bstack11l1llll11_opy_ = url.scheme in [bstack1ll1_opy_ (u"ࠢࡩࡶࡷࡴࠧ໮"), bstack1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ໯")]
      if bstack11l1llll11_opy_:
        if bstack11ll1111ll_opy_:
          logger.info(bstack1ll1_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡨࡲࡶࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲ࠥࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡧ࡫ࡧࡪࡰࠣࡱࡴࡳࡥ࡯ࡶࡤࡶ࡮ࡲࡹ࠯ࠤ໰"))
      return bstack11ll1111ll_opy_
  except Exception as e:
    logger.error(bstack1ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨ໱") + str(e))
    return False
def bstack1ll11l11ll_opy_(driver, class_name, name, module_name, path, bstack111l1l11l_opy_):
  try:
    bstack11ll11llll_opy_ = [class_name] if not class_name is None else []
    bstack11ll111111_opy_ = {
        bstack1ll1_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤ໲"): True,
        bstack1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡇࡩࡹࡧࡩ࡭ࡵࠥ໳"): {
            bstack1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ໴"): name,
            bstack1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡗࡻ࡮ࡊࡦࠥ໵"): os.environ.get(bstack1ll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡗࡉࡘ࡚࡟ࡓࡗࡑࡣࡎࡊࠧ໶")),
            bstack1ll1_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡐࡢࡶ࡫ࠦ໷"): str(path),
            bstack1ll1_opy_ (u"ࠥࡷࡨࡵࡰࡦࡎ࡬ࡷࡹࠨ໸"): [module_name, *bstack11ll11llll_opy_, name],
        },
        bstack1ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ໹"): _11ll111lll_opy_(driver, bstack111l1l11l_opy_)
    }
    logger.debug(bstack1ll1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨ໺"))
    logger.debug(driver.execute_async_script(bstack1111l11ll_opy_.perform_scan, {bstack1ll1_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨ໻"): name}))
    logger.debug(driver.execute_async_script(bstack1111l11ll_opy_.bstack11l1ll111l_opy_, bstack11ll111111_opy_))
    logger.info(bstack1ll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥ໼"))
  except Exception as bstack11ll11l1l1_opy_:
    logger.error(bstack1ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥ໽") + str(path) + bstack1ll1_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦ໾") + str(bstack11ll11l1l1_opy_))