import time
import pyupbit
import datetime

access = "vqTw2OoiMI2JSP01nmU55W8vt1UPkhWMA3gEW5QS"
secret = "spVx1FijHfWtmHjguh3zBanxYvpnm5k0PrsBec8K"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-GLM")
        # end_time = start_time + datetime.timedelta(days=1)
        end_time = start_time + datetime.timedelta(seconds=480)
        # glm = get_balance("GLM")
        
        # if start_time < now < end_time - datetime.timedelta(seconds=3600):
        if start_time < now < end_time:    
            target_price = get_target_price("KRW-GLM", 0.038462)
            target_high = get_target_price("KRW-GLM", 0.192308)
            current_price = get_current_price("KRW-GLM")
            glm = get_balance("GLM")
            if target_price < current_price and glm == 0:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-GLM", krw*0.9995)
            elif target_high < current_price and glm > 13:
                 upbit.sell_market_order("KRW-GLM", glm*0.9995)
        else:
            # pass
            glm = get_balance("GLM")
            if glm > 0.008:
                upbit.sell_market_order("KRW-GLM", glm*0.9995)
        time.sleep(9)
    except Exception as e:
        print(e)
        time.sleep(9)