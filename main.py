from aiohttp import web
import json
from converter import Converter

routes = web.RouteTableDef()


@routes.post('/exchange/{base}/{amount}/{sym}')
async def exchange(request):
    try:
        base = request.match_info.get('base')
    except KeyError:
        response_obj = {'status': 'failed', 'reason': "Конвертируемая валюта не найдена!"}
        return web.Response(text=json.dumps(response_obj, ensure_ascii=False), status=400)
    try:
        sym = request.match_info.get('sym')
    except KeyError:
        response_obj = {'status': 'failed', 'reason': "Валюта, в которую Вы пытаетесь конвертировать, не найдена!"}
        return web.Response(text=json.dumps(response_obj, ensure_ascii=False), status=400)
    try:
        amount = request.match_info.get('amount')
    except KeyError:
        response_obj = {'status': 'failed', 'reason': 'Не удалось обработать количество!'}
        return web.Response(text=json.dumps(response_obj, ensure_ascii=False), status=400)
    if base == sym:
        response_obj = {'status': 'failed', 'reason': "Невозможно перевести одинаковые валюты!"}
        return web.Response(text=json.dumps(response_obj, ensure_ascii=False), status=400)
    try:
        amount = float(amount.replace(",", "."))
    except ValueError:
        response_obj = {'status': 'failed', 'reason': "Введите количество валюты в числовом эквиваленте!"}
        return web.Response(text=json.dumps(response_obj, ensure_ascii=False), status=400)
    try:
        result = f"Цена {amount} {base} в {sym} : {Converter.get_price(base, amount, sym)}"
        response_obj = str(result)
        return web.Response(text=response_obj, status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj, ensure_ascii=False))

app = web.Application()
app.add_routes(routes)
web.run_app(app)
