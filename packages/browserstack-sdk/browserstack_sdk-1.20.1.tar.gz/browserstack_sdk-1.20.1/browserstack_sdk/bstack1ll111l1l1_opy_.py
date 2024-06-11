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
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11ll11ll_opy_ = {}
        bstack1l11l11111_opy_ = os.environ.get(bstack1ll1_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪാ"), bstack1ll1_opy_ (u"ࠪࠫി"))
        if not bstack1l11l11111_opy_:
            return bstack11ll11ll_opy_
        try:
            bstack1l11l1111l_opy_ = json.loads(bstack1l11l11111_opy_)
            if bstack1ll1_opy_ (u"ࠦࡴࡹࠢീ") in bstack1l11l1111l_opy_:
                bstack11ll11ll_opy_[bstack1ll1_opy_ (u"ࠧࡵࡳࠣു")] = bstack1l11l1111l_opy_[bstack1ll1_opy_ (u"ࠨ࡯ࡴࠤൂ")]
            if bstack1ll1_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦൃ") in bstack1l11l1111l_opy_ or bstack1ll1_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦൄ") in bstack1l11l1111l_opy_:
                bstack11ll11ll_opy_[bstack1ll1_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ൅")] = bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢെ"), bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢേ")))
            if bstack1ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨൈ") in bstack1l11l1111l_opy_ or bstack1ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ൉") in bstack1l11l1111l_opy_:
                bstack11ll11ll_opy_[bstack1ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧൊ")] = bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤോ"), bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢൌ")))
            if bstack1ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲ്ࠧ") in bstack1l11l1111l_opy_ or bstack1ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧൎ") in bstack1l11l1111l_opy_:
                bstack11ll11ll_opy_[bstack1ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ൏")] = bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ൐"), bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ൑")))
            if bstack1ll1_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣ൒") in bstack1l11l1111l_opy_ or bstack1ll1_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ൓") in bstack1l11l1111l_opy_:
                bstack11ll11ll_opy_[bstack1ll1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢൔ")] = bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦൕ"), bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤൖ")))
            if bstack1ll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣൗ") in bstack1l11l1111l_opy_ or bstack1ll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ൘") in bstack1l11l1111l_opy_:
                bstack11ll11ll_opy_[bstack1ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ൙")] = bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ൚"), bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ൛")))
            if bstack1ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ൜") in bstack1l11l1111l_opy_ or bstack1ll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ൝") in bstack1l11l1111l_opy_:
                bstack11ll11ll_opy_[bstack1ll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ൞")] = bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥൟ"), bstack1l11l1111l_opy_.get(bstack1ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥൠ")))
            if bstack1ll1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦൡ") in bstack1l11l1111l_opy_:
                bstack11ll11ll_opy_[bstack1ll1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧൢ")] = bstack1l11l1111l_opy_[bstack1ll1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨൣ")]
        except Exception as error:
            logger.error(bstack1ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦ൤") +  str(error))
        return bstack11ll11ll_opy_