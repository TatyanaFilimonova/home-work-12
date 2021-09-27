# home-work-12

Personal news feed build on AIOHTTP framework.

Set of sources stored at settings.py.

All the sources collected and parsed in courutines.

Disclamer: HTMLparser isn't really async, because feed() method call to methods that really are blocking. 
To awoid this there are 2 option: to rewrite of HTMLparser class totlly  or to try find already customized one from third part.

I didn't find the requirement to awoid blocking operations at all in HW12 description, so I've decided to left it as is.
