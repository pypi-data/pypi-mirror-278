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
from uuid import uuid4
from bstack_utils.helper import bstack1ll11l1l11_opy_, bstack111l11llll_opy_
from bstack_utils.bstack1ll11llll_opy_ import bstack1llll1lll11_opy_
class bstack11lllllll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111ll1ll_opy_=None, framework=None, tags=[], scope=[], bstack1lll1ll1111_opy_=None, bstack1lll1llll11_opy_=True, bstack1lll1l1ll11_opy_=None, bstack1llll1l11l_opy_=None, result=None, duration=None, bstack11lll1l11l_opy_=None, meta={}):
        self.bstack11lll1l11l_opy_ = bstack11lll1l11l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll1llll11_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111ll1ll_opy_ = bstack1l111ll1ll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll1ll1111_opy_ = bstack1lll1ll1111_opy_
        self.bstack1lll1l1ll11_opy_ = bstack1lll1l1ll11_opy_
        self.bstack1llll1l11l_opy_ = bstack1llll1l11l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l111l1ll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1lll1ll1l1l_opy_(self):
        bstack1lll1l1l1ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᓬ"): bstack1lll1l1l1ll_opy_,
            bstack1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᓭ"): bstack1lll1l1l1ll_opy_,
            bstack1ll1_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᓮ"): bstack1lll1l1l1ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll1_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧᓯ") + key)
            setattr(self, key, val)
    def bstack1lll1lll1l1_opy_(self):
        return {
            bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᓰ"): self.name,
            bstack1ll1_opy_ (u"࠭ࡢࡰࡦࡼࠫᓱ"): {
                bstack1ll1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᓲ"): bstack1ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᓳ"),
                bstack1ll1_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᓴ"): self.code
            },
            bstack1ll1_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᓵ"): self.scope,
            bstack1ll1_opy_ (u"ࠫࡹࡧࡧࡴࠩᓶ"): self.tags,
            bstack1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᓷ"): self.framework,
            bstack1ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᓸ"): self.bstack1l111ll1ll_opy_
        }
    def bstack1lll1ll111l_opy_(self):
        return {
         bstack1ll1_opy_ (u"ࠧ࡮ࡧࡷࡥࠬᓹ"): self.meta
        }
    def bstack1lll1ll11ll_opy_(self):
        return {
            bstack1ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫᓺ"): {
                bstack1ll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ᓻ"): self.bstack1lll1ll1111_opy_
            }
        }
    def bstack1lll1ll1ll1_opy_(self, bstack1lll1l1lll1_opy_, details):
        step = next(filter(lambda st: st[bstack1ll1_opy_ (u"ࠪ࡭ࡩ࠭ᓼ")] == bstack1lll1l1lll1_opy_, self.meta[bstack1ll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᓽ")]), None)
        step.update(details)
    def bstack1lll1lll1ll_opy_(self, bstack1lll1l1lll1_opy_):
        step = next(filter(lambda st: st[bstack1ll1_opy_ (u"ࠬ࡯ࡤࠨᓾ")] == bstack1lll1l1lll1_opy_, self.meta[bstack1ll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓿ")]), None)
        step.update({
            bstack1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᔀ"): bstack1ll11l1l11_opy_()
        })
    def bstack1l111l1111_opy_(self, bstack1lll1l1lll1_opy_, result, duration=None):
        bstack1lll1l1ll11_opy_ = bstack1ll11l1l11_opy_()
        if bstack1lll1l1lll1_opy_ is not None and self.meta.get(bstack1ll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᔁ")):
            step = next(filter(lambda st: st[bstack1ll1_opy_ (u"ࠩ࡬ࡨࠬᔂ")] == bstack1lll1l1lll1_opy_, self.meta[bstack1ll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᔃ")]), None)
            step.update({
                bstack1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᔄ"): bstack1lll1l1ll11_opy_,
                bstack1ll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᔅ"): duration if duration else bstack111l11llll_opy_(step[bstack1ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᔆ")], bstack1lll1l1ll11_opy_),
                bstack1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᔇ"): result.result,
                bstack1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᔈ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll1l1l1l1_opy_):
        if self.meta.get(bstack1ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᔉ")):
            self.meta[bstack1ll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᔊ")].append(bstack1lll1l1l1l1_opy_)
        else:
            self.meta[bstack1ll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᔋ")] = [ bstack1lll1l1l1l1_opy_ ]
    def bstack1lll1lll111_opy_(self):
        return {
            bstack1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᔌ"): self.bstack1l111l1ll1_opy_(),
            **self.bstack1lll1lll1l1_opy_(),
            **self.bstack1lll1ll1l1l_opy_(),
            **self.bstack1lll1ll111l_opy_()
        }
    def bstack1lll1ll1l11_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᔍ"): self.bstack1lll1l1ll11_opy_,
            bstack1ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᔎ"): self.duration,
            bstack1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᔏ"): self.result.result
        }
        if data[bstack1ll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᔐ")] == bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᔑ"):
            data[bstack1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᔒ")] = self.result.bstack11ll11ll1l_opy_()
            data[bstack1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᔓ")] = [{bstack1ll1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᔔ"): self.result.bstack111l11ll11_opy_()}]
        return data
    def bstack1lll1l1llll_opy_(self):
        return {
            bstack1ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᔕ"): self.bstack1l111l1ll1_opy_(),
            **self.bstack1lll1lll1l1_opy_(),
            **self.bstack1lll1ll1l1l_opy_(),
            **self.bstack1lll1ll1l11_opy_(),
            **self.bstack1lll1ll111l_opy_()
        }
    def bstack1l111l111l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll1_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩᔖ") in event:
            return self.bstack1lll1lll111_opy_()
        elif bstack1ll1_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᔗ") in event:
            return self.bstack1lll1l1llll_opy_()
    def bstack11lllll1l1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1lll1l1ll11_opy_ = time if time else bstack1ll11l1l11_opy_()
        self.duration = duration if duration else bstack111l11llll_opy_(self.bstack1l111ll1ll_opy_, self.bstack1lll1l1ll11_opy_)
        if result:
            self.result = result
class bstack1l1111l1l1_opy_(bstack11lllllll1_opy_):
    def __init__(self, hooks=[], bstack11lll1l1l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11lll1l1l1_opy_ = bstack11lll1l1l1_opy_
        super().__init__(*args, **kwargs, bstack1llll1l11l_opy_=bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࠨᔘ"))
    @classmethod
    def bstack1lll1ll11l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1_opy_ (u"ࠫ࡮ࡪࠧᔙ"): id(step),
                bstack1ll1_opy_ (u"ࠬࡺࡥࡹࡶࠪᔚ"): step.name,
                bstack1ll1_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᔛ"): step.keyword,
            })
        return bstack1l1111l1l1_opy_(
            **kwargs,
            meta={
                bstack1ll1_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᔜ"): {
                    bstack1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᔝ"): feature.name,
                    bstack1ll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᔞ"): feature.filename,
                    bstack1ll1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᔟ"): feature.description
                },
                bstack1ll1_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ᔠ"): {
                    bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᔡ"): scenario.name
                },
                bstack1ll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᔢ"): steps,
                bstack1ll1_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᔣ"): bstack1llll1lll11_opy_(test)
            }
        )
    def bstack1lll1l1ll1l_opy_(self):
        return {
            bstack1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᔤ"): self.hooks
        }
    def bstack1lll1lll11l_opy_(self):
        if self.bstack11lll1l1l1_opy_:
            return {
                bstack1ll1_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᔥ"): self.bstack11lll1l1l1_opy_
            }
        return {}
    def bstack1lll1l1llll_opy_(self):
        return {
            **super().bstack1lll1l1llll_opy_(),
            **self.bstack1lll1l1ll1l_opy_()
        }
    def bstack1lll1lll111_opy_(self):
        return {
            **super().bstack1lll1lll111_opy_(),
            **self.bstack1lll1lll11l_opy_()
        }
    def bstack11lllll1l1_opy_(self):
        return bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᔦ")
class bstack11lll1ll1l_opy_(bstack11lllllll1_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1llll1l11l_opy_=bstack1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᔧ"))
    def bstack11lll11111_opy_(self):
        return self.hook_type
    def bstack1lll1ll1lll_opy_(self):
        return {
            bstack1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᔨ"): self.hook_type
        }
    def bstack1lll1l1llll_opy_(self):
        return {
            **super().bstack1lll1l1llll_opy_(),
            **self.bstack1lll1ll1lll_opy_()
        }
    def bstack1lll1lll111_opy_(self):
        return {
            **super().bstack1lll1lll111_opy_(),
            **self.bstack1lll1ll1lll_opy_()
        }
    def bstack11lllll1l1_opy_(self):
        return bstack1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨᔩ")