class Candle:
    def __init__(
            self,
            open_time,
            open_price,
            close_price,
            high_price,
            low_price,
            volume
    ):
        # https://www.finam.ru/profile/moex-akcii/sberbank/export/
        self.open_time = open_time
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        self.volume = volume
