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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11l11llll1_opy_, bstack1l1ll1l11_opy_, bstack1llllll1l_opy_, bstack1lllll1ll1_opy_,
                                    bstack11l11ll11l_opy_, bstack11l11ll111_opy_)
from bstack_utils.messages import bstack1l11ll1lll_opy_, bstack1l1l111ll1_opy_
from bstack_utils.proxy import bstack11ll1ll11_opy_, bstack11ll1lll_opy_
bstack111l1l1l1_opy_ = Config.bstack1lll11l1l1_opy_()
logger = logging.getLogger(__name__)
def bstack11l1ll1ll1_opy_(config):
    return config[bstack1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᆳ")]
def bstack11ll111l11_opy_(config):
    return config[bstack1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᆴ")]
def bstack1l1ll11l11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111lll111l_opy_(obj):
    values = []
    bstack111l1ll11l_opy_ = re.compile(bstack1ll1_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣᆵ"), re.I)
    for key in obj.keys():
        if bstack111l1ll11l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111llll111_opy_(config):
    tags = []
    tags.extend(bstack111lll111l_opy_(os.environ))
    tags.extend(bstack111lll111l_opy_(config))
    return tags
def bstack111ll1ll11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111llllll1_opy_(bstack111lll1111_opy_):
    if not bstack111lll1111_opy_:
        return bstack1ll1_opy_ (u"ࠬ࠭ᆶ")
    return bstack1ll1_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢᆷ").format(bstack111lll1111_opy_.name, bstack111lll1111_opy_.email)
def bstack11l1l1llll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1111111_opy_ = repo.common_dir
        info = {
            bstack1ll1_opy_ (u"ࠢࡴࡪࡤࠦᆸ"): repo.head.commit.hexsha,
            bstack1ll1_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦᆹ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll1_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤᆺ"): repo.active_branch.name,
            bstack1ll1_opy_ (u"ࠥࡸࡦ࡭ࠢᆻ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢᆼ"): bstack111llllll1_opy_(repo.head.commit.committer),
            bstack1ll1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨᆽ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll1_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨᆾ"): bstack111llllll1_opy_(repo.head.commit.author),
            bstack1ll1_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧᆿ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᇀ"): repo.head.commit.message,
            bstack1ll1_opy_ (u"ࠤࡵࡳࡴࡺࠢᇁ"): repo.git.rev_parse(bstack1ll1_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧᇂ")),
            bstack1ll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧᇃ"): bstack11l1111111_opy_,
            bstack1ll1_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᇄ"): subprocess.check_output([bstack1ll1_opy_ (u"ࠨࡧࡪࡶࠥᇅ"), bstack1ll1_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥᇆ"), bstack1ll1_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦᇇ")]).strip().decode(
                bstack1ll1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᇈ")),
            bstack1ll1_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᇉ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᇊ"): repo.git.rev_list(
                bstack1ll1_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧᇋ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111lllllll_opy_ = []
        for remote in remotes:
            bstack11l111ll11_opy_ = {
                bstack1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇌ"): remote.name,
                bstack1ll1_opy_ (u"ࠢࡶࡴ࡯ࠦᇍ"): remote.url,
            }
            bstack111lllllll_opy_.append(bstack11l111ll11_opy_)
        bstack11l1111ll1_opy_ = {
            bstack1ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨᇎ"): bstack1ll1_opy_ (u"ࠤࡪ࡭ࡹࠨᇏ"),
            **info,
            bstack1ll1_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦᇐ"): bstack111lllllll_opy_
        }
        bstack11l1111ll1_opy_ = bstack111ll1l11l_opy_(bstack11l1111ll1_opy_)
        return bstack11l1111ll1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᇑ").format(err))
        return {}
def bstack111ll1l11l_opy_(bstack11l1111ll1_opy_):
    bstack111lllll11_opy_ = bstack111l1lllll_opy_(bstack11l1111ll1_opy_)
    if bstack111lllll11_opy_ and bstack111lllll11_opy_ > bstack11l11ll11l_opy_:
        bstack111llll1l1_opy_ = bstack111lllll11_opy_ - bstack11l11ll11l_opy_
        bstack111l1ll1l1_opy_ = bstack111lll1lll_opy_(bstack11l1111ll1_opy_[bstack1ll1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᇒ")], bstack111llll1l1_opy_)
        bstack11l1111ll1_opy_[bstack1ll1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᇓ")] = bstack111l1ll1l1_opy_
        logger.info(bstack1ll1_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤᇔ")
                    .format(bstack111l1lllll_opy_(bstack11l1111ll1_opy_) / 1024))
    return bstack11l1111ll1_opy_
def bstack111l1lllll_opy_(bstack1l1ll111_opy_):
    try:
        if bstack1l1ll111_opy_:
            bstack111lll1l1l_opy_ = json.dumps(bstack1l1ll111_opy_)
            bstack111llll1ll_opy_ = sys.getsizeof(bstack111lll1l1l_opy_)
            return bstack111llll1ll_opy_
    except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣᇕ").format(e))
    return -1
def bstack111lll1lll_opy_(field, bstack11l11l111l_opy_):
    try:
        bstack111llll11l_opy_ = len(bytes(bstack11l11ll111_opy_, bstack1ll1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᇖ")))
        bstack111ll11ll1_opy_ = bytes(field, bstack1ll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᇗ"))
        bstack11l111lll1_opy_ = len(bstack111ll11ll1_opy_)
        bstack111l1lll11_opy_ = ceil(bstack11l111lll1_opy_ - bstack11l11l111l_opy_ - bstack111llll11l_opy_)
        if bstack111l1lll11_opy_ > 0:
            bstack11l111111l_opy_ = bstack111ll11ll1_opy_[:bstack111l1lll11_opy_].decode(bstack1ll1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᇘ"), errors=bstack1ll1_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬᇙ")) + bstack11l11ll111_opy_
            return bstack11l111111l_opy_
    except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦᇚ").format(e))
    return field
def bstack1111ll1ll_opy_():
    env = os.environ
    if (bstack1ll1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᇛ") in env and len(env[bstack1ll1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᇜ")]) > 0) or (
            bstack1ll1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᇝ") in env and len(env[bstack1ll1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᇞ")]) > 0):
        return {
            bstack1ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇟ"): bstack1ll1_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨᇠ"),
            bstack1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇡ"): env.get(bstack1ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᇢ")),
            bstack1ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇣ"): env.get(bstack1ll1_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦᇤ")),
            bstack1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇥ"): env.get(bstack1ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᇦ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠧࡉࡉࠣᇧ")) == bstack1ll1_opy_ (u"ࠨࡴࡳࡷࡨࠦᇨ") and bstack1llll1l1ll_opy_(env.get(bstack1ll1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᇩ"))):
        return {
            bstack1ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨᇪ"): bstack1ll1_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᇫ"),
            bstack1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᇬ"): env.get(bstack1ll1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᇭ")),
            bstack1ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇮ"): env.get(bstack1ll1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᇯ")),
            bstack1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇰ"): env.get(bstack1ll1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᇱ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠤࡆࡍࠧᇲ")) == bstack1ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣᇳ") and bstack1llll1l1ll_opy_(env.get(bstack1ll1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᇴ"))):
        return {
            bstack1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇵ"): bstack1ll1_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᇶ"),
            bstack1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇷ"): env.get(bstack1ll1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᇸ")),
            bstack1ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇹ"): env.get(bstack1ll1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᇺ")),
            bstack1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇻ"): env.get(bstack1ll1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᇼ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠨࡃࡊࠤᇽ")) == bstack1ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧᇾ") and env.get(bstack1ll1_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᇿ")) == bstack1ll1_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦሀ"):
        return {
            bstack1ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣሁ"): bstack1ll1_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨሂ"),
            bstack1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሃ"): None,
            bstack1ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሄ"): None,
            bstack1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨህ"): None
        }
    if env.get(bstack1ll1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦሆ")) and env.get(bstack1ll1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧሇ")):
        return {
            bstack1ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣለ"): bstack1ll1_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢሉ"),
            bstack1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሊ"): env.get(bstack1ll1_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦላ")),
            bstack1ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሌ"): None,
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢል"): env.get(bstack1ll1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦሎ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠥࡇࡎࠨሏ")) == bstack1ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤሐ") and bstack1llll1l1ll_opy_(env.get(bstack1ll1_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦሑ"))):
        return {
            bstack1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሒ"): bstack1ll1_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨሓ"),
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሔ"): env.get(bstack1ll1_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧሕ")),
            bstack1ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሖ"): None,
            bstack1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሗ"): env.get(bstack1ll1_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥመ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠨࡃࡊࠤሙ")) == bstack1ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧሚ") and bstack1llll1l1ll_opy_(env.get(bstack1ll1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦማ"))):
        return {
            bstack1ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሜ"): bstack1ll1_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨም"),
            bstack1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢሞ"): env.get(bstack1ll1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦሟ")),
            bstack1ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሠ"): env.get(bstack1ll1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧሡ")),
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሢ"): env.get(bstack1ll1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧሣ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠥࡇࡎࠨሤ")) == bstack1ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤሥ") and bstack1llll1l1ll_opy_(env.get(bstack1ll1_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣሦ"))):
        return {
            bstack1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሧ"): bstack1ll1_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢረ"),
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሩ"): env.get(bstack1ll1_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨሪ")),
            bstack1ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧራ"): env.get(bstack1ll1_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤሬ")),
            bstack1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦር"): env.get(bstack1ll1_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤሮ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠢࡄࡋࠥሯ")) == bstack1ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨሰ") and bstack1llll1l1ll_opy_(env.get(bstack1ll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧሱ"))):
        return {
            bstack1ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣሲ"): bstack1ll1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢሳ"),
            bstack1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሴ"): env.get(bstack1ll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧስ")),
            bstack1ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሶ"): env.get(bstack1ll1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥሷ")) or env.get(bstack1ll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧሸ")),
            bstack1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤሹ"): env.get(bstack1ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨሺ"))
        }
    if bstack1llll1l1ll_opy_(env.get(bstack1ll1_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢሻ"))):
        return {
            bstack1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሼ"): bstack1ll1_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢሽ"),
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሾ"): bstack1ll1_opy_ (u"ࠤࡾࢁࢀࢃࠢሿ").format(env.get(bstack1ll1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ቀ")), env.get(bstack1ll1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫቁ"))),
            bstack1ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢቂ"): env.get(bstack1ll1_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧቃ")),
            bstack1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨቄ"): env.get(bstack1ll1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣቅ"))
        }
    if bstack1llll1l1ll_opy_(env.get(bstack1ll1_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦቆ"))):
        return {
            bstack1ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣቇ"): bstack1ll1_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨቈ"),
            bstack1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ቉"): bstack1ll1_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧቊ").format(env.get(bstack1ll1_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ቋ")), env.get(bstack1ll1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩቌ")), env.get(bstack1ll1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪቍ")), env.get(bstack1ll1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ቎"))),
            bstack1ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ቏"): env.get(bstack1ll1_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤቐ")),
            bstack1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቑ"): env.get(bstack1ll1_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣቒ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤቓ")) and env.get(bstack1ll1_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦቔ")):
        return {
            bstack1ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣቕ"): bstack1ll1_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨቖ"),
            bstack1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ቗"): bstack1ll1_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤቘ").format(env.get(bstack1ll1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪ቙")), env.get(bstack1ll1_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ቚ")), env.get(bstack1ll1_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩቛ"))),
            bstack1ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧቜ"): env.get(bstack1ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦቝ")),
            bstack1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ቞"): env.get(bstack1ll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ቟"))
        }
    if any([env.get(bstack1ll1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧበ")), env.get(bstack1ll1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢቡ")), env.get(bstack1ll1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨቢ"))]):
        return {
            bstack1ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣባ"): bstack1ll1_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦቤ"),
            bstack1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣብ"): env.get(bstack1ll1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧቦ")),
            bstack1ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤቧ"): env.get(bstack1ll1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨቨ")),
            bstack1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣቩ"): env.get(bstack1ll1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣቪ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤቫ")):
        return {
            bstack1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥቬ"): bstack1ll1_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨቭ"),
            bstack1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥቮ"): env.get(bstack1ll1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥቯ")),
            bstack1ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦተ"): env.get(bstack1ll1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤቱ")),
            bstack1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥቲ"): env.get(bstack1ll1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥታ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢቴ")) or env.get(bstack1ll1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤት")):
        return {
            bstack1ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨቶ"): bstack1ll1_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥቷ"),
            bstack1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨቸ"): env.get(bstack1ll1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣቹ")),
            bstack1ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢቺ"): bstack1ll1_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨቻ") if env.get(bstack1ll1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤቼ")) else None,
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢች"): env.get(bstack1ll1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢቾ"))
        }
    if any([env.get(bstack1ll1_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣቿ")), env.get(bstack1ll1_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧኀ")), env.get(bstack1ll1_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧኁ"))]):
        return {
            bstack1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦኂ"): bstack1ll1_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨኃ"),
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦኄ"): None,
            bstack1ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦኅ"): env.get(bstack1ll1_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢኆ")),
            bstack1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥኇ"): env.get(bstack1ll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢኈ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤ኉")):
        return {
            bstack1ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧኊ"): bstack1ll1_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦኋ"),
            bstack1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧኌ"): env.get(bstack1ll1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤኍ")),
            bstack1ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ኎"): bstack1ll1_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨ኏").format(env.get(bstack1ll1_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩነ"))) if env.get(bstack1ll1_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥኑ")) else None,
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢኒ"): env.get(bstack1ll1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦና"))
        }
    if bstack1llll1l1ll_opy_(env.get(bstack1ll1_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦኔ"))):
        return {
            bstack1ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤን"): bstack1ll1_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨኖ"),
            bstack1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤኗ"): env.get(bstack1ll1_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦኘ")),
            bstack1ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥኙ"): env.get(bstack1ll1_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧኚ")),
            bstack1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤኛ"): env.get(bstack1ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨኜ"))
        }
    if bstack1llll1l1ll_opy_(env.get(bstack1ll1_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨኝ"))):
        return {
            bstack1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦኞ"): bstack1ll1_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣኟ"),
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦአ"): bstack1ll1_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥኡ").format(env.get(bstack1ll1_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧኢ")), env.get(bstack1ll1_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨኣ")), env.get(bstack1ll1_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬኤ"))),
            bstack1ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣእ"): env.get(bstack1ll1_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤኦ")),
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢኧ"): env.get(bstack1ll1_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤከ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠥࡇࡎࠨኩ")) == bstack1ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤኪ") and env.get(bstack1ll1_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧካ")) == bstack1ll1_opy_ (u"ࠨ࠱ࠣኬ"):
        return {
            bstack1ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧክ"): bstack1ll1_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣኮ"),
            bstack1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧኯ"): bstack1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨኰ").format(env.get(bstack1ll1_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨ኱"))),
            bstack1ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢኲ"): None,
            bstack1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧኳ"): None,
        }
    if env.get(bstack1ll1_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥኴ")):
        return {
            bstack1ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨኵ"): bstack1ll1_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦ኶"),
            bstack1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ኷"): None,
            bstack1ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨኸ"): env.get(bstack1ll1_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨኹ")),
            bstack1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧኺ"): env.get(bstack1ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨኻ"))
        }
    if any([env.get(bstack1ll1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦኼ")), env.get(bstack1ll1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤኽ")), env.get(bstack1ll1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣኾ")), env.get(bstack1ll1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧ኿"))]):
        return {
            bstack1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥዀ"): bstack1ll1_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤ዁"),
            bstack1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥዂ"): None,
            bstack1ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥዃ"): env.get(bstack1ll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥዄ")) or None,
            bstack1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤዅ"): env.get(bstack1ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ዆"), 0)
        }
    if env.get(bstack1ll1_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ዇")):
        return {
            bstack1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦወ"): bstack1ll1_opy_ (u"ࠢࡈࡱࡆࡈࠧዉ"),
            bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦዊ"): None,
            bstack1ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦዋ"): env.get(bstack1ll1_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣዌ")),
            bstack1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥው"): env.get(bstack1ll1_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦዎ"))
        }
    if env.get(bstack1ll1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦዏ")):
        return {
            bstack1ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧዐ"): bstack1ll1_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦዑ"),
            bstack1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧዒ"): env.get(bstack1ll1_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤዓ")),
            bstack1ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨዔ"): env.get(bstack1ll1_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣዕ")),
            bstack1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧዖ"): env.get(bstack1ll1_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ዗"))
        }
    return {bstack1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢዘ"): None}
def get_host_info():
    return {
        bstack1ll1_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦዙ"): platform.node(),
        bstack1ll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧዚ"): platform.system(),
        bstack1ll1_opy_ (u"ࠦࡹࡿࡰࡦࠤዛ"): platform.machine(),
        bstack1ll1_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨዜ"): platform.version(),
        bstack1ll1_opy_ (u"ࠨࡡࡳࡥ࡫ࠦዝ"): platform.architecture()[0]
    }
def bstack1l1ll1ll11_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l11l11ll_opy_():
    if bstack111l1l1l1_opy_.get_property(bstack1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨዞ")):
        return bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧዟ")
    return bstack1ll1_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨዠ")
def bstack111l1l1111_opy_(driver):
    info = {
        bstack1ll1_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩዡ"): driver.capabilities,
        bstack1ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨዢ"): driver.session_id,
        bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ዣ"): driver.capabilities.get(bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫዤ"), None),
        bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩዥ"): driver.capabilities.get(bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩዦ"), None),
        bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫዧ"): driver.capabilities.get(bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩየ"), None),
    }
    if bstack11l11l11ll_opy_() == bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪዩ"):
        info[bstack1ll1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ዪ")] = bstack1ll1_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬያ") if bstack1lll1ll1l1_opy_() else bstack1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩዬ")
    return info
def bstack1lll1ll1l1_opy_():
    if bstack111l1l1l1_opy_.get_property(bstack1ll1_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧይ")):
        return True
    if bstack1llll1l1ll_opy_(os.environ.get(bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪዮ"), None)):
        return True
    return False
def bstack1l1l11llll_opy_(bstack111lll1l11_opy_, url, data, config):
    headers = config.get(bstack1ll1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫዯ"), None)
    proxies = bstack11ll1ll11_opy_(config, url)
    auth = config.get(bstack1ll1_opy_ (u"ࠫࡦࡻࡴࡩࠩደ"), None)
    response = requests.request(
            bstack111lll1l11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll1l1l1ll_opy_(bstack111l1111_opy_, size):
    bstack111lllll1_opy_ = []
    while len(bstack111l1111_opy_) > size:
        bstack1111l1ll_opy_ = bstack111l1111_opy_[:size]
        bstack111lllll1_opy_.append(bstack1111l1ll_opy_)
        bstack111l1111_opy_ = bstack111l1111_opy_[size:]
    bstack111lllll1_opy_.append(bstack111l1111_opy_)
    return bstack111lllll1_opy_
def bstack111ll1lll1_opy_(message, bstack111l1llll1_opy_=False):
    os.write(1, bytes(message, bstack1ll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫዱ")))
    os.write(1, bytes(bstack1ll1_opy_ (u"࠭࡜࡯ࠩዲ"), bstack1ll1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ዳ")))
    if bstack111l1llll1_opy_:
        with open(bstack1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧዴ") + os.environ[bstack1ll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨድ")] + bstack1ll1_opy_ (u"ࠪ࠲ࡱࡵࡧࠨዶ"), bstack1ll1_opy_ (u"ࠫࡦ࠭ዷ")) as f:
            f.write(message + bstack1ll1_opy_ (u"ࠬࡢ࡮ࠨዸ"))
def bstack111ll111l1_opy_():
    return os.environ[bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩዹ")].lower() == bstack1ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬዺ")
def bstack1l1l11l11l_opy_(bstack11l11111l1_opy_):
    return bstack1ll1_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧዻ").format(bstack11l11llll1_opy_, bstack11l11111l1_opy_)
def bstack1ll11l1l11_opy_():
    return bstack1l111lllll_opy_().replace(tzinfo=None).isoformat() + bstack1ll1_opy_ (u"ࠩ࡝ࠫዼ")
def bstack111l11llll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll1_opy_ (u"ࠪ࡞ࠬዽ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll1_opy_ (u"ࠫ࡟࠭ዾ")))).total_seconds() * 1000
def bstack11l11l11l1_opy_(timestamp):
    return bstack111ll1l111_opy_(timestamp).isoformat() + bstack1ll1_opy_ (u"ࠬࡠࠧዿ")
def bstack111l1l11ll_opy_(bstack111l1ll1ll_opy_):
    date_format = bstack1ll1_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫጀ")
    bstack111ll11l1l_opy_ = datetime.datetime.strptime(bstack111l1ll1ll_opy_, date_format)
    return bstack111ll11l1l_opy_.isoformat() + bstack1ll1_opy_ (u"࡛ࠧࠩጁ")
def bstack11l111llll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨጂ")
    else:
        return bstack1ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩጃ")
def bstack1llll1l1ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll1_opy_ (u"ࠪࡸࡷࡻࡥࠨጄ")
def bstack111ll1ll1l_opy_(val):
    return val.__str__().lower() == bstack1ll1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪጅ")
def bstack1l111lll11_opy_(bstack111l11lll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l11lll1_opy_ as e:
                print(bstack1ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧጆ").format(func.__name__, bstack111l11lll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1111lll_opy_(bstack11l111l1ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l111l1ll_opy_(cls, *args, **kwargs)
            except bstack111l11lll1_opy_ as e:
                print(bstack1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨጇ").format(bstack11l111l1ll_opy_.__name__, bstack111l11lll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1111lll_opy_
    else:
        return decorator
def bstack1l11lll1l_opy_(bstack11ll1l1lll_opy_):
    if bstack1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫገ") in bstack11ll1l1lll_opy_ and bstack111ll1ll1l_opy_(bstack11ll1l1lll_opy_[bstack1ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬጉ")]):
        return False
    if bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫጊ") in bstack11ll1l1lll_opy_ and bstack111ll1ll1l_opy_(bstack11ll1l1lll_opy_[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬጋ")]):
        return False
    return True
def bstack1lll11lll_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1ll1ll1l11_opy_(hub_url):
    if bstack1lll1ll11l_opy_() <= version.parse(bstack1ll1_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫጌ")):
        if hub_url != bstack1ll1_opy_ (u"ࠬ࠭ግ"):
            return bstack1ll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢጎ") + hub_url + bstack1ll1_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦጏ")
        return bstack1llllll1l_opy_
    if hub_url != bstack1ll1_opy_ (u"ࠨࠩጐ"):
        return bstack1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ጑") + hub_url + bstack1ll1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦጒ")
    return bstack1lllll1ll1_opy_
def bstack111ll11111_opy_():
    return isinstance(os.getenv(bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪጓ")), str)
def bstack1l11lll11_opy_(url):
    return urlparse(url).hostname
def bstack1ll1ll11_opy_(hostname):
    for bstack1l111l1l1_opy_ in bstack1l1ll1l11_opy_:
        regex = re.compile(bstack1l111l1l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111l1l1l1l_opy_(bstack111ll1111l_opy_, file_name, logger):
    bstack1l11l11l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠬࢄࠧጔ")), bstack111ll1111l_opy_)
    try:
        if not os.path.exists(bstack1l11l11l1_opy_):
            os.makedirs(bstack1l11l11l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"࠭ࡾࠨጕ")), bstack111ll1111l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll1_opy_ (u"ࠧࡸࠩ጖")):
                pass
            with open(file_path, bstack1ll1_opy_ (u"ࠣࡹ࠮ࠦ጗")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l11ll1lll_opy_.format(str(e)))
def bstack111l1l1l11_opy_(file_name, key, value, logger):
    file_path = bstack111l1l1l1l_opy_(bstack1ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩጘ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1l1l1l11_opy_ = json.load(open(file_path, bstack1ll1_opy_ (u"ࠪࡶࡧ࠭ጙ")))
        else:
            bstack1l1l1l1l11_opy_ = {}
        bstack1l1l1l1l11_opy_[key] = value
        with open(file_path, bstack1ll1_opy_ (u"ࠦࡼ࠱ࠢጚ")) as outfile:
            json.dump(bstack1l1l1l1l11_opy_, outfile)
def bstack1l1l1lll1l_opy_(file_name, logger):
    file_path = bstack111l1l1l1l_opy_(bstack1ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬጛ"), file_name, logger)
    bstack1l1l1l1l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll1_opy_ (u"࠭ࡲࠨጜ")) as bstack1llll1ll1_opy_:
            bstack1l1l1l1l11_opy_ = json.load(bstack1llll1ll1_opy_)
    return bstack1l1l1l1l11_opy_
def bstack1ll1111l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫጝ") + file_path + bstack1ll1_opy_ (u"ࠨࠢࠪጞ") + str(e))
def bstack1lll1ll11l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll1_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦጟ")
def bstack1l1l11l1l1_opy_(config):
    if bstack1ll1_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩጠ") in config:
        del (config[bstack1ll1_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪጡ")])
        return False
    if bstack1lll1ll11l_opy_() < version.parse(bstack1ll1_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫጢ")):
        return False
    if bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬጣ")):
        return True
    if bstack1ll1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧጤ") in config and config[bstack1ll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨጥ")] is False:
        return False
    else:
        return True
def bstack11lll1ll1_opy_(args_list, bstack11l1111l11_opy_):
    index = -1
    for value in bstack11l1111l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11lll1lll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11lll1lll1_opy_ = bstack11lll1lll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩጦ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪጧ"), exception=exception)
    def bstack11ll11ll1l_opy_(self):
        if self.result != bstack1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫጨ"):
            return None
        if bstack1ll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣጩ") in self.exception_type:
            return bstack1ll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢጪ")
        return bstack1ll1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣጫ")
    def bstack111l11ll11_opy_(self):
        if self.result != bstack1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨጬ"):
            return None
        if self.bstack11lll1lll1_opy_:
            return self.bstack11lll1lll1_opy_
        return bstack111l1l1lll_opy_(self.exception)
def bstack111l1l1lll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111ll11l11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll1llll1l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l1ll11_opy_(config, logger):
    try:
        import playwright
        bstack11l1111l1l_opy_ = playwright.__file__
        bstack11l111l111_opy_ = os.path.split(bstack11l1111l1l_opy_)
        bstack111ll1l1ll_opy_ = bstack11l111l111_opy_[0] + bstack1ll1_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬጭ")
        os.environ[bstack1ll1_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ጮ")] = bstack11ll1lll_opy_(config)
        with open(bstack111ll1l1ll_opy_, bstack1ll1_opy_ (u"ࠫࡷ࠭ጯ")) as f:
            bstack11ll1ll1l_opy_ = f.read()
            bstack111l1l111l_opy_ = bstack1ll1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫጰ")
            bstack111l11l1ll_opy_ = bstack11ll1ll1l_opy_.find(bstack111l1l111l_opy_)
            if bstack111l11l1ll_opy_ == -1:
              process = subprocess.Popen(bstack1ll1_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥጱ"), shell=True, cwd=bstack11l111l111_opy_[0])
              process.wait()
              bstack11l111l1l1_opy_ = bstack1ll1_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧጲ")
              bstack11l11111ll_opy_ = bstack1ll1_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧጳ")
              bstack11l11l1111_opy_ = bstack11ll1ll1l_opy_.replace(bstack11l111l1l1_opy_, bstack11l11111ll_opy_)
              with open(bstack111ll1l1ll_opy_, bstack1ll1_opy_ (u"ࠩࡺࠫጴ")) as f:
                f.write(bstack11l11l1111_opy_)
    except Exception as e:
        logger.error(bstack1l1l111ll1_opy_.format(str(e)))
def bstack1l1l1ll1l1_opy_():
  try:
    bstack11l111ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪጵ"))
    bstack111ll1l1l1_opy_ = []
    if os.path.exists(bstack11l111ll1l_opy_):
      with open(bstack11l111ll1l_opy_) as f:
        bstack111ll1l1l1_opy_ = json.load(f)
      os.remove(bstack11l111ll1l_opy_)
    return bstack111ll1l1l1_opy_
  except:
    pass
  return []
def bstack1ll1l111_opy_(bstack11l11l1ll_opy_):
  try:
    bstack111ll1l1l1_opy_ = []
    bstack11l111ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫጶ"))
    if os.path.exists(bstack11l111ll1l_opy_):
      with open(bstack11l111ll1l_opy_) as f:
        bstack111ll1l1l1_opy_ = json.load(f)
    bstack111ll1l1l1_opy_.append(bstack11l11l1ll_opy_)
    with open(bstack11l111ll1l_opy_, bstack1ll1_opy_ (u"ࠬࡽࠧጷ")) as f:
        json.dump(bstack111ll1l1l1_opy_, f)
  except:
    pass
def bstack11l1l111_opy_(logger, bstack111lllll1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩጸ"), bstack1ll1_opy_ (u"ࠧࠨጹ"))
    if test_name == bstack1ll1_opy_ (u"ࠨࠩጺ"):
        test_name = threading.current_thread().__dict__.get(bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨጻ"), bstack1ll1_opy_ (u"ࠪࠫጼ"))
    bstack111lll11ll_opy_ = bstack1ll1_opy_ (u"ࠫ࠱ࠦࠧጽ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111lllll1l_opy_:
        bstack1lll1l1ll_opy_ = os.environ.get(bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬጾ"), bstack1ll1_opy_ (u"࠭࠰ࠨጿ"))
        bstack111ll11l_opy_ = {bstack1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬፀ"): test_name, bstack1ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧፁ"): bstack111lll11ll_opy_, bstack1ll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨፂ"): bstack1lll1l1ll_opy_}
        bstack111ll11lll_opy_ = []
        bstack111l1ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩፃ"))
        if os.path.exists(bstack111l1ll111_opy_):
            with open(bstack111l1ll111_opy_) as f:
                bstack111ll11lll_opy_ = json.load(f)
        bstack111ll11lll_opy_.append(bstack111ll11l_opy_)
        with open(bstack111l1ll111_opy_, bstack1ll1_opy_ (u"ࠫࡼ࠭ፄ")) as f:
            json.dump(bstack111ll11lll_opy_, f)
    else:
        bstack111ll11l_opy_ = {bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪፅ"): test_name, bstack1ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬፆ"): bstack111lll11ll_opy_, bstack1ll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ፇ"): str(multiprocessing.current_process().name)}
        if bstack1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬፈ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack111ll11l_opy_)
  except Exception as e:
      logger.warn(bstack1ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨፉ").format(e))
def bstack1ll11l111_opy_(error_message, test_name, index, logger):
  try:
    bstack111ll111ll_opy_ = []
    bstack111ll11l_opy_ = {bstack1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨፊ"): test_name, bstack1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪፋ"): error_message, bstack1ll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫፌ"): index}
    bstack111lll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧፍ"))
    if os.path.exists(bstack111lll11l1_opy_):
        with open(bstack111lll11l1_opy_) as f:
            bstack111ll111ll_opy_ = json.load(f)
    bstack111ll111ll_opy_.append(bstack111ll11l_opy_)
    with open(bstack111lll11l1_opy_, bstack1ll1_opy_ (u"ࠧࡸࠩፎ")) as f:
        json.dump(bstack111ll111ll_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦፏ").format(e))
def bstack1lll11111_opy_(bstack11ll1ll1_opy_, name, logger):
  try:
    bstack111ll11l_opy_ = {bstack1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧፐ"): name, bstack1ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩፑ"): bstack11ll1ll1_opy_, bstack1ll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪፒ"): str(threading.current_thread()._name)}
    return bstack111ll11l_opy_
  except Exception as e:
    logger.warn(bstack1ll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤፓ").format(e))
  return
def bstack111l11ll1l_opy_():
    return platform.system() == bstack1ll1_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧፔ")
def bstack1l1l11111l_opy_(bstack111l1l1ll1_opy_, config, logger):
    bstack111l1l11l1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l1l1ll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨፕ").format(e))
    return bstack111l1l11l1_opy_
def bstack111l1lll1l_opy_(bstack11l111l11l_opy_, bstack11l11l1l11_opy_):
    bstack111ll1llll_opy_ = version.parse(bstack11l111l11l_opy_)
    bstack111lll1ll1_opy_ = version.parse(bstack11l11l1l11_opy_)
    if bstack111ll1llll_opy_ > bstack111lll1ll1_opy_:
        return 1
    elif bstack111ll1llll_opy_ < bstack111lll1ll1_opy_:
        return -1
    else:
        return 0
def bstack1l111lllll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111ll1l111_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)