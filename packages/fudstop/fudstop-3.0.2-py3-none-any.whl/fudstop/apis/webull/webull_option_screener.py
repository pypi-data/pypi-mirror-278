import httpx
import asyncio
from fudstop.apis.webull.webull_trading import WebullTrading
from fudstop.apis.webull.screener_models import OptionScreenerResults
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop.apis.webull.webull_paper_trader import PaperTrader
from fudstop.apis.webull.option_data import VolumeAnalysisDatas, OptionDataFromIDs
from webull.webull import webull
import aiohttp
import pandas as pd
trader = PaperTrader()

class WebullOptionScreener:
    def __init__(self):
        self.rules = {}
        self.fetch_size = 200
        self.trading = WebullTrading()
        self.wb = webull()
        self.db = PolygonDatabase(host='localhost', user='chuck', database='market_data')

        self.headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Access_token": "dc_us_tech1.18fcb79ee76-acec7fc3ba504ffd8f74511b585c1ae2",
        "App": "global",
        "App-Group": "broker",
        "Appid": "wb_web_app",
        "Content-Type": "application/json",
        "Device-Type": "Web",
        "Did": "9eaa43b1dcea4c069c8989d25c467e67",
        "Dnt": "1",
        "Hl": "en",
        "Locale": "eng",
        "Origin": "https://app.webull.com",
        "Os": "web",
        "Osv": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Ph": "Windows Chrome",
        "Platform": "web",
        "Priority": "u=1, i",
        "Referer": "https://app.webull.com/",
        "Reqid": "027d2a3b119a406c8fca76d785b84c33",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "T_time": "1717109282497",
        "Tz": "America/Chicago",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Ver": "4.6.4",
        "X-S": "4b251ee4db2c0edc8121cc4c705d48d4621b76f98e4061305186d34b53ddcc64",
        "X-Sv": "xodp2vg9"
    } 
    async def get_token(self):
        endpoint = f"https://u1suser.webullfintech.com/api/user/v1/login/account/v2"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.post(endpoint, json={"account":"CHUCKDUSTIN12@GMAIL.COM","accountType":"2","pwd":"fb050b003c6d84da626a4f53f8a1b400","deviceId":"gldaboazf4y28thligawz4a7xamqu91g","deviceName":"Windows Chrome","grade":1,"regionId":1})
        data = data.json()
        token = data.get('accessToken')
        print(token)
        return token

    
    async def get_headers(self):
        headers = self.wb.build_req_headers()
        headers.update({"Access-Token": await self.get_token()})

        return headers

    async def add_rule(self, rule_type, gte_value=None, lte_value=None):
        rule_key = f"options.screener.rule.{rule_type}"
        if gte_value is not None and lte_value is not None:
            self.rules[rule_key] = f"gte={gte_value}&lte={lte_value}"
        elif gte_value is not None:
            self.rules[rule_key] = f"gte={gte_value}"
        elif lte_value is not None:
            self.rules[rule_key] = f"lte={lte_value}"
        print(f"Added rule {rule_key}: {self.rules[rule_key]}")  # Debug print



    async def add_source(self, sources):
        ticker_id = await self.trading.get_ticker_id(sources)
        self.rules["options.screener.rule.source"] = ticker_id
        print(f"Added source: {sources}")  # Debug print

    async def construct_payload(self):
        return {
            "filter": self.rules,
            "page": {"fetchSize": 500}
        }

    async def convert_to_decimal(self, value):
        return value / 100 if value is not None else None

    async def construct_payload(self):
        return {
            "filter": self.rules,
            "page": {"fetchSize": self.fetch_size}
        }
    
    def convert_to_decimal(self, value):
        return value / 100 if value is not None else None
    async def screener(self, **params):
        """
        Execute an options screener with the given parameters.

        Possible Parameters:
        :param expireDate_gte: int, Minimum expiration date.
        :param expireDate_lte: int, Maximum expiration date.
        :param volume_gte: int, Minimum volume.
        :param volume_lte: int, Maximum volume.
        :param openInterest_gte: int, Minimum open interest.
        :param openInterest_lte: int, Maximum open interest.
        :param delta_gte: float, Minimum delta.
        :param delta_lte: float, Maximum delta.
        :param source: list, List of sources.
        :param tickerImplVol_gte: float, Minimum implied volatility of the ticker.
        :param tickerImplVol_lte: float, Maximum implied volatility of the ticker.
        :param ivPercent_gte: float, Minimum implied volatility percentage.
        :param ivPercent_lte: float, Maximum implied volatility percentage.
        :param hisVolatility_gte: float, Minimum historical volatility.
        :param hisVolatility_lte: float, Maximum historical volatility.
        :param pulseIndex_gte: float, Minimum pulse index.
        :param pulseIndex_lte: float, Maximum pulse index.
        :param avg30Volume_gte: int, Minimum average 30-day volume.
        :param avg30Volume_lte: int, Maximum average 30-day volume.
        :param totalVolume_gte: int, Minimum total volume.
        :param totalVolume_lte: int, Maximum total volume.
        :param totalOpenInterest_gte: int, Minimum total open interest.
        :param totalOpenInterest_lte: int, Maximum total open interest.
        :param avg30OpenInterest_gte: int, Minimum average 30-day open interest.
        :param avg30OpenInterest_lte: int, Maximum average 30-day open interest.
        :param direction: str, Option direction.
        :param bid_gte: float, Minimum bid price.
        :param bid_lte: float, Maximum bid price.
        :param changeRatio_gte: float, Minimum change ratio.
        :param changeRatio_lte: float, Maximum change ratio.
        :param ask_gte: float, Minimum ask price.
        :param ask_lte: float, Maximum ask price.
        :param close_gte: float, Minimum close price.
        :param close_lte: float, Maximum close price.
        :param gamma_gte: float, Minimum gamma.
        :param gamma_lte: float, Maximum gamma.
        :param rho_gte: float, Minimum rho.
        :param rho_lte: float, Maximum rho.
        :param theta_gte: float, Minimum theta.
        :param theta_lte: float, Maximum theta.
        :param implVol_gte: float, Minimum implied volatility.
        :param implVol_lte: float, Maximum implied volatility.
        :param vega_gte: float, Minimum vega.
        :param vega_lte: float, Maximum vega.
        :param probITM_gte: float, Minimum probability of being in the money.
        :param probITM_lte: float, Maximum probability of being in the money.
        :param leverageRatio_gte: float, Minimum leverage ratio.
        :param leverageRatio_lte: float, Maximum leverage ratio.

        :return: OptionScreenerResults object containing the results of the screener.
        """
        if 'expireDate_gte' in params or 'expireDate_lte' in params:
            await self.add_rule("expireDate", params.get('expireDate_gte'), params.get('expireDate_lte'))
        if 'volume_gte' in params or 'volume_lte' in params:
            await self.add_rule("volume", params.get('volume_gte'), params.get('volume_lte'))
        if 'openInterest_gte' in params or 'openInterest_lte' in params:
            await self.add_rule("openInterest", params.get('openInterest_gte'), params.get('openInterest_lte'))
        if 'delta_gte' in params or 'delta_lte' in params:
            await self.add_rule("delta", params.get('delta_gte'), params.get('delta_lte'))
        if 'source' in params:
            await self.add_source(sources=params.get('source'))
        if 'tickerImplVol_gte' in params or 'tickerImplVol_lte' in params:
            await self.add_rule("tickerImplVol", params.get('tickerImplVol_gte'), params.get('tickerImplVol_lte'))
        if 'ivPercent_gte' in params or 'ivPercent_lte' in params:
            await self.add_rule("ivPercent", await self.convert_to_decimal(params.get('ivPercent_gte')), await self.convert_to_decimal(params.get('ivPercent_lte')))
        if 'hisVolatility_gte' in params or 'hisVolatility_lte' in params:
            await self.add_rule("hisVolatility", params.get('hisVolatility_gte'), params.get('hisVolatility_lte'))
        if 'pulseIndex_gte' in params or 'pulseIndex_lte' in params:
            await self.add_rule("pulseIndex", await self.convert_to_decimal(params.get('pulseIndex_gte')), await self.convert_to_decimal(params.get('pulseIndex_lte')))
        if 'avg30Volume_gte' in params or 'avg30Volume_lte' in params:
            await self.add_rule("avg30Volume", params.get('avg30Volume_gte'), params.get('avg30Volume_lte'))
        if 'totalVolume_gte' in params or 'totalVolume_lte' in params:
            await self.add_rule("totalVolume", params.get('totalVolume_gte'), params.get('totalVolume_lte'))
        if 'totalOpenInterest_gte' in params or 'totalOpenInterest_lte' in params:
            await self.add_rule("totalOpenInterest", params.get('totalOpenInterest_gte'), params.get('totalOpenInterest_lte'))
        if 'avg30OpenInterest_gte' in params or 'avg30OpenInterest_lte' in params:
            await self.add_rule("avg30OpenInterest", params.get('avg30OpenInterest_gte'), params.get('avg30OpenInterest_lte'))
        if 'direction' in params:
            await self.add_rule("direction", params.get('direction'))
        if 'bid_gte' in params or 'bid_lte' in params:
            await self.add_rule("bid", params.get('bid_gte'), params.get('bid_lte'))
        if 'changeRatio_gte' in params or 'changeRatio_lte' in params:
            await self.add_rule("changeRatio", await self.convert_to_decimal(params.get('changeRatio_gte')), await self.convert_to_decimal(params.get('changeRatio_lte')))
        if 'ask_gte' in params or 'ask_lte' in params:
            await self.add_rule("ask", params.get('ask_gte'), params.get('ask_lte'))
        if 'close_gte' in params or 'close_lte' in params:
            await self.add_rule("close", params.get('close_gte'), params.get('close_lte'))
        if 'gamma_gte' in params or 'gamma_lte' in params:
            await self.add_rule("gamma", params.get('gamma_gte'), params.get('gamma_lte'))
        if 'rho_gte' in params or 'rho_lte' in params:
            await self.add_rule("rho", params.get('rho_gte'), params.get('rho_lte'))
        if 'theta_gte' in params or 'theta_lte' in params:
            await self.add_rule("theta", params.get('theta_gte'), params.get('theta_lte'))
        if 'implVol_gte' in params or 'implVol_lte' in params:
            await self.add_rule("implVol", await self.convert_to_decimal(params.get('implVol_gte')), await self.convert_to_decimal(params.get('implVol_lte')))
        if 'vega_gte' in params or 'vega_lte' in params:
            await self.add_rule("vega", params.get('vega_gte'), params.get('vega_lte'))
        if 'probITM_gte' in params or 'probITM_lte' in params:
            await self.add_rule("probITM", await self.convert_to_decimal(params.get('probITM_gte')), await self.convert_to_decimal(params.get('probITM_lte')))
        if 'leverageRatio_gte' in params or 'leverageRatio_lte' in params:
            await self.add_rule("leverageRatio", params.get('leverageRatio_gte'), params.get('leverageRatio_lte'))

        
        payload = await self.construct_payload()
        print("Constructed Payload:", payload)
        async with httpx.AsyncClient(headers=self.headers) as client:


            data = await client.post("https://quotes-gw.webullfintech.com/api/wlas/option/screener/query", json=payload)

            data = data.json()

            datas = data['datas']

            print(len(datas))


            return OptionScreenerResults(datas)
        

    async def get_option_data_from_ids(self, option_id):

        endpoint=f"https://quotes-gw.webullfintech.com/api/quote/option/quotes/queryBatch?derivativeIds={option_id}"
        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.get(endpoint)
            data = data.json()
            
            data_from_ids = OptionDataFromIDs(data)
            return data_from_ids.data_dict


    async def high_oi(self, ticker=None, open_interest_gte=None, open_interest_lte=None) -> pd.DataFrame:
        try:
            params = {}
            if ticker is not None:
                source = await self.trading.get_ticker_id(ticker)
                params['source'] = [source]
            if open_interest_gte is not None:
                params['openInterest_gte'] = open_interest_gte
            if open_interest_lte is not None:
                params['openInterest_lte'] = open_interest_lte

            data = await self.screener(**params)

            ids = data.tickerId
            all_data = []
            tasks = [self.get_option_data_from_ids(i) for i in ids]

            results = await asyncio.gather(*tasks)

            async with httpx.AsyncClient(headers=self.headers) as client:
                for id, result in zip(ids, results):
                    try:
                        response = await client.get(f"https://quotes-gw.webullfintech.com/api/statistic/option/queryVolumeAnalysis?count=800&tickerId={id}")
                        data = response.json()

                        avgPrice = data.get('avgPrice')
                        buyVolume = data.get('buyVolume')
                        dates = data.get('dates')
                        neutralVolume = data.get('neutralVolume')
                        sellVolume = data.get('sellVolume')
                        totalNum = data.get('totalNum')
                        totalVolume = data.get('totalVolume')

                        data_dict = {
                            'avg_price': avgPrice,
                            'buy_vol': buyVolume,
                            'neut_vol': neutralVolume,
                            'sell_vol': sellVolume,
                            'total_vol': totalVolume,
                            'trades': totalNum,
                        }

                        # Merge the two dictionaries
                        result.update(data_dict)
                        all_data.append(result)
                    except Exception as e:
                        print(f"Error processing ticker ID {id}: {e}")

            df = pd.DataFrame(all_data)
            return df

        except Exception as e:
            print(e)
            return pd.DataFrame()
        


    async def fetch_option_data(self, session, id):
        async with session.get(f"https://quotes-gw.webullfintech.com/api/statistic/option/queryVolumeAnalysis?count=800&tickerId={id}") as response:
            data = await response.json()
            return id, data

    async def opt_multi_vol_analysis(self, ids, conn=None):
        all_data = []
        tasks = [self.get_option_data_from_ids(i) for i in ids]
        results = await asyncio.gather(*tasks)

        async with aiohttp.ClientSession(headers=self.headers) as session:
            fetch_tasks = [self.fetch_option_data(session, id) for id in ids]
            fetch_results = await asyncio.gather(*fetch_tasks)

        for id, data in fetch_results:
            try:
                avgPrice = data.get('avgPrice')
                buyVolume = data.get('buyVolume')
                dates = data.get('dates')
                neutralVolume = data.get('neutralVolume')
                sellVolume = data.get('sellVolume')
                totalNum = data.get('totalNum')
                totalVolume = data.get('totalVolume')

                data_dict = {
                    'avg_price': avgPrice,
                    'buy_vol': buyVolume,
                    'neut_vol': neutralVolume,
                    'sell_vol': sellVolume,
                    'total_vol': totalVolume,
                    'trades': totalNum,
                }

                if conn is not None:
                    async with self.db_pool.acquire() as connection:
                        await connection.execute("""
                            UPDATE wb_opts 
                            SET trades = $1, total_vol = $2, avg_price = $3, buy_vol = $4, neut_vol = $5, sell_vol = $6 
                            WHERE option_id = $7
                        """, data_dict.get('trades'), data_dict.get('total_vol'), data_dict.get('avg_price'), 
                        data_dict.get('buy_vol'), data_dict.get('neut_vol'), data_dict.get('sell_vol'), id)

                result = next(item for item in results if item['option_id'] == id)
                result.update(data_dict)
                all_data.append(result)
            except Exception as e:
                print(f"Error processing ticker ID {id}: {e}")

        df = pd.DataFrame(all_data)
        
        await self.update_options_table(df)
        return df
    

    async def update_options_table(self, df):
        update_query = """
        UPDATE wb_opts
        SET avg_price = $1, buy_vol = $2, neut_vol = $3, sell_vol = $4, total_vol = $5, trades = $6
        WHERE option_symbol = $7;
        """
        
        # Connect to the database
        db = PolygonDatabase()  # Make sure this is defined elsewhere in your code
        await db.connect()
        
        for _, row in df.iterrows():
            await db.execute(update_query, row['avg_price'], row['buy_vol'], row['neut_vol'], row['sell_vol'], row['total_vol'], row['trades'], row['option_symbol'])
        
        await db.close()