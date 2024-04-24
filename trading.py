# import yahoo_historical as yh
# import datetime
# import time
import pandas as pd
import sys


class L2dOptions:
    optionsDisplayMethod = 1
    optionsL2dMethod = 104
    optionsProcessBacktest = False
    optionsProcessHits = False
    optionsProcessBuyats = False
    optionsPriceLow = 0.10
    optionsPriceHigh = 99999.99
    optionsDateLow = 11111111
    optionsDateHigh = 22222222
    optionsDebug = 0
    optionsVolA = 0
    optionsVolL = 0
    optionsQuiet = 0
    optionsP = 0.07
    optionsP1 = 0.07
    optionsP2 = 0.07
    optionsPerTrade = 2000.00


class CucOptions:
    optionsDisplayMethod = 1


o = L2dOptions()
global tickers


def main():
    # optionsFilename = "-empty-"
    pd.options.display.float_format = '{:.2f}'.format
    m = process_method()
    route_by_method(m)
    exit()


def route_by_method(m):
    if m == "l2d":
        load_l2d_defaults()
        load_l2d_options(sys.argv)
        # print_l2d_options()

        process_l2d_options()
        exit()
    if m == "cuc":
        load_cuc_defaults()
        load_cuc_options()


#######################################################################################################################
def l2d_display_usage():
    print("USAGE:")


# class DisplayMethods:
#     print("Please specify a -m parameter (method name) on the command line.")


#######################################################################################################################


def validate_volume(df, cRow):
    sum = 0
    if cRow < 33:
        return False
    for x in range(0, 30):
        sum += df.iloc[cRow - x, 6]
    return (sum / 30) > float(o.optionsVolL)


def l2d_process_buyats():
    print("l2dProcessBuyats")
    with open("/home/rpendrick/stocks/trading.tl.dir.txt") as file:
        tickers = [line.rstrip() for line in file]
    for tick in tickers:
        #0 print(len(astart.tickers), tick)
        df = pd.read_csv(f'/data/stocks/tickers/{tick}.txt', header=None)
        #print(df.head())
        #print(f"rows: {df.shape[0]}")
        totalRows = df.shape[0]
        change = 0.0
        currentRow = 2  # 0 indexed, 2 = Wednesday
        if o.optionsVolA != 0 or o.optionsVolL != 0:
            currentRow += 30
        hitCount = 0
        while (currentRow < totalRows):
            if int(df.iloc[currentRow, 0]) >= int(o.optionsDateLow) and int(df.iloc[currentRow, 0]) <= int(
                    o.optionsDateHigh):
                #mondayDate = int(df.iloc[currentRow-1,0])
                mondayLow = float(df.iloc[currentRow - 1, 3])
                tuesdayDate = int(df.iloc[currentRow, 0])
                tuesdayLow = float(df.iloc[currentRow, 3])

                if mondayLow > 0.0:
                    change = (mondayLow - tuesdayLow) / mondayLow
                else:
                    change = 0.000001
                if change > float(o.optionsP1):
                    if validate_volume(df, currentRow):
                        buyat = tuesdayLow - (mondayLow - tuesdayLow)
                        if buyat >= 0.10:
                            print(f"{tick:6s} {tuesdayDate}  {change * 100:>5.2f}%\t ${buyat:>8.4f}")

            currentRow += 1


#######################################################################################################################



def l2d_process_hits():
    print("l2dProcessHits")
    with open("/home/rpendrick/stocks/trading.tl.dir.txt") as file:
        tickers = [line.rstrip() for line in file]
    for tick in tickers:
        df = pd.read_csv(f'/data/stocks/tickers/{tick}.txt', header=None)
        totalRows = df.shape[0]
        change = 0.0
        currentRow = 2  # 0 indexed, 2 = Wednesday
        if o.optionsVolA != 0 or o.optionsVolL != 0:
            currentRow += 30
        hitCount = 0
        while (currentRow < totalRows):
            if int(df.iloc[currentRow, 0]) >= int(o.optionsDateLow) and int(df.iloc[currentRow, 0]) <= int(
                    o.optionsDateHigh):
                #mondayDate = int(df.iloc[currentRow-2,0])
                mondayLow = float(df.iloc[currentRow - 2, 3])
                #tuesdayDate = int(df.iloc[currentRow-1,0])
                tuesdayLow = float(df.iloc[currentRow - 1, 3])
                wednesdayDate = int(df.iloc[currentRow, 0])
                wednedayLow = float(df.iloc[currentRow, 3])

                if mondayLow > 0.0:
                    change = (mondayLow - tuesdayLow) / mondayLow
                else:
                    change = 0.000001
                if change > float(o.optionsP1):
                    if validate_volume(df, currentRow):
                        buyat = tuesdayLow - (mondayLow - tuesdayLow)
                        if wednedayLow <= buyat and buyat >= 0.10:
                            print(f"{tick:6s} {wednesdayDate}  {change * 100:>5.2f}%\t ${buyat:>8.4f}")

            currentRow += 1


#######################################################################################################################


def l2d_process_backtest():
    print("l2dProcessBacktest")
    with open("/home/rpendrick/stocks/trading.tl.dir.txt") as file:
        tickers = [line.rstrip() for line in file]
    for tick in tickers:
        #0 print(len(astart.tickers), tick)
        df = pd.read_csv(f'/data/stocks/tickers/{tick}.txt', header=None)
        #print(df.head())
        #print(f"rows: {df.shape[0]}")
        totalRows = df.shape[0]
        change = 0.0
        currentRow = 2  # 0 indexed, 2 = Wednesday
        if o.optionsVolA != 0 or o.optionsVolL != 0:
            currentRow += 30
        hitCount = 0
        while (currentRow < totalRows):
            if int(df.iloc[currentRow, 0]) >= int(o.optionsDateLow) and int(df.iloc[currentRow, 0]) <= int(
                    o.optionsDateHigh):
                mondayLow = float(df.iloc[currentRow - 3, 3])
                tuesdayLow = float(df.iloc[currentRow - 2, 3])
                wednesdayDate = int(df.iloc[currentRow - 1, 0])
                wednedayLow = float(df.iloc[currentRow - 1, 3])
                thursdayClose = float(df.iloc[currentRow, 4])

                if mondayLow > 0.0:
                    change = (mondayLow - tuesdayLow) / mondayLow
                else:
                    change = 0.000001
                if change > float(o.optionsP1):
                    if validate_volume(df, currentRow):
                        buyat = tuesdayLow - (mondayLow - tuesdayLow)
                        if wednedayLow <= buyat and buyat >= 0.10:
                            print(f"{tick:6s} {wednesdayDate}  {change * 100:>5.2f}%\t ${buyat:>8.4f} {thursdayClose}")

            currentRow += 1


#######################################################################################################################


def process_method():
    if (len(sys.argv) < 3):
        l2d_display_usage()
        exit()

    for arg in sys.argv[1:]:
        #print(argumentNumber, arg)
        if (arg == "cuc"):
            return arg
        if (arg == "l2d"):
            #options.loadL2dDefaults()
            #options.loadL2dOptions(sys.argv)
            return arg

    exit()


#######################################################################################################################


def load_l2d_defaults():
    # read one line from file .trading.defaults.txt
    optionsFilename = "/home/rpendrick/stocks/trading.l2d.defaults.txt"
    with open(optionsFilename) as file:
        lines = [line.rstrip() for line in file]
    a = lines[0].split()
    load_l2d_options(a)


def load_l2d_options(opt):
    if (len(opt) < 2):
        l2d_display_usage()
        exit()

    #print(f"\na = {opt}")
    argumentNumber = 1
    for arg in opt[1:]:
        if (arg == "-p"):
            o.optionsP = opt[argumentNumber + 1]
            o.optionsP1 = opt[argumentNumber + 1]
            o.optionsP2 = opt[argumentNumber + 1]
            #print("-pa found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-dm"):
            o.optionsDisplayMethod = opt[argumentNumber + 1]
            #print("-dm found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-d"):
            o.optionsDebug = opt[argumentNumber + 1]
            #print("-d found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-lm"):
            o.optionsL2dMethod = opt[argumentNumber + 1]
            #print("-lm found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-pa"):
            o.optionsP1 = opt[argumentNumber + 1]
            #print("-pa found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-pb"):
            o.optionsP2 = opt[argumentNumber + 1]
            #print("-pb found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-dl"):
            o.optionsPriceLow = opt[argumentNumber + 1]
            #print("-dl found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-dh"):
            o.optionsPriceHigh = opt[argumentNumber + 1]
            #print("-dh found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-c"):
            o.optionsDateHigh = opt[argumentNumber + 1]
            o.optionsDateLow = opt[argumentNumber + 1]
            #print("-c found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-cl"):
            o.optionsDateLow = opt[argumentNumber + 1]
            #print("-cl found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-ch"):
            o.optionsDateHigh = opt[argumentNumber + 1]
            #print("-ch found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-va"):
            o.optionsVolA = opt[argumentNumber + 1]
            #print("-va found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-vl"):
            o.optionsVolL = opt[argumentNumber + 1]
            #print("-vl found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-q"):
            o.optionsQuiet = True
            #print("-q found, set options Quiet to True")
        if (opt[argumentNumber] == "-a"):
            o.optionsPerTrade = opt[argumentNumber + 1]
            #print("-a found, set to " + opt[argumentNumber + 1])
        if (opt[argumentNumber] == "-t"):
            o.optionsProcessBacktest = True
            o.optionsProcessHits = False
            o.optionsProcessBuyats = False
            #print("-t found, backtesting")
        if (opt[argumentNumber] == "-h"):
            o.optionsProcessBacktest = False
            o.optionsProcessHits = True
            o.optionsProcessBuyats = False
            o.optionsDateLow = opt[argumentNumber + 1]
            o.optionsDateHigh = opt[argumentNumber + 1]
            o.optionsDisplayMethod = 5  # ?????????????????????????????????????
            #print("-h found, processing hits")
        if (opt[argumentNumber] == "-b"):
            o.optionsProcessBacktest = False
            o.optionsProcessHits = False
            o.optionsProcessBuyats = True
            o.optionsDateLow = opt[argumentNumber + 1]
            o.optionsDateHigh = opt[argumentNumber + 1]
            #print("-t found, processing buyats")
        if (opt[argumentNumber] == "-tl"):
            # load approp ticker list
            tl = opt[argumentNumber + 1].split(sep=",")
            for t in tl:
                # load this list t
                tlFilename = "/home/rpendrick/stocks/trading.tl." + t + ".txt"
                with open(tlFilename) as file:
                    tickers = [line.rstrip() for line in file]
                # print(f"tickers = {tickers}")

        argumentNumber += 1


def load_cuc_defaults():
    return None


def load_cuc_options():
    return None


def print_l2d_options():
    print("-dm found, set to " + str(o.optionsDisplayMethod))
    print("-d found, set to " + str(o.optionsDebug))
    print("-lm found, set to " + str(o.optionsL2dMethod))
    print("-pa found, set to " + str(o.optionsP1))
    print("-pb found, set to " + str(o.optionsP2))
    print("-dl found, set to " + str(o.optionsPriceLow))
    print("-dh found, set to " + str(o.optionsPriceHigh))
    print("-c found, set to " + str(o.optionsDateHigh))
    print("-cl found, set to " + str(o.optionsDateLow))
    print("-ch found, set to " + str(o.optionsDateHigh))
    print("-va found, set to " + str(o.optionsVolA))
    print("-vl found, set to " + str(o.optionsVolL))
    print("-q found, set options Quiet to True")
    print("-a found, set to " + str(o.optionsPerTrade))
    if o.optionsProcessBacktest:
        print("-t found, backtesting")
    if o.optionsProcessBuyats:
        print("-b found, processing buyats")
    if o.optionsProcessHits:
        print("-h found, processing hits")


def process_l2d_options():
    if o.optionsProcessHits == True:
        l2d_process_hits()
    if o.optionsProcessBuyats == True:
        l2d_process_buyats()
    if o.optionsProcessBacktest == True:
        l2d_process_backtest()


#######################################################################################################################

def average(col):
    return col.mean()


#######################################################################################################################

#######################################################################################################################

def ticker_fixes(tick):
    # drop the column (axis=1), in place.  axis=0 when dropping a row.
    tick.drop('Adj Close', axis=1, inplace=True)
    tick['Date'] = pd.to_datetime(tick['Date'])
    tick['Date'] = tick['Date'].dt.strftime('%Y%m%d')
    tick['volume30'] = tick['Volume'].rolling(window=30).mean()


#######################################################################################################################


if __name__ == '__main__':
    main()
