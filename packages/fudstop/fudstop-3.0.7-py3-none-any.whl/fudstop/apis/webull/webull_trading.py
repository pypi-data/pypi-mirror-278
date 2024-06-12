import os
import sys
from pathlib import Path
import time
# Add the project directory to the sys.path
project_dir = str(Path(__file__).resolve().parents[2])
if project_dir not in sys.path:
    sys.path.append(project_dir)
from dotenv import load_dotenv
load_dotenv()
import aiohttp
import httpx
import pandas as pd
from pytz import timezone
from .webull_helpers import calculate_countdown, calculate_setup
from .trade_models.stock_quote import MultiQuote
from .trade_models.capital_flow import CapitalFlow, CapitalFlowHistory
from .trade_models.deals import Deals
from .trade_models.cost_distribution import CostDistribution
from .trade_models.etf_holdings import ETFHoldings
from .trade_models.institutional_holdings import InstitutionHolding, InstitutionStat
from .trade_models.financials import BalanceSheet, FinancialStatement, CashFlow
from .trade_models.news import NewsItem
from .trade_models.forecast_evaluator import ForecastEvaluator
from .trade_models.short_interest import ShortInterest
from .trade_models.volume_analysis import WebullVolAnalysis
from .trade_models.ticker_query import WebullStockData
from .trade_models.analyst_ratings import Analysis
from .trade_models.price_streamer import PriceStreamer
from .trade_models.company_brief import CompanyBrief, Executives, Sectors
from .trade_models.order_flow import OrderFlow
import asyncio

from datetime import datetime, timedelta, timezone

class WebullTrading:
    def __init__(self):
        self.most_active_tickers= ['SNOW', 'IBM', 'DKNG', 'SLV', 'NWL', 'SPXS', 'DIA', 'QCOM', 'CMG', 'WYNN', 'PENN', 'HLF', 'CCJ', 'WW', 'NEM', 'MOS', 'SRPT', 'MS', 'DPST', 'AG', 'PAA', 'PANW', 'XPEV', 'BHC', 'KSS', 'XLP', 'LLY', 'MDB', 'AZN', 'NVO', 'BOIL', 'ZM', 'HUT', 'VIX', 'PDD', 'SLB', 'PCG', 'DIS', 'TFC', 'SIRI', 'TDOC', 'CRSP', 'BSX', 'BITF', 'AAL', 'EOSE', 'RIVN', 'X', 'CCL', 'SOXS', 'NOVA', 'TMUS', 'HES', 'LI', 'NVAX', 'TSM', 'CNC', 'IAU', 'GDDY', 'CVX', 'TGT', 'MCD', 'GDXJ', 'AAPL', 'NKLA', 'EDR', 'NOK', 'SPWR', 'NKE', 'HYG', 'FSLR', 'SGEN', 'DNN', 'BAX', 'CRWD', 'OSTK', 'XLC', 'RIG', 'SEDG', 'SNDL', 'RSP', 'M', 'CD', 'UNG', 'LQD', 'TTD', 'AMGN', 'EQT', 'YINN', 'MULN', 'FTNT', 'WBD', 'MRNA', 'PTON', 'SCHW', 'ABNB', 'EW', 'PM', 'UCO', 'TXN', 'DLR', 'KHC', 'MMAT', 'QQQ', 'GOOGL', 'AEM', 'RTX', 'AVGO', 'RBLX', 'PAAS', 'UUP', 'OXY', 'SQ', 'PLUG', 'CLF', 'GOEV', 'BKLN', 'ALB', 'BALL', 'SMH', 'CVE', 'F', 'KRE', 'TWLO', 'ARCC', 'ARM', 'U', 'SOFI', 'SBUX', 'FXI', 'BMY', 'HSBC', 'EFA', 'SVXY', 'VALE', 'GOLD', 'MSFT', 'OIH', 'ARKK', 'AMD', 'AA', 'DXCM', 'ABT', 'WOLF', 'FDX', 'SOXL', 'MA', 'KWEB', 'BP', 'SNAP', 'NLY', 'KGC', 'URA', 'UVIX', 'KMI', 'ACB', 'NET', 'W', 'GRAB', 'LMT', 'EPD', 'FCX', 'STNE', 'NIO', 'SU', 'ET', 'CVS', 'ADBE', 'MXL', 'HOOD', 'FUBO', 'RIOT', 'CRM', 'TNA', 'DISH', 'XBI', 'VFS', 'GPS', 'NVDA', 'MGM', 'MRK', 'ABBV', 'LABU', 'BEKE', 'VRT', 'LVS', 'CPNG', 'BA', 'MTCH', 'PEP', 'EBAY', 'GDX', 'XLV', 'UBER', 'GOOG', 'COF', 'XLU', 'BILI', 'XLK', 'VXX', 'DVN', 'MSOS', 'KOLD', 'XOM', 'BKNG', 'SPY', 'RUT', 'CMCSA', 'STLA', 'NCLH', 'GRPN', 'ZION', 'UAL', 'GM', 'NDX', 'TQQQ', 'COIN', 'WBA', 'CLSK', 'NFLX', 'FREY', 'AFRM', 'NAT', 'EEM', 'IYR', 'KEY', 'OPEN', 'DM', 'TSLA', 'BXMT', 'T', 'TZA', 'BAC', 'MARA', 'UVXY', 'LOW', 'COST', 'HL', 'CHTR', 'TMF', 'ROKU', 'DOCU', 'PSEC', 'XHB', 'VMW', 'SABR', 'USB', 'DDOG', 'DB', 'V', 'NOW', 'XRT', 'SMCI', 'PFE', 'NYCB', 'BIDU', 'C', 'SPX', 'ETSY', 'EMB', 'SQQQ', 'CHPT', 'DASH', 'VZ', 'DNA', 'CL', 'ANET', 'WMT', 'MRO', 'WFC', 'MO', 'USO', 'ENVX', 'INTC', 'GEO', 'VFC', 'WE', 'MET', 'CHWY', 'PBR', 'KO', 'TH', 'QS', 'BTU', 'GLD', 'JD', 'XLY', 'KR', 'ASTS', 'WDC', 'HTZ', 'XLF', 'COP', 'PATH', 'SHEL', 'MXEF', 'SE', 'SPCE', 'UPS', 'RUN', 'DOW', 'ASHR', 'ONON', 'DAL', 'SPXL', 'SAVE', 'LUV', 'HD', 'JNJ', 'LYFT', 'UNH', 'BBY', 'CZR', 'NEE', 'STNG', 'SPXU', 'MMM', 'VNQ', 'IMGN', 'MSTR', 'AXP', 'TMO', 'XPO', 'FEZ', 'ENPH', 'AX', 'NVCR', 'GS', 'MRVL', 'ADM', 'GILD', 'IBB', 'FTCH', 'PARA', 'PINS', 'JBLU', 'SNY', 'BITO', 'PYPL', 'FAS', 'GME', 'LAZR', 'URNM', 'BX', 'MPW', 'UPRO', 'HPQ', 'AMZN', 'SAVA', 'TLT', 'ON', 'CAT', 'VLO', 'AR', 'IDXX', 'SWN', 'META', 'BABA', 'ZS', 'EWZ', 'ORCL', 'XOP', 'TJX', 'XP', 'EL', 'HAL', 'IEF', 'XLI', 'UPST', 'Z', 'TELL', 'LRCX', 'DLTR', 'BYND', 'PACW', 'CVNA', 'GSAT', 'CSCO', 'NU', 'KVUE', 'JPM', 'LCID', 'TLRY', 'AGNC', 'CGC', 'XLE', 'VOD', 'TEVA', 'JETS', 'UEC', 'FSR', 'ZIM', 'ABR', 'IQ', 'AMC', 'ALLY', 'HE', 'OKTA', 'ACN', 'MU', 'FLEX', 'SHOP', 'PLTR', 'CLX', 'LUMN', 'WHR', 'PAGP', 'IWM', 'WPM', 'TTWO', 'AI', 'ALGN', 'SPOT', 'BTG', 'IONQ', 'GE', 'DG', 'AMAT', 'XSP', 'PG', 'LULU', 'DE', 'MDT', 'RCL']
        self.scalar_tickers = ['SPX', 'VIX', 'OSTK', 'XSP', 'NDX', 'MXEF']
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.semaphore = asyncio.Semaphore(10)
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.thirty_days_from_now = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.fifteen_days_ago = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        self.fifteen_days_from_now = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        self.eight_days_from_now = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
        self.eight_days_ago = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d')
        self.timeframes = ['m1','m5', 'm10', 'm15', 'm20', 'm30', 'm60', 'm120', 'm240', 'd1']
        self.now_timestamp_int = int(datetime.now(timezone.utc).timestamp())
        self.day = int(86400)
        self.id = 15765933
        self.headers  = {
        "Accept": os.getenv("ACCEPT"),
        "Accept-Encoding": os.getenv("ACCEPT_ENCODING"),
        "Accept-Language": "en-US,en;q=0.9",
        'Content-Type': 'application/json',
        "App": os.getenv("APP"),
        "App-Group": os.getenv("APP_GROUP"),
        "Appid": os.getenv("APPID"),
        "Device-Type": os.getenv("DEVICE_TYPE"),
        "Did": 'gldaboazf4y28thligawz4a7xamqu91g',
        "Hl": os.getenv("HL"),
        "Locale": os.getenv("LOCALE"),
        "Origin": os.getenv("ORIGIN"),
        "Os": os.getenv("OS"),
        "Osv": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Ph": os.getenv("PH"),
        "Platform": os.getenv("PLATFORM"),
        "Priority": os.getenv("PRIORITY"),
        "Referer": os.getenv("REFERER"),
        "Reqid": os.getenv("REQID"),
        "T_time": os.getenv("T_TIME"),
        "Tz": os.getenv("TZ"),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Ver": os.getenv("VER"),
        "X-S": os.getenv("X_S"),
        "X-Sv": os.getenv("X_SV")
    }
        #miscellaenous
                #sessions
        self._account_id = ''
        self._trade_token = ''
        self._access_token = ''
        self._refresh_token = ''
        self._token_expire = ''
        self._uuid = ''

        self._region_code = 6
        self.zone_var = 'dc_core_r001'
        self.timeout = 15
        self.device_id = "gldaboazf4y28thligawz4a7xamqu91g"
    async def fetch_endpoint(self, endpoint):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(endpoint) as resp:
                return await resp.json()

    async def get_ticker_id(self, symbol):
        """Converts ticker name to ticker ID to be passed to other API endpoints from Webull."""
        endpoint =f"https://quotes-gw.webullfintech.com/api/search/pc/tickers?keyword={symbol}&pageIndex=1&pageSize=1"

        
        data =  await self.fetch_endpoint(endpoint)
        datas = data['data'] if 'data' in data else None
        if datas is not None:
            tickerID = datas[0]['tickerId']
            return tickerID
        

    async def multi_quote(self, tickers=['AAPL', 'SPY']):
        """Query multiple tickers using the Webull API"""


        tasks = [self.get_ticker_id(str(ticker)) for ticker in tickers]
        
        ticker_ids = await asyncio.gather(*tasks)


        ticker_ids = ','.join(str(ticker_id) for ticker_id in ticker_ids)
        print(ticker_ids)
        endpoint = f"https://quotes-gw.webullfintech.com/api/bgw/quote/realtime?ids={ticker_ids}&includeSecu=1&delay=0&more=1"

        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint)
            data = response.json()


            multi_quote = MultiQuote(data)

            return multi_quote
    

    async def get_bars(self, ticker, interval):
        async with self.semaphore, httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:

            tickerId = await self.get_ticker_id(ticker)

            if interval == 'm1':
                timestamp = self.now_timestamp_int - 2000
                timestamp = str(timestamp)
                timespan = '1 minute'

            if interval == 'm5':
                timestamp = self.now_timestamp_int - 5000
                timestamp = str(timestamp)
                timespan = '5 minute'

            if interval == 'm15':
                timestamp = self.now_timestamp_int - (self.day * 2)
                timestamp = str(timestamp)
                timespan = '15 minute'



            elif interval == 'm30':
                timestamp = self.now_timestamp_int - (self.day * 4)
                timestamp = str(timestamp)
                timespan = '30 minute'


            elif interval == 'm60':
                timestamp = self.now_timestamp_int - (self.day * 12)
                timestamp = str(timestamp)
                timespan = '1 hour'

            elif interval == 'm120':
                timestamp = self.now_timestamp_int - (self.day * 30)
                timestamp = str(timestamp)
                timespan = '2 hour'

            elif interval == 'm240':
                timestamp = self.now_timestamp_int - (self.day * 45)
                timestamp = str(timestamp)
                timespan = '4 hour'


            elif interval == 'd':
                timestamp = self.now_timestamp_int - (self.day * 65)
                timespan = 'day'

            elif interval == 'm':
                timestamp = self.now_timestamp_int - (self.day * 600)
                
                timestamp = str(timestamp)
                timespan = 'month'

            elif interval == 'w':
                timestamp = self.now_timestamp_int - (self.day * 250)
                timestamp = str(timestamp)
                timespan = 'week'
            async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:





                url=f"https://quotes-gw.webullfintech.com/api/quote/charts/kdata/latest?tickerIds={tickerId}&type={interval}&count=800&timestamp={timestamp}"
                url2=f"https://quotes-gw.webullfintech.com/api/quote/charts/query-mini?tickerId={tickerId}&type={interval}&count=800&restorationType=1&loadFactor=1"

                try:
                    data  = await client.get(url)


                    await asyncio.sleep(0)
                    data = data.json()
                    datas = data[0]['data']
            
                    if datas is not None and len(datas) > 0:
                    
                        parsed_data = []
                        for entry in datas:
                            values = entry.split(',')
                            if values[-1] == 'NULL':
                                values = values[:-1]
                            elif values[-1] == 'NULL':
                                values = values[:-1]  # remove the last element if it's 'NULL'
                            parsed_data.append([float(value) if value != 'null' else 0.0 for value in values])
                        
                        sorted_data = sorted(parsed_data, key=lambda x: x[0], reverse=True)
                        
                        # Dynamically assign columns based on the length of the first entry
                        columns = ['Timestamp', 'Open', 'Close', 'High', 'Low', 'N', 'Volume', 'Vwap'][:len(sorted_data[0])]
                        
                        df = pd.DataFrame(sorted_data, columns=columns)
                        # Convert the Unix timestamps to datetime objects in UTC first
                        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', utc=True)

                        # Convert UTC to Eastern Time (ET)
                        df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern')
                        df['Timestamp'] = df['Timestamp'].dt.tz_localize(None)
                        df['Ticker'] = ticker
                        df['interval'] = interval
                        df['timespan'] = timespan

                        df['ticker'] = ticker


                        yield df.head(100)



                except Exception as e:
                    print(f"Connect error")
            
    # Detecting unfilled gaps in stock price data
    async def find_unfilled_gaps(self, ticker:str, interval:str):
        ticker = ticker.upper()
        unfilled_gaps=[]
        async for df in self.get_bars(ticker=ticker, interval=interval):

            df.sort_values(by='Timestamp', ascending=True, inplace=True)
            # Assuming the DataFrame is sorted in ascending order by 'Timestamp'
            for i in range(1, len(df)):
                previous_row = df.iloc[i - 1]
                current_row = df.iloc[i]
                
                # Checking for gap up
                if current_row['Low'] > previous_row['High']:
                    gap = {
                        'gap_date': current_row['Timestamp'],
                        'gap_range': (previous_row['High'], current_row['Low'])
                    }
                    # Check in the following days if the gap has been filled
                    filled = df[i+1:].apply(
                        lambda row: row['Low'] <= gap['gap_range'][1] and row['High'] >= gap['gap_range'][0], axis=1
                    ).any()
                    if not filled:
                        unfilled_gaps.append(gap)

                # Checking for gap down
                elif current_row['High'] < previous_row['Low']:
                    gap = {
                        'gap_date': current_row['Timestamp'],
                        'gap_range': (current_row['High'], previous_row['Low'])
                    }
                    # Check in the following days if the gap has been filled
                    filled = df[i+1:].apply(
                        lambda row: row['Low'] <= gap['gap_range'][1] and row['High'] >= gap['gap_range'][0], axis=1
                    ).any()
                    if not filled:
                        unfilled_gaps.append(gap)

            return unfilled_gaps
        

    async def deals(self, symbol:str):
        try:
            tickerId = await self.get_ticker_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/deals?count=50000&tickerId={tickerId}"

            async with httpx.AsyncClient(headers=self.headers) as client:
                data = await client.get(endpoint)
                data = data.json()

                data = data.get('data')

                data = Deals(data)
                return data
        except Exception as e:
            print(e)

    async def get_stock_quote(self, symbol:str):
        if symbol == 'SPX':
            symbol == 'SPXW'
        ticker_id = await self.get_ticker_id(symbol)

        endpoint = f"https://quotes-gw.webullfintech.com/api/stock/tickerRealTime/getQuote?tickerId={ticker_id}&includeSecu=1&includeQuote=1&more=1"
        print(endpoint)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    r = await resp.json()

                    #data = WebullStockData(r)
                    try:

                        df = pd.DataFrame(r)
                        df = df.drop(columns=['secType', 'exchangeId', 'regionId', 'regionCode'])
                        return df
                    except Exception as e:
                        print(f"{e} | Attempting to use an index of 0...")
                        try:
                            df = pd.DataFrame(r, index=[0])
                            
                        except Exception as e:
                            print(f"Second attempt failed for {symbol}: {e}")
                        try:
                            df = df.drop(columns=['secType', 'exchangeId', 'regionId', 'regionCode'])
                            
                            return df
                        except Exception as e:
                            print(f'Giving up...{symbol}: {e}')
        except Exception as e:
            return f"Failed for {e}"


    async def get_analyst_ratings(self, symbol:str):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint=f"https://quotes-gw.webullfintech.com/api/information/securities/analysis?tickerId={ticker_id}"
        datas = await self.fetch_endpoint(endpoint)
        data = Analysis(datas)
        return data
    

    async def get_short_interest(self, symbol:str):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/information/brief/shortInterest?tickerId={ticker_id}"
        datas = await self.fetch_endpoint(endpoint)
        data = ShortInterest(datas)
        return data
    
    async def institutional_holding(self, symbol:str):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/information/stock/getInstitutionalHolding?tickerId={ticker_id}"
        datas = await self.fetch_endpoint(endpoint)
        data = InstitutionStat(datas)

        return data
    

    async def volume_analysis(self, symbol:str):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count=10&tickerId={ticker_id}&type=0"
        datas = await self.fetch_endpoint(endpoint)
        data = WebullVolAnalysis(datas)
        return data
    

    async def cost_distribution(self, symbol:str, start_date:str=None, end_date:str=None):

        if start_date is None:
            start_date = self.yesterday
            

        if end_date is None:
            end_date = self.today

        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/quotes/chip/query?tickerId={ticker_id}&startDate={start_date}&endDate={end_date}"
        print(endpoint)
        datas = await self.fetch_endpoint(endpoint)
        data = CostDistribution(datas)
        return data
    

    async def stock_quote(self, symbol:str):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/bgw/quote/realtime?ids={ticker_id}&includeSecu=1&delay=0&more=1"
        datas = await self.fetch_endpoint(endpoint)
        data = WebullStockData(datas)
        return data

    async def financials(self, symbol:str, financials_type:str='balancesheet'):
        """Argument
        
        Symbol: the symbol to query
        """
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/information/financial/{financials_type}?tickerId={ticker_id}&type=102&fiscalPeriod=1,2,3,4&limit=4"
    
        datas = await self.fetch_endpoint(endpoint)
        data = datas['data'] if 'data' in datas else None
        if data is not None:
            data = FinancialStatement(datas).df.to_dict('records')
            return data
  

    async def news(self, symbol:str, pageSize:str='100'):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://nacomm.webullfintech.com/api/information/news/tickerNews?tickerId={ticker_id}&currentNewsId=0&pageSize={pageSize}"
        datas = await self.fetch_endpoint(endpoint)
        data = NewsItem(datas)
        return data
    

    async def company_brief(self, symbol:str, as_dataframe:bool=False):
        """
        RETURNS THREE THINGS

        >>> companyBrief_df
        >>> executives_df
        >>> sectors_df
        """
        ticker_id = await self.get_ticker_id(symbol)
        endpoint=f"https://quotes-gw.webullfintech.com/api/information/stock/brief?tickerId={ticker_id}"    
        datas = await self.fetch_endpoint(endpoint)

        companyBrief = CompanyBrief(datas['companyBrief'])
        sectors = Sectors(datas['sectors'])
        executives = Executives(datas['executives'])

        # Convert to DataFrames
        companyBrief_df = companyBrief.as_dataframe
        sectors_df = sectors.as_dataframe
        executives_df = executives.as_dataframe

        
        return companyBrief, sectors, executives

    async def balance_sheet(self, symbol:str, limit:str='11'):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/information/financial/balancesheet?tickerId={ticker_id}&type=101&fiscalPeriod=0&limit={limit}"
        datas = await self.fetch_endpoint(endpoint)
        data = BalanceSheet(datas)
        return data
    
    async def cash_flow(self, symbol:str, limit:str='12'):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/information/financial/cashflow?tickerId={ticker_id}&type=102&fiscalPeriod=1,2,3,4&limit={limit}"
        datas = await self.fetch_endpoint(endpoint)
        data = CashFlow(datas)
        return data
    
    async def income_statement(self, symbol:str, limit:str='12'):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/information/financial/incomestatement?tickerId={ticker_id}&type=102&fiscalPeriod=1,2,3,4&limit={limit}"
        datas = await self.fetch_endpoint(endpoint)
        data = FinancialStatement(datas)
        return data
    

    async def order_flow(self, symbol:str, type:str='0', count:str='1'):
        """
        Gets order flow for tickers
        """
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count={count}&tickerId={ticker_id}&type={type}"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.get(endpoint)
            data = data.json()
            return OrderFlow(data)
    

    async def price_streamer(self, symbol:str, type:str='0'):
        """
        Type:
        >>> 0 = today
        >>> 1 = yesterday
        """
        ticker_id = await self.get_ticker_id(symbol)
        url=f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count=50000&tickerId={ticker_id}&type={type}"
        async with httpx.AsyncClient() as client:
            data = await client.get(url)
            data = data.json()

            return PriceStreamer(data)


    async def capital_flow(self, symbol:str):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/ticker?tickerId={ticker_id}&showHis=true"
        
        datas = await self.fetch_endpoint(endpoint)
        latest = datas['latest']
        historic = datas['historical']
        date = [i.get('date') for i in historic]
        historic_items = [i.get('item') for i in historic]
        item = latest['item']

        print(item)
        data = CapitalFlow(item)
        historic = CapitalFlowHistory(historic_items, date)
    
        return data, historic
    

    async def etf_holdings(self, symbol:str, pageSize:str='200'):
        ticker_id = await self.get_ticker_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/information/company/queryEtfList?tickerId={ticker_id}&pageIndex=1&pageSize={pageSize}"
        datas = await self.fetch_endpoint(endpoint)
        data = ETFHoldings(datas)
        return data
    

    async def multi_quote(self, symbols:str):
        counter = 0
        while True:
            counter = counter + 1
           
            ticker_ids = [await self.get_ticker_id(i) for i in symbols]
            ticker_ids = str(ticker_ids)
            ticker_ids = ','.join([ticker_ids]).replace(']', '').replace('[', '').replace(' ', '')
            endpoint = f"https://quotes-gw.webullfintech.com/api/bgw/quote/realtime?ids={ticker_ids}&includeSecu=1&delay=0&more=1"

            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(endpoint) as resp:
                    datas = await resp.json()
                    all_data = MultiQuote(datas)

                    for sym,price, vol, vr in zip(all_data.symbol, all_data.close, all_data.volume, all_data.vibrateRatio):
                        yield(f'SYM(1): | {sym} | PRICE(3): | {price} | VOL:(5): | {vol} | VIBRATION:(7): | {vr}')

                        if counter == 250:
                            print(f"Stream ending...")
                        
                            break


    async def async_get_td9(self, ticker, interval):
        timeStamp = None
        if ticker == 'I:SPX':
            ticker = 'SPXW'
        elif ticker =='I:NDX':
            ticker = 'NDX'
        elif ticker =='I:VIX':
            ticker = 'VIX'
        
        tickerid = await self.get_ticker_id(ticker)




        if timeStamp is None:
            # if not set, default to current time
            timeStamp = int(time.time())

        base_fintech_gw_url = f'https://quotes-gw.webullfintech.com/api/quote/charts/query?tickerIds={tickerid}&type={interval}&count=300&timestamp={timeStamp}&extendTrading=1'



        if interval == 'm1':
            timespan = 'minute'
        elif interval == 'm60':
            timespan = 'hour'
        elif interval == 'm20':
            timespan = 'hour'
        elif interval == 'm5':
            timespan = 'hour'
        elif interval == 'm15':
            timespan = 'hour'
        elif interval == 'm30':
            timespan = 'hour'
        elif interval == 'm120':
            timespan = 'day'
        elif interval == 'm240':
            timespan = 'day'
        elif interval == 'd1':
            timespan = 'day'
        elif interval == 'w':
            timespan = 'week'
        elif interval == 'm':
            timespan = 'month'
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(base_fintech_gw_url) as resp:
                r = await resp.json()
                try:
                    # Check if the data is present and the expected structure is correct
                    if r and isinstance(r, list) and 'data' in r[0]:
                        data = r[0]['data']

                        data = r[0]['data']
                        if data is not None:
                            parsed_data = []
                            for entry in data:
                                values = entry.split(',')
                                if values[-1] == 'NULL':
                                    values = values[:-1]
                                elif values[-1] == 'NULL':
                                    values = values[:-1]  # remove the last element if it's 'NULL'
                                parsed_data.append([float(value) if value != 'null' else 0.0 for value in values])
                            try:
                                sorted_data = sorted(parsed_data, key=lambda x: x[0], reverse=True)
                                
                                # Dynamically assign columns based on the length of the first entry
                                columns = ['Timestamp', 'Open', 'Close', 'High', 'Low', 'N', 'Volume', 'Vwap'][:len(sorted_data[0])]
                                
                                df = pd.DataFrame(sorted_data, columns=columns)
                                # Convert the Unix timestamps to datetime objects in UTC first
                                df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', utc=True)

                                # Convert UTC to Eastern Time (ET)
                                df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern')
                                df['Timestamp'] = df['Timestamp'].dt.tz_localize(None)
                                df['Ticker'] = ticker
                                df['timespan'] = interval


                                df['ticker'] = ticker

                                
                                td9_df = df.head(13)

                                setup_phase = calculate_setup(td9_df)
                                countdown_phase = calculate_countdown(td9_df)

                                df = df.head(13)
                                df = df.iloc[::-1].reset_index(drop=True)
                                td9_state = "Setup Complete" if setup_phase else "Countdown Complete" if countdown_phase else "Not in TD9 State"  

                                if td9_state in ['Setup Complete', 'Countdown Complete']:
                                    return ticker, td9_state, timespan
                                else:
                                    return None
                            except Exception as e:
                                print(f'error - finished scan?')

                                                
                                        
                    else:
                        # Handle the case where the data is not in the expected format
                        print(f"No data available for {ticker} or unexpected response format.")
                        return None
                except KeyError as e:
                    # Log the error
                    print(f"KeyError encountered while processing {ticker}: {e}")
                    return None

    async def candle(self, ticker: str, timespan: str, count: str = '800'):
        """
        Fetch candlestick data and convert it to a DataFrame.
        """
        ticker_id = await self.get_ticker_id(ticker)
        endpoint = f"https://quotes-gw.webullfintech.com/api/quote/charts/query-mini?tickerId={ticker_id}&type={timespan}&count={count}&restorationType=0"

        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(endpoint)
            data = response.json()

        if isinstance(data, list) and len(data) > 0 and 'data' in data[0]:
            raw_data = data[0]['data']
            rows = [d.split(',') for d in raw_data]
            df = pd.DataFrame(rows, columns=['timestamp', 'open', 'close', 'high', 'low', 'close_adjusted', 'volume', 'unknown'])
            df['ticker'] = ticker
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df['timespan'] = timespan
            df[['open', 'close', 'high', 'low', 'close_adjusted', 'volume']] = df[['open', 'close', 'high', 'low', 'close_adjusted', 'volume']].apply(pd.to_numeric)

            return df
        else:
            print('Error')
    async def async_scan_td9(self, symbol, interval):
        try:
            td9_state = await self.async_get_td9(symbol, interval=interval)
            return symbol, td9_state
        except Exception as e:
            # Handle exceptions, you might want to log this
            print(f"Error processing {symbol}: {e}")
            return symbol, None
        
    async def async_get_all_td9_for_timespan(self, interval):
        tickers = self.most_active_tickers  # Ensure this is a list of ticker symbols
        results = []

        async def get_td9_for_symbol(symbol):
            try:
                _, td9_state = await self.async_scan_td9(symbol, interval)
                if td9_state is not None:
                    return (symbol, td9_state, interval)
            except Exception as e:
                print(f"Error retrieving result for {symbol}: {e}")
            return None

        tasks = [get_td9_for_symbol(symbol) for symbol in tickers]
        completed_tasks = await asyncio.gather(*tasks)

        for task_result in completed_tasks:
            if task_result is not None:
                results.append(task_result)

        return results