import socket
from views import *

URLS = {
    '/': index,
    '/custom': custom
}


def parse_request(request):
    # Получаем метод и url запроса
    parsed = request.split(' ')
    method = 'GET'
    url = '/'
    try:
        method = parsed[0]
        url = parsed[1]
    except:
        pass
    return method, url


def generate_headers(method, url):
    # Правильный ли метод запроса был получен
    if not method == 'GET':
        return 'HTTP/1.1 405 Method not allowed\n\n', 405

    # Есть ли нужный путь в глобальном словаре
    if url not in URLS:
        return 'HTTP/1.1 404 Not found\n\n', 404

    return 'HTTP/1.1 200 Ok\n\n', 200


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'

    # return '<h1>{}</h1>'.format(URLS[url])
    return URLS[url]()


def generate_response(request):
    # Парсинг полученного запроса
    method, url = parse_request(request)

    # Ответ будет состоять из кода/заголовков/тела
    headers, code = generate_headers(method, url)
    # Тело с полезной нагрузкой в ввиде html-страницы
    body = generate_content(code, url)
    response = (headers + body).encode()
    return response


def run():
    # Создание сокета. Указывание какие протоколы он будет использовать
    # AF_INET - ipv4 | SOCK_STREAM - tcp
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Настройка сокета перед его связью с адресом и портом
    # Включение возможности повторного использования порта
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Связь сокета с переданными адресом, портом
    server_socket.bind(('localhost', 5678))

    # Прослушивание порта
    server_socket.listen()

    # Бесконечный цикл. Пока соединение не разорвано идет общение с клиентом
    while True:
        # Принятие подключения. Метод accept возвращает кортеж (новый сокет, адрес клиента)
        # Именно этот сокет и будет использоваться для приема и посылке клиенту данных.
        client_socket, address = server_socket.accept()

        # Получение данных от клиента пакетами по 1024 байта (запрос клиента)
        request = client_socket.recv(1024)

        # Так как ответ приходит в виде bytes, его требуется раскодировать
        # Вывод полного адреса клиента, декодированного ответа
        print(address, client_socket, request.decode('utf-8'))

        # Генерация ответа на полученный запрос
        response = generate_response(request.decode('utf-8'))

        # ### Кодировка данных в bytes, метод sandall принимает только набор байтов
        # ### data_to_sand = 'hello world'.encode()

        # Отправка клиенту ответа
        client_socket.sendall(response)

        # Пока соединение не закрыто ничего не произойдет
        client_socket.close()


if __name__ == '__main__':
    run()
    # print_hi('PyCharm')
