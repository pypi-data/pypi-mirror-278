import asyncio
import httpx
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
import pandas as pd


class FastcaseSDK:
    def __init__(self):
        self.cookie = { 
            'Cookie': '_ga=GA1.3.1707591214.1707962538; _ga_QCWE37JRKM=deleted; __utmc=232144587; _ga_DNNRRPT9DZ=GS1.1.1714196826.1.0.1714196826.60.0.0; _ga_0X3Z0RSVQY=GS1.1.1714454173.5.0.1714454173.0.0.0; _ga_2V6G2TT2M3=GS1.1.1714573656.41.0.1714573656.0.0.0; _gid=GA1.2.681508992.1714196788; __utma=232144587.1707591214.1707962538.1714629627.1714661861.32; __utmz=232144587.1714661861.32.32.utmcsr=sll.texas.gov|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=232144587.1.10.1714661861; ezproxy=JL2g1CdPfdoLuKs; ezproxyl=JL2g1CdPfdoLuKs; ezproxyn=JL2g1CdPfdoLuKs; _ga_QCWE37JRKM=GS1.1.1714661857.44.1.1714661863.54.0.0; _ga=GA1.2.1707591214.1707962538; _gat_gtag_UA_224789_10=1'
        }
        self.token = "mfieVA6RJ7d3pAcxeLaqf65tk3tHGtcpbyee5lrtj6M%3d"
        self.headers = {'user_token': self.token}
        self.db = PolygonDatabase(user='chuck', database='law', password='fud', port=5432, host='localhost')




    
    # async def test(self):
    #     await self.db.connect()
    #     payload = {}
    #     endpoint = f"https://fc7-fastcase-com.ezproxy.sll.texas.gov:2443/searchApi/lookup/document/documentdetails/{universal_id}"

    #     async with httpx.AsyncClient(verify=False) as client:
    #         data = await client.post(endpoint, json=payload, headers=headers)



    async def term_lookup(self, term:str='abuse'):
        endpoint = f"https://fc7-fastcase-com.ezproxy.sll.texas.gov:2443/searchApi/typeahead/terms/{term}"


        async with httpx.AsyncClient(headers=self.cookie,verify=False) as client:

            data = await client.get(endpoint)

            data = data.json()

            for i in data:
                print(i)


    async def document_lookup(self, document:str='abuse'):
        endpoint = f"https://fc7-fastcase-com.ezproxy.sll.texas.gov:2443/searchApi/typeahead/documents/{document}"



        async with httpx.AsyncClient(headers=self.cookie,verify=False) as client:

            data = await client.get(endpoint)

            data = data.json()

            for i in data:
                print(i)


    async def get_cases(self, query):
        counter = 0
        await self.db.connect()
        query = f"\"{query}\""
        endpoint = f"https://fc7-fastcase-com.ezproxy.sll.texas.gov:2443/searchApi/search/results"
        dfs = []
        
        while True:
            counter = counter + 20
            payload = {"q":query,"library":[128,160,15,283],"order":"desc","jdxLibraries":"[{\"jdx\":\"TX\",\"libraries\":[128,160,15,283]}]","selectedJurisdictions":["TX"],"sortBy":1,"skip":counter,"ignoreRegex":True}
            async with httpx.AsyncClient(headers=self.cookie, verify=False) as client:
                data = await client.post(endpoint, data=payload)
                
                response = data.json()
                print(data)
                cited_max = response.get('citedGenerallyMax', None)
                                    



                documents = response.get('documents', [])

                authorityLevel = [i.get('authorityLevel') for i in documents]
                authority_level = [i.get('name') for i in authorityLevel]
                citedGenerally = [i.get('citedGenerally', 0) for i in documents]
                citedHere = [i.get('citedHere') for i in documents]
                date = [i.get('date') for i in documents]
                importDate = [i.get('importDate') for i in documents]
                fullCitation = [i.get('fullCitation') for i in documents]
                identifyingCitations = ', '.join(['; '.join(doc.get('identifyingCitations', [])) for doc in documents])


                jurisdiction = [i.get('jurisdiction') for i in documents]
                libraryType = [i.get('libraryType') for i in documents]
                mostRelevantParagraph = [i.get('mostRelevantParagraph') for i in documents]
                relevance = [i.get('relevance') for i in documents]
                shortName = [i.get('shortName') for i in documents]
                universalFilter = [i.get('universalFilter') for i in documents]
                universalId = [i.get('universalId') for i in documents]
                isbadLaw = ['1' if i.get('isbadLaw') else '0' for i in documents]
                aggregateTreatmentId = [i.get('aggregateTreatmentId') for i in documents]
                showOutline = [i.get('showOutline') for i in documents]
                canBuy = [i.get('canBuy') for i in documents]


                data_dict = { 
                    'date': date,
                    'authority': authority_level,
                    'cited_generally': citedGenerally,
                    'citation': fullCitation,
                    'identifying_citations': identifyingCitations,
                    'short_name': shortName,
                    'relevant_paragraph': mostRelevantParagraph,
                    'is_bad': isbadLaw,
                    'universal_id': universalId,
                    'query': query

                }
        
                df = pd.DataFrame(data_dict)
                print(df)
            
            
        
                df['cited_generally'] = pd.to_numeric(df['cited_generally'], errors='coerce')
                filtered_df = df.loc[(df['is_bad'] == '0') & (df['cited_generally'] > 100)]
                sorted_df = filtered_df.sort_values('cited_generally', ascending=False)

                await self.db.batch_insert_dataframe(sorted_df, table_name='caselaw', unique_columns='universal_id')
                if counter == 2000:
                    break



    async def documents(self, universal_id:str='7694152', input:str='abuse'):

        query = f"""SELECT universal_id FROM caselaw where relevant_paragraph ILIKE '%{input}%'"""


        results = await self.db.fetch(query)


        df = pd.DataFrame(results, columns=['universal_id'])


        print(df)



