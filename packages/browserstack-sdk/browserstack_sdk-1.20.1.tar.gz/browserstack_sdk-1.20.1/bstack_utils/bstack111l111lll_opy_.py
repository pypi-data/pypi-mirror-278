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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111l1lll1l_opy_
from browserstack_sdk.bstack1l1ll11l1l_opy_ import bstack1l1111l11_opy_
def _111l111111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111l111ll1_opy_:
    def __init__(self, handler):
        self._111l1111l1_opy_ = {}
        self._111l111l1l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1111l11_opy_.version()
        if bstack111l1lll1l_opy_(pytest_version, bstack1ll1_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢፖ")) >= 0:
            self._111l1111l1_opy_[bstack1ll1_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬፗ")] = Module._register_setup_function_fixture
            self._111l1111l1_opy_[bstack1ll1_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫፘ")] = Module._register_setup_module_fixture
            self._111l1111l1_opy_[bstack1ll1_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫፙ")] = Class._register_setup_class_fixture
            self._111l1111l1_opy_[bstack1ll1_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ፚ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111l11l1l1_opy_(bstack1ll1_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ፛"))
            Module._register_setup_module_fixture = self.bstack111l11l1l1_opy_(bstack1ll1_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ፜"))
            Class._register_setup_class_fixture = self.bstack111l11l1l1_opy_(bstack1ll1_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ፝"))
            Class._register_setup_method_fixture = self.bstack111l11l1l1_opy_(bstack1ll1_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ፞"))
        else:
            self._111l1111l1_opy_[bstack1ll1_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭፟")] = Module._inject_setup_function_fixture
            self._111l1111l1_opy_[bstack1ll1_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ፠")] = Module._inject_setup_module_fixture
            self._111l1111l1_opy_[bstack1ll1_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ፡")] = Class._inject_setup_class_fixture
            self._111l1111l1_opy_[bstack1ll1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ።")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111l11l1l1_opy_(bstack1ll1_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ፣"))
            Module._inject_setup_module_fixture = self.bstack111l11l1l1_opy_(bstack1ll1_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ፤"))
            Class._inject_setup_class_fixture = self.bstack111l11l1l1_opy_(bstack1ll1_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ፥"))
            Class._inject_setup_method_fixture = self.bstack111l11l1l1_opy_(bstack1ll1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ፦"))
    def bstack111l11111l_opy_(self, bstack1111llll11_opy_, hook_type):
        meth = getattr(bstack1111llll11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111l111l1l_opy_[hook_type] = meth
            setattr(bstack1111llll11_opy_, hook_type, self.bstack111l11l111_opy_(hook_type))
    def bstack1111llllll_opy_(self, instance, bstack1111llll1l_opy_):
        if bstack1111llll1l_opy_ == bstack1ll1_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ፧"):
            self.bstack111l11111l_opy_(instance.obj, bstack1ll1_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨ፨"))
            self.bstack111l11111l_opy_(instance.obj, bstack1ll1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥ፩"))
        if bstack1111llll1l_opy_ == bstack1ll1_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ፪"):
            self.bstack111l11111l_opy_(instance.obj, bstack1ll1_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢ፫"))
            self.bstack111l11111l_opy_(instance.obj, bstack1ll1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦ፬"))
        if bstack1111llll1l_opy_ == bstack1ll1_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥ፭"):
            self.bstack111l11111l_opy_(instance.obj, bstack1ll1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤ፮"))
            self.bstack111l11111l_opy_(instance.obj, bstack1ll1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨ፯"))
        if bstack1111llll1l_opy_ == bstack1ll1_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ፰"):
            self.bstack111l11111l_opy_(instance.obj, bstack1ll1_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨ፱"))
            self.bstack111l11111l_opy_(instance.obj, bstack1ll1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥ፲"))
    @staticmethod
    def bstack111l11l11l_opy_(hook_type, func, args):
        if hook_type in [bstack1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ፳"), bstack1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ፴")]:
            _111l111111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111l11l111_opy_(self, hook_type):
        def bstack111l1111ll_opy_(arg=None):
            self.handler(hook_type, bstack1ll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ፵"))
            result = None
            exception = None
            try:
                self.bstack111l11l11l_opy_(hook_type, self._111l111l1l_opy_[hook_type], (arg,))
                result = Result(result=bstack1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ፶"))
            except Exception as e:
                result = Result(result=bstack1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭፷"), exception=e)
                self.handler(hook_type, bstack1ll1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭፸"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ፹"), result)
        def bstack111l111l11_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ፺"))
            result = None
            exception = None
            try:
                self.bstack111l11l11l_opy_(hook_type, self._111l111l1l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ፻"))
            except Exception as e:
                result = Result(result=bstack1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ፼"), exception=e)
                self.handler(hook_type, bstack1ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ፽"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ፾"), result)
        if hook_type in [bstack1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭፿"), bstack1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᎀ")]:
            return bstack111l111l11_opy_
        return bstack111l1111ll_opy_
    def bstack111l11l1l1_opy_(self, bstack1111llll1l_opy_):
        def bstack1111lllll1_opy_(this, *args, **kwargs):
            self.bstack1111llllll_opy_(this, bstack1111llll1l_opy_)
            self._111l1111l1_opy_[bstack1111llll1l_opy_](this, *args, **kwargs)
        return bstack1111lllll1_opy_