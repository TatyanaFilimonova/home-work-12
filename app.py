import aiohttp_jinja2
import jinja2
from aiohttp import web
import aiohttp
import os
import asyncio

from settings import urls_dict
from get_content2 import *


@aiohttp_jinja2.template('index.html')
async def feed(request):

    async with aiohttp.ClientSession() as session:
        task_lst = []
        for key in urls_dict.keys():
            task_lst.append(asyncio.create_task(
                get_content(
                            urls_dict[key]['url'],
                            ParserCls=globals()[urls_dict[key]['parser']],
                            session=session)))
        feed = await asyncio.gather(*task_lst, loop=None, return_exceptions=False)
        return {'feed': feed}


# RUN async application 
if __name__ == "__main__":
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')
    app = web.Application()
    app.add_routes([web.get('/', feed)])
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(TEMPLATE_PATH)
    )
    web.run_app(app, port=5000, host='127.0.0.1')
