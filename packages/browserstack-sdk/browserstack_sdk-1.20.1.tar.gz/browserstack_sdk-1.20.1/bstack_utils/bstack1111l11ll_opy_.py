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
class bstack11l1l1l111_opy_(object):
  bstack1l11l11l1_opy_ = os.path.join(os.path.expanduser(bstack1ll1_opy_ (u"ࠪࢂࠬ໿")), bstack1ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫༀ"))
  bstack11l1l1ll11_opy_ = os.path.join(bstack1l11l11l1_opy_, bstack1ll1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬ༁"))
  bstack11l1l1l11l_opy_ = None
  perform_scan = None
  bstack111lll111_opy_ = None
  bstack1llll1ll1l_opy_ = None
  bstack11l1ll111l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll1_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨ༂")):
      cls.instance = super(bstack11l1l1l111_opy_, cls).__new__(cls)
      cls.instance.bstack11l1l1l1ll_opy_()
    return cls.instance
  def bstack11l1l1l1ll_opy_(self):
    try:
      with open(self.bstack11l1l1ll11_opy_, bstack1ll1_opy_ (u"ࠧࡳࠩ༃")) as bstack1llll1ll1_opy_:
        bstack11l1l1ll1l_opy_ = bstack1llll1ll1_opy_.read()
        data = json.loads(bstack11l1l1ll1l_opy_)
        if bstack1ll1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ༄") in data:
          self.bstack11ll111l1l_opy_(data[bstack1ll1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ༅")])
        if bstack1ll1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ༆") in data:
          self.bstack11ll111ll1_opy_(data[bstack1ll1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ༇")])
    except:
      pass
  def bstack11ll111ll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1ll1_opy_ (u"ࠬࡹࡣࡢࡰࠪ༈")]
      self.bstack111lll111_opy_ = scripts[bstack1ll1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪ༉")]
      self.bstack1llll1ll1l_opy_ = scripts[bstack1ll1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫ༊")]
      self.bstack11l1ll111l_opy_ = scripts[bstack1ll1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭་")]
  def bstack11ll111l1l_opy_(self, bstack11l1l1l11l_opy_):
    if bstack11l1l1l11l_opy_ != None and len(bstack11l1l1l11l_opy_) != 0:
      self.bstack11l1l1l11l_opy_ = bstack11l1l1l11l_opy_
  def store(self):
    try:
      with open(self.bstack11l1l1ll11_opy_, bstack1ll1_opy_ (u"ࠩࡺࠫ༌")) as file:
        json.dump({
          bstack1ll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧ།"): self.bstack11l1l1l11l_opy_,
          bstack1ll1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧ༎"): {
            bstack1ll1_opy_ (u"ࠧࡹࡣࡢࡰࠥ༏"): self.perform_scan,
            bstack1ll1_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥ༐"): self.bstack111lll111_opy_,
            bstack1ll1_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦ༑"): self.bstack1llll1ll1l_opy_,
            bstack1ll1_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨ༒"): self.bstack11l1ll111l_opy_
          }
        }, file)
    except:
      pass
  def bstack1l1lllll11_opy_(self, bstack11l1l1l1l1_opy_):
    try:
      return any(command.get(bstack1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ༓")) == bstack11l1l1l1l1_opy_ for command in self.bstack11l1l1l11l_opy_)
    except:
      return False
bstack1111l11ll_opy_ = bstack11l1l1l111_opy_()