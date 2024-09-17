import httpx
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status

import asyncio
import dns.resolver
import re
from typing import List, Dict, Set
from urllib.parse import urlparse, quote_plus
import threading
import concurrent.futures
import random


# oauth =


class SubDomainScrapper:
    def __init__(self, domain: str):
        self.domain = domain
        self.subdomains: Set[str] = set()
        self.session = httpx.AsyncClient()
        self.wildcard_subdomains: Set[str] = set()

    def getHeaders(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    async def search_engine_enumerator(self):
        engines = [
            ("https://google.com/search?q={query}&btnG=Search&hl=en-US&biw=&bih=&gbv=1&start={page_no}&filter=0", 'google'),
            ("https://search.yahoo.com/search?p={query}&b={page_no}", 'yahoo'),
            ("https://www.bing.com/search?q={query}&go=Submit&first={page_no}", 'bing'),
            ('https://www.baidu.com/s?pn={page_no}&wd={query}&oq={query}', 'baidu')
        ]
        for search_engine_url, search_engine in engines:
            page_no = 1
            while page_no <= 5:
                query = quote_plus(f"site:{self.domain} --www.{self.domain}")
                url = search_engine_url.format(query=query, page_no=page_no)

                try:
                    res = await self.session.get(url, headers=self.getHeaders())
                    sub_domain = re.findall(
                        r'(?<=//|\s)(\w+\.' + re.escape(self.domain) + ')', res.text)
                    self.subdomains.update(sub_domain)
                    page_no += 10 if search_engine in ['google', 'bing', 'yahoo', 'baidu'] else 1
                except Exception as e:
                    print(f"Error from source {search_engine} search: {str(e)}")
                    break
                await asyncio.sleep(random.randint(2, 7))


    async def crt_sh_query(self):
        url = f"https://crt.sh/?q=%.{self.domain}&output=json"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                data = response.json()
                
                for entry in data:
                    name_value = entry.get('name_value', '')
                    parts = name_value.split('\n')
                    for part in parts:
                        part = part.strip()
                        if part.endswith(self.domain) and part != self.domain:
                            if part.startswith('*.'):
                                self.wildcard_subdomains.add(part)
                            else:
                                self.subdomains.add(part)
            
            print(f"Found {len(self.subdomains)} regular subdomains and {len(self.wildcard_subdomains)} wildcard subdomains from crt.sh")
        except json.JSONDecodeError:
            print("Error: Invalid JSON response from crt.sh")
        except Exception as e:
            print(f"Error fetching from crt.sh query: {str(e)}")
        
    
    async def dns_query(self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8', '8.8.4.4']
        try:
            results = resolver.resolve(f"*.{self.domain}", 'A')
            for d in results:
                sub_domain = str(d).rstrip('.')
                if sub_domain.endswith(self.domain) and sub_domain != self.domain:
                    self.subdomains.add(sub_domain)
        except Exception as e:
            print(f"Error fetching from dns_query: {str(e)}")
            
    
    async def netcraft_query(self):
        url = f'https://searchdns.netcraft.com/?restriction=site+ends+with&host={
            self.domain}'
        try:
            res = await self.session.get(url, headers=self.getHeaders())
            links = re.findall(
                '<a class="results-table__host" href="(.*?)"', res.text)
            for l in links:
                sub_domain = urlparse(l).netloc
                if sub_domain.endswith(self.domain) and sub_domain != self.domain:
                    self.subdomains.add(sub_domain)
        except Exception as e:
            print(f"Error in netcraft query: {str(e)}")
            
    
    async def dns_dumpster_query(self):
        url = 'https://dnsdumpster.com/'
        try:
            res = await self.session.get(url, headers=self.getHeaders())
            csrf_token = re.search(
                r'name="csrfmiddlewaretoken" value="(.*?)"', response.text).group(1)
            cookie_data = res.cookies
            headers = self.getHeaders()
            headers['Referer'] = url
            data = {
                'csrfmiddlewaretoken': csrf_token,
                'targetip': self.domain
            }
            response = await self.session.post(url, headers=headers, cookies=cookie_data, data=data)
            subdomains = re.findall(
                r'<td class="col-md-4">(.*?)<br>', response.text)
            for d in subdomains:
                if d.endswith(self.domain) and d != self.domain:
                    self.subdomains.add(i.strip())
        except Exception as e:
            print(f"Error in dns_dumpster query: {str(e)}")
    
    async def virustotal_query(self):
        url = f'https://www.virustotal.com/ui/domains/{self.domain}/subdomains'
        try:
            response = await self.session.get(url, headers=self.get_headers())
            data = response.json()
            for item in data.get('data', []):
                if item['type'] == 'domain':
                    subdomain = item['id']
                    if subdomain.endswith(self.domain) and subdomain != self.domain:
                        self.subdomains.add(subdomain)
        except Exception as e:
            print(f"Error in VirusTotal query: {str(e)}")


    async def threatcrowd_query(self):
        url = f'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={self.domain}'
        try:
            response = await self.session.get(url, headers=self.get_headers())
            data = response.json()
            for subdomain in data.get('subdomains', []):
                if subdomain.endswith(self.domain) and subdomain != self.domain:
                    self.subdomains.add(subdomain)
        except Exception as e:
            print(f"Error in ThreatCrowd query: {str(e)}")
    
    async def passivedns_query(self):
        url = f'https://api.sublist3r.com/search.php?domain={self.domain}'
        try:
            response = await self.session.get(url, headers=self.get_headers())
            subdomains = response.json()
            for subdomain in subdomains:
                if subdomain.endswith(self.domain) and subdomain != self.domain:
                    self.subdomains.add(subdomain)
        except Exception as e:
            print(f"Error in PassiveDNS query: {str(e)}")
    
    def get_all_subdomains(self) -> List[str]:
        return sorted(list(self.subdomains.union(self.wildcard_subdomains)))
    
    async def run_all_query_async(self):
        tasks = [
            # self.search_engine_enumerator(),
            self.crt_sh_query(),
            # self.dns_query(),
            # self.netcraft_query(),
            # self.dns_dumpster_query(),
            # self.passivedns_query(),
            # self.threatcrowd_query(),
            # self.virustotal_query()
        ]
        await asyncio.gather(*tasks)
        await self.session.aclose()
        return list(self.subdomains)


async def get_subdomain_data(domain:str) -> Dict[str, List[str]]:
    try:
        parsed_domain = urlparse(f"http://{domain}").netloc
        res = SubDomainScrapper(parsed_domain)
        # await scrapper.crt_sh_query()
        data = await res.run_all_query_async()

        all_subdomains = res.get_all_subdomains()
        return {
            "domain": domain,
            # "subdomains": all_subdomains,
            "count": len(all_subdomains),
            "regular": sorted(list(res.subdomains)),
            "wildcards": sorted(list(res.wildcard_subdomains))
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
