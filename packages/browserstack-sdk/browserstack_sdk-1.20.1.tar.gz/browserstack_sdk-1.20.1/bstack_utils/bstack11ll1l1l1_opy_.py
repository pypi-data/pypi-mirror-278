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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l11ll1ll_opy_
import tempfile
import json
bstack1111l1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᎁ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll1_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᎂ"),
      datefmt=bstack1ll1_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ᎃ"),
      stream=sys.stdout
    )
  return logger
def bstack1111ll1l1l_opy_():
  global bstack1111l1llll_opy_
  if os.path.exists(bstack1111l1llll_opy_):
    os.remove(bstack1111l1llll_opy_)
def bstack1l1l1l1l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l1l111l1_opy_(config, log_level):
  bstack1111ll1111_opy_ = log_level
  if bstack1ll1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᎄ") in config and config[bstack1ll1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᎅ")] in bstack11l11ll1ll_opy_:
    bstack1111ll1111_opy_ = bstack11l11ll1ll_opy_[config[bstack1ll1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᎆ")]]
  if config.get(bstack1ll1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᎇ"), False):
    logging.getLogger().setLevel(bstack1111ll1111_opy_)
    return bstack1111ll1111_opy_
  global bstack1111l1llll_opy_
  bstack1l1l1l1l1_opy_()
  bstack1111lll1ll_opy_ = logging.Formatter(
    fmt=bstack1ll1_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᎈ"),
    datefmt=bstack1ll1_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬᎉ")
  )
  bstack1111ll1lll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1111l1llll_opy_)
  file_handler.setFormatter(bstack1111lll1ll_opy_)
  bstack1111ll1lll_opy_.setFormatter(bstack1111lll1ll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111ll1lll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ᎊ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111ll1lll_opy_.setLevel(bstack1111ll1111_opy_)
  logging.getLogger().addHandler(bstack1111ll1lll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1111ll1111_opy_
def bstack1111ll1ll1_opy_(config):
  try:
    bstack1111l1lll1_opy_ = set([
      bstack1ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᎋ"), bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᎌ"), bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᎍ"), bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᎎ"), bstack1ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᎏ"),
      bstack1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭᎐"), bstack1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧ᎑"), bstack1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭᎒"), bstack1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧ᎓")
    ])
    bstack1111ll111l_opy_ = bstack1ll1_opy_ (u"ࠧࠨ᎔")
    with open(bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ᎕")) as bstack1111lll111_opy_:
      bstack1111ll11ll_opy_ = bstack1111lll111_opy_.read()
      bstack1111ll111l_opy_ = re.sub(bstack1ll1_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪ᎖"), bstack1ll1_opy_ (u"ࠪࠫ᎗"), bstack1111ll11ll_opy_, flags=re.M)
      bstack1111ll111l_opy_ = re.sub(
        bstack1ll1_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧ᎘") + bstack1ll1_opy_ (u"ࠬࢂࠧ᎙").join(bstack1111l1lll1_opy_) + bstack1ll1_opy_ (u"࠭ࠩ࠯ࠬࠧࠫ᎚"),
        bstack1ll1_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩ᎛"),
        bstack1111ll111l_opy_, flags=re.M | re.I
      )
    def bstack1111ll11l1_opy_(dic):
      bstack1111lll11l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1111l1lll1_opy_:
          bstack1111lll11l_opy_[key] = bstack1ll1_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ᎜")
        else:
          if isinstance(value, dict):
            bstack1111lll11l_opy_[key] = bstack1111ll11l1_opy_(value)
          else:
            bstack1111lll11l_opy_[key] = value
      return bstack1111lll11l_opy_
    bstack1111lll11l_opy_ = bstack1111ll11l1_opy_(config)
    return {
      bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ᎝"): bstack1111ll111l_opy_,
      bstack1ll1_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭᎞"): json.dumps(bstack1111lll11l_opy_)
    }
  except Exception as e:
    return {}
def bstack111ll1111_opy_(config):
  global bstack1111l1llll_opy_
  try:
    if config.get(bstack1ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭᎟"), False):
      return
    uuid = os.getenv(bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᎠ"))
    if not uuid or uuid == bstack1ll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᎡ"):
      return
    bstack1111lll1l1_opy_ = [bstack1ll1_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪᎢ"), bstack1ll1_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩᎣ"), bstack1ll1_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪᎤ"), bstack1111l1llll_opy_]
    bstack1l1l1l1l1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩᎥ") + uuid + bstack1ll1_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬᎦ"))
    with tarfile.open(output_file, bstack1ll1_opy_ (u"ࠧࡽ࠺ࡨࡼࠥᎧ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1111lll1l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1111ll1ll1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111ll1l11_opy_ = data.encode()
        tarinfo.size = len(bstack1111ll1l11_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111ll1l11_opy_))
    bstack1l11lll1l1_opy_ = MultipartEncoder(
      fields= {
        bstack1ll1_opy_ (u"࠭ࡤࡢࡶࡤࠫᎨ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll1_opy_ (u"ࠧࡳࡤࠪᎩ")), bstack1ll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭Ꭺ")),
        bstack1ll1_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᎫ"): uuid
      }
    )
    response = requests.post(
      bstack1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡺࡶ࡬ࡰࡣࡧ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧᎬ"),
      data=bstack1l11lll1l1_opy_,
      headers={bstack1ll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᎭ"): bstack1l11lll1l1_opy_.content_type},
      auth=(config[bstack1ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᎮ")], config[bstack1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᎯ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭Ꮀ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧᎱ") + str(e))
  finally:
    try:
      bstack1111ll1l1l_opy_()
    except:
      pass