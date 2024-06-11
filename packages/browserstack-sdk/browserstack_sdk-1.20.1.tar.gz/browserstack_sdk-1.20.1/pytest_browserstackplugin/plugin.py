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
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11l111ll1_opy_, bstack1ll1l1llll_opy_, update, bstack1l1ll1l1_opy_,
                                       bstack1l11l1ll1l_opy_, bstack1llll111l_opy_, bstack1llll11l11_opy_, bstack1111l1lll_opy_,
                                       bstack1l1ll1lll_opy_, bstack1lll1111l_opy_, bstack1l1lll11_opy_, bstack1l1ll1111_opy_,
                                       bstack11ll1l111_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l111ll1_opy_)
from browserstack_sdk.bstack1l1ll11l1l_opy_ import bstack1l1111l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11ll1l1l1_opy_
from bstack_utils.capture import bstack1l1111l111_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1ll11ll1_opy_, bstack1l1ll11l_opy_, bstack1l1l11l111_opy_, \
    bstack1l1111l1_opy_
from bstack_utils.helper import bstack1ll1llll1l_opy_, bstack111ll1l111_opy_, bstack1l111lllll_opy_, bstack1l1ll1ll11_opy_, bstack111ll111l1_opy_, bstack1ll11l1l11_opy_, \
    bstack11l111llll_opy_, \
    bstack111ll1ll11_opy_, bstack1lll1ll11l_opy_, bstack1ll1ll1l11_opy_, bstack111ll11111_opy_, bstack1lll11lll_opy_, Notset, \
    bstack1l1l11l1l1_opy_, bstack111l11llll_opy_, bstack111l1l1lll_opy_, Result, bstack11l11l11l1_opy_, bstack111ll11l11_opy_, bstack1l111lll11_opy_, \
    bstack1ll1l111_opy_, bstack11l1l111_opy_, bstack1llll1l1ll_opy_, bstack111l11ll1l_opy_
from bstack_utils.bstack111l111lll_opy_ import bstack111l111ll1_opy_
from bstack_utils.messages import bstack1l1l11ll1_opy_, bstack11ll11ll1_opy_, bstack1lll111l1l_opy_, bstack1l111lll_opy_, bstack1l11lll111_opy_, \
    bstack1l1l111ll1_opy_, bstack111lll11_opy_, bstack111ll111_opy_, bstack1ll111llll_opy_, bstack1l11llll1l_opy_, \
    bstack111ll1l1l_opy_, bstack111ll1lll_opy_
from bstack_utils.proxy import bstack11ll1lll_opy_, bstack1l1l1l11ll_opy_
from bstack_utils.bstack1ll11llll_opy_ import bstack1llll1ll11l_opy_, bstack1llll1ll1l1_opy_, bstack1llll1l11ll_opy_, bstack1llll1l111l_opy_, \
    bstack1llll1lll1l_opy_, bstack1llll1l11l1_opy_, bstack1llll1l1l11_opy_, bstack1ll1l11l1l_opy_, bstack1llll1l1l1l_opy_
from bstack_utils.bstack1lllll1ll_opy_ import bstack1l1llll1l_opy_
from bstack_utils.bstack1l1l111ll_opy_ import bstack11l1lll1l_opy_, bstack1ll11llll1_opy_, bstack1l11llll1_opy_, \
    bstack11111l1ll_opy_, bstack1l1l1ll11l_opy_
from bstack_utils.bstack11lll11l11_opy_ import bstack1l1111l1l1_opy_
from bstack_utils.bstack1ll11ll1ll_opy_ import bstack1lllll1l1_opy_
import bstack_utils.bstack1111ll111_opy_ as bstack1111111l1_opy_
from bstack_utils.bstack1111l11ll_opy_ import bstack1111l11ll_opy_
bstack1l11l11l_opy_ = None
bstack1l111l11_opy_ = None
bstack11111l1l1_opy_ = None
bstack1111ll11_opy_ = None
bstack11lll1lll_opy_ = None
bstack1ll11ll1l_opy_ = None
bstack1l1ll111l_opy_ = None
bstack1ll111lll1_opy_ = None
bstack111l1lll_opy_ = None
bstack1lll1l11ll_opy_ = None
bstack11l111l1_opy_ = None
bstack1ll1l1l111_opy_ = None
bstack1ll11l11_opy_ = None
bstack11l1l1l11_opy_ = bstack1ll1_opy_ (u"ࠩࠪᘓ")
CONFIG = {}
bstack1lll1l1l_opy_ = False
bstack111111l1_opy_ = bstack1ll1_opy_ (u"ࠪࠫᘔ")
bstack1l1lll1l11_opy_ = bstack1ll1_opy_ (u"ࠫࠬᘕ")
bstack1llllll11_opy_ = False
bstack1llll111_opy_ = []
bstack111ll1ll_opy_ = bstack1ll11ll1_opy_
bstack1ll1llll111_opy_ = bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᘖ")
bstack1ll1lll11l1_opy_ = False
bstack1ll11lll1l_opy_ = {}
bstack11llll1l1_opy_ = False
logger = bstack11ll1l1l1_opy_.get_logger(__name__, bstack111ll1ll_opy_)
store = {
    bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᘗ"): []
}
bstack1lll111111l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11llll1lll_opy_ = {}
current_test_uuid = None
def bstack11l1lll1_opy_(page, bstack1l1llll1_opy_):
    try:
        page.evaluate(bstack1ll1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᘘ"),
                      bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬᘙ") + json.dumps(
                          bstack1l1llll1_opy_) + bstack1ll1_opy_ (u"ࠤࢀࢁࠧᘚ"))
    except Exception as e:
        print(bstack1ll1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣᘛ"), e)
def bstack1ll111ll1_opy_(page, message, level):
    try:
        page.evaluate(bstack1ll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᘜ"), bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪᘝ") + json.dumps(
            message) + bstack1ll1_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩᘞ") + json.dumps(level) + bstack1ll1_opy_ (u"ࠧࡾࡿࠪᘟ"))
    except Exception as e:
        print(bstack1ll1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦᘠ"), e)
def pytest_configure(config):
    bstack111l1l1l1_opy_ = Config.bstack1lll11l1l1_opy_()
    config.args = bstack1lllll1l1_opy_.bstack1lll1l111l1_opy_(config.args)
    bstack111l1l1l1_opy_.bstack111l111l_opy_(bstack1llll1l1ll_opy_(config.getoption(bstack1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᘡ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lll11l111l_opy_ = item.config.getoption(bstack1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᘢ"))
    plugins = item.config.getoption(bstack1ll1_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧᘣ"))
    report = outcome.get_result()
    bstack1lll11l11ll_opy_(item, call, report)
    if bstack1ll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥᘤ") not in plugins or bstack1lll11lll_opy_():
        return
    summary = []
    driver = getattr(item, bstack1ll1_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢᘥ"), None)
    page = getattr(item, bstack1ll1_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨᘦ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lll111l111_opy_(item, report, summary, bstack1lll11l111l_opy_)
    if (page is not None):
        bstack1lll111l1ll_opy_(item, report, summary, bstack1lll11l111l_opy_)
def bstack1lll111l111_opy_(item, report, summary, bstack1lll11l111l_opy_):
    if report.when == bstack1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᘧ") and report.skipped:
        bstack1llll1l1l1l_opy_(report)
    if report.when in [bstack1ll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᘨ"), bstack1ll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᘩ")]:
        return
    if not bstack111ll111l1_opy_():
        return
    try:
        if (str(bstack1lll11l111l_opy_).lower() != bstack1ll1_opy_ (u"ࠫࡹࡸࡵࡦࠩᘪ")):
            item._driver.execute_script(
                bstack1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪᘫ") + json.dumps(
                    report.nodeid) + bstack1ll1_opy_ (u"࠭ࡽࡾࠩᘬ"))
        os.environ[bstack1ll1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᘭ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1ll1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣᘮ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᘯ")))
    bstack1lllll11ll_opy_ = bstack1ll1_opy_ (u"ࠥࠦᘰ")
    bstack1llll1l1l1l_opy_(report)
    if not passed:
        try:
            bstack1lllll11ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1ll1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᘱ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lllll11ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1ll1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᘲ")))
        bstack1lllll11ll_opy_ = bstack1ll1_opy_ (u"ࠨࠢᘳ")
        if not passed:
            try:
                bstack1lllll11ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᘴ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lllll11ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬᘵ")
                    + json.dumps(bstack1ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥᘶ"))
                    + bstack1ll1_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᘷ")
                )
            else:
                item._driver.execute_script(
                    bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᘸ")
                    + json.dumps(str(bstack1lllll11ll_opy_))
                    + bstack1ll1_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᘹ")
                )
        except Exception as e:
            summary.append(bstack1ll1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦᘺ").format(e))
def bstack1lll1111l11_opy_(test_name, error_message):
    try:
        bstack1ll1lll1l11_opy_ = []
        bstack1lll1l1ll_opy_ = os.environ.get(bstack1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᘻ"), bstack1ll1_opy_ (u"ࠨ࠲ࠪᘼ"))
        bstack111ll11l_opy_ = {bstack1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᘽ"): test_name, bstack1ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᘾ"): error_message, bstack1ll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᘿ"): bstack1lll1l1ll_opy_}
        bstack1ll1lllll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᙀ"))
        if os.path.exists(bstack1ll1lllll1l_opy_):
            with open(bstack1ll1lllll1l_opy_) as f:
                bstack1ll1lll1l11_opy_ = json.load(f)
        bstack1ll1lll1l11_opy_.append(bstack111ll11l_opy_)
        with open(bstack1ll1lllll1l_opy_, bstack1ll1_opy_ (u"࠭ࡷࠨᙁ")) as f:
            json.dump(bstack1ll1lll1l11_opy_, f)
    except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬᙂ") + str(e))
def bstack1lll111l1ll_opy_(item, report, summary, bstack1lll11l111l_opy_):
    if report.when in [bstack1ll1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᙃ"), bstack1ll1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᙄ")]:
        return
    if (str(bstack1lll11l111l_opy_).lower() != bstack1ll1_opy_ (u"ࠪࡸࡷࡻࡥࠨᙅ")):
        bstack11l1lll1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᙆ")))
    bstack1lllll11ll_opy_ = bstack1ll1_opy_ (u"ࠧࠨᙇ")
    bstack1llll1l1l1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lllll11ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᙈ").format(e)
                )
        try:
            if passed:
                bstack1l1l1ll11l_opy_(getattr(item, bstack1ll1_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᙉ"), None), bstack1ll1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᙊ"))
            else:
                error_message = bstack1ll1_opy_ (u"ࠩࠪᙋ")
                if bstack1lllll11ll_opy_:
                    bstack1ll111ll1_opy_(item._page, str(bstack1lllll11ll_opy_), bstack1ll1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᙌ"))
                    bstack1l1l1ll11l_opy_(getattr(item, bstack1ll1_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᙍ"), None), bstack1ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᙎ"), str(bstack1lllll11ll_opy_))
                    error_message = str(bstack1lllll11ll_opy_)
                else:
                    bstack1l1l1ll11l_opy_(getattr(item, bstack1ll1_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᙏ"), None), bstack1ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᙐ"))
                bstack1lll1111l11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1ll1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧᙑ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1ll1_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᙒ"), default=bstack1ll1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᙓ"), help=bstack1ll1_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᙔ"))
    parser.addoption(bstack1ll1_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᙕ"), default=bstack1ll1_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧᙖ"), help=bstack1ll1_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨᙗ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1ll1_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥᙘ"), action=bstack1ll1_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣᙙ"), default=bstack1ll1_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥᙚ"),
                         help=bstack1ll1_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥᙛ"))
def bstack11lll1l1ll_opy_(log):
    if not (log[bstack1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙜ")] and log[bstack1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᙝ")].strip()):
        return
    active = bstack11llllll1l_opy_()
    log = {
        bstack1ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᙞ"): log[bstack1ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᙟ")],
        bstack1ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᙠ"): bstack1l111lllll_opy_().isoformat() + bstack1ll1_opy_ (u"ࠪ࡞ࠬᙡ"),
        bstack1ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙢ"): log[bstack1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙣ")],
    }
    if active:
        if active[bstack1ll1_opy_ (u"࠭ࡴࡺࡲࡨࠫᙤ")] == bstack1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᙥ"):
            log[bstack1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᙦ")] = active[bstack1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᙧ")]
        elif active[bstack1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨᙨ")] == bstack1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᙩ"):
            log[bstack1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᙪ")] = active[bstack1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᙫ")]
    bstack1lllll1l1_opy_.bstack111ll1111_opy_([log])
def bstack11llllll1l_opy_():
    if len(store[bstack1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᙬ")]) > 0 and store[bstack1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ᙭")][-1]:
        return {
            bstack1ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ᙮"): bstack1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᙯ"),
            bstack1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᙰ"): store[bstack1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᙱ")][-1]
        }
    if store.get(bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᙲ"), None):
        return {
            bstack1ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬᙳ"): bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᙴ"),
            bstack1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᙵ"): store[bstack1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᙶ")]
        }
    return None
bstack11lllll11l_opy_ = bstack1l1111l111_opy_(bstack11lll1l1ll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1ll1lll11l1_opy_
        item._1lll111llll_opy_ = True
        bstack1lll1l111l_opy_ = bstack1111111l1_opy_.bstack1l11l1lll_opy_(CONFIG, bstack111ll1ll11_opy_(item.own_markers))
        item._a11y_test_case = bstack1lll1l111l_opy_
        if bstack1ll1lll11l1_opy_:
            driver = getattr(item, bstack1ll1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᙷ"), None)
            item._a11y_started = bstack1111111l1_opy_.bstack1111lll1l_opy_(driver, bstack1lll1l111l_opy_)
        if not bstack1lllll1l1_opy_.on() or bstack1ll1llll111_opy_ != bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᙸ"):
            return
        global current_test_uuid, bstack11lllll11l_opy_
        bstack11lllll11l_opy_.start()
        bstack1l111111l1_opy_ = {
            bstack1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᙹ"): uuid4().__str__(),
            bstack1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᙺ"): bstack1l111lllll_opy_().isoformat() + bstack1ll1_opy_ (u"ࠨ࡜ࠪᙻ")
        }
        current_test_uuid = bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᙼ")]
        store[bstack1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᙽ")] = bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᙾ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11llll1lll_opy_[item.nodeid] = {**_11llll1lll_opy_[item.nodeid], **bstack1l111111l1_opy_}
        bstack1ll1lllllll_opy_(item, _11llll1lll_opy_[item.nodeid], bstack1ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᙿ"))
    except Exception as err:
        print(bstack1ll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨ "), str(err))
def pytest_runtest_setup(item):
    global bstack1lll111111l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111ll11111_opy_():
        atexit.register(bstack11llll11_opy_)
        if not bstack1lll111111l_opy_:
            try:
                bstack1ll1lll1lll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111l11ll1l_opy_():
                    bstack1ll1lll1lll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1lll1lll_opy_:
                    signal.signal(s, bstack1lll1111ll1_opy_)
                bstack1lll111111l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩ࡬࡯ࡳࡵࡧࡵࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࡸࡀࠠࠣᚁ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llll1ll11l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᚂ")
    try:
        if not bstack1lllll1l1_opy_.on():
            return
        bstack11lllll11l_opy_.start()
        uuid = uuid4().__str__()
        bstack1l111111l1_opy_ = {
            bstack1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᚃ"): uuid,
            bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᚄ"): bstack1l111lllll_opy_().isoformat() + bstack1ll1_opy_ (u"ࠫ࡟࠭ᚅ"),
            bstack1ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪᚆ"): bstack1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᚇ"),
            bstack1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᚈ"): bstack1ll1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᚉ"),
            bstack1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᚊ"): bstack1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᚋ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᚌ")] = item
        store[bstack1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᚍ")] = [uuid]
        if not _11llll1lll_opy_.get(item.nodeid, None):
            _11llll1lll_opy_[item.nodeid] = {bstack1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᚎ"): [], bstack1ll1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᚏ"): []}
        _11llll1lll_opy_[item.nodeid][bstack1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᚐ")].append(bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᚑ")])
        _11llll1lll_opy_[item.nodeid + bstack1ll1_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪᚒ")] = bstack1l111111l1_opy_
        bstack1lll11111ll_opy_(item, bstack1l111111l1_opy_, bstack1ll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᚓ"))
    except Exception as err:
        print(bstack1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨᚔ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1ll11lll1l_opy_
        if CONFIG.get(bstack1ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᚕ"), False):
            if CONFIG.get(bstack1ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᚖ"), bstack1ll1_opy_ (u"ࠣࡣࡸࡸࡴࠨᚗ")) == bstack1ll1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᚘ"):
                bstack1ll1lll1l1l_opy_ = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᚙ"), None)
                bstack1lll1llll1_opy_ = bstack1ll1lll1l1l_opy_ + bstack1ll1_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᚚ")
                driver = getattr(item, bstack1ll1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭᚛"), None)
                PercySDK.screenshot(driver, bstack1lll1llll1_opy_)
        if getattr(item, bstack1ll1_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭᚜"), False):
            bstack1l1111l11_opy_.bstack1l1l11l1l_opy_(getattr(item, bstack1ll1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ᚝"), None), bstack1ll11lll1l_opy_, logger, item)
        if not bstack1lllll1l1_opy_.on():
            return
        bstack1l111111l1_opy_ = {
            bstack1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᚞"): uuid4().__str__(),
            bstack1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭᚟"): bstack1l111lllll_opy_().isoformat() + bstack1ll1_opy_ (u"ࠪ࡞ࠬᚠ"),
            bstack1ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩᚡ"): bstack1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᚢ"),
            bstack1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᚣ"): bstack1ll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᚤ"),
            bstack1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᚥ"): bstack1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᚦ")
        }
        _11llll1lll_opy_[item.nodeid + bstack1ll1_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᚧ")] = bstack1l111111l1_opy_
        bstack1lll11111ll_opy_(item, bstack1l111111l1_opy_, bstack1ll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᚨ"))
    except Exception as err:
        print(bstack1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫᚩ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1lllll1l1_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1llll1l111l_opy_(fixturedef.argname):
        store[bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬᚪ")] = request.node
    elif bstack1llll1lll1l_opy_(fixturedef.argname):
        store[bstack1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬᚫ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᚬ"): fixturedef.argname,
            bstack1ll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᚭ"): bstack11l111llll_opy_(outcome),
            bstack1ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᚮ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᚯ")]
        if not _11llll1lll_opy_.get(current_test_item.nodeid, None):
            _11llll1lll_opy_[current_test_item.nodeid] = {bstack1ll1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᚰ"): []}
        _11llll1lll_opy_[current_test_item.nodeid][bstack1ll1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᚱ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᚲ"), str(err))
if bstack1lll11lll_opy_() and bstack1lllll1l1_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11llll1lll_opy_[request.node.nodeid][bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᚳ")].bstack1lll1lll1ll_opy_(id(step))
        except Exception as err:
            print(bstack1ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧᚴ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11llll1lll_opy_[request.node.nodeid][bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᚵ")].bstack1l111l1111_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᚶ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11lll11l11_opy_: bstack1l1111l1l1_opy_ = _11llll1lll_opy_[request.node.nodeid][bstack1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᚷ")]
            bstack11lll11l11_opy_.bstack1l111l1111_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1ll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᚸ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll1llll111_opy_
        try:
            if not bstack1lllll1l1_opy_.on() or bstack1ll1llll111_opy_ != bstack1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᚹ"):
                return
            global bstack11lllll11l_opy_
            bstack11lllll11l_opy_.start()
            driver = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᚺ"), None)
            if not _11llll1lll_opy_.get(request.node.nodeid, None):
                _11llll1lll_opy_[request.node.nodeid] = {}
            bstack11lll11l11_opy_ = bstack1l1111l1l1_opy_.bstack1lll1ll11l1_opy_(
                scenario, feature, request.node,
                name=bstack1llll1l11l1_opy_(request.node, scenario),
                bstack1l111ll1ll_opy_=bstack1ll11l1l11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1ll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᚻ"),
                tags=bstack1llll1l1l11_opy_(feature, scenario),
                bstack11lll1l1l1_opy_=bstack1lllll1l1_opy_.bstack11lll11ll1_opy_(driver) if driver and driver.session_id else {}
            )
            _11llll1lll_opy_[request.node.nodeid][bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᚼ")] = bstack11lll11l11_opy_
            bstack1lll111l1l1_opy_(bstack11lll11l11_opy_.uuid)
            bstack1lllll1l1_opy_.bstack1l111l1l1l_opy_(bstack1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᚽ"), bstack11lll11l11_opy_)
        except Exception as err:
            print(bstack1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧᚾ"), str(err))
def bstack1ll1llll1l1_opy_(bstack1lll1111lll_opy_):
    if bstack1lll1111lll_opy_ in store[bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᚿ")]:
        store[bstack1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᛀ")].remove(bstack1lll1111lll_opy_)
def bstack1lll111l1l1_opy_(bstack1lll11l1111_opy_):
    store[bstack1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᛁ")] = bstack1lll11l1111_opy_
    threading.current_thread().current_test_uuid = bstack1lll11l1111_opy_
@bstack1lllll1l1_opy_.bstack1lll11ll1ll_opy_
def bstack1lll11l11ll_opy_(item, call, report):
    global bstack1ll1llll111_opy_
    bstack1l1l1l1lll_opy_ = bstack1ll11l1l11_opy_()
    if hasattr(report, bstack1ll1_opy_ (u"ࠩࡶࡸࡴࡶࠧᛂ")):
        bstack1l1l1l1lll_opy_ = bstack11l11l11l1_opy_(report.stop)
    elif hasattr(report, bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩᛃ")):
        bstack1l1l1l1lll_opy_ = bstack11l11l11l1_opy_(report.start)
    try:
        if getattr(report, bstack1ll1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᛄ"), bstack1ll1_opy_ (u"ࠬ࠭ᛅ")) == bstack1ll1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᛆ"):
            bstack11lllll11l_opy_.reset()
        if getattr(report, bstack1ll1_opy_ (u"ࠧࡸࡪࡨࡲࠬᛇ"), bstack1ll1_opy_ (u"ࠨࠩᛈ")) == bstack1ll1_opy_ (u"ࠩࡦࡥࡱࡲࠧᛉ"):
            if bstack1ll1llll111_opy_ == bstack1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᛊ"):
                _11llll1lll_opy_[item.nodeid][bstack1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᛋ")] = bstack1l1l1l1lll_opy_
                bstack1ll1lllllll_opy_(item, _11llll1lll_opy_[item.nodeid], bstack1ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᛌ"), report, call)
                store[bstack1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᛍ")] = None
            elif bstack1ll1llll111_opy_ == bstack1ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᛎ"):
                bstack11lll11l11_opy_ = _11llll1lll_opy_[item.nodeid][bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᛏ")]
                bstack11lll11l11_opy_.set(hooks=_11llll1lll_opy_[item.nodeid].get(bstack1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᛐ"), []))
                exception, bstack11lll1lll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11lll1lll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1ll1_opy_ (u"ࠪࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠩᛑ"), bstack1ll1_opy_ (u"ࠫࠬᛒ"))]
                bstack11lll11l11_opy_.stop(time=bstack1l1l1l1lll_opy_, result=Result(result=getattr(report, bstack1ll1_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭ᛓ"), bstack1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᛔ")), exception=exception, bstack11lll1lll1_opy_=bstack11lll1lll1_opy_))
                bstack1lllll1l1_opy_.bstack1l111l1l1l_opy_(bstack1ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᛕ"), _11llll1lll_opy_[item.nodeid][bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᛖ")])
        elif getattr(report, bstack1ll1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᛗ"), bstack1ll1_opy_ (u"ࠪࠫᛘ")) in [bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᛙ"), bstack1ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᛚ")]:
            bstack11llll1ll1_opy_ = item.nodeid + bstack1ll1_opy_ (u"࠭࠭ࠨᛛ") + getattr(report, bstack1ll1_opy_ (u"ࠧࡸࡪࡨࡲࠬᛜ"), bstack1ll1_opy_ (u"ࠨࠩᛝ"))
            if getattr(report, bstack1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᛞ"), False):
                hook_type = bstack1ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᛟ") if getattr(report, bstack1ll1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᛠ"), bstack1ll1_opy_ (u"ࠬ࠭ᛡ")) == bstack1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᛢ") else bstack1ll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᛣ")
                _11llll1lll_opy_[bstack11llll1ll1_opy_] = {
                    bstack1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᛤ"): uuid4().__str__(),
                    bstack1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᛥ"): bstack1l1l1l1lll_opy_,
                    bstack1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᛦ"): hook_type
                }
            _11llll1lll_opy_[bstack11llll1ll1_opy_][bstack1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᛧ")] = bstack1l1l1l1lll_opy_
            bstack1ll1llll1l1_opy_(_11llll1lll_opy_[bstack11llll1ll1_opy_][bstack1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᛨ")])
            bstack1lll11111ll_opy_(item, _11llll1lll_opy_[bstack11llll1ll1_opy_], bstack1ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᛩ"), report, call)
            if getattr(report, bstack1ll1_opy_ (u"ࠧࡸࡪࡨࡲࠬᛪ"), bstack1ll1_opy_ (u"ࠨࠩ᛫")) == bstack1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ᛬"):
                if getattr(report, bstack1ll1_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ᛭"), bstack1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᛮ")) == bstack1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᛯ"):
                    bstack1l111111l1_opy_ = {
                        bstack1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᛰ"): uuid4().__str__(),
                        bstack1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᛱ"): bstack1ll11l1l11_opy_(),
                        bstack1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛲ"): bstack1ll11l1l11_opy_()
                    }
                    _11llll1lll_opy_[item.nodeid] = {**_11llll1lll_opy_[item.nodeid], **bstack1l111111l1_opy_}
                    bstack1ll1lllllll_opy_(item, _11llll1lll_opy_[item.nodeid], bstack1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᛳ"))
                    bstack1ll1lllllll_opy_(item, _11llll1lll_opy_[item.nodeid], bstack1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᛴ"), report, call)
    except Exception as err:
        print(bstack1ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩᛵ"), str(err))
def bstack1lll111ll11_opy_(test, bstack1l111111l1_opy_, result=None, call=None, bstack1llll1l11l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11lll11l11_opy_ = {
        bstack1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᛶ"): bstack1l111111l1_opy_[bstack1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᛷ")],
        bstack1ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬᛸ"): bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹ࠭᛹"),
        bstack1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᛺"): test.name,
        bstack1ll1_opy_ (u"ࠪࡦࡴࡪࡹࠨ᛻"): {
            bstack1ll1_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ᛼"): bstack1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ᛽"),
            bstack1ll1_opy_ (u"࠭ࡣࡰࡦࡨࠫ᛾"): inspect.getsource(test.obj)
        },
        bstack1ll1_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ᛿"): test.name,
        bstack1ll1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧᜀ"): test.name,
        bstack1ll1_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᜁ"): bstack1lllll1l1_opy_.bstack1l111ll1l1_opy_(test),
        bstack1ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᜂ"): file_path,
        bstack1ll1_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᜃ"): file_path,
        bstack1ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᜄ"): bstack1ll1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᜅ"),
        bstack1ll1_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᜆ"): file_path,
        bstack1ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᜇ"): bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᜈ")],
        bstack1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᜉ"): bstack1ll1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᜊ"),
        bstack1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᜋ"): {
            bstack1ll1_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᜌ"): test.nodeid
        },
        bstack1ll1_opy_ (u"ࠧࡵࡣࡪࡷࠬᜍ"): bstack111ll1ll11_opy_(test.own_markers)
    }
    if bstack1llll1l11l_opy_ in [bstack1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᜎ"), bstack1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᜏ")]:
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠪࡱࡪࡺࡡࠨᜐ")] = {
            bstack1ll1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᜑ"): bstack1l111111l1_opy_.get(bstack1ll1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᜒ"), [])
        }
    if bstack1llll1l11l_opy_ == bstack1ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᜓ"):
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺ᜔ࠧ")] = bstack1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥ᜕ࠩ")
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᜖")] = bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᜗")]
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᜘")] = bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᜙")]
    if result:
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᜚")] = result.outcome
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ᜛")] = result.duration * 1000
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᜜")] = bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᜝")]
        if result.failed:
            bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ᜞")] = bstack1lllll1l1_opy_.bstack11ll11ll1l_opy_(call.excinfo.typename)
            bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᜟ")] = bstack1lllll1l1_opy_.bstack1lll1l11111_opy_(call.excinfo, result)
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᜠ")] = bstack1l111111l1_opy_[bstack1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᜡ")]
    if outcome:
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᜢ")] = bstack11l111llll_opy_(outcome)
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᜣ")] = 0
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᜤ")] = bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᜥ")]
        if bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᜦ")] == bstack1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᜧ"):
            bstack11lll11l11_opy_[bstack1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᜨ")] = bstack1ll1_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᜩ")  # bstack1ll1llllll1_opy_
            bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᜪ")] = [{bstack1ll1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᜫ"): [bstack1ll1_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᜬ")]}]
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᜭ")] = bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᜮ")]
    return bstack11lll11l11_opy_
def bstack1lll111lll1_opy_(test, bstack1l1111l11l_opy_, bstack1llll1l11l_opy_, result, call, outcome, bstack1lll1111111_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l1111l11l_opy_[bstack1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᜯ")]
    hook_name = bstack1l1111l11l_opy_[bstack1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᜰ")]
    hook_data = {
        bstack1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᜱ"): bstack1l1111l11l_opy_[bstack1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᜲ")],
        bstack1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨᜳ"): bstack1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬᜴ࠩ"),
        bstack1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᜵"): bstack1ll1_opy_ (u"࠭ࡻࡾࠩ᜶").format(bstack1llll1ll1l1_opy_(hook_name)),
        bstack1ll1_opy_ (u"ࠧࡣࡱࡧࡽࠬ᜷"): {
            bstack1ll1_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭᜸"): bstack1ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ᜹"),
            bstack1ll1_opy_ (u"ࠪࡧࡴࡪࡥࠨ᜺"): None
        },
        bstack1ll1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ᜻"): test.name,
        bstack1ll1_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ᜼"): bstack1lllll1l1_opy_.bstack1l111ll1l1_opy_(test, hook_name),
        bstack1ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ᜽"): file_path,
        bstack1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ᜾"): file_path,
        bstack1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᜿"): bstack1ll1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᝀ"),
        bstack1ll1_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᝁ"): file_path,
        bstack1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᝂ"): bstack1l1111l11l_opy_[bstack1ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᝃ")],
        bstack1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᝄ"): bstack1ll1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᝅ") if bstack1ll1llll111_opy_ == bstack1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᝆ") else bstack1ll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᝇ"),
        bstack1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᝈ"): hook_type
    }
    bstack1ll1llll11l_opy_ = bstack11llll11l1_opy_(_11llll1lll_opy_.get(test.nodeid, None))
    if bstack1ll1llll11l_opy_:
        hook_data[bstack1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᝉ")] = bstack1ll1llll11l_opy_
    if result:
        hook_data[bstack1ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᝊ")] = result.outcome
        hook_data[bstack1ll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᝋ")] = result.duration * 1000
        hook_data[bstack1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᝌ")] = bstack1l1111l11l_opy_[bstack1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᝍ")]
        if result.failed:
            hook_data[bstack1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᝎ")] = bstack1lllll1l1_opy_.bstack11ll11ll1l_opy_(call.excinfo.typename)
            hook_data[bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᝏ")] = bstack1lllll1l1_opy_.bstack1lll1l11111_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᝐ")] = bstack11l111llll_opy_(outcome)
        hook_data[bstack1ll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᝑ")] = 100
        hook_data[bstack1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᝒ")] = bstack1l1111l11l_opy_[bstack1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᝓ")]
        if hook_data[bstack1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᝔")] == bstack1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᝕"):
            hook_data[bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ᝖")] = bstack1ll1_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ᝗")  # bstack1ll1llllll1_opy_
            hook_data[bstack1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭᝘")] = [{bstack1ll1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ᝙"): [bstack1ll1_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ᝚")]}]
    if bstack1lll1111111_opy_:
        hook_data[bstack1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᝛")] = bstack1lll1111111_opy_.result
        hook_data[bstack1ll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ᝜")] = bstack111l11llll_opy_(bstack1l1111l11l_opy_[bstack1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᝝")], bstack1l1111l11l_opy_[bstack1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᝞")])
        hook_data[bstack1ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᝟")] = bstack1l1111l11l_opy_[bstack1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᝠ")]
        if hook_data[bstack1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᝡ")] == bstack1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᝢ"):
            hook_data[bstack1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᝣ")] = bstack1lllll1l1_opy_.bstack11ll11ll1l_opy_(bstack1lll1111111_opy_.exception_type)
            hook_data[bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᝤ")] = [{bstack1ll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᝥ"): bstack111l1l1lll_opy_(bstack1lll1111111_opy_.exception)}]
    return hook_data
def bstack1ll1lllllll_opy_(test, bstack1l111111l1_opy_, bstack1llll1l11l_opy_, result=None, call=None, outcome=None):
    bstack11lll11l11_opy_ = bstack1lll111ll11_opy_(test, bstack1l111111l1_opy_, result, call, bstack1llll1l11l_opy_, outcome)
    driver = getattr(test, bstack1ll1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᝦ"), None)
    if bstack1llll1l11l_opy_ == bstack1ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᝧ") and driver:
        bstack11lll11l11_opy_[bstack1ll1_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᝨ")] = bstack1lllll1l1_opy_.bstack11lll11ll1_opy_(driver)
    if bstack1llll1l11l_opy_ == bstack1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᝩ"):
        bstack1llll1l11l_opy_ = bstack1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᝪ")
    bstack1l11111lll_opy_ = {
        bstack1ll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᝫ"): bstack1llll1l11l_opy_,
        bstack1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᝬ"): bstack11lll11l11_opy_
    }
    bstack1lllll1l1_opy_.bstack11llll111l_opy_(bstack1l11111lll_opy_)
def bstack1lll11111ll_opy_(test, bstack1l111111l1_opy_, bstack1llll1l11l_opy_, result=None, call=None, outcome=None, bstack1lll1111111_opy_=None):
    hook_data = bstack1lll111lll1_opy_(test, bstack1l111111l1_opy_, bstack1llll1l11l_opy_, result, call, outcome, bstack1lll1111111_opy_)
    bstack1l11111lll_opy_ = {
        bstack1ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ᝭"): bstack1llll1l11l_opy_,
        bstack1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨᝮ"): hook_data
    }
    bstack1lllll1l1_opy_.bstack11llll111l_opy_(bstack1l11111lll_opy_)
def bstack11llll11l1_opy_(bstack1l111111l1_opy_):
    if not bstack1l111111l1_opy_:
        return None
    if bstack1l111111l1_opy_.get(bstack1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᝯ"), None):
        return getattr(bstack1l111111l1_opy_[bstack1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᝰ")], bstack1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᝱"), None)
    return bstack1l111111l1_opy_.get(bstack1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᝲ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1lllll1l1_opy_.on():
            return
        places = [bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᝳ"), bstack1ll1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ᝴"), bstack1ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ᝵")]
        bstack1l111l11ll_opy_ = []
        for bstack1ll1llll1ll_opy_ in places:
            records = caplog.get_records(bstack1ll1llll1ll_opy_)
            bstack1ll1lllll11_opy_ = bstack1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᝶") if bstack1ll1llll1ll_opy_ == bstack1ll1_opy_ (u"ࠨࡥࡤࡰࡱ࠭᝷") else bstack1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᝸")
            bstack1ll1lll1ll1_opy_ = request.node.nodeid + (bstack1ll1_opy_ (u"ࠪࠫ᝹") if bstack1ll1llll1ll_opy_ == bstack1ll1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ᝺") else bstack1ll1_opy_ (u"ࠬ࠳ࠧ᝻") + bstack1ll1llll1ll_opy_)
            bstack1lll11l1111_opy_ = bstack11llll11l1_opy_(_11llll1lll_opy_.get(bstack1ll1lll1ll1_opy_, None))
            if not bstack1lll11l1111_opy_:
                continue
            for record in records:
                if bstack111ll11l11_opy_(record.message):
                    continue
                bstack1l111l11ll_opy_.append({
                    bstack1ll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ᝼"): bstack111ll1l111_opy_(record.created).isoformat() + bstack1ll1_opy_ (u"࡛ࠧࠩ᝽"),
                    bstack1ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ᝾"): record.levelname,
                    bstack1ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᝿"): record.message,
                    bstack1ll1lllll11_opy_: bstack1lll11l1111_opy_
                })
        if len(bstack1l111l11ll_opy_) > 0:
            bstack1lllll1l1_opy_.bstack111ll1111_opy_(bstack1l111l11ll_opy_)
    except Exception as err:
        print(bstack1ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡨࡵ࡮ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ࠽ࠤࢀࢃࠧក"), str(err))
def bstack1l1lll1ll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11llll1l1_opy_
    bstack1l11lllll1_opy_ = bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨខ"), None) and bstack1ll1llll1l_opy_(
            threading.current_thread(), bstack1ll1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫគ"), None)
    bstack1llllllll1_opy_ = getattr(driver, bstack1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ឃ"), None) != None and getattr(driver, bstack1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧង"), None) == True
    if sequence == bstack1ll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨច") and driver != None:
      if not bstack11llll1l1_opy_ and bstack111ll111l1_opy_() and bstack1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩឆ") in CONFIG and CONFIG[bstack1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪជ")] == True and bstack1111l11ll_opy_.bstack1l1lllll11_opy_(driver_command) and (bstack1llllllll1_opy_ or bstack1l11lllll1_opy_) and not bstack1l111ll1_opy_(args):
        try:
          bstack11llll1l1_opy_ = True
          logger.debug(bstack1ll1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ឈ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1ll1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪញ").format(str(err)))
        bstack11llll1l1_opy_ = False
    if sequence == bstack1ll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬដ"):
        if driver_command == bstack1ll1_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫឋ"):
            bstack1lllll1l1_opy_.bstack1llll111ll_opy_({
                bstack1ll1_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧឌ"): response[bstack1ll1_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨឍ")],
                bstack1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪណ"): store[bstack1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨត")]
            })
def bstack11llll11_opy_():
    global bstack1llll111_opy_
    bstack11ll1l1l1_opy_.bstack1l1l1l1l1_opy_()
    logging.shutdown()
    bstack1lllll1l1_opy_.bstack1l1111llll_opy_()
    for driver in bstack1llll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1111ll1_opy_(*args):
    global bstack1llll111_opy_
    bstack1lllll1l1_opy_.bstack1l1111llll_opy_()
    for driver in bstack1llll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11l11l11l_opy_(self, *args, **kwargs):
    bstack1l1lll11l_opy_ = bstack1l11l11l_opy_(self, *args, **kwargs)
    bstack1lllll1l1_opy_.bstack1l1l1ll11_opy_(self)
    return bstack1l1lll11l_opy_
def bstack11l1ll1l_opy_(framework_name):
    global bstack11l1l1l11_opy_
    global bstack11ll11111_opy_
    bstack11l1l1l11_opy_ = framework_name
    logger.info(bstack111ll1lll_opy_.format(bstack11l1l1l11_opy_.split(bstack1ll1_opy_ (u"ࠬ࠳ࠧថ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack111ll111l1_opy_():
            Service.start = bstack1llll11l11_opy_
            Service.stop = bstack1111l1lll_opy_
            webdriver.Remote.__init__ = bstack1ll11l1ll1_opy_
            webdriver.Remote.get = bstack1lll1ll1ll_opy_
            if not isinstance(os.getenv(bstack1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧទ")), str):
                return
            WebDriver.close = bstack1l1ll1lll_opy_
            WebDriver.quit = bstack1ll1lll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack111ll111l1_opy_() and bstack1lllll1l1_opy_.on():
            webdriver.Remote.__init__ = bstack11l11l11l_opy_
        bstack11ll11111_opy_ = True
    except Exception as e:
        pass
    bstack1lll11llll_opy_()
    if os.environ.get(bstack1ll1_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬធ")):
        bstack11ll11111_opy_ = eval(os.environ.get(bstack1ll1_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭ន")))
    if not bstack11ll11111_opy_:
        bstack1l1lll11_opy_(bstack1ll1_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦប"), bstack111ll1l1l_opy_)
    if bstack111l1ll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1llll1ll11_opy_
        except Exception as e:
            logger.error(bstack1l1l111ll1_opy_.format(str(e)))
    if bstack1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪផ") in str(framework_name).lower():
        if not bstack111ll111l1_opy_():
            return
        try:
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
def bstack1ll1lll1_opy_(self):
    global bstack11l1l1l11_opy_
    global bstack11l11llll_opy_
    global bstack1l111l11_opy_
    try:
        if bstack1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫព") in bstack11l1l1l11_opy_ and self.session_id != None and bstack1ll1llll1l_opy_(threading.current_thread(), bstack1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩភ"), bstack1ll1_opy_ (u"࠭ࠧម")) != bstack1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨយ"):
            bstack1l1l1l11_opy_ = bstack1ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨរ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩល")
            bstack11l1l111_opy_(logger, True)
            if self != None:
                bstack11111l1ll_opy_(self, bstack1l1l1l11_opy_, bstack1ll1_opy_ (u"ࠪ࠰ࠥ࠭វ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨឝ"), None)
        if item is not None and bstack1ll1lll11l1_opy_:
            bstack1l1111l11_opy_.bstack1l1l11l1l_opy_(self, bstack1ll11lll1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1ll1_opy_ (u"ࠬ࠭ឞ")
    except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢស") + str(e))
    bstack1l111l11_opy_(self)
    self.session_id = None
def bstack1ll11l1ll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11l11llll_opy_
    global bstack11l111l1l_opy_
    global bstack1llllll11_opy_
    global bstack11l1l1l11_opy_
    global bstack1l11l11l_opy_
    global bstack1llll111_opy_
    global bstack111111l1_opy_
    global bstack1l1lll1l11_opy_
    global bstack1ll1lll11l1_opy_
    global bstack1ll11lll1l_opy_
    CONFIG[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩហ")] = str(bstack11l1l1l11_opy_) + str(__version__)
    command_executor = bstack1ll1ll1l11_opy_(bstack111111l1_opy_)
    logger.debug(bstack1l111lll_opy_.format(command_executor))
    proxy = bstack11ll1l111_opy_(CONFIG, proxy)
    bstack1lll1l1ll_opy_ = 0
    try:
        if bstack1llllll11_opy_ is True:
            bstack1lll1l1ll_opy_ = int(os.environ.get(bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨឡ")))
    except:
        bstack1lll1l1ll_opy_ = 0
    bstack1lll11ll1_opy_ = bstack11l111ll1_opy_(CONFIG, bstack1lll1l1ll_opy_)
    logger.debug(bstack111ll111_opy_.format(str(bstack1lll11ll1_opy_)))
    bstack1ll11lll1l_opy_ = CONFIG.get(bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬអ"))[bstack1lll1l1ll_opy_]
    if bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧឣ") in CONFIG and CONFIG[bstack1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨឤ")]:
        bstack1l11llll1_opy_(bstack1lll11ll1_opy_, bstack1l1lll1l11_opy_)
    if bstack1111111l1_opy_.bstack1ll1ll1111_opy_(CONFIG, bstack1lll1l1ll_opy_) and bstack1111111l1_opy_.bstack1l11ll1l_opy_(bstack1lll11ll1_opy_, options, desired_capabilities):
        bstack1ll1lll11l1_opy_ = True
        bstack1111111l1_opy_.set_capabilities(bstack1lll11ll1_opy_, CONFIG)
    if desired_capabilities:
        bstack11l1l1111_opy_ = bstack1ll1l1llll_opy_(desired_capabilities)
        bstack11l1l1111_opy_[bstack1ll1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬឥ")] = bstack1l1l11l1l1_opy_(CONFIG)
        bstack1ll111ll1l_opy_ = bstack11l111ll1_opy_(bstack11l1l1111_opy_)
        if bstack1ll111ll1l_opy_:
            bstack1lll11ll1_opy_ = update(bstack1ll111ll1l_opy_, bstack1lll11ll1_opy_)
        desired_capabilities = None
    if options:
        bstack1lll1111l_opy_(options, bstack1lll11ll1_opy_)
    if not options:
        options = bstack1l1ll1l1_opy_(bstack1lll11ll1_opy_)
    if proxy and bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ឦ")):
        options.proxy(proxy)
    if options and bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ឧ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lll1ll11l_opy_() < version.parse(bstack1ll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧឨ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1lll11ll1_opy_)
    logger.info(bstack1lll111l1l_opy_)
    if bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩឩ")):
        bstack1l11l11l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩឪ")):
        bstack1l11l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫឫ")):
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
        bstack11l11l1ll_opy_ = bstack1ll1_opy_ (u"ࠬ࠭ឬ")
        if bstack1lll1ll11l_opy_() >= version.parse(bstack1ll1_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧឭ")):
            bstack11l11l1ll_opy_ = self.caps.get(bstack1ll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢឮ"))
        else:
            bstack11l11l1ll_opy_ = self.capabilities.get(bstack1ll1_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣឯ"))
        if bstack11l11l1ll_opy_:
            bstack1ll1l111_opy_(bstack11l11l1ll_opy_)
            if bstack1lll1ll11l_opy_() <= version.parse(bstack1ll1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩឰ")):
                self.command_executor._url = bstack1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦឱ") + bstack111111l1_opy_ + bstack1ll1_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣឲ")
            else:
                self.command_executor._url = bstack1ll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢឳ") + bstack11l11l1ll_opy_ + bstack1ll1_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ឴")
            logger.debug(bstack11ll11ll1_opy_.format(bstack11l11l1ll_opy_))
        else:
            logger.debug(bstack1l1l11ll1_opy_.format(bstack1ll1_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ឵")))
    except Exception as e:
        logger.debug(bstack1l1l11ll1_opy_.format(e))
    bstack11l11llll_opy_ = self.session_id
    if bstack1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨា") in bstack11l1l1l11_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ិ"), None)
        if item:
            bstack1lll11l1l11_opy_ = getattr(item, bstack1ll1_opy_ (u"ࠪࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨី"), False)
            if not getattr(item, bstack1ll1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬឹ"), None) and bstack1lll11l1l11_opy_:
                setattr(store[bstack1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩឺ")], bstack1ll1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧុ"), self)
        bstack1lllll1l1_opy_.bstack1l1l1ll11_opy_(self)
    bstack1llll111_opy_.append(self)
    if bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪូ") in CONFIG and bstack1ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ួ") in CONFIG[bstack1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬើ")][bstack1lll1l1ll_opy_]:
        bstack11l111l1l_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ឿ")][bstack1lll1l1ll_opy_][bstack1ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩៀ")]
    logger.debug(bstack1l11llll1l_opy_.format(bstack11l11llll_opy_))
def bstack1lll1ll1ll_opy_(self, url):
    global bstack111l1lll_opy_
    global CONFIG
    try:
        bstack1ll11llll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll111llll_opy_.format(str(err)))
    try:
        bstack111l1lll_opy_(self, url)
    except Exception as e:
        try:
            bstack111l1llll_opy_ = str(e)
            if any(err_msg in bstack111l1llll_opy_ for err_msg in bstack1l1l11l111_opy_):
                bstack1ll11llll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll111llll_opy_.format(str(err)))
        raise e
def bstack11l11111l_opy_(item, when):
    global bstack1ll1l1l111_opy_
    try:
        bstack1ll1l1l111_opy_(item, when)
    except Exception as e:
        pass
def bstack1llll1111_opy_(item, call, rep):
    global bstack1ll11l11_opy_
    global bstack1llll111_opy_
    name = bstack1ll1_opy_ (u"ࠬ࠭េ")
    try:
        if rep.when == bstack1ll1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫែ"):
            bstack11l11llll_opy_ = threading.current_thread().bstackSessionId
            bstack1lll11l111l_opy_ = item.config.getoption(bstack1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩៃ"))
            try:
                if (str(bstack1lll11l111l_opy_).lower() != bstack1ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ោ")):
                    name = str(rep.nodeid)
                    bstack1111llll1_opy_ = bstack11l1lll1l_opy_(bstack1ll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪៅ"), name, bstack1ll1_opy_ (u"ࠪࠫំ"), bstack1ll1_opy_ (u"ࠫࠬះ"), bstack1ll1_opy_ (u"ࠬ࠭ៈ"), bstack1ll1_opy_ (u"࠭ࠧ៉"))
                    os.environ[bstack1ll1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ៊")] = name
                    for driver in bstack1llll111_opy_:
                        if bstack11l11llll_opy_ == driver.session_id:
                            driver.execute_script(bstack1111llll1_opy_)
            except Exception as e:
                logger.debug(bstack1ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ់").format(str(e)))
            try:
                bstack1ll1l11l1l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ៌"):
                    status = bstack1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ៍") if rep.outcome.lower() == bstack1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ៎") else bstack1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ៏")
                    reason = bstack1ll1_opy_ (u"࠭ࠧ័")
                    if status == bstack1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ៑"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1ll1_opy_ (u"ࠨ࡫ࡱࡪࡴ្࠭") if status == bstack1ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ៓") else bstack1ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ។")
                    data = name + bstack1ll1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭៕") if status == bstack1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ៖") else name + bstack1ll1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩៗ") + reason
                    bstack1l1ll1llll_opy_ = bstack11l1lll1l_opy_(bstack1ll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ៘"), bstack1ll1_opy_ (u"ࠨࠩ៙"), bstack1ll1_opy_ (u"ࠩࠪ៚"), bstack1ll1_opy_ (u"ࠪࠫ៛"), level, data)
                    for driver in bstack1llll111_opy_:
                        if bstack11l11llll_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1ll1llll_opy_)
            except Exception as e:
                logger.debug(bstack1ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨៜ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ៝").format(str(e)))
    bstack1ll11l11_opy_(item, call, rep)
notset = Notset()
def bstack1llll11lll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11l111l1_opy_
    if str(name).lower() == bstack1ll1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭៞"):
        return bstack1ll1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ៟")
    else:
        return bstack11l111l1_opy_(self, name, default, skip)
def bstack1llll1ll11_opy_(self):
    global CONFIG
    global bstack1l1ll111l_opy_
    try:
        proxy = bstack11ll1lll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1ll1_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭០")):
                proxies = bstack1l1l1l11ll_opy_(proxy, bstack1ll1ll1l11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1llll1lll_opy_ = proxies.popitem()
                    if bstack1ll1_opy_ (u"ࠤ࠽࠳࠴ࠨ១") in bstack1llll1lll_opy_:
                        return bstack1llll1lll_opy_
                    else:
                        return bstack1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ២") + bstack1llll1lll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣ៣").format(str(e)))
    return bstack1l1ll111l_opy_(self)
def bstack111l1ll1_opy_():
    return (bstack1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ៤") in CONFIG or bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ៥") in CONFIG) and bstack1l1ll1ll11_opy_() and bstack1lll1ll11l_opy_() >= version.parse(
        bstack1l1ll11l_opy_)
def bstack11l11lll1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack11l111l1l_opy_
    global bstack1llllll11_opy_
    global bstack11l1l1l11_opy_
    CONFIG[bstack1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ៦")] = str(bstack11l1l1l11_opy_) + str(__version__)
    bstack1lll1l1ll_opy_ = 0
    try:
        if bstack1llllll11_opy_ is True:
            bstack1lll1l1ll_opy_ = int(os.environ.get(bstack1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ៧")))
    except:
        bstack1lll1l1ll_opy_ = 0
    CONFIG[bstack1ll1_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ៨")] = True
    bstack1lll11ll1_opy_ = bstack11l111ll1_opy_(CONFIG, bstack1lll1l1ll_opy_)
    logger.debug(bstack111ll111_opy_.format(str(bstack1lll11ll1_opy_)))
    if CONFIG.get(bstack1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ៩")):
        bstack1l11llll1_opy_(bstack1lll11ll1_opy_, bstack1l1lll1l11_opy_)
    if bstack1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ៪") in CONFIG and bstack1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ៫") in CONFIG[bstack1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ៬")][bstack1lll1l1ll_opy_]:
        bstack11l111l1l_opy_ = CONFIG[bstack1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ៭")][bstack1lll1l1ll_opy_][bstack1ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭៮")]
    import urllib
    import json
    bstack11l1111l_opy_ = bstack1ll1_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ៯") + urllib.parse.quote(json.dumps(bstack1lll11ll1_opy_))
    browser = self.connect(bstack11l1111l_opy_)
    return browser
def bstack1lll11llll_opy_():
    if not bstack111ll111l1_opy_():
        return
    global bstack11ll11111_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11l11lll1_opy_
        bstack11ll11111_opy_ = True
    except Exception as e:
        pass
def bstack1lll111l11l_opy_():
    global CONFIG
    global bstack1lll1l1l_opy_
    global bstack111111l1_opy_
    global bstack1l1lll1l11_opy_
    global bstack1llllll11_opy_
    global bstack111ll1ll_opy_
    CONFIG = json.loads(os.environ.get(bstack1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ៰")))
    bstack1lll1l1l_opy_ = eval(os.environ.get(bstack1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ៱")))
    bstack111111l1_opy_ = os.environ.get(bstack1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ៲"))
    bstack1l1ll1111_opy_(CONFIG, bstack1lll1l1l_opy_)
    bstack111ll1ll_opy_ = bstack11ll1l1l1_opy_.bstack1l1l111l1_opy_(CONFIG, bstack111ll1ll_opy_)
    global bstack1l11l11l_opy_
    global bstack1l111l11_opy_
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
    except Exception as e:
        pass
    if (bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ៳") in CONFIG or bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ៴") in CONFIG) and bstack1l1ll1ll11_opy_():
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
        logger.debug(bstack1ll1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ៵"))
    bstack1l1lll1l11_opy_ = CONFIG.get(bstack1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭៶"), {}).get(bstack1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ៷"))
    bstack1llllll11_opy_ = True
    bstack11l1ll1l_opy_(bstack1l1111l1_opy_)
if (bstack111ll11111_opy_()):
    bstack1lll111l11l_opy_()
@bstack1l111lll11_opy_(class_method=False)
def bstack1lll11l11l1_opy_(hook_name, event, bstack1lll111ll1l_opy_=None):
    if hook_name not in [bstack1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ៸"), bstack1ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ៹"), bstack1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ៺"), bstack1ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ៻"), bstack1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭៼"), bstack1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ៽"), bstack1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ៾"), bstack1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭៿")]:
        return
    node = store[bstack1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᠀")]
    if hook_name in [bstack1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ᠁"), bstack1ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ᠂")]:
        node = store[bstack1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧ᠃")]
    elif hook_name in [bstack1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ᠄"), bstack1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ᠅")]:
        node = store[bstack1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ᠆")]
    if event == bstack1ll1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ᠇"):
        hook_type = bstack1llll1l11ll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l1111l11l_opy_ = {
            bstack1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᠈"): uuid,
            bstack1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᠉"): bstack1ll11l1l11_opy_(),
            bstack1ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭᠊"): bstack1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ᠋"),
            bstack1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭᠌"): hook_type,
            bstack1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ᠍"): hook_name
        }
        store[bstack1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ᠎")].append(uuid)
        bstack1lll1111l1l_opy_ = node.nodeid
        if hook_type == bstack1ll1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ᠏"):
            if not _11llll1lll_opy_.get(bstack1lll1111l1l_opy_, None):
                _11llll1lll_opy_[bstack1lll1111l1l_opy_] = {bstack1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭᠐"): []}
            _11llll1lll_opy_[bstack1lll1111l1l_opy_][bstack1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᠑")].append(bstack1l1111l11l_opy_[bstack1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᠒")])
        _11llll1lll_opy_[bstack1lll1111l1l_opy_ + bstack1ll1_opy_ (u"ࠪ࠱ࠬ᠓") + hook_name] = bstack1l1111l11l_opy_
        bstack1lll11111ll_opy_(node, bstack1l1111l11l_opy_, bstack1ll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ᠔"))
    elif event == bstack1ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ᠕"):
        bstack11llll1ll1_opy_ = node.nodeid + bstack1ll1_opy_ (u"࠭࠭ࠨ᠖") + hook_name
        _11llll1lll_opy_[bstack11llll1ll1_opy_][bstack1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᠗")] = bstack1ll11l1l11_opy_()
        bstack1ll1llll1l1_opy_(_11llll1lll_opy_[bstack11llll1ll1_opy_][bstack1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᠘")])
        bstack1lll11111ll_opy_(node, _11llll1lll_opy_[bstack11llll1ll1_opy_], bstack1ll1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ᠙"), bstack1lll1111111_opy_=bstack1lll111ll1l_opy_)
def bstack1ll1lll11ll_opy_():
    global bstack1ll1llll111_opy_
    if bstack1lll11lll_opy_():
        bstack1ll1llll111_opy_ = bstack1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ᠚")
    else:
        bstack1ll1llll111_opy_ = bstack1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᠛")
@bstack1lllll1l1_opy_.bstack1lll11ll1ll_opy_
def bstack1lll11111l1_opy_():
    bstack1ll1lll11ll_opy_()
    if bstack1l1ll1ll11_opy_():
        bstack1l1llll1l_opy_(bstack1l1lll1ll1_opy_)
    try:
        bstack111l111ll1_opy_(bstack1lll11l11l1_opy_)
    except Exception as e:
        logger.debug(bstack1ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ᠜").format(e))
bstack1lll11111l1_opy_()