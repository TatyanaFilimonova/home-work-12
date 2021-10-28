# home-work-12


Personal news feed build on AIOHTTP framework.

Set of sources stored at settings.py.

All the sources collected and parsed in corutines.

Disclamer: HTMLparser isn't really async, because feed() method call to methods that really are blocking. 
To avoid this there are 2 option: 

    - rewrite the HTMLparser class totally

    - try to find already customized one.

I didn't find the requirement to avoid blocking operations at all in HW12 description. So I've decided to left it as is.

So run app.py and find the feed on http://127.0.0.1:5000
