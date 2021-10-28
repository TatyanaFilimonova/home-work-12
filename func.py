import logging
import time

import aiohttp
import asyncio
import re
from datetime import datetime
import db
from db import mention


async def get_resources(app):
    # возвращает из БД список словарей [{'id': XX, 'name': 'Glavrom', 'url': 'https://gla.....'}]
    async with app['db'].begin() as conn:
        cursor = await conn.execute(db.resource.select())
        records = cursor.fetchall()
        return [dict(s) for s in records]


async def get_scpoes(app):
    # возвращает из БД сок словарей [{'id_scope': XX, 'name': 'Меркель', 'scope': ['Меркель', 'Бундестаг' ,.....'], ...}]
    async with app['db'].begin() as conn:
        cursor = await conn.execute(db.word_scope.select())
        records = cursor.fetchall()
        scopes = [dict(s) for s in records]
        print('scopes = ', scopes)
        return [{'id': scope['id'], 'name': scope['name'], 'scope': scope['scope'].split()} for scope in scopes]


async def put_data_to_db(app, data):
    # полученные данные data записывает в БД, соединение к которой хранится в app['db']
    async with app['db'].begin() as conn:
        await conn.execute(mention.insert(), data)


def get_table_data(data):
    # конвертирует данные data формата get_data() в формат
    # --> {resource_name_1: {scope_1: res 1,
    #                       scope_2: res_2,
    #                       .............},
    #      resource_name_2: {scope_1: res 1,
    #                       scope_2: res_2,
    #                       .............},
    #     ...............................}
    table_data = {}
    for result in data:
        if not result['resource_name'] in table_data:
            table_data[result['resource_name']] = {}
        table_data[result['resource_name']
                   ][result['scope_name']] = result['result']
    return table_data

async def get_data(resources, scopes):
    # асинхнхронно делает запросы к ресурсам из resources и считает число повторений каждого элемента
    # темы scope['id'] по словам списка scope['scope'] и возвращает список словарей:
    # results = [{'datetime': XXX, 'scope_name': ZZZ, 'resource_name': YYY, 'result': FFF},
    #           {...}, ...]
    async with aiohttp.ClientSession() as session:
        with open('get_data_async.log', 'w') as log:
            time = datetime.now()
            results = []
            task_lst = []
            for resource in resources:
                task_lst.append(asyncio.create_task(
                    get_mentions(resource, scopes, log, session=session)))
            result = await asyncio.gather(*task_lst, loop=None, return_exceptions=False)
            for res in result:
                for res1 in res:
                    results.append(res1)
            print(f'Consumed time = {datetime.now()-time}')
            return results

async def get_response(url, session):
    try:
        print(f'Start loading URl {url}')
        async with session.get(url) as response:
            assert response.status == 200
            resp = await response.text()
            print(f'Finish loading URl {url}')
            return resp
    except TimeoutError:
        return None

async def get_calc(source, scopes, resource):
    result = []
    print('Start to calc mentions fo url ' + str(resource['url']) + '\n')
    for scope in scopes:
        res = sum([len(re.findall(word, source))
                   for word in scope['scope']])
        result.append(
            {
                'datetime': datetime.now().replace(microsecond=0),
                'scope_name': scope['name'],
                'resource_name': resource['name'],
                'result': res
            })
    print('Finished to calc mentions fo url ' + str(resource['url']) + '\n')
    return result

async def get_mentions(resource, scopes, log, session):
    result = []
    try:
        source = await get_response(resource['url'], session)
        result = await get_calc(source, scopes, resource)
    except Exception as ex:
        print(f'ошибка в функции get_mentions(): {ex}')
    return result


