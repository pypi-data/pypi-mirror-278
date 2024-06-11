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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11l1l1llll_opy_, bstack1111ll1ll_opy_, get_host_info, bstack11l1ll1ll1_opy_, bstack11ll111l11_opy_, bstack111llll111_opy_, bstack1l111lllll_opy_, \
    bstack111l1l1111_opy_, bstack11l11l11ll_opy_, bstack1l1l11llll_opy_, bstack111ll1lll1_opy_, bstack1llll1l1ll_opy_, bstack1l111lll11_opy_, bstack1l1ll11l11_opy_, bstack1ll11l1l11_opy_
from bstack_utils.bstack1llll111ll1_opy_ import bstack1llll111lll_opy_
from bstack_utils.bstack11lll11l11_opy_ import bstack11lllllll1_opy_
import bstack_utils.bstack1111ll111_opy_ as bstack1111111l1_opy_
from bstack_utils.constants import bstack11l11l1l1l_opy_
bstack1lll1l11lll_opy_ = [
    bstack1ll1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᔪ"), bstack1ll1_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᔫ"), bstack1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᔬ"), bstack1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᔭ"),
    bstack1ll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᔮ"), bstack1ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᔯ"), bstack1ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᔰ")
]
bstack1lll1l1111l_opy_ = bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᔱ")
logger = logging.getLogger(__name__)
class bstack1lllll1l1_opy_:
    bstack1llll111ll1_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l111lll11_opy_(class_method=True)
    def launch(cls, bs_config, bstack1lll11ll1l1_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll1l11l1l_opy_()
        bstack11l1ll1lll_opy_ = bstack11l1ll1ll1_opy_(bs_config)
        bstack11ll11111l_opy_ = bstack11ll111l11_opy_(bs_config)
        bstack11l11ll11_opy_ = False
        bstack1111l11l_opy_ = False
        if bstack1ll1_opy_ (u"ࠨࡣࡳࡴࠬᔲ") in bs_config:
            bstack11l11ll11_opy_ = True
        else:
            bstack1111l11l_opy_ = True
        bstack1l11ll1ll1_opy_ = {
            bstack1ll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᔳ"): cls.bstack1l1lllll1_opy_(bstack1lll11ll1l1_opy_.get(bstack1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫᔴ"), bstack1ll1_opy_ (u"ࠫࠬᔵ"))),
            bstack1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᔶ"): bstack1111111l1_opy_.bstack111l1lll1_opy_(bs_config),
            bstack1ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᔷ"): bs_config.get(bstack1ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᔸ"), False),
            bstack1ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᔹ"): bstack1111l11l_opy_,
            bstack1ll1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨᔺ"): bstack11l11ll11_opy_
        }
        data = {
            bstack1ll1_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪᔻ"): bstack1ll1_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩᔼ"),
            bstack1ll1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫᔽ"): bs_config.get(bstack1ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᔾ"), bstack1ll1_opy_ (u"ࠧࠨᔿ")),
            bstack1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᕀ"): bs_config.get(bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᕁ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᕂ"): bs_config.get(bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᕃ")),
            bstack1ll1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᕄ"): bs_config.get(bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᕅ"), bstack1ll1_opy_ (u"ࠧࠨᕆ")),
            bstack1ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺ࡟ࡵ࡫ࡰࡩࠬᕇ"): datetime.datetime.now().isoformat(),
            bstack1ll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᕈ"): bstack111llll111_opy_(bs_config),
            bstack1ll1_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭ᕉ"): get_host_info(),
            bstack1ll1_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬᕊ"): bstack1111ll1ll_opy_(),
            bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᕋ"): os.environ.get(bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬᕌ")),
            bstack1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬᕍ"): os.environ.get(bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ᕎ"), False),
            bstack1ll1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫᕏ"): bstack11l1l1llll_opy_(),
            bstack1ll1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨᕐ"): bstack1l11ll1ll1_opy_,
            bstack1ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᕑ"): {
                bstack1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᕒ"): bstack1lll11ll1l1_opy_.get(bstack1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧᕓ"), bstack1ll1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᕔ")),
                bstack1ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᕕ"): bstack1lll11ll1l1_opy_.get(bstack1ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᕖ")),
                bstack1ll1_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᕗ"): bstack1lll11ll1l1_opy_.get(bstack1ll1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᕘ"))
            }
        }
        config = {
            bstack1ll1_opy_ (u"ࠬࡧࡵࡵࡪࠪᕙ"): (bstack11l1ll1lll_opy_, bstack11ll11111l_opy_),
            bstack1ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᕚ"): cls.default_headers()
        }
        response = bstack1l1l11llll_opy_(bstack1ll1_opy_ (u"ࠧࡑࡑࡖࡘࠬᕛ"), cls.request_url(bstack1ll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳࠨᕜ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᕝ")] = bstack1ll1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᕞ")
            os.environ[bstack1ll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪᕟ")] = bstack1ll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᕠ")
            os.environ[bstack1ll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᕡ")] = bstack1ll1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᕢ")
            os.environ[bstack1ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᕣ")] = bstack1ll1_opy_ (u"ࠤࡱࡹࡱࡲࠢᕤ")
            os.environ[bstack1ll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᕥ")] = bstack1ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᕦ")
            bstack1lll11llll1_opy_ = response.json()
            if bstack1lll11llll1_opy_ and bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕧ")]:
                error_message = bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕨ")]
                if bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࡚ࡹࡱࡧࠪᕩ")] == bstack1ll1_opy_ (u"ࠨࡇࡕࡖࡔࡘ࡟ࡊࡐ࡙ࡅࡑࡏࡄࡠࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘ࠭ᕪ"):
                    logger.error(error_message)
                elif bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᕫ")] == bstack1ll1_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠩᕬ"):
                    logger.info(error_message)
                elif bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᕭ")] == bstack1ll1_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡘࡊࡋࡠࡆࡈࡔࡗࡋࡃࡂࡖࡈࡈࠬᕮ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1ll1_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᕯ"))
            return [None, None, None]
        bstack1lll11llll1_opy_ = response.json()
        os.environ[bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᕰ")] = bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᕱ")]
        if cls.bstack1l1lllll1_opy_(bstack1lll11ll1l1_opy_.get(bstack1ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪᕲ"), bstack1ll1_opy_ (u"ࠪࠫᕳ"))) is True:
            logger.debug(bstack1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨᕴ"))
            os.environ[bstack1ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫᕵ")] = bstack1ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫᕶ")
            if bstack1lll11llll1_opy_.get(bstack1ll1_opy_ (u"ࠧ࡫ࡹࡷࠫᕷ")):
                os.environ[bstack1ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᕸ")] = bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"ࠩ࡭ࡻࡹ࠭ᕹ")]
                os.environ[bstack1ll1_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧᕺ")] = json.dumps({
                    bstack1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭ᕻ"): bstack11l1ll1lll_opy_,
                    bstack1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧᕼ"): bstack11ll11111l_opy_
                })
            if bstack1lll11llll1_opy_.get(bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᕽ")):
                os.environ[bstack1ll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᕾ")] = bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᕿ")]
            if bstack1lll11llll1_opy_.get(bstack1ll1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᖀ")):
                os.environ[bstack1ll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᖁ")] = str(bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᖂ")])
        return [bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"ࠬࡰࡷࡵࠩᖃ")], bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᖄ")], bstack1lll11llll1_opy_[bstack1ll1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᖅ")]]
    @classmethod
    @bstack1l111lll11_opy_(class_method=True)
    def stop(cls, bstack1lll11lll11_opy_ = None):
        if not cls.on():
            return
        if os.environ[bstack1ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᖆ")] == bstack1ll1_opy_ (u"ࠤࡱࡹࡱࡲࠢᖇ") or os.environ[bstack1ll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᖈ")] == bstack1ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᖉ"):
            print(bstack1ll1_opy_ (u"ࠬࡋࡘࡄࡇࡓࡘࡎࡕࡎࠡࡋࡑࠤࡸࡺ࡯ࡱࡄࡸ࡭ࡱࡪࡕࡱࡵࡷࡶࡪࡧ࡭ࠡࡔࡈࡕ࡚ࡋࡓࡕࠢࡗࡓ࡚ࠥࡅࡔࡖࠣࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠣ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ᖊ"))
            return {
                bstack1ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᖋ"): bstack1ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᖌ"),
                bstack1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖍ"): bstack1ll1_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧᖎ")
            }
        else:
            cls.bstack1llll111ll1_opy_.shutdown()
            data = {
                bstack1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᖏ"): bstack1ll11l1l11_opy_()
            }
            if not bstack1lll11lll11_opy_ is None:
                data[bstack1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨᖐ")] = [{
                    bstack1ll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᖑ"): bstack1ll1_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫᖒ"),
                    bstack1ll1_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧᖓ"): bstack1lll11lll11_opy_
                }]
            config = {
                bstack1ll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᖔ"): cls.default_headers()
            }
            bstack11l11111l1_opy_ = bstack1ll1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪᖕ").format(os.environ[bstack1ll1_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠤᖖ")])
            bstack1lll11ll11l_opy_ = cls.request_url(bstack11l11111l1_opy_)
            response = bstack1l1l11llll_opy_(bstack1ll1_opy_ (u"ࠫࡕ࡛ࡔࠨᖗ"), bstack1lll11ll11l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1ll1_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦᖘ"))
    @classmethod
    def bstack1l1111llll_opy_(cls):
        if cls.bstack1llll111ll1_opy_ is None:
            return
        cls.bstack1llll111ll1_opy_.shutdown()
    @classmethod
    def bstack11l1l11l1_opy_(cls):
        if cls.on():
            print(
                bstack1ll1_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩᖙ").format(os.environ[bstack1ll1_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨᖚ")]))
    @classmethod
    def bstack1lll1l11l1l_opy_(cls):
        if cls.bstack1llll111ll1_opy_ is not None:
            return
        cls.bstack1llll111ll1_opy_ = bstack1llll111lll_opy_(cls.bstack1lll1l11ll1_opy_)
        cls.bstack1llll111ll1_opy_.start()
    @classmethod
    def bstack11llll111l_opy_(cls, bstack11llll1111_opy_, bstack1lll1l11l11_opy_=bstack1ll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᖛ")):
        if not cls.on():
            return
        bstack1llll1l11l_opy_ = bstack11llll1111_opy_[bstack1ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᖜ")]
        bstack1lll11l1l1l_opy_ = {
            bstack1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᖝ"): bstack1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡖࡸࡦࡸࡴࡠࡗࡳࡰࡴࡧࡤࠨᖞ"),
            bstack1ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᖟ"): bstack1ll1_opy_ (u"࠭ࡔࡦࡵࡷࡣࡊࡴࡤࡠࡗࡳࡰࡴࡧࡤࠨᖠ"),
            bstack1ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᖡ"): bstack1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡥࡓ࡬࡫ࡳࡴࡪࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᖢ"),
            bstack1ll1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᖣ"): bstack1ll1_opy_ (u"ࠪࡐࡴ࡭࡟ࡖࡲ࡯ࡳࡦࡪࠧᖤ"),
            bstack1ll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᖥ"): bstack1ll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡗࡹࡧࡲࡵࡡࡘࡴࡱࡵࡡࡥࠩᖦ"),
            bstack1ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᖧ"): bstack1ll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡤࡋ࡮ࡥࡡࡘࡴࡱࡵࡡࡥࠩᖨ"),
            bstack1ll1_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᖩ"): bstack1ll1_opy_ (u"ࠩࡆࡆ࡙ࡥࡕࡱ࡮ࡲࡥࡩ࠭ᖪ")
        }.get(bstack1llll1l11l_opy_)
        if bstack1lll1l11l11_opy_ == bstack1ll1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᖫ"):
            cls.bstack1lll1l11l1l_opy_()
            cls.bstack1llll111ll1_opy_.add(bstack11llll1111_opy_)
        elif bstack1lll1l11l11_opy_ == bstack1ll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᖬ"):
            cls.bstack1lll1l11ll1_opy_([bstack11llll1111_opy_], bstack1lll1l11l11_opy_)
    @classmethod
    @bstack1l111lll11_opy_(class_method=True)
    def bstack1lll1l11ll1_opy_(cls, bstack11llll1111_opy_, bstack1lll1l11l11_opy_=bstack1ll1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᖭ")):
        config = {
            bstack1ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᖮ"): cls.default_headers()
        }
        response = bstack1l1l11llll_opy_(bstack1ll1_opy_ (u"ࠧࡑࡑࡖࡘࠬᖯ"), cls.request_url(bstack1lll1l11l11_opy_), bstack11llll1111_opy_, config)
        bstack11l1ll1l1l_opy_ = response.json()
    @classmethod
    @bstack1l111lll11_opy_(class_method=True)
    def bstack111ll1111_opy_(cls, bstack1l111l11ll_opy_):
        bstack1lll11lllll_opy_ = []
        for log in bstack1l111l11ll_opy_:
            bstack1lll11lll1l_opy_ = {
                bstack1ll1_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ᖰ"): bstack1ll1_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫᖱ"),
                bstack1ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᖲ"): log[bstack1ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᖳ")],
                bstack1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᖴ"): log[bstack1ll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᖵ")],
                bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧᖶ"): {},
                bstack1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖷ"): log[bstack1ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖸ")],
            }
            if bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖹ") in log:
                bstack1lll11lll1l_opy_[bstack1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖺ")] = log[bstack1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖻ")]
            elif bstack1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖼ") in log:
                bstack1lll11lll1l_opy_[bstack1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖽ")] = log[bstack1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖾ")]
            bstack1lll11lllll_opy_.append(bstack1lll11lll1l_opy_)
        cls.bstack11llll111l_opy_({
            bstack1ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᖿ"): bstack1ll1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᗀ"),
            bstack1ll1_opy_ (u"ࠫࡱࡵࡧࡴࠩᗁ"): bstack1lll11lllll_opy_
        })
    @classmethod
    @bstack1l111lll11_opy_(class_method=True)
    def bstack1lll1l1l11l_opy_(cls, steps):
        bstack1lll11l1lll_opy_ = []
        for step in steps:
            bstack1lll11ll111_opy_ = {
                bstack1ll1_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᗂ"): bstack1ll1_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩᗃ"),
                bstack1ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᗄ"): step[bstack1ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᗅ")],
                bstack1ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᗆ"): step[bstack1ll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᗇ")],
                bstack1ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᗈ"): step[bstack1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᗉ")],
                bstack1ll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᗊ"): step[bstack1ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᗋ")]
            }
            if bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᗌ") in step:
                bstack1lll11ll111_opy_[bstack1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᗍ")] = step[bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᗎ")]
            elif bstack1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᗏ") in step:
                bstack1lll11ll111_opy_[bstack1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᗐ")] = step[bstack1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᗑ")]
            bstack1lll11l1lll_opy_.append(bstack1lll11ll111_opy_)
        cls.bstack11llll111l_opy_({
            bstack1ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᗒ"): bstack1ll1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᗓ"),
            bstack1ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᗔ"): bstack1lll11l1lll_opy_
        })
    @classmethod
    @bstack1l111lll11_opy_(class_method=True)
    def bstack1llll111ll_opy_(cls, screenshot):
        cls.bstack11llll111l_opy_({
            bstack1ll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᗕ"): bstack1ll1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᗖ"),
            bstack1ll1_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᗗ"): [{
                bstack1ll1_opy_ (u"࠭࡫ࡪࡰࡧࠫᗘ"): bstack1ll1_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩᗙ"),
                bstack1ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᗚ"): bstack1l111lllll_opy_().isoformat() + bstack1ll1_opy_ (u"ࠩ࡝ࠫᗛ"),
                bstack1ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᗜ"): screenshot[bstack1ll1_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪᗝ")],
                bstack1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᗞ"): screenshot[bstack1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᗟ")]
            }]
        }, bstack1lll1l11l11_opy_=bstack1ll1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᗠ"))
    @classmethod
    @bstack1l111lll11_opy_(class_method=True)
    def bstack1l1l1ll11_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11llll111l_opy_({
            bstack1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᗡ"): bstack1ll1_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᗢ"),
            bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᗣ"): {
                bstack1ll1_opy_ (u"ࠦࡺࡻࡩࡥࠤᗤ"): cls.current_test_uuid(),
                bstack1ll1_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦᗥ"): cls.bstack11lll11ll1_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᗦ"), None) is None or os.environ[bstack1ll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᗧ")] == bstack1ll1_opy_ (u"ࠣࡰࡸࡰࡱࠨᗨ"):
            return False
        return True
    @classmethod
    def bstack1l1lllll1_opy_(cls, framework=bstack1ll1_opy_ (u"ࠤࠥᗩ")):
        if framework not in bstack11l11l1l1l_opy_:
            return False
        bstack1lll11l1ll1_opy_ = not bstack1l1ll11l11_opy_()
        return bstack1llll1l1ll_opy_(cls.bs_config.get(bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᗪ"), bstack1lll11l1ll1_opy_))
    @staticmethod
    def request_url(url):
        return bstack1ll1_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᗫ").format(bstack1lll1l1111l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1ll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᗬ"): bstack1ll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᗭ"),
            bstack1ll1_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪᗮ"): bstack1ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᗯ")
        }
        if os.environ.get(bstack1ll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᗰ"), None):
            headers[bstack1ll1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᗱ")] = bstack1ll1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧᗲ").format(os.environ[bstack1ll1_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙ࠨᗳ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᗴ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᗵ"), None)
    @staticmethod
    def bstack11llllll1l_opy_():
        if getattr(threading.current_thread(), bstack1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᗶ"), None):
            return {
                bstack1ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᗷ"): bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࠨᗸ"),
                bstack1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᗹ"): getattr(threading.current_thread(), bstack1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᗺ"), None)
            }
        if getattr(threading.current_thread(), bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᗻ"), None):
            return {
                bstack1ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬᗼ"): bstack1ll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᗽ"),
                bstack1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᗾ"): getattr(threading.current_thread(), bstack1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᗿ"), None)
            }
        return None
    @staticmethod
    def bstack11lll11ll1_opy_(driver):
        return {
            bstack11l11l11ll_opy_(): bstack111l1l1111_opy_(driver)
        }
    @staticmethod
    def bstack1lll1l11111_opy_(exception_info, report):
        return [{bstack1ll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᘀ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11ll11ll1l_opy_(typename):
        if bstack1ll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᘁ") in typename:
            return bstack1ll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᘂ")
        return bstack1ll1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᘃ")
    @staticmethod
    def bstack1lll11ll1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lllll1l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l111ll1l1_opy_(test, hook_name=None):
        bstack1lll1l111ll_opy_ = test.parent
        if hook_name in [bstack1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᘄ"), bstack1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᘅ"), bstack1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᘆ"), bstack1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᘇ")]:
            bstack1lll1l111ll_opy_ = test
        scope = []
        while bstack1lll1l111ll_opy_ is not None:
            scope.append(bstack1lll1l111ll_opy_.name)
            bstack1lll1l111ll_opy_ = bstack1lll1l111ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll1l1l111_opy_(hook_type):
        if hook_type == bstack1ll1_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥᘈ"):
            return bstack1ll1_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥᘉ")
        elif hook_type == bstack1ll1_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦᘊ"):
            return bstack1ll1_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣᘋ")
    @staticmethod
    def bstack1lll1l111l1_opy_(bstack1l1l11l11_opy_):
        try:
            if not bstack1lllll1l1_opy_.on():
                return bstack1l1l11l11_opy_
            if os.environ.get(bstack1ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢᘌ"), None) == bstack1ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣᘍ"):
                tests = os.environ.get(bstack1ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣᘎ"), None)
                if tests is None or tests == bstack1ll1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᘏ"):
                    return bstack1l1l11l11_opy_
                bstack1l1l11l11_opy_ = tests.split(bstack1ll1_opy_ (u"࠭ࠬࠨᘐ"))
                return bstack1l1l11l11_opy_
        except Exception as exc:
            print(bstack1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣᘑ"), str(exc))
        return bstack1l1l11l11_opy_
    @classmethod
    def bstack1l111l1l1l_opy_(cls, event: str, bstack11llll1111_opy_: bstack11lllllll1_opy_):
        bstack1l11111lll_opy_ = {
            bstack1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᘒ"): event,
            bstack11llll1111_opy_.bstack11lllll1l1_opy_(): bstack11llll1111_opy_.bstack1l111l111l_opy_(event)
        }
        bstack1lllll1l1_opy_.bstack11llll111l_opy_(bstack1l11111lll_opy_)