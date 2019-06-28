class Candle:
    def __init__(self, datetime, price_open, price_close, price_high, price_low, volume):
        # https://www.finam.ru/profile/moex-akcii/sberbank/export/
        self.datetime = datetime
        self.price_open = price_open
        self.price_close = price_close
        self.price_high = price_high
        self.price_low = price_low
        self.volume = volume
