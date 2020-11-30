"""

ask - high

bid - low

spred = ask-bid

"""
import numpy
import psycopg2

from Conf import DbConfig, Config
from Desc.Candle import Candle
from Desc.Pattern import Pattern


def get_patterns_for_window_and_num(window, length, limit=None):
    conf = Config.Config()
    dbConf = DbConfig.DbConfig()
    connect = psycopg2.connect(
        database=dbConf.dbname,
        user=dbConf.user,
        host=dbConf.address,
        password=dbConf.password
    )
    cursor = connect.cursor()

    print('Successfully connected')
    tName = conf.insName.lower()
    cmd = 'SELECT COUNT(*) FROM {0};'.format(tName)
    cursor.execute(cmd)
    totalCount = cursor.fetchone()[0]
    print('Total items count {0}'.format(totalCount))
    cmd = 'SELECT * FROM {0} ORDER BY open_time'.format(tName)
    if limit is None:
        cmd = '{0};'.format(cmd)
    else:
        cmd = '{0} LIMIT {1};'.format(cmd, limit)
    cursor.execute(cmd)

    wl = list()
    patterns = list()
    profits = list()
    indicies = list()
    i = 1
    for row in cursor:
        nextCandle = Candle(
            open_price=row[0],
            high_price=row[1],
            low_price=row[2],
            close_price=row[3],
            volume=row[4],
            open_time=row[5]
        )
        wl.append(nextCandle)
        print(
            'Row {0} of {1}, {2:.3f}% total'.format(
                i,
                totalCount,
                100 * (float(i) / float(totalCount)))
        )
        if len(wl) == window + length:
            # find pattern of 0..length elements
            # that indicates price falls / grows
            # in the next window elements to get profit
            candle = wl[length - 1]
            ind = length + 1
            # take real data only
            if candle.volume != 0:
                while ind <= window + length:
                    iCandle = wl[ind - 1]
                    # define patterns for analyzing iCandle
                    if iCandle.volume != 0:
                        # if iCandle.low_price > candle.high_price:
                        if iCandle.open_price > candle.close_price:
                            # buy pattern
                            p = Pattern(wl[:length], 'buy')
                            patterns.append(p)
                            indicies.append(ind - length)
                            # profits.append(iCandle.low_price - candle.high_price)
                            profits.append(iCandle.open_price - candle.close_price)
                            break
                        # if iCandle.high_price < candle.low_price:
                        if iCandle.close_price < candle.open_price:
                            # sell pattern
                            p = Pattern(wl[:length], 'sell')
                            patterns.append(p)
                            indicies.append(ind - length)
                            # profits.append(candle.low_price - iCandle.high_price)
                            profits.append(candle.open_price - iCandle.close_price)
                            break
                    ind = ind + 1
            wl.pop(0)
        i = i + 1
    print('Total patterns: {0}'.format(len(patterns)))
    print('Mean index[after]: {0}'.format(numpy.mean(indicies)))
    print('Mean profit: {0}'.format(numpy.mean(profits)))
    connect.close()
    return patterns


def pattern_serie_to_vector(pattern):
    sum = 0
    for candle in pattern.serie:
        # sum = sum + float(candle.low_price + candle.high_price) / 2
        sum = sum + float(candle.open_price + candle.close_price) / 2
    mean = sum / len(pattern.serie)
    vec = []
    for candle in pattern.serie:
        # vec = numpy.hstack((vec, [(candle.low_price+candle.high_price) / (2 * mean)]))
        vec = numpy.hstack((vec, [(candle.open_price + candle.close_price) / (2 * mean)]))
    return vec


def get_x_y_for_patterns(patterns, expected_result):
    X = []
    y = []
    for p in patterns:
        X.append(pattern_serie_to_vector(p))
        if p.result == expected_result:
            y.append(1)
        else:
            y.append(0)
    return X, y
