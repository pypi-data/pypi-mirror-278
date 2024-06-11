from ccxt.base.types import Entry


class ImplicitAPI:
    sapipublic_get_symbols = sapiPublicGetSymbols = Entry('symbols', 'sapiPublic', 'GET', {'cost': 1})
    sapipublic_get_depth = sapiPublicGetDepth = Entry('depth', 'sapiPublic', 'GET', {'cost': 5})
    sapipublic_get_ticker = sapiPublicGetTicker = Entry('ticker', 'sapiPublic', 'GET', {'cost': 5})
    sapipublic_get_klines = sapiPublicGetKlines = Entry('klines', 'sapiPublic', 'GET', {'cost': 1})
    sapipublic_get_time = sapiPublicGetTime = Entry('time', 'sapiPublic', 'GET', {'cost': 1})
    sapipublic_get_ping = sapiPublicGetPing = Entry('ping', 'sapiPublic', 'GET', {'cost': 1})
    sapipublic_get_trades = sapiPublicGetTrades = Entry('trades', 'sapiPublic', 'GET', {'cost': 5})
    sapiprivate_get_order = sapiPrivateGetOrder = Entry('order', 'sapiPrivate', 'GET', {'cost': 1})
    sapiprivate_get_mytrades = sapiPrivateGetMyTrades = Entry('myTrades', 'sapiPrivate', 'GET', {'cost': 1})
    sapiprivate_get_openorders = sapiPrivateGetOpenOrders = Entry('openOrders', 'sapiPrivate', 'GET', {'cost': 1})
    sapiprivate_get_account = sapiPrivateGetAccount = Entry('account', 'sapiPrivate', 'GET', {'cost': 1})
    sapiprivate_post_order = sapiPrivatePostOrder = Entry('order', 'sapiPrivate', 'POST', {'cost': 5})
    sapiprivate_post_order_test = sapiPrivatePostOrderTest = Entry('order/test', 'sapiPrivate', 'POST', {'cost': 1})
    sapiprivate_post_batchorders = sapiPrivatePostBatchOrders = Entry('batchOrders', 'sapiPrivate', 'POST', {'cost': 10})
    sapiprivate_post_cancel = sapiPrivatePostCancel = Entry('cancel', 'sapiPrivate', 'POST', {'cost': 5})
    sapiprivate_post_batchcancel = sapiPrivatePostBatchCancel = Entry('batchCancel', 'sapiPrivate', 'POST', {'cost': 10})
