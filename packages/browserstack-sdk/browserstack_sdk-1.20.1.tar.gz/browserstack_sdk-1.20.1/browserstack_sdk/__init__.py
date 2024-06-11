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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1ll111l1l1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1llll1llll_opy_ import bstack1l1ll1ll1_opy_
import time
import requests
def bstack1l1l1l11l1_opy_():
  global CONFIG
  headers = {
        bstack1ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11ll1ll11_opy_(CONFIG, bstack11ll1111_opy_)
  try:
    response = requests.get(bstack11ll1111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11ll111l1_opy_ = response.json()[bstack1ll1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1111111l_opy_.format(response.json()))
      return bstack11ll111l1_opy_
    else:
      logger.debug(bstack1lll11l11_opy_.format(bstack1ll1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1lll11l11_opy_.format(e))
def bstack1ll1111ll1_opy_(hub_url):
  global CONFIG
  url = bstack1ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11ll1ll11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11111lll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11lll11l_opy_.format(hub_url, e))
def bstack111llll11_opy_():
  try:
    global bstack111111l1_opy_
    bstack11ll111l1_opy_ = bstack1l1l1l11l1_opy_()
    bstack11llll111_opy_ = []
    results = []
    for bstack1l111l11l_opy_ in bstack11ll111l1_opy_:
      bstack11llll111_opy_.append(bstack1lllllllll_opy_(target=bstack1ll1111ll1_opy_,args=(bstack1l111l11l_opy_,)))
    for t in bstack11llll111_opy_:
      t.start()
    for t in bstack11llll111_opy_:
      results.append(t.join())
    bstack1ll1lllll1_opy_ = {}
    for item in results:
      hub_url = item[bstack1ll1_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1ll1_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1ll1lllll1_opy_[hub_url] = latency
    bstack111l11lll_opy_ = min(bstack1ll1lllll1_opy_, key= lambda x: bstack1ll1lllll1_opy_[x])
    bstack111111l1_opy_ = bstack111l11lll_opy_
    logger.debug(bstack1ll1l1lll1_opy_.format(bstack111l11lll_opy_))
  except Exception as e:
    logger.debug(bstack1lll1lll_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack11ll1l1l1_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l1l11111l_opy_, bstack1l1l11llll_opy_, bstack1l1l11l11l_opy_, bstack1ll1llll1l_opy_, bstack1l11lll1l_opy_, \
  Notset, bstack1l1l11l1l1_opy_, \
  bstack1l1l1lll1l_opy_, bstack1ll1111l_opy_, bstack11lll1ll1_opy_, bstack1111ll1ll_opy_, bstack1lll11lll_opy_, bstack1l1ll1ll11_opy_, \
  bstack1l1ll11l11_opy_, \
  bstack11l1ll11_opy_, bstack1l1l1ll1l1_opy_, bstack1ll1l111_opy_, bstack1lll11111_opy_, \
  bstack11l1l111_opy_, bstack1ll11l111_opy_, bstack1llll1l1ll_opy_
from bstack_utils.bstack1l1ll1ll_opy_ import bstack1ll1l1lll_opy_
from bstack_utils.bstack1lllll1ll_opy_ import bstack1l1llll1l_opy_
from bstack_utils.bstack1l1l111ll_opy_ import bstack11111l1ll_opy_, bstack1l1l1ll11l_opy_
from bstack_utils.bstack1ll11ll1ll_opy_ import bstack1lllll1l1_opy_
from bstack_utils.bstack1111l11ll_opy_ import bstack1111l11ll_opy_
from bstack_utils.proxy import bstack1l1l1l11ll_opy_, bstack11ll1ll11_opy_, bstack11ll1lll_opy_, bstack1l11l1ll1_opy_
import bstack_utils.bstack1111ll111_opy_ as bstack1111111l1_opy_
from browserstack_sdk.bstack1l1ll11l1l_opy_ import *
from browserstack_sdk.bstack1l1lll111_opy_ import *
from bstack_utils.bstack1ll11llll_opy_ import bstack1ll1l11l1l_opy_
bstack1l1l111l11_opy_ = bstack1ll1_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack111111l1l_opy_ = bstack1ll1_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1l11l11ll_opy_ = None
CONFIG = {}
bstack1llll1l1l1_opy_ = {}
bstack1lllll11_opy_ = {}
bstack11l11llll_opy_ = None
bstack11l1l11ll_opy_ = None
bstack11l111l1l_opy_ = None
bstack1ll1llll1_opy_ = -1
bstack1111ll1l_opy_ = 0
bstack111ll1ll_opy_ = bstack1ll11ll1_opy_
bstack11l111111_opy_ = 1
bstack1llllll11_opy_ = False
bstack1l11lll11l_opy_ = False
bstack11l1l1l11_opy_ = bstack1ll1_opy_ (u"ࠨࠩࢂ")
bstack1l1lll1l11_opy_ = bstack1ll1_opy_ (u"ࠩࠪࢃ")
bstack1lll1l1l_opy_ = False
bstack1l1l111l_opy_ = True
bstack1l1l111111_opy_ = bstack1ll1_opy_ (u"ࠪࠫࢄ")
bstack1llll111_opy_ = []
bstack111111l1_opy_ = bstack1ll1_opy_ (u"ࠫࠬࢅ")
bstack11ll11111_opy_ = False
bstack1lll111l11_opy_ = None
bstack1l1ll1ll1l_opy_ = None
bstack1l11lllll_opy_ = None
bstack1ll11l1lll_opy_ = -1
bstack1l1l1lll1_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠬࢄࠧࢆ")), bstack1ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack1ll1_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1lll1lllll_opy_ = 0
bstack1llll1l11_opy_ = 0
bstack11ll1l11l_opy_ = []
bstack1111llll_opy_ = []
bstack1l1lllll_opy_ = []
bstack111111lll_opy_ = []
bstack1l1l1llll1_opy_ = bstack1ll1_opy_ (u"ࠨࠩࢉ")
bstack1l1l11ll1l_opy_ = bstack1ll1_opy_ (u"ࠩࠪࢊ")
bstack1111lll11_opy_ = False
bstack1lllll11l1_opy_ = False
bstack1ll11lll1l_opy_ = {}
bstack1l11l11l_opy_ = None
bstack1l111l11_opy_ = None
bstack1l11l1l11_opy_ = None
bstack1l11111l_opy_ = None
bstack11lllll11_opy_ = None
bstack1llll11l1_opy_ = None
bstack11111l1l1_opy_ = None
bstack1111ll11_opy_ = None
bstack1llll11l1l_opy_ = None
bstack11lll1lll_opy_ = None
bstack1ll11ll1l_opy_ = None
bstack1l1ll111l_opy_ = None
bstack1ll111lll1_opy_ = None
bstack111l1lll_opy_ = None
bstack1lll1l11ll_opy_ = None
bstack11l111l1_opy_ = None
bstack1ll1l1l111_opy_ = None
bstack1l1l1llll_opy_ = None
bstack1ll11l11_opy_ = None
bstack1l11l11l11_opy_ = None
bstack11ll11l1_opy_ = None
bstack11llll1l1_opy_ = False
bstack1l1l1ll1l_opy_ = bstack1ll1_opy_ (u"ࠥࠦࢋ")
logger = bstack11ll1l1l1_opy_.get_logger(__name__, bstack111ll1ll_opy_)
bstack111l1l1l1_opy_ = Config.bstack1lll11l1l1_opy_()
percy = bstack1l11l1lll1_opy_()
bstack1l1ll11111_opy_ = bstack1l1ll1ll1_opy_()
def bstack11lll1111_opy_():
  global CONFIG
  global bstack1111lll11_opy_
  global bstack111l1l1l1_opy_
  bstack11ll11l11_opy_ = bstack1lll111l1_opy_(CONFIG)
  if bstack1l11lll1l_opy_(CONFIG):
    if (bstack1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack11ll11l11_opy_ and str(bstack11ll11l11_opy_[bstack1ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack1ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
      bstack1111lll11_opy_ = True
    bstack111l1l1l1_opy_.bstack111l111l_opy_(bstack11ll11l11_opy_.get(bstack1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
  else:
    bstack1111lll11_opy_ = True
    bstack111l1l1l1_opy_.bstack111l111l_opy_(True)
def bstack1l11lll1ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lll1ll11l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1ll1l1ll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll1_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack1ll1_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1l111111_opy_
      bstack1l1l111111_opy_ += bstack1ll1_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1lll11l11l_opy_ = re.compile(bstack1ll1_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1ll1l111l1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1lll11l11l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll1_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack1ll1_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1llllll111_opy_():
  bstack1111l1l1_opy_ = bstack1l1ll1l1ll_opy_()
  if bstack1111l1l1_opy_ and os.path.exists(os.path.abspath(bstack1111l1l1_opy_)):
    fileName = bstack1111l1l1_opy_
  if bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack1ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack11l11ll_opy_ = os.path.abspath(fileName)
  else:
    bstack11l11ll_opy_ = bstack1ll1_opy_ (u"࢛ࠬ࠭")
  bstack11lll1ll_opy_ = os.getcwd()
  bstack11l1111l1_opy_ = bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1l1ll1111l_opy_ = bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack11l11ll_opy_)) and bstack11lll1ll_opy_ != bstack1ll1_opy_ (u"ࠣࠤ࢞"):
    bstack11l11ll_opy_ = os.path.join(bstack11lll1ll_opy_, bstack11l1111l1_opy_)
    if not os.path.exists(bstack11l11ll_opy_):
      bstack11l11ll_opy_ = os.path.join(bstack11lll1ll_opy_, bstack1l1ll1111l_opy_)
    if bstack11lll1ll_opy_ != os.path.dirname(bstack11lll1ll_opy_):
      bstack11lll1ll_opy_ = os.path.dirname(bstack11lll1ll_opy_)
    else:
      bstack11lll1ll_opy_ = bstack1ll1_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack11l11ll_opy_):
    bstack11111l111_opy_(
      bstack1ll11l1l_opy_.format(os.getcwd()))
  try:
    with open(bstack11l11ll_opy_, bstack1ll1_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack1ll1_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1lll11l11l_opy_)
      yaml.add_constructor(bstack1ll1_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1ll1l111l1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11l11ll_opy_, bstack1ll1_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11111l111_opy_(bstack1111111ll_opy_.format(str(exc)))
def bstack1lll1ll111_opy_(config):
  bstack1l1lll1ll_opy_ = bstack11l111lll_opy_(config)
  for option in list(bstack1l1lll1ll_opy_):
    if option.lower() in bstack1lllllll11_opy_ and option != bstack1lllllll11_opy_[option.lower()]:
      bstack1l1lll1ll_opy_[bstack1lllllll11_opy_[option.lower()]] = bstack1l1lll1ll_opy_[option]
      del bstack1l1lll1ll_opy_[option]
  return config
def bstack1lllll1l1l_opy_():
  global bstack1lllll11_opy_
  for key, bstack1l1111ll_opy_ in bstack1llll1l111_opy_.items():
    if isinstance(bstack1l1111ll_opy_, list):
      for var in bstack1l1111ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lllll11_opy_[key] = os.environ[var]
          break
    elif bstack1l1111ll_opy_ in os.environ and os.environ[bstack1l1111ll_opy_] and str(os.environ[bstack1l1111ll_opy_]).strip():
      bstack1lllll11_opy_[key] = os.environ[bstack1l1111ll_opy_]
  if bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1lllll11_opy_[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1lllll11_opy_[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack111l11l1l_opy_():
  global bstack1llll1l1l1_opy_
  global bstack1l1l111111_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1ll1_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1llll1l1l1_opy_[bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1llll1l1l1_opy_[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l11l111_opy_ in bstack11llll1l_opy_.items():
    if isinstance(bstack1l11l111_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l11l111_opy_:
          if idx < len(sys.argv) and bstack1ll1_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1llll1l1l1_opy_:
            bstack1llll1l1l1_opy_[key] = sys.argv[idx + 1]
            bstack1l1l111111_opy_ += bstack1ll1_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack1ll1_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1ll1_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1l11l111_opy_.lower() == val.lower() and not key in bstack1llll1l1l1_opy_:
          bstack1llll1l1l1_opy_[key] = sys.argv[idx + 1]
          bstack1l1l111111_opy_ += bstack1ll1_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1l11l111_opy_ + bstack1ll1_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1ll1l1llll_opy_(config):
  bstack1lll1111l1_opy_ = config.keys()
  for bstack1l1l1111l1_opy_, bstack1l11l11lll_opy_ in bstack11111lll1_opy_.items():
    if bstack1l11l11lll_opy_ in bstack1lll1111l1_opy_:
      config[bstack1l1l1111l1_opy_] = config[bstack1l11l11lll_opy_]
      del config[bstack1l11l11lll_opy_]
  for bstack1l1l1111l1_opy_, bstack1l11l11lll_opy_ in bstack1l111l1l_opy_.items():
    if isinstance(bstack1l11l11lll_opy_, list):
      for bstack1l111lll1_opy_ in bstack1l11l11lll_opy_:
        if bstack1l111lll1_opy_ in bstack1lll1111l1_opy_:
          config[bstack1l1l1111l1_opy_] = config[bstack1l111lll1_opy_]
          del config[bstack1l111lll1_opy_]
          break
    elif bstack1l11l11lll_opy_ in bstack1lll1111l1_opy_:
      config[bstack1l1l1111l1_opy_] = config[bstack1l11l11lll_opy_]
      del config[bstack1l11l11lll_opy_]
  for bstack1l111lll1_opy_ in list(config):
    for bstack11111ll11_opy_ in bstack111111l11_opy_:
      if bstack1l111lll1_opy_.lower() == bstack11111ll11_opy_.lower() and bstack1l111lll1_opy_ != bstack11111ll11_opy_:
        config[bstack11111ll11_opy_] = config[bstack1l111lll1_opy_]
        del config[bstack1l111lll1_opy_]
  bstack11l11ll1_opy_ = [{}]
  if not config.get(bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ")):
    config[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")] = [{}]
  bstack11l11ll1_opy_ = config[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࢵ")]
  for platform in bstack11l11ll1_opy_:
    for bstack1l111lll1_opy_ in list(platform):
      for bstack11111ll11_opy_ in bstack111111l11_opy_:
        if bstack1l111lll1_opy_.lower() == bstack11111ll11_opy_.lower() and bstack1l111lll1_opy_ != bstack11111ll11_opy_:
          platform[bstack11111ll11_opy_] = platform[bstack1l111lll1_opy_]
          del platform[bstack1l111lll1_opy_]
  for bstack1l1l1111l1_opy_, bstack1l11l11lll_opy_ in bstack1l111l1l_opy_.items():
    for platform in bstack11l11ll1_opy_:
      if isinstance(bstack1l11l11lll_opy_, list):
        for bstack1l111lll1_opy_ in bstack1l11l11lll_opy_:
          if bstack1l111lll1_opy_ in platform:
            platform[bstack1l1l1111l1_opy_] = platform[bstack1l111lll1_opy_]
            del platform[bstack1l111lll1_opy_]
            break
      elif bstack1l11l11lll_opy_ in platform:
        platform[bstack1l1l1111l1_opy_] = platform[bstack1l11l11lll_opy_]
        del platform[bstack1l11l11lll_opy_]
  for bstack1l1lll11l1_opy_ in bstack1l11l1l1_opy_:
    if bstack1l1lll11l1_opy_ in config:
      if not bstack1l11l1l1_opy_[bstack1l1lll11l1_opy_] in config:
        config[bstack1l11l1l1_opy_[bstack1l1lll11l1_opy_]] = {}
      config[bstack1l11l1l1_opy_[bstack1l1lll11l1_opy_]].update(config[bstack1l1lll11l1_opy_])
      del config[bstack1l1lll11l1_opy_]
  for platform in bstack11l11ll1_opy_:
    for bstack1l1lll11l1_opy_ in bstack1l11l1l1_opy_:
      if bstack1l1lll11l1_opy_ in list(platform):
        if not bstack1l11l1l1_opy_[bstack1l1lll11l1_opy_] in platform:
          platform[bstack1l11l1l1_opy_[bstack1l1lll11l1_opy_]] = {}
        platform[bstack1l11l1l1_opy_[bstack1l1lll11l1_opy_]].update(platform[bstack1l1lll11l1_opy_])
        del platform[bstack1l1lll11l1_opy_]
  config = bstack1lll1ll111_opy_(config)
  return config
def bstack1l1ll1l1l1_opy_(config):
  global bstack1l1lll1l11_opy_
  if bstack1l11lll1l_opy_(config) and bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ") in config and str(config[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢷ")]).lower() != bstack1ll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࢸ"):
    if not bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ") in config:
      config[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢺ")] = {}
    if not config[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")].get(bstack1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧࢼ")) and not bstack1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢽ") in config[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢾ")]:
      bstack1ll11l1l11_opy_ = datetime.datetime.now()
      bstack1l1l1lllll_opy_ = bstack1ll11l1l11_opy_.strftime(bstack1ll1_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪࢿ"))
      hostname = socket.gethostname()
      bstack1ll1ll1l_opy_ = bstack1ll1_opy_ (u"ࠧࠨࣀ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll1_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪࣁ").format(bstack1l1l1lllll_opy_, hostname, bstack1ll1ll1l_opy_)
      config[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣂ")][bstack1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣃ")] = identifier
    bstack1l1lll1l11_opy_ = config[bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣄ")].get(bstack1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ"))
  return config
def bstack11l1l111l_opy_():
  bstack11l1l1lll_opy_ =  bstack1111ll1ll_opy_()[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠬࣆ")]
  return bstack11l1l1lll_opy_ if bstack11l1l1lll_opy_ else -1
def bstack1ll11l1111_opy_(bstack11l1l1lll_opy_):
  global CONFIG
  if not bstack1ll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣇ") in CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣈ")]:
    return
  CONFIG[bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")] = CONFIG[bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")].replace(
    bstack1ll1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭࣋"),
    str(bstack11l1l1lll_opy_)
  )
def bstack11ll1l1l_opy_():
  global CONFIG
  if not bstack1ll1_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ࣌") in CONFIG[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")]:
    return
  bstack1ll11l1l11_opy_ = datetime.datetime.now()
  bstack1l1l1lllll_opy_ = bstack1ll11l1l11_opy_.strftime(bstack1ll1_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ࣎"))
  CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ")] = CONFIG[bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")].replace(
    bstack1ll1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾ࣑ࠩ"),
    bstack1l1l1lllll_opy_
  )
def bstack1ll1111l1_opy_():
  global CONFIG
  if bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG and not bool(CONFIG[bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")]):
    del CONFIG[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]
    return
  if not bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ") in CONFIG:
    CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")] = bstack1ll1_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬࣗ")
  if bstack1ll1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩࣘ") in CONFIG[bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣙ")]:
    bstack11ll1l1l_opy_()
    os.environ[bstack1ll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩࣚ")] = CONFIG[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣛ")]
  if not bstack1ll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣜ") in CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣝ")]:
    return
  bstack11l1l1lll_opy_ = bstack1ll1_opy_ (u"ࠩࠪࣞ")
  bstack1111ll11l_opy_ = bstack11l1l111l_opy_()
  if bstack1111ll11l_opy_ != -1:
    bstack11l1l1lll_opy_ = bstack1ll1_opy_ (u"ࠪࡇࡎࠦࠧࣟ") + str(bstack1111ll11l_opy_)
  if bstack11l1l1lll_opy_ == bstack1ll1_opy_ (u"ࠫࠬ࣠"):
    bstack1111l1111_opy_ = bstack11l111ll_opy_(CONFIG[bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࣡")])
    if bstack1111l1111_opy_ != -1:
      bstack11l1l1lll_opy_ = str(bstack1111l1111_opy_)
  if bstack11l1l1lll_opy_:
    bstack1ll11l1111_opy_(bstack11l1l1lll_opy_)
    os.environ[bstack1ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ࣢")] = CONFIG[bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")]
def bstack1l1l1l1ll1_opy_(bstack1ll11lll11_opy_, bstack111l11ll1_opy_, path):
  bstack1l1ll111_opy_ = {
    bstack1ll1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣤ"): bstack111l11ll1_opy_
  }
  if os.path.exists(path):
    bstack1l1l1l1l11_opy_ = json.load(open(path, bstack1ll1_opy_ (u"ࠩࡵࡦࠬࣥ")))
  else:
    bstack1l1l1l1l11_opy_ = {}
  bstack1l1l1l1l11_opy_[bstack1ll11lll11_opy_] = bstack1l1ll111_opy_
  with open(path, bstack1ll1_opy_ (u"ࠥࡻ࠰ࠨࣦ")) as outfile:
    json.dump(bstack1l1l1l1l11_opy_, outfile)
def bstack11l111ll_opy_(bstack1ll11lll11_opy_):
  bstack1ll11lll11_opy_ = str(bstack1ll11lll11_opy_)
  bstack1l11l11l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠫࢃ࠭ࣧ")), bstack1ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࣨ"))
  try:
    if not os.path.exists(bstack1l11l11l1_opy_):
      os.makedirs(bstack1l11l11l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"࠭ࡾࠨࣩ")), bstack1ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࣪"), bstack1ll1_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪ࣫"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll1_opy_ (u"ࠩࡺࠫ࣬")):
        pass
      with open(file_path, bstack1ll1_opy_ (u"ࠥࡻ࠰ࠨ࣭")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll1_opy_ (u"ࠫࡷ࣮࠭")) as bstack1llll1ll1_opy_:
      bstack11lll11ll_opy_ = json.load(bstack1llll1ll1_opy_)
    if bstack1ll11lll11_opy_ in bstack11lll11ll_opy_:
      bstack111l111ll_opy_ = bstack11lll11ll_opy_[bstack1ll11lll11_opy_][bstack1ll1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࣯ࠩ")]
      bstack1l1ll11lll_opy_ = int(bstack111l111ll_opy_) + 1
      bstack1l1l1l1ll1_opy_(bstack1ll11lll11_opy_, bstack1l1ll11lll_opy_, file_path)
      return bstack1l1ll11lll_opy_
    else:
      bstack1l1l1l1ll1_opy_(bstack1ll11lll11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l11ll1lll_opy_.format(str(e)))
    return -1
def bstack1l1llll11_opy_(config):
  if not config[bstack1ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࣰ")] or not config[bstack1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࣱࠪ")]:
    return True
  else:
    return False
def bstack1ll1llllll_opy_(config, index=0):
  global bstack1lll1l1l_opy_
  bstack1lll11l1_opy_ = {}
  caps = bstack11l11l1l_opy_ + bstack1lll111111_opy_
  if bstack1lll1l1l_opy_:
    caps += bstack1lll1l1ll1_opy_
  for key in config:
    if key in caps + [bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]:
      continue
    bstack1lll11l1_opy_[key] = config[key]
  if bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ") in config:
    for bstack1ll111ll11_opy_ in config[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index]:
      if bstack1ll111ll11_opy_ in caps:
        continue
      bstack1lll11l1_opy_[bstack1ll111ll11_opy_] = config[bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index][bstack1ll111ll11_opy_]
  bstack1lll11l1_opy_[bstack1ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࣶࠧ")] = socket.gethostname()
  if bstack1ll1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ") in bstack1lll11l1_opy_:
    del (bstack1lll11l1_opy_[bstack1ll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣸ")])
  return bstack1lll11l1_opy_
def bstack1ll1ll1lll_opy_(config):
  global bstack1lll1l1l_opy_
  bstack1l1l1lll_opy_ = {}
  caps = bstack1lll111111_opy_
  if bstack1lll1l1l_opy_:
    caps += bstack1lll1l1ll1_opy_
  for key in caps:
    if key in config:
      bstack1l1l1lll_opy_[key] = config[key]
  return bstack1l1l1lll_opy_
def bstack1ll111lll_opy_(bstack1lll11l1_opy_, bstack1l1l1lll_opy_):
  bstack1lll1l1lll_opy_ = {}
  for key in bstack1lll11l1_opy_.keys():
    if key in bstack11111lll1_opy_:
      bstack1lll1l1lll_opy_[bstack11111lll1_opy_[key]] = bstack1lll11l1_opy_[key]
    else:
      bstack1lll1l1lll_opy_[key] = bstack1lll11l1_opy_[key]
  for key in bstack1l1l1lll_opy_:
    if key in bstack11111lll1_opy_:
      bstack1lll1l1lll_opy_[bstack11111lll1_opy_[key]] = bstack1l1l1lll_opy_[key]
    else:
      bstack1lll1l1lll_opy_[key] = bstack1l1l1lll_opy_[key]
  return bstack1lll1l1lll_opy_
def bstack11l111ll1_opy_(config, index=0):
  global bstack1lll1l1l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1lll1ll1l_opy_ = bstack1l1l11111l_opy_(bstack11l1l1l1l_opy_, config, logger)
  bstack1l1l1lll_opy_ = bstack1ll1ll1lll_opy_(config)
  bstack11llllll_opy_ = bstack1lll111111_opy_
  bstack11llllll_opy_ += bstack111ll1l1_opy_
  bstack1l1l1lll_opy_ = update(bstack1l1l1lll_opy_, bstack1lll1ll1l_opy_)
  if bstack1lll1l1l_opy_:
    bstack11llllll_opy_ += bstack1lll1l1ll1_opy_
  if bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ") in config:
    if bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࣺࠧ") in config[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")][index]:
      caps[bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩࣼ")] = config[bstack1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")][index][bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫࣾ")]
    if bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨࣿ") in config[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index]:
      caps[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪँ")] = str(config[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ं")][index][bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬः")])
    bstack1ll1l1111l_opy_ = bstack1l1l11111l_opy_(bstack11l1l1l1l_opy_, config[bstack1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index], logger)
    bstack11llllll_opy_ += list(bstack1ll1l1111l_opy_.keys())
    for bstack1lll1111ll_opy_ in bstack11llllll_opy_:
      if bstack1lll1111ll_opy_ in config[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index]:
        if bstack1lll1111ll_opy_ == bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩआ"):
          try:
            bstack1ll1l1111l_opy_[bstack1lll1111ll_opy_] = str(config[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1lll1111ll_opy_] * 1.0)
          except:
            bstack1ll1l1111l_opy_[bstack1lll1111ll_opy_] = str(config[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1lll1111ll_opy_])
        else:
          bstack1ll1l1111l_opy_[bstack1lll1111ll_opy_] = config[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1lll1111ll_opy_]
        del (config[bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1lll1111ll_opy_])
    bstack1l1l1lll_opy_ = update(bstack1l1l1lll_opy_, bstack1ll1l1111l_opy_)
  bstack1lll11l1_opy_ = bstack1ll1llllll_opy_(config, index)
  for bstack1l111lll1_opy_ in bstack1lll111111_opy_ + list(bstack1lll1ll1l_opy_.keys()):
    if bstack1l111lll1_opy_ in bstack1lll11l1_opy_:
      bstack1l1l1lll_opy_[bstack1l111lll1_opy_] = bstack1lll11l1_opy_[bstack1l111lll1_opy_]
      del (bstack1lll11l1_opy_[bstack1l111lll1_opy_])
  if bstack1l1l11l1l1_opy_(config):
    bstack1lll11l1_opy_[bstack1ll1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack1l1l1lll_opy_)
    caps[bstack1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack1lll11l1_opy_
  else:
    bstack1lll11l1_opy_[bstack1ll1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack1ll111lll_opy_(bstack1lll11l1_opy_, bstack1l1l1lll_opy_))
    if bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack1ll1ll1l11_opy_():
  global bstack111111l1_opy_
  if bstack1lll1ll11l_opy_() <= version.parse(bstack1ll1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack111111l1_opy_ != bstack1ll1_opy_ (u"ࠪࠫग"):
      return bstack1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack111111l1_opy_ + bstack1ll1_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack1llllll1l_opy_
  if bstack111111l1_opy_ != bstack1ll1_opy_ (u"࠭ࠧच"):
    return bstack1ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack111111l1_opy_ + bstack1ll1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack1lllll1ll1_opy_
def bstack1l1l1l111l_opy_(options):
  return hasattr(options, bstack1ll1_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111ll111l_opy_(options, bstack1ll11ll11l_opy_):
  for bstack11ll1llll_opy_ in bstack1ll11ll11l_opy_:
    if bstack11ll1llll_opy_ in [bstack1ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack1ll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack11ll1llll_opy_ in options._experimental_options:
      options._experimental_options[bstack11ll1llll_opy_] = update(options._experimental_options[bstack11ll1llll_opy_],
                                                         bstack1ll11ll11l_opy_[bstack11ll1llll_opy_])
    else:
      options.add_experimental_option(bstack11ll1llll_opy_, bstack1ll11ll11l_opy_[bstack11ll1llll_opy_])
  if bstack1ll1_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack1ll11ll11l_opy_:
    for arg in bstack1ll11ll11l_opy_[bstack1ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack1ll11ll11l_opy_[bstack1ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack1ll1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack1ll11ll11l_opy_:
    for ext in bstack1ll11ll11l_opy_[bstack1ll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack1ll11ll11l_opy_[bstack1ll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack1llllll1l1_opy_(options, bstack1ll1lll11l_opy_):
  if bstack1ll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack1ll1lll11l_opy_:
    for bstack1ll111l111_opy_ in bstack1ll1lll11l_opy_[bstack1ll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack1ll111l111_opy_ in options._preferences:
        options._preferences[bstack1ll111l111_opy_] = update(options._preferences[bstack1ll111l111_opy_], bstack1ll1lll11l_opy_[bstack1ll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack1ll111l111_opy_])
      else:
        options.set_preference(bstack1ll111l111_opy_, bstack1ll1lll11l_opy_[bstack1ll1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack1ll111l111_opy_])
  if bstack1ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack1ll1lll11l_opy_:
    for arg in bstack1ll1lll11l_opy_[bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1llll11ll_opy_(options, bstack111111ll_opy_):
  if bstack1ll1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack111111ll_opy_:
    options.use_webview(bool(bstack111111ll_opy_[bstack1ll1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack111ll111l_opy_(options, bstack111111ll_opy_)
def bstack11ll111l_opy_(options, bstack1l1lll1lll_opy_):
  for bstack1ll1l1111_opy_ in bstack1l1lll1lll_opy_:
    if bstack1ll1l1111_opy_ in [bstack1ll1_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack1ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack1ll1l1111_opy_, bstack1l1lll1lll_opy_[bstack1ll1l1111_opy_])
  if bstack1ll1_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack1l1lll1lll_opy_:
    for arg in bstack1l1lll1lll_opy_[bstack1ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack1ll1_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack1l1lll1lll_opy_:
    options.bstack111l11l11_opy_(bool(bstack1l1lll1lll_opy_[bstack1ll1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack1l1ll1l111_opy_(options, bstack11l1ll111_opy_):
  for bstack1l1lll1l_opy_ in bstack11l1ll111_opy_:
    if bstack1l1lll1l_opy_ in [bstack1ll1_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack1ll1_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack1l1lll1l_opy_] = bstack11l1ll111_opy_[bstack1l1lll1l_opy_]
  if bstack1ll1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack11l1ll111_opy_:
    for bstack1ll111l1l_opy_ in bstack11l1ll111_opy_[bstack1ll1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack1111lll1_opy_(
        bstack1ll111l1l_opy_, bstack11l1ll111_opy_[bstack1ll1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack1ll111l1l_opy_])
  if bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack11l1ll111_opy_:
    for arg in bstack11l1ll111_opy_[bstack1ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack1lll1l11l1_opy_(options, caps):
  if not hasattr(options, bstack1ll1_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack1ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack111ll111l_opy_(options, caps[bstack1ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack1ll1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1llllll1l1_opy_(options, caps[bstack1ll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack11ll111l_opy_(options, caps[bstack1ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack1ll1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1llll11ll_opy_(options, caps[bstack1ll1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack1ll1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack1l1ll1l111_opy_(options, caps[bstack1ll1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack1l1ll1l1_opy_(caps):
  global bstack1lll1l1l_opy_
  if isinstance(os.environ.get(bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack1lll1l1l_opy_ = eval(os.getenv(bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack1lll1l1l_opy_:
    if bstack1l11lll1ll_opy_() < version.parse(bstack1ll1_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack1ll1_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack1ll1_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack1ll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack1ll1_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack1ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack1ll1_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack1ll1_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack1ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack1ll1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack1ll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack1ll1_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1l1l111l_opy_(options):
        return None
      for bstack1l111lll1_opy_ in caps.keys():
        options.set_capability(bstack1l111lll1_opy_, caps[bstack1l111lll1_opy_])
      bstack1lll1l11l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lll1111l_opy_(options, bstack1lll11ll1_opy_):
  if not bstack1l1l1l111l_opy_(options):
    return
  for bstack1l111lll1_opy_ in bstack1lll11ll1_opy_.keys():
    if bstack1l111lll1_opy_ in bstack111ll1l1_opy_:
      continue
    if bstack1l111lll1_opy_ in options._caps and type(options._caps[bstack1l111lll1_opy_]) in [dict, list]:
      options._caps[bstack1l111lll1_opy_] = update(options._caps[bstack1l111lll1_opy_], bstack1lll11ll1_opy_[bstack1l111lll1_opy_])
    else:
      options.set_capability(bstack1l111lll1_opy_, bstack1lll11ll1_opy_[bstack1l111lll1_opy_])
  bstack1lll1l11l1_opy_(options, bstack1lll11ll1_opy_)
  if bstack1ll1_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack1ll1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack1ll1_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack1lll1lll1l_opy_(proxy_config):
  if bstack1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack1ll1_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack1ll1_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack1ll1_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack1ll1_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack11ll1l111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack1lll1lll1l_opy_(config[bstack1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack1llll1ll11_opy_(self):
  global CONFIG
  global bstack1l1ll111l_opy_
  try:
    proxy = bstack11ll1lll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack1l1l1l11ll_opy_(proxy, bstack1ll1ll1l11_opy_())
        if len(proxies) > 0:
          protocol, bstack1llll1lll_opy_ = proxies.popitem()
          if bstack1ll1_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack1llll1lll_opy_:
            return bstack1llll1lll_opy_
          else:
            return bstack1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1llll1lll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack1l1ll111l_opy_(self)
def bstack111l1ll1_opy_():
  global CONFIG
  return bstack1l11l1ll1_opy_(CONFIG) and bstack1l1ll1ll11_opy_() and bstack1lll1ll11l_opy_() >= version.parse(bstack1l1ll11l_opy_)
def bstack1l1ll11ll_opy_():
  global CONFIG
  return (bstack1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧॳ") in CONFIG or bstack1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩॴ") in CONFIG) and bstack1l1ll11l11_opy_()
def bstack11l111lll_opy_(config):
  bstack1l1lll1ll_opy_ = {}
  if bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॵ") in config:
    bstack1l1lll1ll_opy_ = config[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ")]
  if bstack1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॷ") in config:
    bstack1l1lll1ll_opy_ = config[bstack1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ")]
  proxy = bstack11ll1lll_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")) and os.path.isfile(proxy):
      bstack1l1lll1ll_opy_[bstack1ll1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧॺ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪॻ")):
        proxies = bstack11ll1ll11_opy_(config, bstack1ll1ll1l11_opy_())
        if len(proxies) > 0:
          protocol, bstack1llll1lll_opy_ = proxies.popitem()
          if bstack1ll1_opy_ (u"ࠨ࠺࠰࠱ࠥॼ") in bstack1llll1lll_opy_:
            parsed_url = urlparse(bstack1llll1lll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll1_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") + bstack1llll1lll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l1lll1ll_opy_[bstack1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫॾ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l1lll1ll_opy_[bstack1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬॿ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l1lll1ll_opy_[bstack1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ঀ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l1lll1ll_opy_[bstack1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧঁ")] = str(parsed_url.password)
  return bstack1l1lll1ll_opy_
def bstack1lll111l1_opy_(config):
  if bstack1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪং") in config:
    return config[bstack1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ")]
  return {}
def bstack1l11llll1_opy_(caps):
  global bstack1l1lll1l11_opy_
  if bstack1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ঄") in caps:
    caps[bstack1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨআ")] = True
    if bstack1l1lll1l11_opy_:
      caps[bstack1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই")][bstack1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ঈ")] = bstack1l1lll1l11_opy_
  else:
    caps[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪউ")] = True
    if bstack1l1lll1l11_opy_:
      caps[bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧঊ")] = bstack1l1lll1l11_opy_
def bstack1ll1l111ll_opy_():
  global CONFIG
  if not bstack1l11lll1l_opy_(CONFIG):
    return
  if bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫঋ") in CONFIG and bstack1llll1l1ll_opy_(CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ")]):
    if (
      bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍") in CONFIG
      and bstack1llll1l1ll_opy_(CONFIG[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ঎")].get(bstack1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨএ")))
    ):
      logger.debug(bstack1ll1_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨঐ"))
      return
    bstack1l1lll1ll_opy_ = bstack11l111lll_opy_(CONFIG)
    bstack1l1l1ll1_opy_(CONFIG[bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1l1lll1ll_opy_)
def bstack1l1l1ll1_opy_(key, bstack1l1lll1ll_opy_):
  global bstack1l11l11ll_opy_
  logger.info(bstack1ll1l11ll_opy_)
  try:
    bstack1l11l11ll_opy_ = Local()
    bstack1l11ll111l_opy_ = {bstack1ll1_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1l11ll111l_opy_.update(bstack1l1lll1ll_opy_)
    logger.debug(bstack11111111l_opy_.format(str(bstack1l11ll111l_opy_)))
    bstack1l11l11ll_opy_.start(**bstack1l11ll111l_opy_)
    if bstack1l11l11ll_opy_.isRunning():
      logger.info(bstack1ll111l1ll_opy_)
  except Exception as e:
    bstack11111l111_opy_(bstack1llll111l1_opy_.format(str(e)))
def bstack1ll1llll_opy_():
  global bstack1l11l11ll_opy_
  if bstack1l11l11ll_opy_.isRunning():
    logger.info(bstack1l111l111_opy_)
    bstack1l11l11ll_opy_.stop()
  bstack1l11l11ll_opy_ = None
def bstack1l1l1111ll_opy_(bstack111l1111l_opy_=[]):
  global CONFIG
  bstack1ll1111l11_opy_ = []
  bstack1l1l1l1ll_opy_ = [bstack1ll1_opy_ (u"ࠨࡱࡶࠫও"), bstack1ll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack1ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack111l1111l_opy_:
      bstack1111ll1l1_opy_ = {}
      for k in bstack1l1l1l1ll_opy_:
        val = CONFIG[bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack1ll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1111ll1l1_opy_[k] = val
      if(err[bstack1ll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack1ll1_opy_ (u"ࠪࠫজ")):
        bstack1111ll1l1_opy_[bstack1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack1ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack1ll1111l11_opy_.append(bstack1111ll1l1_opy_)
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack1ll1111l11_opy_
def bstack1ll1lllll_opy_(file_name):
  bstack11ll1l1ll_opy_ = []
  try:
    bstack11ll1111l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11ll1111l_opy_):
      with open(bstack11ll1111l_opy_) as f:
        bstack1ll1l11lll_opy_ = json.load(f)
        bstack11ll1l1ll_opy_ = bstack1ll1l11lll_opy_
      os.remove(bstack11ll1111l_opy_)
    return bstack11ll1l1ll_opy_
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
    return bstack11ll1l1ll_opy_
def bstack11llll11_opy_():
  global bstack1l1l1ll1l_opy_
  global bstack1llll111_opy_
  global bstack11ll1l11l_opy_
  global bstack1111llll_opy_
  global bstack1l1lllll_opy_
  global bstack1l1l11ll1l_opy_
  global CONFIG
  bstack1ll11111l_opy_ = os.environ.get(bstack1ll1_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1ll11111l_opy_ in [bstack1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack1ll1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1l11111ll_opy_()
  percy.shutdown()
  if bstack1l1l1ll1l_opy_:
    logger.warning(bstack1lllll1l11_opy_.format(str(bstack1l1l1ll1l_opy_)))
  else:
    try:
      bstack1l1l1l1l11_opy_ = bstack1l1l1lll1l_opy_(bstack1ll1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1l1l1l1l11_opy_.get(bstack1ll1_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1l1l1l1l11_opy_.get(bstack1ll1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack1ll1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1lllll1l11_opy_.format(str(bstack1l1l1l1l11_opy_[bstack1ll1_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack1ll1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1lllll1111_opy_)
  global bstack1l11l11ll_opy_
  if bstack1l11l11ll_opy_:
    bstack1ll1llll_opy_()
  try:
    for driver in bstack1llll111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack111l1l111_opy_)
  if bstack1l1l11ll1l_opy_ == bstack1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack1l1lllll_opy_ = bstack1ll1lllll_opy_(bstack1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack1l1l11ll1l_opy_ == bstack1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1111llll_opy_) == 0:
    bstack1111llll_opy_ = bstack1ll1lllll_opy_(bstack1ll1_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1111llll_opy_) == 0:
      bstack1111llll_opy_ = bstack1ll1lllll_opy_(bstack1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1ll11lll1_opy_ = bstack1ll1_opy_ (u"ࠩࠪর")
  if len(bstack11ll1l11l_opy_) > 0:
    bstack1ll11lll1_opy_ = bstack1l1l1111ll_opy_(bstack11ll1l11l_opy_)
  elif len(bstack1111llll_opy_) > 0:
    bstack1ll11lll1_opy_ = bstack1l1l1111ll_opy_(bstack1111llll_opy_)
  elif len(bstack1l1lllll_opy_) > 0:
    bstack1ll11lll1_opy_ = bstack1l1l1111ll_opy_(bstack1l1lllll_opy_)
  elif len(bstack111111lll_opy_) > 0:
    bstack1ll11lll1_opy_ = bstack1l1l1111ll_opy_(bstack111111lll_opy_)
  if bool(bstack1ll11lll1_opy_):
    bstack11llll11l_opy_(bstack1ll11lll1_opy_)
  else:
    bstack11llll11l_opy_()
  bstack1ll1111l_opy_(bstack1lll1llll_opy_, logger)
  bstack11ll1l1l1_opy_.bstack111ll1111_opy_(CONFIG)
  if len(bstack1l1lllll_opy_) > 0:
    sys.exit(len(bstack1l1lllll_opy_))
def bstack1l1lll11ll_opy_(bstack1l1ll1l1l_opy_, frame):
  global bstack111l1l1l1_opy_
  logger.error(bstack111l1ll11_opy_)
  bstack111l1l1l1_opy_.bstack1l1lll111l_opy_(bstack1ll1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭঱"), bstack1l1ll1l1l_opy_)
  if hasattr(signal, bstack1ll1_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬল")):
    bstack111l1l1l1_opy_.bstack1l1lll111l_opy_(bstack1ll1_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ঳"), signal.Signals(bstack1l1ll1l1l_opy_).name)
  else:
    bstack111l1l1l1_opy_.bstack1l1lll111l_opy_(bstack1ll1_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭঴"), bstack1ll1_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫ঵"))
  bstack1ll11111l_opy_ = os.environ.get(bstack1ll1_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩশ"))
  if bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩষ"):
    bstack1lllll1l1_opy_.stop(bstack111l1l1l1_opy_.get_property(bstack1ll1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪস")))
  bstack11llll11_opy_()
  sys.exit(1)
def bstack11111l111_opy_(err):
  logger.critical(bstack1ll11l1ll_opy_.format(str(err)))
  bstack11llll11l_opy_(bstack1ll11l1ll_opy_.format(str(err)), True)
  atexit.unregister(bstack11llll11_opy_)
  bstack1l11111ll_opy_()
  sys.exit(1)
def bstack1l1lll11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11llll11l_opy_(message, True)
  atexit.unregister(bstack11llll11_opy_)
  bstack1l11111ll_opy_()
  sys.exit(1)
def bstack1111l1l11_opy_():
  global CONFIG
  global bstack1llll1l1l1_opy_
  global bstack1lllll11_opy_
  global bstack1l1l111l_opy_
  CONFIG = bstack1llllll111_opy_()
  load_dotenv(CONFIG.get(bstack1ll1_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬহ")))
  bstack1lllll1l1l_opy_()
  bstack111l11l1l_opy_()
  CONFIG = bstack1ll1l1llll_opy_(CONFIG)
  update(CONFIG, bstack1lllll11_opy_)
  update(CONFIG, bstack1llll1l1l1_opy_)
  CONFIG = bstack1l1ll1l1l1_opy_(CONFIG)
  bstack1l1l111l_opy_ = bstack1l11lll1l_opy_(CONFIG)
  bstack111l1l1l1_opy_.bstack1l1lll111l_opy_(bstack1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭঺"), bstack1l1l111l_opy_)
  if (bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঻") in CONFIG and bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") in bstack1llll1l1l1_opy_) or (
          bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫঽ") in CONFIG and bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬা") not in bstack1lllll11_opy_):
    if os.getenv(bstack1ll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧি")):
      CONFIG[bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ী")] = os.getenv(bstack1ll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩু"))
    else:
      bstack1ll1111l1_opy_()
  elif (bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩূ") not in CONFIG and bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩৃ") in CONFIG) or (
          bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫৄ") in bstack1lllll11_opy_ and bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ৅") not in bstack1llll1l1l1_opy_):
    del (CONFIG[bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৆")])
  if bstack1l1llll11_opy_(CONFIG):
    bstack11111l111_opy_(bstack11l1lllll_opy_)
  bstack111llllll_opy_()
  bstack111l11111_opy_()
  if bstack1lll1l1l_opy_:
    CONFIG[bstack1ll1_opy_ (u"ࠫࡦࡶࡰࠨে")] = bstack1l11ll111_opy_(CONFIG)
    logger.info(bstack1l1lll1111_opy_.format(CONFIG[bstack1ll1_opy_ (u"ࠬࡧࡰࡱࠩৈ")]))
  if not bstack1l1l111l_opy_:
    CONFIG[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৉")] = [{}]
def bstack1l1ll1111_opy_(config, bstack1lll1ll1l1_opy_):
  global CONFIG
  global bstack1lll1l1l_opy_
  CONFIG = config
  bstack1lll1l1l_opy_ = bstack1lll1ll1l1_opy_
def bstack111l11111_opy_():
  global CONFIG
  global bstack1lll1l1l_opy_
  if bstack1ll1_opy_ (u"ࠧࡢࡲࡳࠫ৊") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1lll11_opy_(e, bstack111l11ll_opy_)
    bstack1lll1l1l_opy_ = True
    bstack111l1l1l1_opy_.bstack1l1lll111l_opy_(bstack1ll1_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧো"), True)
def bstack1l11ll111_opy_(config):
  bstack1lll1l11l_opy_ = bstack1ll1_opy_ (u"ࠩࠪৌ")
  app = config[bstack1ll1_opy_ (u"ࠪࡥࡵࡶ্ࠧ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1llll1l1_opy_:
      if os.path.exists(app):
        bstack1lll1l11l_opy_ = bstack1ll1111111_opy_(config, app)
      elif bstack11l11lll_opy_(app):
        bstack1lll1l11l_opy_ = app
      else:
        bstack11111l111_opy_(bstack1ll1ll11l1_opy_.format(app))
    else:
      if bstack11l11lll_opy_(app):
        bstack1lll1l11l_opy_ = app
      elif os.path.exists(app):
        bstack1lll1l11l_opy_ = bstack1ll1111111_opy_(app)
      else:
        bstack11111l111_opy_(bstack1ll1lll11_opy_)
  else:
    if len(app) > 2:
      bstack11111l111_opy_(bstack111lllll_opy_)
    elif len(app) == 2:
      if bstack1ll1_opy_ (u"ࠫࡵࡧࡴࡩࠩৎ") in app and bstack1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ৏") in app:
        if os.path.exists(app[bstack1ll1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ৐")]):
          bstack1lll1l11l_opy_ = bstack1ll1111111_opy_(config, app[bstack1ll1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ৑")], app[bstack1ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ৒")])
        else:
          bstack11111l111_opy_(bstack1ll1ll11l1_opy_.format(app))
      else:
        bstack11111l111_opy_(bstack111lllll_opy_)
    else:
      for key in app:
        if key in bstack1lll11ll11_opy_:
          if key == bstack1ll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৓"):
            if os.path.exists(app[key]):
              bstack1lll1l11l_opy_ = bstack1ll1111111_opy_(config, app[key])
            else:
              bstack11111l111_opy_(bstack1ll1ll11l1_opy_.format(app))
          else:
            bstack1lll1l11l_opy_ = app[key]
        else:
          bstack11111l111_opy_(bstack111l111l1_opy_)
  return bstack1lll1l11l_opy_
def bstack11l11lll_opy_(bstack1lll1l11l_opy_):
  import re
  bstack1l11l1ll_opy_ = re.compile(bstack1ll1_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ৔"))
  bstack1111l11l1_opy_ = re.compile(bstack1ll1_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ৕"))
  if bstack1ll1_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫ৖") in bstack1lll1l11l_opy_ or re.fullmatch(bstack1l11l1ll_opy_, bstack1lll1l11l_opy_) or re.fullmatch(bstack1111l11l1_opy_, bstack1lll1l11l_opy_):
    return True
  else:
    return False
def bstack1ll1111111_opy_(config, path, bstack1l11l1l11l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll1_opy_ (u"࠭ࡲࡣࠩৗ")).read()).hexdigest()
  bstack1l1111lll_opy_ = bstack11111l1l_opy_(md5_hash)
  bstack1lll1l11l_opy_ = None
  if bstack1l1111lll_opy_:
    logger.info(bstack1lll11111l_opy_.format(bstack1l1111lll_opy_, md5_hash))
    return bstack1l1111lll_opy_
  bstack1l11lll1l1_opy_ = MultipartEncoder(
    fields={
      bstack1ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࠬ৘"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll1_opy_ (u"ࠨࡴࡥࠫ৙")), bstack1ll1_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭৚")),
      bstack1ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭৛"): bstack1l11l1l11l_opy_
    }
  )
  response = requests.post(bstack1lllllll1l_opy_, data=bstack1l11lll1l1_opy_,
                           headers={bstack1ll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪড়"): bstack1l11lll1l1_opy_.content_type},
                           auth=(config[bstack1ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧঢ়")], config[bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ৞")]))
  try:
    res = json.loads(response.text)
    bstack1lll1l11l_opy_ = res[bstack1ll1_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨয়")]
    logger.info(bstack1l1l1111l_opy_.format(bstack1lll1l11l_opy_))
    bstack1ll1ll11l_opy_(md5_hash, bstack1lll1l11l_opy_)
  except ValueError as err:
    bstack11111l111_opy_(bstack1l11ll1111_opy_.format(str(err)))
  return bstack1lll1l11l_opy_
def bstack111llllll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11l111111_opy_
  bstack11ll11ll_opy_ = 1
  bstack1ll11ll1l1_opy_ = 1
  if bstack1ll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨৠ") in CONFIG:
    bstack1ll11ll1l1_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩৡ")]
  else:
    bstack1ll11ll1l1_opy_ = bstack1lll1l11_opy_(framework_name, args) or 1
  if bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ৢ") in CONFIG:
    bstack11ll11ll_opy_ = len(CONFIG[bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৣ")])
  bstack11l111111_opy_ = int(bstack1ll11ll1l1_opy_) * int(bstack11ll11ll_opy_)
def bstack1lll1l11_opy_(framework_name, args):
  if framework_name == bstack1ll1ll1ll1_opy_ and args and bstack1ll1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ৤") in args:
      bstack1ll1111ll_opy_ = args.index(bstack1ll1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ৥"))
      return int(args[bstack1ll1111ll_opy_ + 1]) or 1
  return 1
def bstack11111l1l_opy_(md5_hash):
  bstack1lll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠧࡿࠩ০")), bstack1ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ১"), bstack1ll1_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ২"))
  if os.path.exists(bstack1lll1lll1_opy_):
    bstack11l11l111_opy_ = json.load(open(bstack1lll1lll1_opy_, bstack1ll1_opy_ (u"ࠪࡶࡧ࠭৩")))
    if md5_hash in bstack11l11l111_opy_:
      bstack11ll11lll_opy_ = bstack11l11l111_opy_[md5_hash]
      bstack1l1l1l1lll_opy_ = datetime.datetime.now()
      bstack1l111ll1l_opy_ = datetime.datetime.strptime(bstack11ll11lll_opy_[bstack1ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ৪")], bstack1ll1_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ৫"))
      if (bstack1l1l1l1lll_opy_ - bstack1l111ll1l_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11ll11lll_opy_[bstack1ll1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ৬")]):
        return None
      return bstack11ll11lll_opy_[bstack1ll1_opy_ (u"ࠧࡪࡦࠪ৭")]
  else:
    return None
def bstack1ll1ll11l_opy_(md5_hash, bstack1lll1l11l_opy_):
  bstack1l11l11l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠨࢀࠪ৮")), bstack1ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ৯"))
  if not os.path.exists(bstack1l11l11l1_opy_):
    os.makedirs(bstack1l11l11l1_opy_)
  bstack1lll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠪࢂࠬৰ")), bstack1ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫৱ"), bstack1ll1_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭৲"))
  bstack1l11l1llll_opy_ = {
    bstack1ll1_opy_ (u"࠭ࡩࡥࠩ৳"): bstack1lll1l11l_opy_,
    bstack1ll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ৴"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll1_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ৵")),
    bstack1ll1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ৶"): str(__version__)
  }
  if os.path.exists(bstack1lll1lll1_opy_):
    bstack11l11l111_opy_ = json.load(open(bstack1lll1lll1_opy_, bstack1ll1_opy_ (u"ࠪࡶࡧ࠭৷")))
  else:
    bstack11l11l111_opy_ = {}
  bstack11l11l111_opy_[md5_hash] = bstack1l11l1llll_opy_
  with open(bstack1lll1lll1_opy_, bstack1ll1_opy_ (u"ࠦࡼ࠱ࠢ৸")) as outfile:
    json.dump(bstack11l11l111_opy_, outfile)
def bstack1llll11l11_opy_(self):
  return
def bstack1111l1lll_opy_(self):
  return
def bstack1l1ll1lll_opy_(self):
  global bstack1ll111lll1_opy_
  bstack1ll111lll1_opy_(self)
def bstack1l11ll11_opy_():
  global bstack1l11lllll_opy_
  bstack1l11lllll_opy_ = True
def bstack1ll1lll1_opy_(self):
  global bstack11l1l1l11_opy_
  global bstack11l11llll_opy_
  global bstack1l111l11_opy_
  try:
    if bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ৹") in bstack11l1l1l11_opy_ and self.session_id != None and bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ৺"), bstack1ll1_opy_ (u"ࠧࠨ৻")) != bstack1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩৼ"):
      bstack1l1l1l11_opy_ = bstack1ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ৽") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ৾")
      if bstack1l1l1l11_opy_ == bstack1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ৿"):
        bstack11l1l111_opy_(logger)
      if self != None:
        bstack11111l1ll_opy_(self, bstack1l1l1l11_opy_, bstack1ll1_opy_ (u"ࠬ࠲ࠠࠨ਀").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll1_opy_ (u"࠭ࠧਁ")
    if bstack1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧਂ") in bstack11l1l1l11_opy_ and getattr(threading.current_thread(), bstack1ll1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧਃ"), None):
      bstack1l1111l11_opy_.bstack1l1l11l1l_opy_(self, bstack1ll11lll1l_opy_, logger, wait=True)
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ਄") + str(e))
  bstack1l111l11_opy_(self)
  self.session_id = None
def bstack11l11l11l_opy_(self, command_executor=bstack1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲࠵࠷࠽࠮࠱࠰࠳࠲࠶ࡀ࠴࠵࠶࠷ࠦਅ"), *args, **kwargs):
  bstack1l1lll11l_opy_ = bstack1l11l11l_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack1ll1_opy_ (u"ࠫࡈࡵ࡭࡮ࡣࡱࡨࠥࡋࡸࡦࡥࡸࡸࡴࡸࠠࡸࡪࡨࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫ࡧ࡬ࡴࡧࠣ࠱ࠥࢁࡽࠨਆ").format(str(command_executor)))
    logger.debug(bstack1ll1_opy_ (u"ࠬࡎࡵࡣࠢࡘࡖࡑࠦࡩࡴࠢ࠰ࠤࢀࢃࠧਇ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩਈ") in command_executor._url:
      bstack111l1l1l1_opy_.bstack1l1lll111l_opy_(bstack1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨਉ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਊ") in command_executor):
    bstack111l1l1l1_opy_.bstack1l1lll111l_opy_(bstack1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ਋"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1lllll1l1_opy_.bstack1l1l1ll11_opy_(self)
  return bstack1l1lll11l_opy_
def bstack1l111ll1_opy_(args):
  return bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫ਌") in str(args)
def bstack1l111111_opy_(self, driver_command, *args, **kwargs):
  global bstack1l11l11l11_opy_
  global bstack11llll1l1_opy_
  bstack1l11lllll1_opy_ = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ਍"), None) and bstack1ll1llll1l_opy_(
          threading.current_thread(), bstack1ll1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ਎"), None)
  bstack1llllllll1_opy_ = getattr(self, bstack1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ਏ"), None) != None and getattr(self, bstack1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧਐ"), None) == True
  if not bstack11llll1l1_opy_ and bstack1l1l111l_opy_ and bstack1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ਑") in CONFIG and CONFIG[bstack1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ਒")] == True and bstack1111l11ll_opy_.bstack1l1lllll11_opy_(driver_command) and (bstack1llllllll1_opy_ or bstack1l11lllll1_opy_) and not bstack1l111ll1_opy_(args):
    try:
      bstack11llll1l1_opy_ = True
      logger.debug(bstack1ll1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬਓ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1ll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩਔ").format(str(err)))
    bstack11llll1l1_opy_ = False
  response = bstack1l11l11l11_opy_(self, driver_command, *args, **kwargs)
  if bstack1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਕ") in str(bstack11l1l1l11_opy_).lower() and bstack1lllll1l1_opy_.on():
    try:
      if driver_command == bstack1ll1_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪਖ"):
        bstack1lllll1l1_opy_.bstack1llll111ll_opy_({
            bstack1ll1_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ਗ"): response[bstack1ll1_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧਘ")],
            bstack1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩਙ"): bstack1lllll1l1_opy_.current_test_uuid() if bstack1lllll1l1_opy_.current_test_uuid() else bstack1lllll1l1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1ll11l1ll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11l11llll_opy_
  global bstack1ll1llll1_opy_
  global bstack11l111l1l_opy_
  global bstack1llllll11_opy_
  global bstack1l11lll11l_opy_
  global bstack11l1l1l11_opy_
  global bstack1l11l11l_opy_
  global bstack1llll111_opy_
  global bstack1ll11l1lll_opy_
  global bstack1ll11lll1l_opy_
  CONFIG[bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬਚ")] = str(bstack11l1l1l11_opy_) + str(__version__)
  command_executor = bstack1ll1ll1l11_opy_()
  logger.debug(bstack1l111lll_opy_.format(command_executor))
  proxy = bstack11ll1l111_opy_(CONFIG, proxy)
  bstack1lll1l1ll_opy_ = 0 if bstack1ll1llll1_opy_ < 0 else bstack1ll1llll1_opy_
  try:
    if bstack1llllll11_opy_ is True:
      bstack1lll1l1ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l11lll11l_opy_ is True:
      bstack1lll1l1ll_opy_ = int(threading.current_thread().name)
  except:
    bstack1lll1l1ll_opy_ = 0
  bstack1lll11ll1_opy_ = bstack11l111ll1_opy_(CONFIG, bstack1lll1l1ll_opy_)
  logger.debug(bstack111ll111_opy_.format(str(bstack1lll11ll1_opy_)))
  if bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨਛ") in CONFIG and bstack1llll1l1ll_opy_(CONFIG[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩਜ")]):
    bstack1l11llll1_opy_(bstack1lll11ll1_opy_)
  if bstack1111111l1_opy_.bstack1ll1ll1111_opy_(CONFIG, bstack1lll1l1ll_opy_) and bstack1111111l1_opy_.bstack1l11ll1l_opy_(bstack1lll11ll1_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack1111111l1_opy_.set_capabilities(bstack1lll11ll1_opy_, CONFIG)
  if desired_capabilities:
    bstack11l1l1111_opy_ = bstack1ll1l1llll_opy_(desired_capabilities)
    bstack11l1l1111_opy_[bstack1ll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ਝ")] = bstack1l1l11l1l1_opy_(CONFIG)
    bstack1ll111ll1l_opy_ = bstack11l111ll1_opy_(bstack11l1l1111_opy_)
    if bstack1ll111ll1l_opy_:
      bstack1lll11ll1_opy_ = update(bstack1ll111ll1l_opy_, bstack1lll11ll1_opy_)
    desired_capabilities = None
  if options:
    bstack1lll1111l_opy_(options, bstack1lll11ll1_opy_)
  if not options:
    options = bstack1l1ll1l1_opy_(bstack1lll11ll1_opy_)
  bstack1ll11lll1l_opy_ = CONFIG.get(bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਞ"))[bstack1lll1l1ll_opy_]
  if proxy and bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨਟ")):
    options.proxy(proxy)
  if options and bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨਠ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1lll1ll11l_opy_() < version.parse(bstack1ll1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩਡ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll11ll1_opy_)
  logger.info(bstack1lll111l1l_opy_)
  if bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫਢ")):
    bstack1l11l11l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫਣ")):
    bstack1l11l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ਤ")):
    bstack1l11l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l11l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack11l11l1ll_opy_ = bstack1ll1_opy_ (u"ࠧࠨਥ")
    if bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩਦ")):
      bstack11l11l1ll_opy_ = self.caps.get(bstack1ll1_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤਧ"))
    else:
      bstack11l11l1ll_opy_ = self.capabilities.get(bstack1ll1_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥਨ"))
    if bstack11l11l1ll_opy_:
      bstack1ll1l111_opy_(bstack11l11l1ll_opy_)
      if bstack1lll1ll11l_opy_() <= version.parse(bstack1ll1_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ਩")):
        self.command_executor._url = bstack1ll1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨਪ") + bstack111111l1_opy_ + bstack1ll1_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥਫ")
      else:
        self.command_executor._url = bstack1ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤਬ") + bstack11l11l1ll_opy_ + bstack1ll1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤਭ")
      logger.debug(bstack11ll11ll1_opy_.format(bstack11l11l1ll_opy_))
    else:
      logger.debug(bstack1l1l11ll1_opy_.format(bstack1ll1_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥਮ")))
  except Exception as e:
    logger.debug(bstack1l1l11ll1_opy_.format(e))
  if bstack1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਯ") in bstack11l1l1l11_opy_:
    bstack1l11l1111_opy_(bstack1ll1llll1_opy_, bstack1ll11l1lll_opy_)
  bstack11l11llll_opy_ = self.session_id
  if bstack1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਰ") in bstack11l1l1l11_opy_ or bstack1ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ਱") in bstack11l1l1l11_opy_ or bstack1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਲ") in bstack11l1l1l11_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1lllll1l1_opy_.bstack1l1l1ll11_opy_(self)
  bstack1llll111_opy_.append(self)
  if bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਲ਼") in CONFIG and bstack1ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭਴") in CONFIG[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਵ")][bstack1lll1l1ll_opy_]:
    bstack11l111l1l_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਸ਼")][bstack1lll1l1ll_opy_][bstack1ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ਷")]
  logger.debug(bstack1l11llll1l_opy_.format(bstack11l11llll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1llll11l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11ll11111_opy_
      if(bstack1ll1_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢਸ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"࠭ࡾࠨਹ")), bstack1ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ਺"), bstack1ll1_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ਻")), bstack1ll1_opy_ (u"ࠩࡺ਼ࠫ")) as fp:
          fp.write(bstack1ll1_opy_ (u"ࠥࠦ਽"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll1_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨਾ")))):
          with open(args[1], bstack1ll1_opy_ (u"ࠬࡸࠧਿ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll1_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬੀ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1l111l11_opy_)
            lines.insert(1, bstack111111l1l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll1_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤੁ")), bstack1ll1_opy_ (u"ࠨࡹࠪੂ")) as bstack1ll11l1l1_opy_:
              bstack1ll11l1l1_opy_.writelines(lines)
        CONFIG[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ੃")] = str(bstack11l1l1l11_opy_) + str(__version__)
        bstack1lll1l1ll_opy_ = 0 if bstack1ll1llll1_opy_ < 0 else bstack1ll1llll1_opy_
        try:
          if bstack1llllll11_opy_ is True:
            bstack1lll1l1ll_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l11lll11l_opy_ is True:
            bstack1lll1l1ll_opy_ = int(threading.current_thread().name)
        except:
          bstack1lll1l1ll_opy_ = 0
        CONFIG[bstack1ll1_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ੄")] = False
        CONFIG[bstack1ll1_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ੅")] = True
        bstack1lll11ll1_opy_ = bstack11l111ll1_opy_(CONFIG, bstack1lll1l1ll_opy_)
        logger.debug(bstack111ll111_opy_.format(str(bstack1lll11ll1_opy_)))
        if CONFIG.get(bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ੆")):
          bstack1l11llll1_opy_(bstack1lll11ll1_opy_)
        if bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੇ") in CONFIG and bstack1ll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੈ") in CONFIG[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੉")][bstack1lll1l1ll_opy_]:
          bstack11l111l1l_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੊")][bstack1lll1l1ll_opy_][bstack1ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨੋ")]
        args.append(os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠫࢃ࠭ੌ")), bstack1ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯੍ࠬ"), bstack1ll1_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ੎")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lll11ll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll1_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ੏"))
      bstack11ll11111_opy_ = True
      return bstack1lll1l11ll_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11l11lll1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1ll1llll1_opy_
    global bstack11l111l1l_opy_
    global bstack1llllll11_opy_
    global bstack1l11lll11l_opy_
    global bstack11l1l1l11_opy_
    CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ੐")] = str(bstack11l1l1l11_opy_) + str(__version__)
    bstack1lll1l1ll_opy_ = 0 if bstack1ll1llll1_opy_ < 0 else bstack1ll1llll1_opy_
    try:
      if bstack1llllll11_opy_ is True:
        bstack1lll1l1ll_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l11lll11l_opy_ is True:
        bstack1lll1l1ll_opy_ = int(threading.current_thread().name)
    except:
      bstack1lll1l1ll_opy_ = 0
    CONFIG[bstack1ll1_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣੑ")] = True
    bstack1lll11ll1_opy_ = bstack11l111ll1_opy_(CONFIG, bstack1lll1l1ll_opy_)
    logger.debug(bstack111ll111_opy_.format(str(bstack1lll11ll1_opy_)))
    if CONFIG.get(bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ੒")):
      bstack1l11llll1_opy_(bstack1lll11ll1_opy_)
    if bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੓") in CONFIG and bstack1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ੔") in CONFIG[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੕")][bstack1lll1l1ll_opy_]:
      bstack11l111l1l_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੖")][bstack1lll1l1ll_opy_][bstack1ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭੗")]
    import urllib
    import json
    bstack11l1111l_opy_ = bstack1ll1_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ੘") + urllib.parse.quote(json.dumps(bstack1lll11ll1_opy_))
    browser = self.connect(bstack11l1111l_opy_)
    return browser
except Exception as e:
    pass
def bstack1lll11llll_opy_():
    if not bstack1l1l111l_opy_:
      return
    global bstack11ll11111_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11l11lll1_opy_
        bstack11ll11111_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1llll11l_opy_
      bstack11ll11111_opy_ = True
    except Exception as e:
      pass
def bstack11l1lll1_opy_(context, bstack1l1llll1_opy_):
  try:
    context.page.evaluate(bstack1ll1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦਖ਼"), bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨਗ਼")+ json.dumps(bstack1l1llll1_opy_) + bstack1ll1_opy_ (u"ࠧࢃࡽࠣਜ਼"))
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦੜ"), e)
def bstack1ll111ll1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1ll1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ੝"), bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ਫ਼") + json.dumps(message) + bstack1ll1_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ੟") + json.dumps(level) + bstack1ll1_opy_ (u"ࠪࢁࢂ࠭੠"))
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢ੡"), e)
def bstack1lll1ll1ll_opy_(self, url):
  global bstack111l1lll_opy_
  try:
    bstack1ll11llll1_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll111llll_opy_.format(str(err)))
  try:
    bstack111l1lll_opy_(self, url)
  except Exception as e:
    try:
      bstack111l1llll_opy_ = str(e)
      if any(err_msg in bstack111l1llll_opy_ for err_msg in bstack1l1l11l111_opy_):
        bstack1ll11llll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll111llll_opy_.format(str(err)))
    raise e
def bstack1l1l11111_opy_(self):
  global bstack1l1ll1ll1l_opy_
  bstack1l1ll1ll1l_opy_ = self
  return
def bstack1l1111ll1_opy_(self):
  global bstack1lll111l11_opy_
  bstack1lll111l11_opy_ = self
  return
def bstack1lll111lll_opy_(test_name, bstack1llll1ll_opy_):
  global CONFIG
  if CONFIG.get(bstack1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ੢"), False):
    bstack11l111l11_opy_ = os.path.relpath(bstack1llll1ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l111l11_opy_)
    bstack1l11l1l1ll_opy_ = suite_name + bstack1ll1_opy_ (u"ࠨ࠭ࠣ੣") + test_name
    threading.current_thread().percySessionName = bstack1l11l1l1ll_opy_
def bstack1l11l11ll1_opy_(self, test, *args, **kwargs):
  global bstack1l11l1l11_opy_
  test_name = None
  bstack1llll1ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1llll1ll_opy_ = str(test.source)
  bstack1lll111lll_opy_(test_name, bstack1llll1ll_opy_)
  bstack1l11l1l11_opy_(self, test, *args, **kwargs)
def bstack1l1l1lll11_opy_(driver, bstack1l11l1l1ll_opy_):
  if not bstack1111lll11_opy_ and bstack1l11l1l1ll_opy_:
      bstack11lll111l_opy_ = {
          bstack1ll1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ੤"): bstack1ll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੥"),
          bstack1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ੦"): {
              bstack1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ੧"): bstack1l11l1l1ll_opy_
          }
      }
      bstack1l11ll11l_opy_ = bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੨").format(json.dumps(bstack11lll111l_opy_))
      driver.execute_script(bstack1l11ll11l_opy_)
  if bstack11l1l11ll_opy_:
      bstack1ll11111_opy_ = {
          bstack1ll1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ੩"): bstack1ll1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ੪"),
          bstack1ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੫"): {
              bstack1ll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭੬"): bstack1l11l1l1ll_opy_ + bstack1ll1_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ੭"),
              bstack1ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ੮"): bstack1ll1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ੯")
          }
      }
      if bstack11l1l11ll_opy_.status == bstack1ll1_opy_ (u"ࠬࡖࡁࡔࡕࠪੰ"):
          bstack1l1l11ll_opy_ = bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫੱ").format(json.dumps(bstack1ll11111_opy_))
          driver.execute_script(bstack1l1l11ll_opy_)
          bstack11111l1ll_opy_(driver, bstack1ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧੲ"))
      elif bstack11l1l11ll_opy_.status == bstack1ll1_opy_ (u"ࠨࡈࡄࡍࡑ࠭ੳ"):
          reason = bstack1ll1_opy_ (u"ࠤࠥੴ")
          bstack1lllll11l_opy_ = bstack1l11l1l1ll_opy_ + bstack1ll1_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫੵ")
          if bstack11l1l11ll_opy_.message:
              reason = str(bstack11l1l11ll_opy_.message)
              bstack1lllll11l_opy_ = bstack1lllll11l_opy_ + bstack1ll1_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫ੶") + reason
          bstack1ll11111_opy_[bstack1ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ੷")] = {
              bstack1ll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ੸"): bstack1ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭੹"),
              bstack1ll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭੺"): bstack1lllll11l_opy_
          }
          bstack1l1l11ll_opy_ = bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ੻").format(json.dumps(bstack1ll11111_opy_))
          driver.execute_script(bstack1l1l11ll_opy_)
          bstack11111l1ll_opy_(driver, bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ੼"), reason)
          bstack1ll11l111_opy_(reason, str(bstack11l1l11ll_opy_), str(bstack1ll1llll1_opy_), logger)
def bstack1l111111l_opy_(driver, test):
  if CONFIG.get(bstack1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ੽"), False) and CONFIG.get(bstack1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨ੾"), bstack1ll1_opy_ (u"ࠨࡡࡶࡶࡲࠦ੿")) == bstack1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ઀"):
      bstack1lll1llll1_opy_ = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫઁ"), None)
      bstack1l1l1ll111_opy_(driver, bstack1lll1llll1_opy_)
  if bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ં"), None) and bstack1ll1llll1l_opy_(
          threading.current_thread(), bstack1ll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩઃ"), None):
      logger.info(bstack1ll1_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠣࠦ઄"))
      bstack1111111l1_opy_.bstack1ll11l11ll_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None,
                              path=test.source, bstack111l1l11l_opy_=bstack1ll11lll1l_opy_)
def bstack1llll1lll1_opy_(test, bstack1l11l1l1ll_opy_):
    try:
      data = {}
      if test:
        data[bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪઅ")] = bstack1l11l1l1ll_opy_
      if bstack11l1l11ll_opy_:
        if bstack11l1l11ll_opy_.status == bstack1ll1_opy_ (u"࠭ࡐࡂࡕࡖࠫઆ"):
          data[bstack1ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧઇ")] = bstack1ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨઈ")
        elif bstack11l1l11ll_opy_.status == bstack1ll1_opy_ (u"ࠩࡉࡅࡎࡒࠧઉ"):
          data[bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪઊ")] = bstack1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫઋ")
          if bstack11l1l11ll_opy_.message:
            data[bstack1ll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬઌ")] = str(bstack11l1l11ll_opy_.message)
      user = CONFIG[bstack1ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨઍ")]
      key = CONFIG[bstack1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ઎")]
      url = bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳ࠭એ").format(user, key, bstack11l11llll_opy_)
      headers = {
        bstack1ll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨઐ"): bstack1ll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ઑ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack11111ll1l_opy_.format(str(e)))
def bstack1lllll111l_opy_(test, bstack1l11l1l1ll_opy_):
  global CONFIG
  global bstack1lll111l11_opy_
  global bstack1l1ll1ll1l_opy_
  global bstack11l11llll_opy_
  global bstack11l1l11ll_opy_
  global bstack11l111l1l_opy_
  global bstack1l11111l_opy_
  global bstack11lllll11_opy_
  global bstack1llll11l1_opy_
  global bstack11ll11l1_opy_
  global bstack1llll111_opy_
  global bstack1ll11lll1l_opy_
  try:
    if not bstack11l11llll_opy_:
      with open(os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠫࢃ࠭઒")), bstack1ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬઓ"), bstack1ll1_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨઔ"))) as f:
        bstack1ll1l1l1l1_opy_ = json.loads(bstack1ll1_opy_ (u"ࠢࡼࠤક") + f.read().strip() + bstack1ll1_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪખ") + bstack1ll1_opy_ (u"ࠤࢀࠦગ"))
        bstack11l11llll_opy_ = bstack1ll1l1l1l1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1llll111_opy_:
    for driver in bstack1llll111_opy_:
      if bstack11l11llll_opy_ == driver.session_id:
        if test:
          bstack1l111111l_opy_(driver, test)
        bstack1l1l1lll11_opy_(driver, bstack1l11l1l1ll_opy_)
  elif bstack11l11llll_opy_:
    bstack1llll1lll1_opy_(test, bstack1l11l1l1ll_opy_)
  if bstack1lll111l11_opy_:
    bstack11lllll11_opy_(bstack1lll111l11_opy_)
  if bstack1l1ll1ll1l_opy_:
    bstack1llll11l1_opy_(bstack1l1ll1ll1l_opy_)
  if bstack1l11lllll_opy_:
    bstack11ll11l1_opy_()
def bstack1l11llll11_opy_(self, test, *args, **kwargs):
  bstack1l11l1l1ll_opy_ = None
  if test:
    bstack1l11l1l1ll_opy_ = str(test.name)
  bstack1lllll111l_opy_(test, bstack1l11l1l1ll_opy_)
  bstack1l11111l_opy_(self, test, *args, **kwargs)
def bstack11l11l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11111l1l1_opy_
  global CONFIG
  global bstack1llll111_opy_
  global bstack11l11llll_opy_
  bstack1l11ll11l1_opy_ = None
  try:
    if bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩઘ"), None):
      try:
        if not bstack11l11llll_opy_:
          with open(os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠫࢃ࠭ઙ")), bstack1ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬચ"), bstack1ll1_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨછ"))) as f:
            bstack1ll1l1l1l1_opy_ = json.loads(bstack1ll1_opy_ (u"ࠢࡼࠤજ") + f.read().strip() + bstack1ll1_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪઝ") + bstack1ll1_opy_ (u"ࠤࢀࠦઞ"))
            bstack11l11llll_opy_ = bstack1ll1l1l1l1_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1llll111_opy_:
        for driver in bstack1llll111_opy_:
          if bstack11l11llll_opy_ == driver.session_id:
            bstack1l11ll11l1_opy_ = driver
    bstack1lll1l111l_opy_ = bstack1111111l1_opy_.bstack1l11l1lll_opy_(CONFIG, test.tags)
    if bstack1l11ll11l1_opy_:
      threading.current_thread().isA11yTest = bstack1111111l1_opy_.bstack1111lll1l_opy_(bstack1l11ll11l1_opy_, bstack1lll1l111l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1lll1l111l_opy_
  except:
    pass
  bstack11111l1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l1l11ll_opy_
  bstack11l1l11ll_opy_ = self._test
def bstack11llll1ll_opy_():
  global bstack1l1l1lll1_opy_
  try:
    if os.path.exists(bstack1l1l1lll1_opy_):
      os.remove(bstack1l1l1lll1_opy_)
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ટ") + str(e))
def bstack1ll111l11_opy_():
  global bstack1l1l1lll1_opy_
  bstack1l1l1l1l11_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1l1lll1_opy_):
      with open(bstack1l1l1lll1_opy_, bstack1ll1_opy_ (u"ࠫࡼ࠭ઠ")):
        pass
      with open(bstack1l1l1lll1_opy_, bstack1ll1_opy_ (u"ࠧࡽࠫࠣડ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1l1lll1_opy_):
      bstack1l1l1l1l11_opy_ = json.load(open(bstack1l1l1lll1_opy_, bstack1ll1_opy_ (u"࠭ࡲࡣࠩઢ")))
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩણ") + str(e))
  finally:
    return bstack1l1l1l1l11_opy_
def bstack1l11l1111_opy_(platform_index, item_index):
  global bstack1l1l1lll1_opy_
  try:
    bstack1l1l1l1l11_opy_ = bstack1ll111l11_opy_()
    bstack1l1l1l1l11_opy_[item_index] = platform_index
    with open(bstack1l1l1lll1_opy_, bstack1ll1_opy_ (u"ࠣࡹ࠮ࠦત")) as outfile:
      json.dump(bstack1l1l1l1l11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧથ") + str(e))
def bstack1l1l1l1l1l_opy_(bstack111ll1ll1_opy_):
  global CONFIG
  bstack11lllll1_opy_ = bstack1ll1_opy_ (u"ࠪࠫદ")
  if not bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧધ") in CONFIG:
    logger.info(bstack1ll1_opy_ (u"ࠬࡔ࡯ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠤࡵࡧࡳࡴࡧࡧࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡵࡩࡵࡵࡲࡵࠢࡩࡳࡷࠦࡒࡰࡤࡲࡸࠥࡸࡵ࡯ࠩન"))
  try:
    platform = CONFIG[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ઩")][bstack111ll1ll1_opy_]
    if bstack1ll1_opy_ (u"ࠧࡰࡵࠪપ") in platform:
      bstack11lllll1_opy_ += str(platform[bstack1ll1_opy_ (u"ࠨࡱࡶࠫફ")]) + bstack1ll1_opy_ (u"ࠩ࠯ࠤࠬબ")
    if bstack1ll1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ભ") in platform:
      bstack11lllll1_opy_ += str(platform[bstack1ll1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧમ")]) + bstack1ll1_opy_ (u"ࠬ࠲ࠠࠨય")
    if bstack1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪર") in platform:
      bstack11lllll1_opy_ += str(platform[bstack1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ઱")]) + bstack1ll1_opy_ (u"ࠨ࠮ࠣࠫલ")
    if bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫળ") in platform:
      bstack11lllll1_opy_ += str(platform[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ઴")]) + bstack1ll1_opy_ (u"ࠫ࠱ࠦࠧવ")
    if bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪશ") in platform:
      bstack11lllll1_opy_ += str(platform[bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫષ")]) + bstack1ll1_opy_ (u"ࠧ࠭ࠢࠪસ")
    if bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩહ") in platform:
      bstack11lllll1_opy_ += str(platform[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ઺")]) + bstack1ll1_opy_ (u"ࠪ࠰ࠥ࠭઻")
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠫࡘࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡹࡸࡩ࡯ࡩࠣࡪࡴࡸࠠࡳࡧࡳࡳࡷࡺࠠࡨࡧࡱࡩࡷࡧࡴࡪࡱࡱ઼ࠫ") + str(e))
  finally:
    if bstack11lllll1_opy_[len(bstack11lllll1_opy_) - 2:] == bstack1ll1_opy_ (u"ࠬ࠲ࠠࠨઽ"):
      bstack11lllll1_opy_ = bstack11lllll1_opy_[:-2]
    return bstack11lllll1_opy_
def bstack1lllll1lll_opy_(path, bstack11lllll1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1l11ll11_opy_ = ET.parse(path)
    bstack1l1llllll1_opy_ = bstack1l1l11ll11_opy_.getroot()
    bstack1111l111l_opy_ = None
    for suite in bstack1l1llllll1_opy_.iter(bstack1ll1_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬા")):
      if bstack1ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧિ") in suite.attrib:
        suite.attrib[bstack1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ી")] += bstack1ll1_opy_ (u"ࠩࠣࠫુ") + bstack11lllll1_opy_
        bstack1111l111l_opy_ = suite
    bstack1ll1l11l11_opy_ = None
    for robot in bstack1l1llllll1_opy_.iter(bstack1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩૂ")):
      bstack1ll1l11l11_opy_ = robot
    bstack1l111llll_opy_ = len(bstack1ll1l11l11_opy_.findall(bstack1ll1_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪૃ")))
    if bstack1l111llll_opy_ == 1:
      bstack1ll1l11l11_opy_.remove(bstack1ll1l11l11_opy_.findall(bstack1ll1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫૄ"))[0])
      bstack1ll1l11l_opy_ = ET.Element(bstack1ll1_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬૅ"), attrib={bstack1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ૆"): bstack1ll1_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࡳࠨે"), bstack1ll1_opy_ (u"ࠩ࡬ࡨࠬૈ"): bstack1ll1_opy_ (u"ࠪࡷ࠵࠭ૉ")})
      bstack1ll1l11l11_opy_.insert(1, bstack1ll1l11l_opy_)
      bstack11lll1l1l_opy_ = None
      for suite in bstack1ll1l11l11_opy_.iter(bstack1ll1_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ૊")):
        bstack11lll1l1l_opy_ = suite
      bstack11lll1l1l_opy_.append(bstack1111l111l_opy_)
      bstack1l1llll11l_opy_ = None
      for status in bstack1111l111l_opy_.iter(bstack1ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬો")):
        bstack1l1llll11l_opy_ = status
      bstack11lll1l1l_opy_.append(bstack1l1llll11l_opy_)
    bstack1l1l11ll11_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠫૌ") + str(e))
def bstack11111ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1l1llll_opy_
  global CONFIG
  if bstack1ll1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫્ࠦ") in options:
    del options[bstack1ll1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ૎")]
  bstack1l1ll111_opy_ = bstack1ll111l11_opy_()
  for bstack1l1l1111_opy_ in bstack1l1ll111_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࡠࡴࡨࡷࡺࡲࡴࡴࠩ૏"), str(bstack1l1l1111_opy_), bstack1ll1_opy_ (u"ࠪࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠧૐ"))
    bstack1lllll1lll_opy_(path, bstack1l1l1l1l1l_opy_(bstack1l1ll111_opy_[bstack1l1l1111_opy_]))
  bstack11llll1ll_opy_()
  return bstack1l1l1llll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lll111ll1_opy_(self, ff_profile_dir):
  global bstack1111ll11_opy_
  if not ff_profile_dir:
    return None
  return bstack1111ll11_opy_(self, ff_profile_dir)
def bstack1111l1ll1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1lll1l11_opy_
  bstack1ll1l1l1l_opy_ = []
  if bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૑") in CONFIG:
    bstack1ll1l1l1l_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૒")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢ૓")],
      pabot_args[bstack1ll1_opy_ (u"ࠢࡷࡧࡵࡦࡴࡹࡥࠣ૔")],
      argfile,
      pabot_args.get(bstack1ll1_opy_ (u"ࠣࡪ࡬ࡺࡪࠨ૕")),
      pabot_args[bstack1ll1_opy_ (u"ࠤࡳࡶࡴࡩࡥࡴࡵࡨࡷࠧ૖")],
      platform[0],
      bstack1l1lll1l11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࡫࡯࡬ࡦࡵࠥ૗")] or [(bstack1ll1_opy_ (u"ࠦࠧ૘"), None)]
    for platform in enumerate(bstack1ll1l1l1l_opy_)
  ]
def bstack11ll1l11_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11l1l1ll_opy_=bstack1ll1_opy_ (u"ࠬ࠭૙")):
  global bstack11lll1lll_opy_
  self.platform_index = platform_index
  self.bstack1l11lll1_opy_ = bstack11l1l1ll_opy_
  bstack11lll1lll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l11ll1l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll11ll1l_opy_
  global bstack1l1l111111_opy_
  bstack1ll11111l1_opy_ = copy.deepcopy(item)
  if not bstack1ll1_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ૚") in item.options:
    bstack1ll11111l1_opy_.options[bstack1ll1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૛")] = []
  bstack1lllll111_opy_ = bstack1ll11111l1_opy_.options[bstack1ll1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૜")].copy()
  for v in bstack1ll11111l1_opy_.options[bstack1ll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૝")]:
    if bstack1ll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩ૞") in v:
      bstack1lllll111_opy_.remove(v)
    if bstack1ll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫ૟") in v:
      bstack1lllll111_opy_.remove(v)
    if bstack1ll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩૠ") in v:
      bstack1lllll111_opy_.remove(v)
  bstack1lllll111_opy_.insert(0, bstack1ll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜࠿ࢁࡽࠨૡ").format(bstack1ll11111l1_opy_.platform_index))
  bstack1lllll111_opy_.insert(0, bstack1ll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࠾ࢀࢃࠧૢ").format(bstack1ll11111l1_opy_.bstack1l11lll1_opy_))
  bstack1ll11111l1_opy_.options[bstack1ll1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪૣ")] = bstack1lllll111_opy_
  if bstack1l1l111111_opy_:
    bstack1ll11111l1_opy_.options[bstack1ll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૤")].insert(0, bstack1ll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕ࠽ࡿࢂ࠭૥").format(bstack1l1l111111_opy_))
  return bstack1ll11ll1l_opy_(caller_id, datasources, is_last, bstack1ll11111l1_opy_, outs_dir)
def bstack1l1l11lll1_opy_(command, item_index):
  if bstack111l1l1l1_opy_.get_property(bstack1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ૦")):
    os.environ[bstack1ll1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭૧")] = json.dumps(CONFIG[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૨")][item_index % bstack1111ll1l_opy_])
  global bstack1l1l111111_opy_
  if bstack1l1l111111_opy_:
    command[0] = command[0].replace(bstack1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૩"), bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ૪") + str(
      item_index) + bstack1ll1_opy_ (u"ࠩࠣࠫ૫") + bstack1l1l111111_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૬"),
                                    bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨ૭") + str(item_index), 1)
def bstack11111l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1llll11l1l_opy_
  bstack1l1l11lll1_opy_(command, item_index)
  return bstack1llll11l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll11111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1llll11l1l_opy_
  bstack1l1l11lll1_opy_(command, item_index)
  return bstack1llll11l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1llll11l1l_opy_
  bstack1l1l11lll1_opy_(command, item_index)
  return bstack1llll11l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1lll11ll_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll1ll1l1_opy_
  bstack1lll1l1111_opy_ = bstack1ll1ll1l1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1ll1_opy_ (u"ࠬ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡠࡣࡵࡶࠬ૮")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll1_opy_ (u"࠭ࡥࡹࡥࡢࡸࡷࡧࡣࡦࡤࡤࡧࡰࡥࡡࡳࡴࠪ૯")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll1l1111_opy_
def bstack1l11llll_opy_(self, name, context, *args):
  os.environ[bstack1ll1_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ૰")] = json.dumps(CONFIG[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૱")][int(threading.current_thread()._name) % bstack1111ll1l_opy_])
  global bstack1ll1l111l_opy_
  if name == bstack1ll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ૲"):
    bstack1ll1l111l_opy_(self, name, context, *args)
    try:
      if not bstack1111lll11_opy_:
        bstack1l11ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l11111_opy_(bstack1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૳")) else context.browser
        bstack1l1llll1_opy_ = str(self.feature.name)
        bstack11l1lll1_opy_(context, bstack1l1llll1_opy_)
        bstack1l11ll11l1_opy_.execute_script(bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ૴") + json.dumps(bstack1l1llll1_opy_) + bstack1ll1_opy_ (u"ࠬࢃࡽࠨ૵"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭૶").format(str(e)))
  elif name == bstack1ll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ૷"):
    bstack1ll1l111l_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack1ll1_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ૸")):
        self.driver_before_scenario = True
      if (not bstack1111lll11_opy_):
        scenario_name = args[0].name
        feature_name = bstack1l1llll1_opy_ = str(self.feature.name)
        bstack1l1llll1_opy_ = feature_name + bstack1ll1_opy_ (u"ࠩࠣ࠱ࠥ࠭ૹ") + scenario_name
        bstack1l11ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l11111_opy_(bstack1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩૺ")) else context.browser
        if self.driver_before_scenario:
          bstack11l1lll1_opy_(context, bstack1l1llll1_opy_)
          bstack1l11ll11l1_opy_.execute_script(bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩૻ") + json.dumps(bstack1l1llll1_opy_) + bstack1ll1_opy_ (u"ࠬࢃࡽࠨૼ"))
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ૽").format(str(e)))
  elif name == bstack1ll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ૾"):
    try:
      bstack1ll1111l1l_opy_ = args[0].status.name
      bstack1l11ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ૿") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1ll1111l1l_opy_).lower() == bstack1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ଀"):
        bstack1lllll11ll_opy_ = bstack1ll1_opy_ (u"ࠪࠫଁ")
        bstack11111111_opy_ = bstack1ll1_opy_ (u"ࠫࠬଂ")
        bstack1l1llll111_opy_ = bstack1ll1_opy_ (u"ࠬ࠭ଃ")
        try:
          import traceback
          bstack1lllll11ll_opy_ = self.exception.__class__.__name__
          bstack1ll11l1l1l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack11111111_opy_ = bstack1ll1_opy_ (u"࠭ࠠࠨ଄").join(bstack1ll11l1l1l_opy_)
          bstack1l1llll111_opy_ = bstack1ll11l1l1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l11ll11ll_opy_.format(str(e)))
        bstack1lllll11ll_opy_ += bstack1l1llll111_opy_
        bstack1ll111ll1_opy_(context, json.dumps(str(args[0].name) + bstack1ll1_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨଅ") + str(bstack11111111_opy_)),
                            bstack1ll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢଆ"))
        if self.driver_before_scenario:
          bstack1l1l1ll11l_opy_(getattr(context, bstack1ll1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧଇ"), None), bstack1ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥଈ"), bstack1lllll11ll_opy_)
          bstack1l11ll11l1_opy_.execute_script(bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଉ") + json.dumps(str(args[0].name) + bstack1ll1_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦଊ") + str(bstack11111111_opy_)) + bstack1ll1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ଋ"))
        if self.driver_before_scenario:
          bstack11111l1ll_opy_(bstack1l11ll11l1_opy_, bstack1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧଌ"), bstack1ll1_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ଍") + str(bstack1lllll11ll_opy_))
      else:
        bstack1ll111ll1_opy_(context, bstack1ll1_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ଎"), bstack1ll1_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣଏ"))
        if self.driver_before_scenario:
          bstack1l1l1ll11l_opy_(getattr(context, bstack1ll1_opy_ (u"ࠫࡵࡧࡧࡦࠩଐ"), None), bstack1ll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ଑"))
        bstack1l11ll11l1_opy_.execute_script(bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ଒") + json.dumps(str(args[0].name) + bstack1ll1_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦଓ")) + bstack1ll1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧଔ"))
        if self.driver_before_scenario:
          bstack11111l1ll_opy_(bstack1l11ll11l1_opy_, bstack1ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤକ"))
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬଖ").format(str(e)))
  elif name == bstack1ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫଗ"):
    try:
      bstack1l11ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l11111_opy_(bstack1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫଘ")) else context.browser
      if context.failed is True:
        bstack1l11ll1l11_opy_ = []
        bstack1ll1ll111_opy_ = []
        bstack1lllllll1_opy_ = []
        bstack11ll1ll1_opy_ = bstack1ll1_opy_ (u"࠭ࠧଙ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l11ll1l11_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll11l1l1l_opy_ = traceback.format_tb(exc_tb)
            bstack11lll1l11_opy_ = bstack1ll1_opy_ (u"ࠧࠡࠩଚ").join(bstack1ll11l1l1l_opy_)
            bstack1ll1ll111_opy_.append(bstack11lll1l11_opy_)
            bstack1lllllll1_opy_.append(bstack1ll11l1l1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l11ll11ll_opy_.format(str(e)))
        bstack1lllll11ll_opy_ = bstack1ll1_opy_ (u"ࠨࠩଛ")
        for i in range(len(bstack1l11ll1l11_opy_)):
          bstack1lllll11ll_opy_ += bstack1l11ll1l11_opy_[i] + bstack1lllllll1_opy_[i] + bstack1ll1_opy_ (u"ࠩ࡟ࡲࠬଜ")
        bstack11ll1ll1_opy_ = bstack1ll1_opy_ (u"ࠪࠤࠬଝ").join(bstack1ll1ll111_opy_)
        if not self.driver_before_scenario:
          bstack1ll111ll1_opy_(context, bstack11ll1ll1_opy_, bstack1ll1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥଞ"))
          bstack1l1l1ll11l_opy_(getattr(context, bstack1ll1_opy_ (u"ࠬࡶࡡࡨࡧࠪଟ"), None), bstack1ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨଠ"), bstack1lllll11ll_opy_)
          bstack1l11ll11l1_opy_.execute_script(bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬଡ") + json.dumps(bstack11ll1ll1_opy_) + bstack1ll1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨଢ"))
          bstack11111l1ll_opy_(bstack1l11ll11l1_opy_, bstack1ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤଣ"), bstack1ll1_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣତ") + str(bstack1lllll11ll_opy_))
          bstack111ll11l_opy_ = bstack1lll11111_opy_(bstack11ll1ll1_opy_, self.feature.name, logger)
          if (bstack111ll11l_opy_ != None):
            bstack111111lll_opy_.append(bstack111ll11l_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1ll111ll1_opy_(context, bstack1ll1_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢଥ") + str(self.feature.name) + bstack1ll1_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢଦ"), bstack1ll1_opy_ (u"ࠨࡩ࡯ࡨࡲࠦଧ"))
          bstack1l1l1ll11l_opy_(getattr(context, bstack1ll1_opy_ (u"ࠧࡱࡣࡪࡩࠬନ"), None), bstack1ll1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ଩"))
          bstack1l11ll11l1_opy_.execute_script(bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧପ") + json.dumps(bstack1ll1_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨଫ") + str(self.feature.name) + bstack1ll1_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨବ")) + bstack1ll1_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫଭ"))
          bstack11111l1ll_opy_(bstack1l11ll11l1_opy_, bstack1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ମ"))
          bstack111ll11l_opy_ = bstack1lll11111_opy_(bstack11ll1ll1_opy_, self.feature.name, logger)
          if (bstack111ll11l_opy_ != None):
            bstack111111lll_opy_.append(bstack111ll11l_opy_)
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩଯ").format(str(e)))
  else:
    bstack1ll1l111l_opy_(self, name, context, *args)
  if name in [bstack1ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨର"), bstack1ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ଱")]:
    bstack1ll1l111l_opy_(self, name, context, *args)
    if (name == bstack1ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫଲ") and self.driver_before_scenario) or (
            name == bstack1ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫଳ") and not self.driver_before_scenario):
      try:
        bstack1l11ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l11111_opy_(bstack1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ଴")) else context.browser
        bstack1l11ll11l1_opy_.quit()
      except Exception:
        pass
def bstack1l11l1ll1l_opy_(config, startdir):
  return bstack1ll1_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦଵ").format(bstack1ll1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨଶ"))
notset = Notset()
def bstack1llll11lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11l111l1_opy_
  if str(name).lower() == bstack1ll1_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨଷ"):
    return bstack1ll1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣସ")
  else:
    return bstack11l111l1_opy_(self, name, default, skip)
def bstack11l11111l_opy_(item, when):
  global bstack1ll1l1l111_opy_
  try:
    bstack1ll1l1l111_opy_(item, when)
  except Exception as e:
    pass
def bstack1llll111l_opy_():
  return
def bstack11l1lll1l_opy_(type, name, status, reason, bstack1l1ll1l11l_opy_, bstack1l1lllllll_opy_):
  bstack11lll111l_opy_ = {
    bstack1ll1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪହ"): type,
    bstack1ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ଺"): {}
  }
  if type == bstack1ll1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ଻"):
    bstack11lll111l_opy_[bstack1ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴ଼ࠩ")][bstack1ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ଽ")] = bstack1l1ll1l11l_opy_
    bstack11lll111l_opy_[bstack1ll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫା")][bstack1ll1_opy_ (u"ࠩࡧࡥࡹࡧࠧି")] = json.dumps(str(bstack1l1lllllll_opy_))
  if type == bstack1ll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫୀ"):
    bstack11lll111l_opy_[bstack1ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧୁ")][bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪୂ")] = name
  if type == bstack1ll1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩୃ"):
    bstack11lll111l_opy_[bstack1ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪୄ")][bstack1ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ୅")] = status
    if status == bstack1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ୆"):
      bstack11lll111l_opy_[bstack1ll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭େ")][bstack1ll1_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫୈ")] = json.dumps(str(reason))
  bstack1l11ll11l_opy_ = bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ୉").format(json.dumps(bstack11lll111l_opy_))
  return bstack1l11ll11l_opy_
def bstack1l1lll1ll1_opy_(driver_command, response):
    if driver_command == bstack1ll1_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ୊"):
        bstack1lllll1l1_opy_.bstack1llll111ll_opy_({
            bstack1ll1_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ୋ"): response[bstack1ll1_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧୌ")],
            bstack1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥ୍ࠩ"): bstack1lllll1l1_opy_.current_test_uuid()
        })
def bstack1llll1111_opy_(item, call, rep):
  global bstack1ll11l11_opy_
  global bstack1llll111_opy_
  global bstack1111lll11_opy_
  name = bstack1ll1_opy_ (u"ࠪࠫ୎")
  try:
    if rep.when == bstack1ll1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ୏"):
      bstack11l11llll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1111lll11_opy_:
          name = str(rep.nodeid)
          bstack1111llll1_opy_ = bstack11l1lll1l_opy_(bstack1ll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୐"), name, bstack1ll1_opy_ (u"࠭ࠧ୑"), bstack1ll1_opy_ (u"ࠧࠨ୒"), bstack1ll1_opy_ (u"ࠨࠩ୓"), bstack1ll1_opy_ (u"ࠩࠪ୔"))
          threading.current_thread().bstack1ll1llll11_opy_ = name
          for driver in bstack1llll111_opy_:
            if bstack11l11llll_opy_ == driver.session_id:
              driver.execute_script(bstack1111llll1_opy_)
      except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ୕").format(str(e)))
      try:
        bstack1ll1l11l1l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬୖ"):
          status = bstack1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬୗ") if rep.outcome.lower() == bstack1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭୘") else bstack1ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ୙")
          reason = bstack1ll1_opy_ (u"ࠨࠩ୚")
          if status == bstack1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ୛"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨଡ଼") if status == bstack1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫଢ଼") else bstack1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ୞")
          data = name + bstack1ll1_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨୟ") if status == bstack1ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧୠ") else name + bstack1ll1_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫୡ") + reason
          bstack1l1ll1llll_opy_ = bstack11l1lll1l_opy_(bstack1ll1_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫୢ"), bstack1ll1_opy_ (u"ࠪࠫୣ"), bstack1ll1_opy_ (u"ࠫࠬ୤"), bstack1ll1_opy_ (u"ࠬ࠭୥"), level, data)
          for driver in bstack1llll111_opy_:
            if bstack11l11llll_opy_ == driver.session_id:
              driver.execute_script(bstack1l1ll1llll_opy_)
      except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ୦").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫ୧").format(str(e)))
  bstack1ll11l11_opy_(item, call, rep)
def bstack1l1l1ll111_opy_(driver, bstack11l1l1l1_opy_):
  PercySDK.screenshot(driver, bstack11l1l1l1_opy_)
def bstack1llllll11l_opy_(driver):
  if bstack1l1ll11111_opy_.bstack1ll1l1l11_opy_() is True or bstack1l1ll11111_opy_.capturing() is True:
    return
  bstack1l1ll11111_opy_.bstack1ll1l11l1_opy_()
  while not bstack1l1ll11111_opy_.bstack1ll1l1l11_opy_():
    bstack11l11ll1l_opy_ = bstack1l1ll11111_opy_.bstack111lll1ll_opy_()
    bstack1l1l1ll111_opy_(driver, bstack11l11ll1l_opy_)
  bstack1l1ll11111_opy_.bstack1ll1ll11ll_opy_()
def bstack1l1ll111ll_opy_(sequence, driver_command, response = None, bstack1ll11l11l1_opy_ = None, args = None):
    try:
      if sequence != bstack1ll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ୨"):
        return
      if not CONFIG.get(bstack1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ୩"), False):
        return
      bstack11l11ll1l_opy_ = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୪"), None)
      for command in bstack1l11ll1l1l_opy_:
        if command == driver_command:
          for driver in bstack1llll111_opy_:
            bstack1llllll11l_opy_(driver)
      bstack1llllllll_opy_ = CONFIG.get(bstack1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ୫"), bstack1ll1_opy_ (u"ࠧࡧࡵࡵࡱࠥ୬"))
      if driver_command in bstack1ll1ll1ll_opy_[bstack1llllllll_opy_]:
        bstack1l1ll11111_opy_.bstack1l1l1l1111_opy_(bstack11l11ll1l_opy_, driver_command)
    except Exception as e:
      pass
def bstack11l1ll1l_opy_(framework_name):
  global bstack11l1l1l11_opy_
  global bstack11ll11111_opy_
  global bstack1lllll11l1_opy_
  bstack11l1l1l11_opy_ = framework_name
  logger.info(bstack111ll1lll_opy_.format(bstack11l1l1l11_opy_.split(bstack1ll1_opy_ (u"࠭࠭ࠨ୭"))[0]))
  bstack11lll1111_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1l111l_opy_:
      Service.start = bstack1llll11l11_opy_
      Service.stop = bstack1111l1lll_opy_
      webdriver.Remote.get = bstack1lll1ll1ll_opy_
      WebDriver.close = bstack1l1ll1lll_opy_
      WebDriver.quit = bstack1ll1lll1_opy_
      webdriver.Remote.__init__ = bstack1ll11l1ll1_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1l1l111l_opy_ and bstack1lllll1l1_opy_.on():
      webdriver.Remote.__init__ = bstack11l11l11l_opy_
    WebDriver.execute = bstack1l111111_opy_
    bstack11ll11111_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1l111l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l11ll11_opy_
  except Exception as e:
    pass
  bstack1lll11llll_opy_()
  if not bstack11ll11111_opy_:
    bstack1l1lll11_opy_(bstack1ll1_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ୮"), bstack111ll1l1l_opy_)
  if bstack111l1ll1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1llll1ll11_opy_
    except Exception as e:
      logger.error(bstack1l1l111ll1_opy_.format(str(e)))
  if bstack1l1ll11ll_opy_():
    bstack11l1ll11_opy_(CONFIG, logger)
  if (bstack1ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ୯") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ୰"), False):
          bstack1l1llll1l_opy_(bstack1l1ll111ll_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll111ll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l1111ll1_opy_
      except Exception as e:
        logger.warn(bstack1l1llll1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l1l11111_opy_
      except Exception as e:
        logger.debug(bstack1l1llllll_opy_ + str(e))
    except Exception as e:
      bstack1l1lll11_opy_(e, bstack1l1llll1ll_opy_)
    Output.start_test = bstack1l11l11ll1_opy_
    Output.end_test = bstack1l11llll11_opy_
    TestStatus.__init__ = bstack11l11l11_opy_
    QueueItem.__init__ = bstack11ll1l11_opy_
    pabot._create_items = bstack1111l1ll1_opy_
    try:
      from pabot import __version__ as bstack1ll1lll1l1_opy_
      if version.parse(bstack1ll1lll1l1_opy_) >= version.parse(bstack1ll1_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪୱ")):
        pabot._run = bstack1llll1l1l_opy_
      elif version.parse(bstack1ll1lll1l1_opy_) >= version.parse(bstack1ll1_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫ୲")):
        pabot._run = bstack1ll11111ll_opy_
      else:
        pabot._run = bstack11111l11_opy_
    except Exception as e:
      pabot._run = bstack11111l11_opy_
    pabot._create_command_for_execution = bstack1l11ll1l1_opy_
    pabot._report_results = bstack11111ll1_opy_
  if bstack1ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ୳") in str(framework_name).lower():
    if not bstack1l1l111l_opy_:
      return
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll11_opy_(e, bstack11l1llll_opy_)
    Runner.run_hook = bstack1l11llll_opy_
    Step.run = bstack1lll11ll_opy_
  if bstack1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭୴") in str(framework_name).lower():
    if not bstack1l1l111l_opy_:
      return
    try:
      if CONFIG.get(bstack1ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭୵"), False):
          bstack1l1llll1l_opy_(bstack1l1ll111ll_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l11l1ll1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1llll111l_opy_
      Config.getoption = bstack1llll11lll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1llll1111_opy_
    except Exception as e:
      pass
def bstack11l1l1ll1_opy_():
  global CONFIG
  if bstack1ll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ୶") in CONFIG and int(CONFIG[bstack1ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ୷")]) > 1:
    logger.warn(bstack111ll11l1_opy_)
def bstack11lll111_opy_(arg, bstack1l1l11lll_opy_, bstack11ll1l1ll_opy_=None):
  global CONFIG
  global bstack111111l1_opy_
  global bstack1lll1l1l_opy_
  global bstack1l1l111l_opy_
  global bstack111l1l1l1_opy_
  bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ୸")
  if bstack1l1l11lll_opy_ and isinstance(bstack1l1l11lll_opy_, str):
    bstack1l1l11lll_opy_ = eval(bstack1l1l11lll_opy_)
  CONFIG = bstack1l1l11lll_opy_[bstack1ll1_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ୹")]
  bstack111111l1_opy_ = bstack1l1l11lll_opy_[bstack1ll1_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭୺")]
  bstack1lll1l1l_opy_ = bstack1l1l11lll_opy_[bstack1ll1_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ୻")]
  bstack1l1l111l_opy_ = bstack1l1l11lll_opy_[bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ୼")]
  bstack111l1l1l1_opy_.bstack1l1lll111l_opy_(bstack1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ୽"), bstack1l1l111l_opy_)
  os.environ[bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ୾")] = bstack1ll11111l_opy_
  os.environ[bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ୿")] = json.dumps(CONFIG)
  os.environ[bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ஀")] = bstack111111l1_opy_
  os.environ[bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭஁")] = str(bstack1lll1l1l_opy_)
  os.environ[bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬஂ")] = str(True)
  if bstack11lll1ll1_opy_(arg, [bstack1ll1_opy_ (u"ࠧ࠮ࡰࠪஃ"), bstack1ll1_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ஄")]) != -1:
    os.environ[bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪஅ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11ll11l1l_opy_)
    return
  bstack111l11l1_opy_()
  global bstack11l111111_opy_
  global bstack1ll1llll1_opy_
  global bstack1l1lll1l11_opy_
  global bstack1l1l111111_opy_
  global bstack1111llll_opy_
  global bstack1lllll11l1_opy_
  global bstack1llllll11_opy_
  arg.append(bstack1ll1_opy_ (u"ࠥ࠱࡜ࠨஆ"))
  arg.append(bstack1ll1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢஇ"))
  arg.append(bstack1ll1_opy_ (u"ࠧ࠳ࡗࠣஈ"))
  arg.append(bstack1ll1_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧஉ"))
  global bstack1l11l11l_opy_
  global bstack1l111l11_opy_
  global bstack1l11l11l11_opy_
  global bstack11111l1l1_opy_
  global bstack1111ll11_opy_
  global bstack11lll1lll_opy_
  global bstack1ll11ll1l_opy_
  global bstack1ll111lll1_opy_
  global bstack111l1lll_opy_
  global bstack1l1ll111l_opy_
  global bstack11l111l1_opy_
  global bstack1ll1l1l111_opy_
  global bstack1ll11l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l11l11l_opy_ = webdriver.Remote.__init__
    bstack1l111l11_opy_ = WebDriver.quit
    bstack1ll111lll1_opy_ = WebDriver.close
    bstack111l1lll_opy_ = WebDriver.get
    bstack1l11l11l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l11l1ll1_opy_(CONFIG) and bstack1l1ll1ll11_opy_():
    if bstack1lll1ll11l_opy_() < version.parse(bstack1l1ll11l_opy_):
      logger.error(bstack111lll11_opy_.format(bstack1lll1ll11l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1ll111l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1l111ll1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack11l111l1_opy_ = Config.getoption
    from _pytest import runner
    bstack1ll1l1l111_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l11lll111_opy_)
  try:
    from pytest_bdd import reporting
    bstack1ll11l11_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨஊ"))
  bstack1l1lll1l11_opy_ = CONFIG.get(bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ஋"), {}).get(bstack1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ஌"))
  bstack1llllll11_opy_ = True
  bstack11l1ll1l_opy_(bstack1l1111l1_opy_)
  os.environ[bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ஍")] = CONFIG[bstack1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭எ")]
  os.environ[bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨஏ")] = CONFIG[bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩஐ")]
  os.environ[bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ஑")] = bstack1l1l111l_opy_.__str__()
  from _pytest.config import main as bstack11l1lll11_opy_
  bstack1lll1l111_opy_ = []
  try:
    bstack1ll1l1ll1l_opy_ = bstack11l1lll11_opy_(arg)
    if bstack1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬஒ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1ll1lll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll1l111_opy_.append(bstack1l1ll1lll1_opy_)
    try:
      bstack1ll1l1l11l_opy_ = (bstack1lll1l111_opy_, int(bstack1ll1l1ll1l_opy_))
      bstack11ll1l1ll_opy_.append(bstack1ll1l1l11l_opy_)
    except:
      bstack11ll1l1ll_opy_.append((bstack1lll1l111_opy_, bstack1ll1l1ll1l_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1lll1l111_opy_.append({bstack1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧஓ"): bstack1ll1_opy_ (u"ࠪࡔࡷࡵࡣࡦࡵࡶࠤࠬஔ") + os.environ.get(bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫக")), bstack1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ஖"): traceback.format_exc(), bstack1ll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ஗"): int(os.environ.get(bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ஘")))})
    bstack11ll1l1ll_opy_.append((bstack1lll1l111_opy_, 1))
def bstack1lll11l111_opy_(arg):
  global bstack1llll1l11_opy_
  bstack11l1ll1l_opy_(bstack1l1llll1l1_opy_)
  os.environ[bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩங")] = str(bstack1lll1l1l_opy_)
  from behave.__main__ import main as bstack1l111l1ll_opy_
  status_code = bstack1l111l1ll_opy_(arg)
  if status_code != 0:
    bstack1llll1l11_opy_ = status_code
def bstack1ll1l1ll_opy_():
  logger.info(bstack1lll1111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨச"), help=bstack1ll1_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫ஛"))
  parser.add_argument(bstack1ll1_opy_ (u"ࠫ࠲ࡻࠧஜ"), bstack1ll1_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ஝"), help=bstack1ll1_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬஞ"))
  parser.add_argument(bstack1ll1_opy_ (u"ࠧ࠮࡭ࠪட"), bstack1ll1_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧ஠"), help=bstack1ll1_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪ஡"))
  parser.add_argument(bstack1ll1_opy_ (u"ࠪ࠱࡫࠭஢"), bstack1ll1_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩண"), help=bstack1ll1_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫத"))
  bstack1ll11lll_opy_ = parser.parse_args()
  try:
    bstack1l1ll11l1_opy_ = bstack1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪ஥")
    if bstack1ll11lll_opy_.framework and bstack1ll11lll_opy_.framework not in (bstack1ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ஦"), bstack1ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ஧")):
      bstack1l1ll11l1_opy_ = bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨந")
    bstack111llll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1ll11l1_opy_)
    bstack1ll1lll111_opy_ = open(bstack111llll1_opy_, bstack1ll1_opy_ (u"ࠪࡶࠬன"))
    bstack1ll111l11l_opy_ = bstack1ll1lll111_opy_.read()
    bstack1ll1lll111_opy_.close()
    if bstack1ll11lll_opy_.username:
      bstack1ll111l11l_opy_ = bstack1ll111l11l_opy_.replace(bstack1ll1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫப"), bstack1ll11lll_opy_.username)
    if bstack1ll11lll_opy_.key:
      bstack1ll111l11l_opy_ = bstack1ll111l11l_opy_.replace(bstack1ll1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ஫"), bstack1ll11lll_opy_.key)
    if bstack1ll11lll_opy_.framework:
      bstack1ll111l11l_opy_ = bstack1ll111l11l_opy_.replace(bstack1ll1_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ஬"), bstack1ll11lll_opy_.framework)
    file_name = bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ஭")
    file_path = os.path.abspath(file_name)
    bstack1ll1lll1ll_opy_ = open(file_path, bstack1ll1_opy_ (u"ࠨࡹࠪம"))
    bstack1ll1lll1ll_opy_.write(bstack1ll111l11l_opy_)
    bstack1ll1lll1ll_opy_.close()
    logger.info(bstack111l1l1l_opy_)
    try:
      os.environ[bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫய")] = bstack1ll11lll_opy_.framework if bstack1ll11lll_opy_.framework != None else bstack1ll1_opy_ (u"ࠥࠦர")
      config = yaml.safe_load(bstack1ll111l11l_opy_)
      config[bstack1ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫற")] = bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫல")
      bstack1l11l1l1l1_opy_(bstack1ll11lllll_opy_, config)
    except Exception as e:
      logger.debug(bstack1lll111l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11llllll1_opy_.format(str(e)))
def bstack1l11l1l1l1_opy_(bstack1llll1l11l_opy_, config, bstack1l11l111ll_opy_={}):
  global bstack1l1l111l_opy_
  global bstack1l1l11ll1l_opy_
  global bstack111l1l1l1_opy_
  if not config:
    return
  bstack1l1lll1l1l_opy_ = bstack1ll1ll111l_opy_ if not bstack1l1l111l_opy_ else (
    bstack1l11l111l_opy_ if bstack1ll1_opy_ (u"࠭ࡡࡱࡲࠪள") in config else bstack1lll1ll11_opy_)
  bstack11l11ll11_opy_ = False
  bstack1111l11l_opy_ = False
  if bstack1l1l111l_opy_ is True:
      if bstack1ll1_opy_ (u"ࠧࡢࡲࡳࠫழ") in config:
          bstack11l11ll11_opy_ = True
      else:
          bstack1111l11l_opy_ = True
  bstack1l11ll1ll1_opy_ = {
      bstack1ll1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨவ"): bstack1lllll1l1_opy_.bstack1l1lllll1_opy_(bstack1l1l11ll1l_opy_),
      bstack1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩஶ"): bstack1111111l1_opy_.bstack111l1lll1_opy_(config),
      bstack1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩஷ"): config.get(bstack1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪஸ"), False),
      bstack1ll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧஹ"): bstack1111l11l_opy_,
      bstack1ll1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ஺"): bstack11l11ll11_opy_
  }
  data = {
    bstack1ll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ஻"): config[bstack1ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ஼")],
    bstack1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ஽"): config[bstack1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ா")],
    bstack1ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨி"): bstack1llll1l11l_opy_,
    bstack1ll1_opy_ (u"ࠬࡪࡥࡵࡧࡦࡸࡪࡪࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩீ"): os.environ.get(bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨு"), bstack1l1l11ll1l_opy_),
    bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩூ"): bstack1l1l1llll1_opy_,
    bstack1ll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮ࠪ௃"): bstack1l1l1ll1l1_opy_(),
    bstack1ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ௄"): {
      bstack1ll1_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௅"): str(config[bstack1ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫெ")]) if bstack1ll1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬே") in config else bstack1ll1_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢை"),
      bstack1ll1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡘࡨࡶࡸ࡯࡯࡯ࠩ௉"): sys.version,
      bstack1ll1_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪொ"): bstack1l11l1l111_opy_(os.getenv(bstack1ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦோ"), bstack1ll1_opy_ (u"ࠥࠦௌ"))),
      bstack1ll1_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ்࠭"): bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௎"),
      bstack1ll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ௏"): bstack1l1lll1l1l_opy_,
      bstack1ll1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬௐ"): bstack1l11ll1ll1_opy_,
      bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧ௑"): os.environ[bstack1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ௒")],
      bstack1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௓"): bstack1ll1l1lll_opy_(os.environ.get(bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭௔"), bstack1l1l11ll1l_opy_)),
      bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௕"): config[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ௖")] if config[bstack1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪௗ")] else bstack1ll1_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ௘"),
      bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ௙"): str(config[bstack1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ௚")]) if bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭௛") in config else bstack1ll1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ௜"),
      bstack1ll1_opy_ (u"࠭࡯ࡴࠩ௝"): sys.platform,
      bstack1ll1_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ௞"): socket.gethostname(),
      bstack1ll1_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ௟"): bstack111l1l1l1_opy_.get_property(bstack1ll1_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ௠"))
    }
  }
  if not bstack111l1l1l1_opy_.get_property(bstack1ll1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ௡")) is None:
    data[bstack1ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ௢")][bstack1ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨ௣")] = {
      bstack1ll1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭௤"): bstack1ll1_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ௥"),
      bstack1ll1_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ௦"): bstack111l1l1l1_opy_.get_property(bstack1ll1_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ௧")),
      bstack1ll1_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩ௨"): bstack111l1l1l1_opy_.get_property(bstack1ll1_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ௩"))
    }
  update(data[bstack1ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ௪")], bstack1l11l111ll_opy_)
  try:
    response = bstack1l1l11llll_opy_(bstack1ll1_opy_ (u"࠭ࡐࡐࡕࡗࠫ௫"), bstack1l1l11l11l_opy_(bstack1l11llllll_opy_), data, {
      bstack1ll1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ௬"): (config[bstack1ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ௭")], config[bstack1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ௮")])
    })
    if response:
      logger.debug(bstack111ll11ll_opy_.format(bstack1llll1l11l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11lllllll_opy_.format(str(e)))
def bstack1l11l1l111_opy_(framework):
  return bstack1ll1_opy_ (u"ࠥࡿࢂ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ௯").format(str(framework), __version__) if framework else bstack1ll1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ௰").format(
    __version__)
def bstack111l11l1_opy_():
  global CONFIG
  global bstack111ll1ll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1111l1l11_opy_()
    logger.debug(bstack1l1l11l1ll_opy_.format(str(CONFIG)))
    bstack111ll1ll_opy_ = bstack11ll1l1l1_opy_.bstack1l1l111l1_opy_(CONFIG, bstack111ll1ll_opy_)
    bstack11lll1111_opy_()
  except Exception as e:
    logger.error(bstack1ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠤ௱") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1111lllll_opy_
  atexit.register(bstack11llll11_opy_)
  signal.signal(signal.SIGINT, bstack1l1lll11ll_opy_)
  signal.signal(signal.SIGTERM, bstack1l1lll11ll_opy_)
def bstack1111lllll_opy_(exctype, value, traceback):
  global bstack1llll111_opy_
  try:
    for driver in bstack1llll111_opy_:
      bstack11111l1ll_opy_(driver, bstack1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭௲"), bstack1ll1_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ௳") + str(value))
  except Exception:
    pass
  bstack11llll11l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11llll11l_opy_(message=bstack1ll1_opy_ (u"ࠨࠩ௴"), bstack111lll1l1_opy_ = False):
  global CONFIG
  bstack1ll1ll1l1l_opy_ = bstack1ll1_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡇࡻࡧࡪࡶࡴࡪࡱࡱࠫ௵") if bstack111lll1l1_opy_ else bstack1ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ௶")
  try:
    if message:
      bstack1l11l111ll_opy_ = {
        bstack1ll1ll1l1l_opy_ : str(message)
      }
      bstack1l11l1l1l1_opy_(bstack1l11l11l1l_opy_, CONFIG, bstack1l11l111ll_opy_)
    else:
      bstack1l11l1l1l1_opy_(bstack1l11l11l1l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack111lll1l_opy_.format(str(e)))
def bstack1ll1l1l1ll_opy_(bstack111l1111_opy_, size):
  bstack111lllll1_opy_ = []
  while len(bstack111l1111_opy_) > size:
    bstack1111l1ll_opy_ = bstack111l1111_opy_[:size]
    bstack111lllll1_opy_.append(bstack1111l1ll_opy_)
    bstack111l1111_opy_ = bstack111l1111_opy_[size:]
  bstack111lllll1_opy_.append(bstack111l1111_opy_)
  return bstack111lllll1_opy_
def bstack11lllll1l_opy_(args):
  if bstack1ll1_opy_ (u"ࠫ࠲ࡳࠧ௷") in args and bstack1ll1_opy_ (u"ࠬࡶࡤࡣࠩ௸") in args:
    return True
  return False
def run_on_browserstack(bstack1llll1111l_opy_=None, bstack11ll1l1ll_opy_=None, bstack1lll1ll1_opy_=False):
  global CONFIG
  global bstack111111l1_opy_
  global bstack1lll1l1l_opy_
  global bstack1l1l11ll1l_opy_
  global bstack111l1l1l1_opy_
  bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"࠭ࠧ௹")
  bstack1ll1111l_opy_(bstack1lll1llll_opy_, logger)
  if bstack1llll1111l_opy_ and isinstance(bstack1llll1111l_opy_, str):
    bstack1llll1111l_opy_ = eval(bstack1llll1111l_opy_)
  if bstack1llll1111l_opy_:
    CONFIG = bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ௺")]
    bstack111111l1_opy_ = bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ௻")]
    bstack1lll1l1l_opy_ = bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ௼")]
    bstack111l1l1l1_opy_.bstack1l1lll111l_opy_(bstack1ll1_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ௽"), bstack1lll1l1l_opy_)
    bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௾")
  bstack111l1l1l1_opy_.bstack1l1lll111l_opy_(bstack1ll1_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ௿"), uuid4().__str__())
  logger.debug(bstack1ll1_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤ࠾ࠩఀ") + bstack111l1l1l1_opy_.get_property(bstack1ll1_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩఁ")))
  if not bstack1lll1ll1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11ll11l1l_opy_)
      return
    if sys.argv[1] == bstack1ll1_opy_ (u"ࠨ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫం") or sys.argv[1] == bstack1ll1_opy_ (u"ࠩ࠰ࡺࠬః"):
      logger.info(bstack1ll1_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠦࡶࡼࡿࠪఄ").format(__version__))
      return
    if sys.argv[1] == bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪఅ"):
      bstack1ll1l1ll_opy_()
      return
  args = sys.argv
  bstack111l11l1_opy_()
  global bstack11l111111_opy_
  global bstack1111ll1l_opy_
  global bstack1llllll11_opy_
  global bstack1l11lll11l_opy_
  global bstack1ll1llll1_opy_
  global bstack1l1lll1l11_opy_
  global bstack1l1l111111_opy_
  global bstack11ll1l11l_opy_
  global bstack1111llll_opy_
  global bstack1lllll11l1_opy_
  global bstack1lll1lllll_opy_
  bstack1111ll1l_opy_ = len(CONFIG.get(bstack1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఆ"), []))
  if not bstack1ll11111l_opy_:
    if args[1] == bstack1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ఇ") or args[1] == bstack1ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨఈ"):
      bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨఉ")
      args = args[2:]
    elif args[1] == bstack1ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨఊ"):
      bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩఋ")
      args = args[2:]
    elif args[1] == bstack1ll1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪఌ"):
      bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ఍")
      args = args[2:]
    elif args[1] == bstack1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧఎ"):
      bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨఏ")
      args = args[2:]
    elif args[1] == bstack1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨఐ"):
      bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ఑")
      args = args[2:]
    elif args[1] == bstack1ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪఒ"):
      bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫఓ")
      args = args[2:]
    else:
      if not bstack1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨఔ") in CONFIG or str(CONFIG[bstack1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩక")]).lower() in [bstack1ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧఖ"), bstack1ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩగ")]:
        bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩఘ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ఙ")]).lower() == bstack1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪచ"):
        bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫఛ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩజ")]).lower() == bstack1ll1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ఝ"):
        bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧఞ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬట")]).lower() == bstack1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪఠ"):
        bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫడ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨఢ")]).lower() == bstack1ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ణ"):
        bstack1ll11111l_opy_ = bstack1ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧత")
        args = args[1:]
      else:
        os.environ[bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪథ")] = bstack1ll11111l_opy_
        bstack11111l111_opy_(bstack1l1l1l1l_opy_)
  os.environ[bstack1ll1_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪద")] = bstack1ll11111l_opy_
  bstack1l1l11ll1l_opy_ = bstack1ll11111l_opy_
  global bstack1lll1l11ll_opy_
  if bstack1llll1111l_opy_:
    try:
      os.environ[bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬధ")] = bstack1ll11111l_opy_
      bstack1l11l1l1l1_opy_(bstack11lll1l1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack111111111_opy_.format(str(e)))
  global bstack1l11l11l_opy_
  global bstack1l111l11_opy_
  global bstack1l11l1l11_opy_
  global bstack1l11111l_opy_
  global bstack1llll11l1_opy_
  global bstack11lllll11_opy_
  global bstack11111l1l1_opy_
  global bstack1111ll11_opy_
  global bstack1llll11l1l_opy_
  global bstack11lll1lll_opy_
  global bstack1ll11ll1l_opy_
  global bstack1ll111lll1_opy_
  global bstack1ll1l111l_opy_
  global bstack1ll1ll1l1_opy_
  global bstack111l1lll_opy_
  global bstack1l1ll111l_opy_
  global bstack11l111l1_opy_
  global bstack1ll1l1l111_opy_
  global bstack1l1l1llll_opy_
  global bstack1ll11l11_opy_
  global bstack1l11l11l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l11l11l_opy_ = webdriver.Remote.__init__
    bstack1l111l11_opy_ = WebDriver.quit
    bstack1ll111lll1_opy_ = WebDriver.close
    bstack111l1lll_opy_ = WebDriver.get
    bstack1l11l11l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lll1l11ll_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack11ll11l1_opy_
    from QWeb.keywords import browser
    bstack11ll11l1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l11l1ll1_opy_(CONFIG) and bstack1l1ll1ll11_opy_():
    if bstack1lll1ll11l_opy_() < version.parse(bstack1l1ll11l_opy_):
      logger.error(bstack111lll11_opy_.format(bstack1lll1ll11l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1ll111l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1l111ll1_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭న"), False) and not bstack1llll1111l_opy_:
    logger.info(bstack1l1ll11ll1_opy_)
  if bstack1ll11111l_opy_ != bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ఩") or (bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ప") and not bstack1llll1111l_opy_):
    bstack111llll11_opy_()
  if (bstack1ll11111l_opy_ in [bstack1ll1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ఫ"), bstack1ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧబ"), bstack1ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪభ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1lll111ll1_opy_
        bstack11lllll11_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1llll1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1llll11l1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l1llllll_opy_ + str(e))
    except Exception as e:
      bstack1l1lll11_opy_(e, bstack1l1llll1ll_opy_)
    if bstack1ll11111l_opy_ != bstack1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫమ"):
      bstack11llll1ll_opy_()
    bstack1l11l1l11_opy_ = Output.start_test
    bstack1l11111l_opy_ = Output.end_test
    bstack11111l1l1_opy_ = TestStatus.__init__
    bstack1llll11l1l_opy_ = pabot._run
    bstack11lll1lll_opy_ = QueueItem.__init__
    bstack1ll11ll1l_opy_ = pabot._create_command_for_execution
    bstack1l1l1llll_opy_ = pabot._report_results
  if bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫయ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll11_opy_(e, bstack11l1llll_opy_)
    bstack1ll1l111l_opy_ = Runner.run_hook
    bstack1ll1ll1l1_opy_ = Step.run
  if bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬర"):
    try:
      from _pytest.config import Config
      bstack11l111l1_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll1l1l111_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l11lll111_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll11l11_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧఱ"))
  try:
    framework_name = bstack1ll1_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ల") if bstack1ll11111l_opy_ in [bstack1ll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧళ"), bstack1ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨఴ"), bstack1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫవ")] else bstack1l1l11l1_opy_(bstack1ll11111l_opy_)
    bstack1lllll1l1_opy_.launch(CONFIG, {
      bstack1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬశ"): bstack1ll1_opy_ (u"ࠬࢁ࠰ࡾ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫష").format(framework_name) if bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭స") and bstack1lll11lll_opy_() else framework_name,
      bstack1ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫహ"): bstack1ll1l1lll_opy_(framework_name),
      bstack1ll1_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭఺"): __version__,
      bstack1ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ఻"): bstack1ll11111l_opy_
    })
  except Exception as e:
    logger.debug(bstack1ll111111_opy_.format(bstack1ll1_opy_ (u"ࠪࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ఼ࠪ"), str(e)))
  if bstack1ll11111l_opy_ in bstack1lll1l1l11_opy_:
    try:
      framework_name = bstack1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪఽ") if bstack1ll11111l_opy_ in [bstack1ll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫా"), bstack1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬి")] else bstack1ll11111l_opy_
      if bstack1l1l111l_opy_ and bstack1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧీ") in CONFIG and CONFIG[bstack1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨు")] == True:
        if bstack1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩూ") in CONFIG:
          os.environ[bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫృ")] = os.getenv(bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬౄ"), json.dumps(CONFIG[bstack1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ౅")]))
          CONFIG[bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ె")].pop(bstack1ll1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬే"), None)
          CONFIG[bstack1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨై")].pop(bstack1ll1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ౉"), None)
        bstack111llll1l_opy_, bstack1ll1l1l1_opy_ = bstack1111111l1_opy_.bstack1lll11ll1l_opy_(CONFIG, bstack1ll11111l_opy_, bstack1ll1l1lll_opy_(framework_name), str(bstack1lll1ll11l_opy_()))
        if not bstack111llll1l_opy_ is None:
          os.environ[bstack1ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨొ")] = bstack111llll1l_opy_
          os.environ[bstack1ll1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤ࡚ࡅࡔࡖࡢࡖ࡚ࡔ࡟ࡊࡆࠪో")] = str(bstack1ll1l1l1_opy_)
    except Exception as e:
      logger.debug(bstack1ll111111_opy_.format(bstack1ll1_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬౌ"), str(e)))
  if bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ్࠭"):
    bstack1llllll11_opy_ = True
    if bstack1llll1111l_opy_ and bstack1lll1ll1_opy_:
      bstack1l1lll1l11_opy_ = CONFIG.get(bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ౎"), {}).get(bstack1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ౏"))
      bstack11l1ll1l_opy_(bstack111l1ll1l_opy_)
    elif bstack1llll1111l_opy_:
      bstack1l1lll1l11_opy_ = CONFIG.get(bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭౐"), {}).get(bstack1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ౑"))
      global bstack1llll111_opy_
      try:
        if bstack11lllll1l_opy_(bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ౒")]) and multiprocessing.current_process().name == bstack1ll1_opy_ (u"ࠬ࠶ࠧ౓"):
          bstack1llll1111l_opy_[bstack1ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ౔")].remove(bstack1ll1_opy_ (u"ࠧ࠮࡯ౕࠪ"))
          bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨౖࠫ")].remove(bstack1ll1_opy_ (u"ࠩࡳࡨࡧ࠭౗"))
          bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ౘ")] = bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧౙ")][0]
          with open(bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨౚ")], bstack1ll1_opy_ (u"࠭ࡲࠨ౛")) as f:
            bstack11ll1ll1l_opy_ = f.read()
          bstack11111llll_opy_ = bstack1ll1_opy_ (u"ࠢࠣࠤࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡥ࡭ࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡁࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࠫࡿࢂ࠯࠻ࠡࡨࡵࡳࡲࠦࡰࡥࡤࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡔࡩࡨ࠻ࠡࡱࡪࡣࡩࡨࠠ࠾ࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫࠼ࠌࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࡸࡷࡿ࠺ࠋࠢࠣࠤࠥࡧࡲࡨࠢࡀࠤࡸࡺࡲࠩ࡫ࡱࡸ࠭ࡧࡲࡨࠫ࠮࠵࠵࠯ࠊࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࡐࡥࡤ࠱ࡨࡴࡥࡢࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࡔࡩࡨࠨࠪ࠰ࡶࡩࡹࡥࡴࡳࡣࡦࡩ࠭࠯࡜࡯ࠤࠥࠦ౜").format(str(bstack1llll1111l_opy_))
          bstack1ll111111l_opy_ = bstack11111llll_opy_ + bstack11ll1ll1l_opy_
          bstack11l1llll1_opy_ = bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫౝ")] + bstack1ll1_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡸࡪࡳࡰ࠯ࡲࡼࠫ౞")
          with open(bstack11l1llll1_opy_, bstack1ll1_opy_ (u"ࠪࡻࠬ౟")):
            pass
          with open(bstack11l1llll1_opy_, bstack1ll1_opy_ (u"ࠦࡼ࠱ࠢౠ")) as f:
            f.write(bstack1ll111111l_opy_)
          import subprocess
          bstack1l1l1ll1ll_opy_ = subprocess.run([bstack1ll1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧౡ"), bstack11l1llll1_opy_])
          if os.path.exists(bstack11l1llll1_opy_):
            os.unlink(bstack11l1llll1_opy_)
          os._exit(bstack1l1l1ll1ll_opy_.returncode)
        else:
          if bstack11lllll1l_opy_(bstack1llll1111l_opy_[bstack1ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩౢ")]):
            bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪౣ")].remove(bstack1ll1_opy_ (u"ࠨ࠯ࡰࠫ౤"))
            bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ౥")].remove(bstack1ll1_opy_ (u"ࠪࡴࡩࡨࠧ౦"))
            bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ౧")] = bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ౨")][0]
          bstack11l1ll1l_opy_(bstack111l1ll1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1llll1111l_opy_[bstack1ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ౩")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll1_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩ౪")] = bstack1ll1_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪ౫")
          mod_globals[bstack1ll1_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ౬")] = os.path.abspath(bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭౭")])
          exec(open(bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ౮")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll1_opy_ (u"ࠬࡉࡡࡶࡩ࡫ࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠬ౯").format(str(e)))
          for driver in bstack1llll111_opy_:
            bstack11ll1l1ll_opy_.append({
              bstack1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ౰"): bstack1llll1111l_opy_[bstack1ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ౱")],
              bstack1ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ౲"): str(e),
              bstack1ll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ౳"): multiprocessing.current_process().name
            })
            bstack11111l1ll_opy_(driver, bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౴"), bstack1ll1_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ౵") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1llll111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1lll1l1l_opy_, CONFIG, logger)
      bstack1ll1l111ll_opy_()
      bstack11l1l1ll1_opy_()
      bstack1l1l11lll_opy_ = {
        bstack1ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ౶"): args[0],
        bstack1ll1_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭౷"): CONFIG,
        bstack1ll1_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ౸"): bstack111111l1_opy_,
        bstack1ll1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ౹"): bstack1lll1l1l_opy_
      }
      percy.bstack1l11111l1_opy_()
      if bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౺") in CONFIG:
        bstack11l1ll1ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll1111lll_opy_ = manager.list()
        if bstack11lllll1l_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౻")]):
            if index == 0:
              bstack1l1l11lll_opy_[bstack1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ౼")] = args
            bstack11l1ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1l11lll_opy_, bstack1ll1111lll_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౽")]):
            bstack11l1ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1l11lll_opy_, bstack1ll1111lll_opy_)))
        for t in bstack11l1ll1ll_opy_:
          t.start()
        for t in bstack11l1ll1ll_opy_:
          t.join()
        bstack11ll1l11l_opy_ = list(bstack1ll1111lll_opy_)
      else:
        if bstack11lllll1l_opy_(args):
          bstack1l1l11lll_opy_[bstack1ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ౾")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1l11lll_opy_,))
          test.start()
          test.join()
        else:
          bstack11l1ll1l_opy_(bstack111l1ll1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll1_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩ౿")] = bstack1ll1_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪಀ")
          mod_globals[bstack1ll1_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫಁ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩಂ") or bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪಃ"):
    percy.init(bstack1lll1l1l_opy_, CONFIG, logger)
    percy.bstack1l11111l1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1lll11_opy_(e, bstack1l1llll1ll_opy_)
    bstack1ll1l111ll_opy_()
    bstack11l1ll1l_opy_(bstack1ll1ll1ll1_opy_)
    if bstack1l1l111l_opy_:
      bstack111llllll_opy_(bstack1ll1ll1ll1_opy_, args)
      if bstack1ll1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ಄") in args:
        i = args.index(bstack1ll1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫಅ"))
        args.pop(i)
        args.pop(i)
      if bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಆ") not in CONFIG:
        CONFIG[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಇ")] = [{}]
        bstack1111ll1l_opy_ = 1
      if bstack11l111111_opy_ == 0:
        bstack11l111111_opy_ = 1
      args.insert(0, str(bstack11l111111_opy_))
      args.insert(0, str(bstack1ll1_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧಈ")))
    if bstack1lllll1l1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11l11111_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l1111l1l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll1_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥಉ"),
        ).parse_args(bstack11l11111_opy_)
        bstack111ll1l11_opy_ = args.index(bstack11l11111_opy_[0]) if len(bstack11l11111_opy_) > 0 else len(args)
        args.insert(bstack111ll1l11_opy_, str(bstack1ll1_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨಊ")))
        args.insert(bstack111ll1l11_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩಋ"))))
        if bstack1llll1l1ll_opy_(os.environ.get(bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫಌ"))) and str(os.environ.get(bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ಍"), bstack1ll1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ಎ"))) != bstack1ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧಏ"):
          for bstack1l1111111_opy_ in bstack1l1111l1l_opy_:
            args.remove(bstack1l1111111_opy_)
          bstack11l1ll1l1_opy_ = os.environ.get(bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧಐ")).split(bstack1ll1_opy_ (u"ࠫ࠱࠭಑"))
          for bstack1l11l111l1_opy_ in bstack11l1ll1l1_opy_:
            args.append(bstack1l11l111l1_opy_)
      except Exception as e:
        logger.error(bstack1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࠣಒ").format(e))
    pabot.main(args)
  elif bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧಓ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1lll11_opy_(e, bstack1l1llll1ll_opy_)
    for a in args:
      if bstack1ll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ಔ") in a:
        bstack1ll1llll1_opy_ = int(a.split(bstack1ll1_opy_ (u"ࠨ࠼ࠪಕ"))[1])
      if bstack1ll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ಖ") in a:
        bstack1l1lll1l11_opy_ = str(a.split(bstack1ll1_opy_ (u"ࠪ࠾ࠬಗ"))[1])
      if bstack1ll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫಘ") in a:
        bstack1l1l111111_opy_ = str(a.split(bstack1ll1_opy_ (u"ࠬࡀࠧಙ"))[1])
    bstack1llllll1ll_opy_ = None
    if bstack1ll1_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬಚ") in args:
      i = args.index(bstack1ll1_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ಛ"))
      args.pop(i)
      bstack1llllll1ll_opy_ = args.pop(i)
    if bstack1llllll1ll_opy_ is not None:
      global bstack1ll11l1lll_opy_
      bstack1ll11l1lll_opy_ = bstack1llllll1ll_opy_
    bstack11l1ll1l_opy_(bstack1ll1ll1ll1_opy_)
    run_cli(args)
    if bstack1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬಜ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1ll1lll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11ll1l1ll_opy_.append(bstack1l1ll1lll1_opy_)
  elif bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಝ"):
    percy.init(bstack1lll1l1l_opy_, CONFIG, logger)
    percy.bstack1l11111l1_opy_()
    bstack1l1l1l111_opy_ = bstack1l1111l11_opy_(args, logger, CONFIG, bstack1l1l111l_opy_)
    bstack1l1l1l111_opy_.bstack1ll11ll111_opy_()
    bstack1ll1l111ll_opy_()
    bstack1l11lll11l_opy_ = True
    bstack1lllll11l1_opy_ = bstack1l1l1l111_opy_.bstack11lll11l1_opy_()
    bstack1l1l1l111_opy_.bstack1l1l11lll_opy_(bstack1111lll11_opy_)
    bstack11l1ll11l_opy_ = bstack1l1l1l111_opy_.bstack1lll111ll_opy_(bstack11lll111_opy_, {
      bstack1ll1_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫಞ"): bstack111111l1_opy_,
      bstack1ll1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ಟ"): bstack1lll1l1l_opy_,
      bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨಠ"): bstack1l1l111l_opy_
    })
    try:
      bstack1lll1l111_opy_, bstack111l1l11_opy_ = map(list, zip(*bstack11l1ll11l_opy_))
      bstack1111llll_opy_ = bstack1lll1l111_opy_[0]
      for status_code in bstack111l1l11_opy_:
        if status_code != 0:
          bstack1lll1lllll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡦࡴࡵࡳࡷࡹࠠࡢࡰࡧࠤࡸࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠰ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠺ࠡࡽࢀࠦಡ").format(str(e)))
  elif bstack1ll11111l_opy_ == bstack1ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧಢ"):
    try:
      from behave.__main__ import main as bstack1l111l1ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1lll11_opy_(e, bstack11l1llll_opy_)
    bstack1ll1l111ll_opy_()
    bstack1l11lll11l_opy_ = True
    bstack1llll11111_opy_ = 1
    if bstack1ll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಣ") in CONFIG:
      bstack1llll11111_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩತ")]
    if bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಥ") in CONFIG:
      bstack1l11ll1ll_opy_ = int(bstack1llll11111_opy_) * int(len(CONFIG[bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧದ")]))
    else:
      bstack1l11ll1ll_opy_ = int(bstack1llll11111_opy_)
    config = Configuration(args)
    bstack1l11l1ll11_opy_ = config.paths
    if len(bstack1l11l1ll11_opy_) == 0:
      import glob
      pattern = bstack1ll1_opy_ (u"ࠬ࠰ࠪ࠰ࠬ࠱ࡪࡪࡧࡴࡶࡴࡨࠫಧ")
      bstack1l1lll1l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1lll1l1_opy_)
      config = Configuration(args)
      bstack1l11l1ll11_opy_ = config.paths
    bstack1l1l11l11_opy_ = [os.path.normpath(item) for item in bstack1l11l1ll11_opy_]
    bstack1lll11l1l_opy_ = [os.path.normpath(item) for item in args]
    bstack11l11l1l1_opy_ = [item for item in bstack1lll11l1l_opy_ if item not in bstack1l1l11l11_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll1_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧನ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1l11l11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1ll111l1_opy_)))
                    for bstack1l1ll111l1_opy_ in bstack1l1l11l11_opy_]
    bstack1l1l1l11l_opy_ = []
    for spec in bstack1l1l11l11_opy_:
      bstack11l1111ll_opy_ = []
      bstack11l1111ll_opy_ += bstack11l11l1l1_opy_
      bstack11l1111ll_opy_.append(spec)
      bstack1l1l1l11l_opy_.append(bstack11l1111ll_opy_)
    execution_items = []
    for bstack11l1111ll_opy_ in bstack1l1l1l11l_opy_:
      if bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ಩") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಪ")]):
          item = {}
          item[bstack1ll1_opy_ (u"ࠩࡤࡶ࡬࠭ಫ")] = bstack1ll1_opy_ (u"ࠪࠤࠬಬ").join(bstack11l1111ll_opy_)
          item[bstack1ll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪಭ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1ll1_opy_ (u"ࠬࡧࡲࡨࠩಮ")] = bstack1ll1_opy_ (u"࠭ࠠࠨಯ").join(bstack11l1111ll_opy_)
        item[bstack1ll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ರ")] = 0
        execution_items.append(item)
    bstack1lll1l1l1_opy_ = bstack1ll1l1l1ll_opy_(execution_items, bstack1l11ll1ll_opy_)
    for execution_item in bstack1lll1l1l1_opy_:
      bstack11l1ll1ll_opy_ = []
      for item in execution_item:
        bstack11l1ll1ll_opy_.append(bstack1lllllllll_opy_(name=str(item[bstack1ll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧಱ")]),
                                             target=bstack1lll11l111_opy_,
                                             args=(item[bstack1ll1_opy_ (u"ࠩࡤࡶ࡬࠭ಲ")],)))
      for t in bstack11l1ll1ll_opy_:
        t.start()
      for t in bstack11l1ll1ll_opy_:
        t.join()
  else:
    bstack11111l111_opy_(bstack1l1l1l1l_opy_)
  if not bstack1llll1111l_opy_:
    bstack1l11111ll_opy_()
  bstack11ll1l1l1_opy_.bstack1l1l1l1l1_opy_()
def browserstack_initialize(bstack111l1l1ll_opy_=None):
  run_on_browserstack(bstack111l1l1ll_opy_, None, True)
def bstack1l11111ll_opy_():
  global CONFIG
  global bstack1l1l11ll1l_opy_
  global bstack1lll1lllll_opy_
  global bstack1llll1l11_opy_
  global bstack111l1l1l1_opy_
  bstack1lllll1l1_opy_.stop(bstack111l1l1l1_opy_.get_property(bstack1ll1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪಳ")))
  bstack1lllll1l1_opy_.bstack11l1l11l1_opy_()
  if bstack1111111l1_opy_.bstack111l1lll1_opy_(CONFIG):
    bstack1111111l1_opy_.bstack1l11l1l1l_opy_()
  [bstack1ll111l1_opy_, bstack111111ll1_opy_] = get_build_link()
  if bstack1ll111l1_opy_ is not None and bstack11l1l111l_opy_() != -1:
    sessions = bstack111lll11l_opy_(bstack1ll111l1_opy_)
    bstack1ll1lll1l_opy_(sessions, bstack111111ll1_opy_)
  if bstack1l1l11ll1l_opy_ == bstack1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ಴") and bstack1lll1lllll_opy_ != 0:
    sys.exit(bstack1lll1lllll_opy_)
  if bstack1l1l11ll1l_opy_ == bstack1ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬವ") and bstack1llll1l11_opy_ != 0:
    sys.exit(bstack1llll1l11_opy_)
def bstack1l1l11l1_opy_(bstack11l1l11l_opy_):
  if bstack11l1l11l_opy_:
    return bstack11l1l11l_opy_.capitalize()
  else:
    return bstack1ll1_opy_ (u"࠭ࠧಶ")
def bstack1lll11lll1_opy_(bstack1l1l111l1l_opy_):
  if bstack1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಷ") in bstack1l1l111l1l_opy_ and bstack1l1l111l1l_opy_[bstack1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಸ")] != bstack1ll1_opy_ (u"ࠩࠪಹ"):
    return bstack1l1l111l1l_opy_[bstack1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ಺")]
  else:
    bstack1l11l1l1ll_opy_ = bstack1ll1_opy_ (u"ࠦࠧ಻")
    if bstack1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩ಼ࠬ") in bstack1l1l111l1l_opy_ and bstack1l1l111l1l_opy_[bstack1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ಽ")] != None:
      bstack1l11l1l1ll_opy_ += bstack1l1l111l1l_opy_[bstack1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧಾ")] + bstack1ll1_opy_ (u"ࠣ࠮ࠣࠦಿ")
      if bstack1l1l111l1l_opy_[bstack1ll1_opy_ (u"ࠩࡲࡷࠬೀ")] == bstack1ll1_opy_ (u"ࠥ࡭ࡴࡹࠢು"):
        bstack1l11l1l1ll_opy_ += bstack1ll1_opy_ (u"ࠦ࡮ࡕࡓࠡࠤೂ")
      bstack1l11l1l1ll_opy_ += (bstack1l1l111l1l_opy_[bstack1ll1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩೃ")] or bstack1ll1_opy_ (u"࠭ࠧೄ"))
      return bstack1l11l1l1ll_opy_
    else:
      bstack1l11l1l1ll_opy_ += bstack1l1l11l1_opy_(bstack1l1l111l1l_opy_[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ೅")]) + bstack1ll1_opy_ (u"ࠣࠢࠥೆ") + (
              bstack1l1l111l1l_opy_[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫೇ")] or bstack1ll1_opy_ (u"ࠪࠫೈ")) + bstack1ll1_opy_ (u"ࠦ࠱ࠦࠢ೉")
      if bstack1l1l111l1l_opy_[bstack1ll1_opy_ (u"ࠬࡵࡳࠨೊ")] == bstack1ll1_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢೋ"):
        bstack1l11l1l1ll_opy_ += bstack1ll1_opy_ (u"ࠢࡘ࡫ࡱࠤࠧೌ")
      bstack1l11l1l1ll_opy_ += bstack1l1l111l1l_opy_[bstack1ll1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲ್ࠬ")] or bstack1ll1_opy_ (u"ࠩࠪ೎")
      return bstack1l11l1l1ll_opy_
def bstack1ll11l11l_opy_(bstack11111l11l_opy_):
  if bstack11111l11l_opy_ == bstack1ll1_opy_ (u"ࠥࡨࡴࡴࡥࠣ೏"):
    return bstack1ll1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ೐")
  elif bstack11111l11l_opy_ == bstack1ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ೑"):
    return bstack1ll1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ೒")
  elif bstack11111l11l_opy_ == bstack1ll1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ೓"):
    return bstack1ll1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ೔")
  elif bstack11111l11l_opy_ == bstack1ll1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣೕ"):
    return bstack1ll1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬೖ")
  elif bstack11111l11l_opy_ == bstack1ll1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ೗"):
    return bstack1ll1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ೘")
  elif bstack11111l11l_opy_ == bstack1ll1_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢ೙"):
    return bstack1ll1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ೚")
  else:
    return bstack1ll1_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬ೛") + bstack1l1l11l1_opy_(
      bstack11111l11l_opy_) + bstack1ll1_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ೜")
def bstack1ll1l1ll1_opy_(session):
  return bstack1ll1_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪೝ").format(
    session[bstack1ll1_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨೞ")], bstack1lll11lll1_opy_(session), bstack1ll11l11l_opy_(session[bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫ೟")]),
    bstack1ll11l11l_opy_(session[bstack1ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ೠ")]),
    bstack1l1l11l1_opy_(session[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨೡ")] or session[bstack1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨೢ")] or bstack1ll1_opy_ (u"ࠩࠪೣ")) + bstack1ll1_opy_ (u"ࠥࠤࠧ೤") + (session[bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭೥")] or bstack1ll1_opy_ (u"ࠬ࠭೦")),
    session[bstack1ll1_opy_ (u"࠭࡯ࡴࠩ೧")] + bstack1ll1_opy_ (u"ࠢࠡࠤ೨") + session[bstack1ll1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ೩")], session[bstack1ll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ೪")] or bstack1ll1_opy_ (u"ࠪࠫ೫"),
    session[bstack1ll1_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨ೬")] if session[bstack1ll1_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ೭")] else bstack1ll1_opy_ (u"࠭ࠧ೮"))
def bstack1ll1lll1l_opy_(sessions, bstack111111ll1_opy_):
  try:
    bstack11ll1lll1_opy_ = bstack1ll1_opy_ (u"ࠢࠣ೯")
    if not os.path.exists(bstack11ll111ll_opy_):
      os.mkdir(bstack11ll111ll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭೰")), bstack1ll1_opy_ (u"ࠩࡵࠫೱ")) as f:
      bstack11ll1lll1_opy_ = f.read()
    bstack11ll1lll1_opy_ = bstack11ll1lll1_opy_.replace(bstack1ll1_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧೲ"), str(len(sessions)))
    bstack11ll1lll1_opy_ = bstack11ll1lll1_opy_.replace(bstack1ll1_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫೳ"), bstack111111ll1_opy_)
    bstack11ll1lll1_opy_ = bstack11ll1lll1_opy_.replace(bstack1ll1_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭೴"),
                                              sessions[0].get(bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪ೵")) if sessions[0] else bstack1ll1_opy_ (u"ࠧࠨ೶"))
    with open(os.path.join(bstack11ll111ll_opy_, bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ೷")), bstack1ll1_opy_ (u"ࠩࡺࠫ೸")) as stream:
      stream.write(bstack11ll1lll1_opy_.split(bstack1ll1_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ೹"))[0])
      for session in sessions:
        stream.write(bstack1ll1l1ll1_opy_(session))
      stream.write(bstack11ll1lll1_opy_.split(bstack1ll1_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨ೺"))[1])
    logger.info(bstack1ll1_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨ೻").format(bstack11ll111ll_opy_));
  except Exception as e:
    logger.debug(bstack1l111ll11_opy_.format(str(e)))
def bstack111lll11l_opy_(bstack1ll111l1_opy_):
  global CONFIG
  try:
    host = bstack1ll1_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩ೼") if bstack1ll1_opy_ (u"ࠧࡢࡲࡳࠫ೽") in CONFIG else bstack1ll1_opy_ (u"ࠨࡣࡳ࡭ࠬ೾")
    user = CONFIG[bstack1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ೿")]
    key = CONFIG[bstack1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ഀ")]
    bstack1ll1l11ll1_opy_ = bstack1ll1_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪഁ") if bstack1ll1_opy_ (u"ࠬࡧࡰࡱࠩം") in CONFIG else bstack1ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨഃ")
    url = bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬഄ").format(user, key, host, bstack1ll1l11ll1_opy_,
                                                                                bstack1ll111l1_opy_)
    headers = {
      bstack1ll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧഅ"): bstack1ll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬആ"),
    }
    proxies = bstack11ll1ll11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨഇ")], response.json()))
  except Exception as e:
    logger.debug(bstack1111l1l1l_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1l1l1llll1_opy_
  try:
    if bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧഈ") in CONFIG:
      host = bstack1ll1_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨഉ") if bstack1ll1_opy_ (u"࠭ࡡࡱࡲࠪഊ") in CONFIG else bstack1ll1_opy_ (u"ࠧࡢࡲ࡬ࠫഋ")
      user = CONFIG[bstack1ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪഌ")]
      key = CONFIG[bstack1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ഍")]
      bstack1ll1l11ll1_opy_ = bstack1ll1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩഎ") if bstack1ll1_opy_ (u"ࠫࡦࡶࡰࠨഏ") in CONFIG else bstack1ll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧഐ")
      url = bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭഑").format(user, key, host, bstack1ll1l11ll1_opy_)
      headers = {
        bstack1ll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ഒ"): bstack1ll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫഓ"),
      }
      if bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫഔ") in CONFIG:
        params = {bstack1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨക"): CONFIG[bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧഖ")], bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨഗ"): CONFIG[bstack1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨഘ")]}
      else:
        params = {bstack1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬങ"): CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫച")]}
      proxies = bstack11ll1ll11_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1ll1l1ll11_opy_ = response.json()[0][bstack1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬഛ")]
        if bstack1ll1l1ll11_opy_:
          bstack111111ll1_opy_ = bstack1ll1l1ll11_opy_[bstack1ll1_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧജ")].split(bstack1ll1_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪഝ"))[0] + bstack1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭ഞ") + bstack1ll1l1ll11_opy_[
            bstack1ll1_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩട")]
          logger.info(bstack1111l111_opy_.format(bstack111111ll1_opy_))
          bstack1l1l1llll1_opy_ = bstack1ll1l1ll11_opy_[bstack1ll1_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪഠ")]
          bstack1lll1lll11_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫഡ")]
          if bstack1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫഢ") in CONFIG:
            bstack1lll1lll11_opy_ += bstack1ll1_opy_ (u"ࠪࠤࠬണ") + CONFIG[bstack1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ത")]
          if bstack1lll1lll11_opy_ != bstack1ll1l1ll11_opy_[bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪഥ")]:
            logger.debug(bstack1ll11l111l_opy_.format(bstack1ll1l1ll11_opy_[bstack1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫദ")], bstack1lll1lll11_opy_))
          return [bstack1ll1l1ll11_opy_[bstack1ll1_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪധ")], bstack111111ll1_opy_]
    else:
      logger.warn(bstack1l1l111lll_opy_)
  except Exception as e:
    logger.debug(bstack1llll11ll1_opy_.format(str(e)))
  return [None, None]
def bstack1ll11llll1_opy_(url, bstack1ll111ll_opy_=False):
  global CONFIG
  global bstack1l1l1ll1l_opy_
  if not bstack1l1l1ll1l_opy_:
    hostname = bstack1l11lll11_opy_(url)
    is_private = bstack1ll1ll11_opy_(hostname)
    if (bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬന") in CONFIG and not bstack1llll1l1ll_opy_(CONFIG[bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ഩ")])) and (is_private or bstack1ll111ll_opy_):
      bstack1l1l1ll1l_opy_ = hostname
def bstack1l11lll11_opy_(url):
  return urlparse(url).hostname
def bstack1ll1ll11_opy_(hostname):
  for bstack1l111l1l1_opy_ in bstack1l1ll1l11_opy_:
    regex = re.compile(bstack1l111l1l1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1ll1l11111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1ll1llll1_opy_
  bstack1l1lllll1l_opy_ = not (bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧപ"), None) and bstack1ll1llll1l_opy_(
          threading.current_thread(), bstack1ll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪഫ"), None))
  bstack1ll11ll11_opy_ = getattr(driver, bstack1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬബ"), None) != True
  if not bstack1111111l1_opy_.bstack1ll1ll1111_opy_(CONFIG, bstack1ll1llll1_opy_) or (bstack1ll11ll11_opy_ and bstack1l1lllll1l_opy_):
    logger.warning(bstack1ll1_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤഭ"))
    return {}
  try:
    logger.debug(bstack1ll1_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫമ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1111l11ll_opy_.bstack111lll111_opy_)
    return results
  except Exception:
    logger.error(bstack1ll1_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥയ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1ll1llll1_opy_
  bstack1l1lllll1l_opy_ = not (bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ര"), None) and bstack1ll1llll1l_opy_(
          threading.current_thread(), bstack1ll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩറ"), None))
  bstack1ll11ll11_opy_ = getattr(driver, bstack1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫല"), None) != True
  if not bstack1111111l1_opy_.bstack1ll1ll1111_opy_(CONFIG, bstack1ll1llll1_opy_) or (bstack1ll11ll11_opy_ and bstack1l1lllll1l_opy_):
    logger.warning(bstack1ll1_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤള"))
    return {}
  try:
    logger.debug(bstack1ll1_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫഴ"))
    logger.debug(perform_scan(driver))
    bstack1lll1l1l1l_opy_ = driver.execute_async_script(bstack1111l11ll_opy_.bstack1llll1ll1l_opy_)
    return bstack1lll1l1l1l_opy_
  except Exception:
    logger.error(bstack1ll1_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣവ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1ll1llll1_opy_
  bstack1l1lllll1l_opy_ = not (bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬശ"), None) and bstack1ll1llll1l_opy_(
          threading.current_thread(), bstack1ll1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨഷ"), None))
  bstack1ll11ll11_opy_ = getattr(driver, bstack1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪസ"), None) != True
  if not bstack1111111l1_opy_.bstack1ll1ll1111_opy_(CONFIG, bstack1ll1llll1_opy_) or (bstack1ll11ll11_opy_ and bstack1l1lllll1l_opy_):
    logger.warning(bstack1ll1_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨഹ"))
    return {}
  try:
    bstack1lll11l1ll_opy_ = driver.execute_async_script(bstack1111l11ll_opy_.perform_scan, {bstack1ll1_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬഺ"): kwargs.get(bstack1ll1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪ഻ࠧ"), None) or bstack1ll1_opy_ (u"ࠧࠨ഼")})
    return bstack1lll11l1ll_opy_
  except Exception:
    logger.error(bstack1ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢഽ"))
    return {}