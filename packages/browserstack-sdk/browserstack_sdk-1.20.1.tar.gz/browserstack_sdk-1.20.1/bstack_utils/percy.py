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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l1l11l11l_opy_, bstack1l1l11llll_opy_
class bstack1l11l1lll1_opy_:
  working_dir = os.getcwd()
  bstack1lll1ll1l1_opy_ = False
  config = {}
  binary_path = bstack1ll1_opy_ (u"ࠪࠫᏹ")
  bstack111111ll11_opy_ = bstack1ll1_opy_ (u"ࠫࠬᏺ")
  bstack1l1ll11111_opy_ = False
  bstack11111l11ll_opy_ = None
  bstack1lllllll111_opy_ = {}
  bstack1llllll1lll_opy_ = 300
  bstack11111ll11l_opy_ = False
  logger = None
  bstack11111l111l_opy_ = False
  bstack11111l1ll1_opy_ = bstack1ll1_opy_ (u"ࠬ࠭ᏻ")
  bstack111111l111_opy_ = {
    bstack1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᏼ") : 1,
    bstack1ll1_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨᏽ") : 2,
    bstack1ll1_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭᏾") : 3,
    bstack1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ᏿") : 4
  }
  def __init__(self) -> None: pass
  def bstack1111l11ll1_opy_(self):
    bstack11111111ll_opy_ = bstack1ll1_opy_ (u"ࠪࠫ᐀")
    bstack11111lll1l_opy_ = sys.platform
    bstack1llllll1ll1_opy_ = bstack1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᐁ")
    if re.match(bstack1ll1_opy_ (u"ࠧࡪࡡࡳࡹ࡬ࡲࢁࡳࡡࡤࠢࡲࡷࠧᐂ"), bstack11111lll1l_opy_) != None:
      bstack11111111ll_opy_ = bstack11l11lllll_opy_ + bstack1ll1_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡯ࡴࡺ࠱ࡾ࡮ࡶࠢᐃ")
      self.bstack11111l1ll1_opy_ = bstack1ll1_opy_ (u"ࠧ࡮ࡣࡦࠫᐄ")
    elif re.match(bstack1ll1_opy_ (u"ࠣ࡯ࡶࡻ࡮ࡴࡼ࡮ࡵࡼࡷࢁࡳࡩ࡯ࡩࡺࢀࡨࡿࡧࡸ࡫ࡱࢀࡧࡩࡣࡸ࡫ࡱࢀࡼ࡯࡮ࡤࡧࡿࡩࡲࡩࡼࡸ࡫ࡱ࠷࠷ࠨᐅ"), bstack11111lll1l_opy_) != None:
      bstack11111111ll_opy_ = bstack11l11lllll_opy_ + bstack1ll1_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡺ࡭ࡳ࠴ࡺࡪࡲࠥᐆ")
      bstack1llllll1ll1_opy_ = bstack1ll1_opy_ (u"ࠥࡴࡪࡸࡣࡺ࠰ࡨࡼࡪࠨᐇ")
      self.bstack11111l1ll1_opy_ = bstack1ll1_opy_ (u"ࠫࡼ࡯࡮ࠨᐈ")
    else:
      bstack11111111ll_opy_ = bstack11l11lllll_opy_ + bstack1ll1_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡲࡩ࡯ࡷࡻ࠲ࡿ࡯ࡰࠣᐉ")
      self.bstack11111l1ll1_opy_ = bstack1ll1_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬᐊ")
    return bstack11111111ll_opy_, bstack1llllll1ll1_opy_
  def bstack1lllllllll1_opy_(self):
    try:
      bstack11111l1l11_opy_ = [os.path.join(expanduser(bstack1ll1_opy_ (u"ࠢࡿࠤᐋ")), bstack1ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᐌ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11111l1l11_opy_:
        if(self.bstack1111111lll_opy_(path)):
          return path
      raise bstack1ll1_opy_ (u"ࠤࡘࡲࡦࡲࡢࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᐍ")
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠮ࠢࡾࢁࠧᐎ").format(e))
  def bstack1111111lll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111111l11_opy_(self, bstack11111111ll_opy_, bstack1llllll1ll1_opy_):
    try:
      bstack1111l111ll_opy_ = self.bstack1lllllllll1_opy_()
      bstack1lllllll1l1_opy_ = os.path.join(bstack1111l111ll_opy_, bstack1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡾ࡮ࡶࠧᐏ"))
      bstack1111l11lll_opy_ = os.path.join(bstack1111l111ll_opy_, bstack1llllll1ll1_opy_)
      if os.path.exists(bstack1111l11lll_opy_):
        self.logger.info(bstack1ll1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᐐ").format(bstack1111l11lll_opy_))
        return bstack1111l11lll_opy_
      if os.path.exists(bstack1lllllll1l1_opy_):
        self.logger.info(bstack1ll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࢀࡩࡱࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡷࡱࡾ࡮ࡶࡰࡪࡰࡪࠦᐑ").format(bstack1lllllll1l1_opy_))
        return self.bstack111111l1ll_opy_(bstack1lllllll1l1_opy_, bstack1llllll1ll1_opy_)
      self.logger.info(bstack1ll1_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮ࠢࡾࢁࠧᐒ").format(bstack11111111ll_opy_))
      response = bstack1l1l11llll_opy_(bstack1ll1_opy_ (u"ࠨࡉࡈࡘࠬᐓ"), bstack11111111ll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1lllllll1l1_opy_, bstack1ll1_opy_ (u"ࠩࡺࡦࠬᐔ")) as file:
          file.write(response.content)
        self.logger.info(bstack1ll1_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡡ࡯ࡦࠣࡷࡦࡼࡥࡥࠢࡤࡸࠥࢁࡽࠣᐕ").format(bstack1lllllll1l1_opy_))
        return self.bstack111111l1ll_opy_(bstack1lllllll1l1_opy_, bstack1llllll1ll1_opy_)
      else:
        raise(bstack1ll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲࡙ࠥࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠽ࠤࢀࢃࠢᐖ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨᐗ").format(e))
  def bstack111111ll1l_opy_(self, bstack11111111ll_opy_, bstack1llllll1ll1_opy_):
    try:
      retry = 2
      bstack1111l11lll_opy_ = None
      bstack11111ll1ll_opy_ = False
      while retry > 0:
        bstack1111l11lll_opy_ = self.bstack1111111l11_opy_(bstack11111111ll_opy_, bstack1llllll1ll1_opy_)
        bstack11111ll1ll_opy_ = self.bstack1111l111l1_opy_(bstack11111111ll_opy_, bstack1llllll1ll1_opy_, bstack1111l11lll_opy_)
        if bstack11111ll1ll_opy_:
          break
        retry -= 1
      return bstack1111l11lll_opy_, bstack11111ll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡶࡡࡵࡪࠥᐘ").format(e))
    return bstack1111l11lll_opy_, False
  def bstack1111l111l1_opy_(self, bstack11111111ll_opy_, bstack1llllll1ll1_opy_, bstack1111l11lll_opy_, bstack1111111ll1_opy_ = 0):
    if bstack1111111ll1_opy_ > 1:
      return False
    if bstack1111l11lll_opy_ == None or os.path.exists(bstack1111l11lll_opy_) == False:
      self.logger.warn(bstack1ll1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡴࡨࡸࡷࡿࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᐙ"))
      return False
    bstack111111l1l1_opy_ = bstack1ll1_opy_ (u"ࠣࡠ࠱࠮ࡅࡶࡥࡳࡥࡼࡠ࠴ࡩ࡬ࡪࠢ࡟ࡨ࠳ࡢࡤࠬ࠰࡟ࡨ࠰ࠨᐚ")
    command = bstack1ll1_opy_ (u"ࠩࡾࢁࠥ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᐛ").format(bstack1111l11lll_opy_)
    bstack11111l1l1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111111l1l1_opy_, bstack11111l1l1l_opy_) != None:
      return True
    else:
      self.logger.error(bstack1ll1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡥ࡮ࡲࡥࡥࠤᐜ"))
      return False
  def bstack111111l1ll_opy_(self, bstack1lllllll1l1_opy_, bstack1llllll1ll1_opy_):
    try:
      working_dir = os.path.dirname(bstack1lllllll1l1_opy_)
      shutil.unpack_archive(bstack1lllllll1l1_opy_, working_dir)
      bstack1111l11lll_opy_ = os.path.join(working_dir, bstack1llllll1ll1_opy_)
      os.chmod(bstack1111l11lll_opy_, 0o755)
      return bstack1111l11lll_opy_
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡶࡰࡽ࡭ࡵࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᐝ"))
  def bstack111111111l_opy_(self):
    try:
      percy = str(self.config.get(bstack1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᐞ"), bstack1ll1_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧᐟ"))).lower()
      if percy != bstack1ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧᐠ"):
        return False
      self.bstack1l1ll11111_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᐡ").format(e))
  def bstack1llllll1l1l_opy_(self):
    try:
      bstack1llllll1l1l_opy_ = str(self.config.get(bstack1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᐢ"), bstack1ll1_opy_ (u"ࠥࡥࡺࡺ࡯ࠣᐣ"))).lower()
      return bstack1llllll1l1l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾࠦࡣࡢࡲࡷࡹࡷ࡫ࠠ࡮ࡱࡧࡩ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᐤ").format(e))
  def init(self, bstack1lll1ll1l1_opy_, config, logger):
    self.bstack1lll1ll1l1_opy_ = bstack1lll1ll1l1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111111111l_opy_():
      return
    self.bstack1lllllll111_opy_ = config.get(bstack1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᐥ"), {})
    self.bstack111111lll1_opy_ = config.get(bstack1ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᐦ"), bstack1ll1_opy_ (u"ࠢࡢࡷࡷࡳࠧᐧ"))
    try:
      bstack11111111ll_opy_, bstack1llllll1ll1_opy_ = self.bstack1111l11ll1_opy_()
      bstack1111l11lll_opy_, bstack11111ll1ll_opy_ = self.bstack111111ll1l_opy_(bstack11111111ll_opy_, bstack1llllll1ll1_opy_)
      if bstack11111ll1ll_opy_:
        self.binary_path = bstack1111l11lll_opy_
        thread = Thread(target=self.bstack1111111l1l_opy_)
        thread.start()
      else:
        self.bstack11111l111l_opy_ = True
        self.logger.error(bstack1ll1_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦࡦࡰࡷࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤ࡚ࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡐࡦࡴࡦࡽࠧᐨ").format(bstack1111l11lll_opy_))
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᐩ").format(e))
  def bstack11111ll1l1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1ll1_opy_ (u"ࠪࡰࡴ࡭ࠧᐪ"), bstack1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡰࡴ࡭ࠧᐫ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1ll1_opy_ (u"ࠧࡖࡵࡴࡪ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࡵࠣࡥࡹࠦࡻࡾࠤᐬ").format(logfile))
      self.bstack111111ll11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࠢࡳࡥࡹ࡮ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᐭ").format(e))
  def bstack1111111l1l_opy_(self):
    bstack11111ll111_opy_ = self.bstack11111l1111_opy_()
    if bstack11111ll111_opy_ == None:
      self.bstack11111l111l_opy_ = True
      self.logger.error(bstack1ll1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠥᐮ"))
      return False
    command_args = [bstack1ll1_opy_ (u"ࠣࡣࡳࡴ࠿࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠤᐯ") if self.bstack1lll1ll1l1_opy_ else bstack1ll1_opy_ (u"ࠩࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹ࠭ᐰ")]
    bstack11111111l1_opy_ = self.bstack1111111111_opy_()
    if bstack11111111l1_opy_ != None:
      command_args.append(bstack1ll1_opy_ (u"ࠥ࠱ࡨࠦࡻࡾࠤᐱ").format(bstack11111111l1_opy_))
    env = os.environ.copy()
    env[bstack1ll1_opy_ (u"ࠦࡕࡋࡒࡄ࡛ࡢࡘࡔࡑࡅࡏࠤᐲ")] = bstack11111ll111_opy_
    bstack111111l11l_opy_ = [self.binary_path]
    self.bstack11111ll1l1_opy_()
    self.bstack11111l11ll_opy_ = self.bstack11111l1lll_opy_(bstack111111l11l_opy_ + command_args, env)
    self.logger.debug(bstack1ll1_opy_ (u"࡙ࠧࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠨᐳ"))
    bstack1111111ll1_opy_ = 0
    while self.bstack11111l11ll_opy_.poll() == None:
      bstack1111l1111l_opy_ = self.bstack1lllllll1ll_opy_()
      if bstack1111l1111l_opy_:
        self.logger.debug(bstack1ll1_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠤᐴ"))
        self.bstack11111ll11l_opy_ = True
        return True
      bstack1111111ll1_opy_ += 1
      self.logger.debug(bstack1ll1_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡒࡦࡶࡵࡽࠥ࠳ࠠࡼࡿࠥᐵ").format(bstack1111111ll1_opy_))
      time.sleep(2)
    self.logger.error(bstack1ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡉࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࠤࡦࡺࡴࡦ࡯ࡳࡸࡸࠨᐶ").format(bstack1111111ll1_opy_))
    self.bstack11111l111l_opy_ = True
    return False
  def bstack1lllllll1ll_opy_(self, bstack1111111ll1_opy_ = 0):
    try:
      if bstack1111111ll1_opy_ > 10:
        return False
      bstack11111llll1_opy_ = os.environ.get(bstack1ll1_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡕࡈࡖ࡛ࡋࡒࡠࡃࡇࡈࡗࡋࡓࡔࠩᐷ"), bstack1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠵࠴࠵࠻ࠫᐸ"))
      bstack11111lllll_opy_ = bstack11111llll1_opy_ + bstack11l11l1ll1_opy_
      response = requests.get(bstack11111lllll_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack11111l1111_opy_(self):
    bstack1llllllll1l_opy_ = bstack1ll1_opy_ (u"ࠫࡦࡶࡰࠨᐹ") if self.bstack1lll1ll1l1_opy_ else bstack1ll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᐺ")
    bstack11l11111l1_opy_ = bstack1ll1_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠧᐻ").format(self.config[bstack1ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᐼ")], bstack1llllllll1l_opy_)
    uri = bstack1l1l11l11l_opy_(bstack11l11111l1_opy_)
    try:
      response = bstack1l1l11llll_opy_(bstack1ll1_opy_ (u"ࠨࡉࡈࡘࠬᐽ"), uri, {}, {bstack1ll1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᐾ"): (self.config[bstack1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᐿ")], self.config[bstack1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᑀ")])})
      if response.status_code == 200:
        bstack1llllllllll_opy_ = response.json()
        if bstack1ll1_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦᑁ") in bstack1llllllllll_opy_:
          return bstack1llllllllll_opy_[bstack1ll1_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᑂ")]
        else:
          raise bstack1ll1_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧᑃ").format(bstack1llllllllll_opy_)
      else:
        raise bstack1ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣᑄ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥᑅ").format(e))
  def bstack1111111111_opy_(self):
    bstack1111l11l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨᑆ"))
    try:
      if bstack1ll1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᑇ") not in self.bstack1lllllll111_opy_:
        self.bstack1lllllll111_opy_[bstack1ll1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᑈ")] = 2
      with open(bstack1111l11l1l_opy_, bstack1ll1_opy_ (u"࠭ࡷࠨᑉ")) as fp:
        json.dump(self.bstack1lllllll111_opy_, fp)
      return bstack1111l11l1l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᑊ").format(e))
  def bstack11111l1lll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11111l1ll1_opy_ == bstack1ll1_opy_ (u"ࠨࡹ࡬ࡲࠬᑋ"):
        bstack1lllllll11l_opy_ = [bstack1ll1_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧࠪᑌ"), bstack1ll1_opy_ (u"ࠪ࠳ࡨ࠭ᑍ")]
        cmd = bstack1lllllll11l_opy_ + cmd
      cmd = bstack1ll1_opy_ (u"ࠫࠥ࠭ᑎ").join(cmd)
      self.logger.debug(bstack1ll1_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤᑏ").format(cmd))
      with open(self.bstack111111ll11_opy_, bstack1ll1_opy_ (u"ࠨࡡࠣᑐ")) as bstack1llllllll11_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llllllll11_opy_, text=True, stderr=bstack1llllllll11_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11111l111l_opy_ = True
      self.logger.error(bstack1ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᑑ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11111ll11l_opy_:
        self.logger.info(bstack1ll1_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤᑒ"))
        cmd = [self.binary_path, bstack1ll1_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧᑓ")]
        self.bstack11111l1lll_opy_(cmd)
        self.bstack11111ll11l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᑔ").format(cmd, e))
  def bstack1l11111l1_opy_(self):
    if not self.bstack1l1ll11111_opy_:
      return
    try:
      bstack11111l11l1_opy_ = 0
      while not self.bstack11111ll11l_opy_ and bstack11111l11l1_opy_ < self.bstack1llllll1lll_opy_:
        if self.bstack11111l111l_opy_:
          self.logger.info(bstack1ll1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤᑕ"))
          return
        time.sleep(1)
        bstack11111l11l1_opy_ += 1
      os.environ[bstack1ll1_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫᑖ")] = str(self.bstack1111l11111_opy_())
      self.logger.info(bstack1ll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠢᑗ"))
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᑘ").format(e))
  def bstack1111l11111_opy_(self):
    if self.bstack1lll1ll1l1_opy_:
      return
    try:
      bstack1111l1l111_opy_ = [platform[bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᑙ")].lower() for platform in self.config.get(bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᑚ"), [])]
      bstack1111l11l11_opy_ = sys.maxsize
      bstack111111llll_opy_ = bstack1ll1_opy_ (u"ࠪࠫᑛ")
      for browser in bstack1111l1l111_opy_:
        if browser in self.bstack111111l111_opy_:
          bstack11111lll11_opy_ = self.bstack111111l111_opy_[browser]
        if bstack11111lll11_opy_ < bstack1111l11l11_opy_:
          bstack1111l11l11_opy_ = bstack11111lll11_opy_
          bstack111111llll_opy_ = browser
      return bstack111111llll_opy_
    except Exception as e:
      self.logger.error(bstack1ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᑜ").format(e))