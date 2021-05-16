import time
import pyupbit
import datetime

access = "IcQa6tEhx2B716i6Hwxy2Rl8t2rFRtlVNXhHwxns"
secret = "hOixhxPXEK3UIvhWBvM5CTKLgeNvRhWrTeZiDzlN"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_target_row(ticker, r):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_row1 = df.iloc[0]['close'] * r
    return target_row1


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

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTS") #9:00
        end_time = start_time + datetime.timedelta(days=1) #9:00 + 1일

        # 9:00 < 현재 < #8:00:00
        if start_time < now < end_time - datetime.timedelta(seconds=3600):
            target_price_ENJ = get_target_price("KRW-ENJ", 0.5)
            target_price_CRE = get_target_price("KRW-CRE", 0.5)
            target_price_TSHP = get_target_price("KRW-TSHP", 0.5)
            target_row1_ENJ = get_target_row("KRW-ENJ", 0.82)
            target_row2_ENJ = get_target_row("KRW-ENJ", 0.72)
            current_price_ENJ = get_current_price("KRW-ENJ")
            current_price_CRE = get_current_price("KRW-CRE")
            current_price_TSHP = get_current_price("KRW-TSHP")
            if target_price_ENJ < current_price_ENJ:
                krw = get_balance("KRW")
                if krw > 1000:
                    upbit.buy_market_order("KRW-ENJ", krw*0.69)
            elif target_row1_ENJ > current_price_ENJ:
                krw = get_balance("KRW")
                if target_row2_ENJ > current_price_ENJ:
                    if krw > 1000:
                        upbit.buy_market_order("KRW-ENJ", krw*0.9995)
                elif krw > 1000:
                    upbit.buy_market_order("KRW-ENJ", krw*0.5)

            elif target_price_CRE < current_price_CRE:
                krw = get_balance("KRW")
                if krw > 1000:
                    upbit.buy_market_order("KRW-CRE", krw*0.69)

            elif target_price_TSHP < current_price_TSHP:
                krw = get_balance("KRW")
                if krw > 1000:
                    upbit.buy_market_order("KRW-TSHP", krw*0.69)
                
        else:
            ENJ = get_balance("ENJ")
            CRE = get_balance("CRE")
            TSHP = get_balance("TSHP")
            if ENJ > 0.00009:
                upbit.sell_market_order("KRW-ENJ", ENJ*0.9995)
            elif CRE > 0.00009:
                upbit.sell_market_order("KRW-CRE", CRE*0.9995)
            elif TSHP > 0.00009:
                upbit.sell_market_order("KRW-TSHP", TSHP*0.9995)
        time.sleep(1)
    except Exception as e:

        
        print(e)
        time.sleep(1)
