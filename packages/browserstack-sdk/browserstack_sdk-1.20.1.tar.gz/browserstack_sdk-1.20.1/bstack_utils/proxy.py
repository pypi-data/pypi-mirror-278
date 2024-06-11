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
from urllib.parse import urlparse
from bstack_utils.messages import bstack1111l1ll11_opy_
def bstack1lllll11l11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lllll111l1_opy_(bstack1lllll1111l_opy_, bstack1lllll111ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lllll1111l_opy_):
        with open(bstack1lllll1111l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lllll11l11_opy_(bstack1lllll1111l_opy_):
        pac = get_pac(url=bstack1lllll1111l_opy_)
    else:
        raise Exception(bstack1ll1_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭ᑞ").format(bstack1lllll1111l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll1_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣᑟ"), 80))
        bstack1lllll11l1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lllll11l1l_opy_ = bstack1ll1_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩᑠ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lllll111ll_opy_, bstack1lllll11l1l_opy_)
    return proxy_url
def bstack1l11l1ll1_opy_(config):
    return bstack1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᑡ") in config or bstack1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᑢ") in config
def bstack11ll1lll_opy_(config):
    if not bstack1l11l1ll1_opy_(config):
        return
    if config.get(bstack1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᑣ")):
        return config.get(bstack1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᑤ"))
    if config.get(bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᑥ")):
        return config.get(bstack1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᑦ"))
def bstack11ll1ll11_opy_(config, bstack1lllll111ll_opy_):
    proxy = bstack11ll1lll_opy_(config)
    proxies = {}
    if config.get(bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᑧ")) or config.get(bstack1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᑨ")):
        if proxy.endswith(bstack1ll1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨᑩ")):
            proxies = bstack1l1l1l11ll_opy_(proxy, bstack1lllll111ll_opy_)
        else:
            proxies = {
                bstack1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᑪ"): proxy
            }
    return proxies
def bstack1l1l1l11ll_opy_(bstack1lllll1111l_opy_, bstack1lllll111ll_opy_):
    proxies = {}
    global bstack1llll1lllll_opy_
    if bstack1ll1_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᑫ") in globals():
        return bstack1llll1lllll_opy_
    try:
        proxy = bstack1lllll111l1_opy_(bstack1lllll1111l_opy_, bstack1lllll111ll_opy_)
        if bstack1ll1_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᑬ") in proxy:
            proxies = {}
        elif bstack1ll1_opy_ (u"ࠢࡉࡖࡗࡔࠧᑭ") in proxy or bstack1ll1_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᑮ") in proxy or bstack1ll1_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᑯ") in proxy:
            bstack1lllll11111_opy_ = proxy.split(bstack1ll1_opy_ (u"ࠥࠤࠧᑰ"))
            if bstack1ll1_opy_ (u"ࠦ࠿࠵࠯ࠣᑱ") in bstack1ll1_opy_ (u"ࠧࠨᑲ").join(bstack1lllll11111_opy_[1:]):
                proxies = {
                    bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᑳ"): bstack1ll1_opy_ (u"ࠢࠣᑴ").join(bstack1lllll11111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᑵ"): str(bstack1lllll11111_opy_[0]).lower() + bstack1ll1_opy_ (u"ࠤ࠽࠳࠴ࠨᑶ") + bstack1ll1_opy_ (u"ࠥࠦᑷ").join(bstack1lllll11111_opy_[1:])
                }
        elif bstack1ll1_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᑸ") in proxy:
            bstack1lllll11111_opy_ = proxy.split(bstack1ll1_opy_ (u"ࠧࠦࠢᑹ"))
            if bstack1ll1_opy_ (u"ࠨ࠺࠰࠱ࠥᑺ") in bstack1ll1_opy_ (u"ࠢࠣᑻ").join(bstack1lllll11111_opy_[1:]):
                proxies = {
                    bstack1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᑼ"): bstack1ll1_opy_ (u"ࠤࠥᑽ").join(bstack1lllll11111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᑾ"): bstack1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᑿ") + bstack1ll1_opy_ (u"ࠧࠨᒀ").join(bstack1lllll11111_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᒁ"): proxy
            }
    except Exception as e:
        print(bstack1ll1_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᒂ"), bstack1111l1ll11_opy_.format(bstack1lllll1111l_opy_, str(e)))
    bstack1llll1lllll_opy_ = proxies
    return proxies