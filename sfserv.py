from bottle import route, run, HTTPError, request
import work


def save_album(user_data):
    """Парсит POST запрос, проверяет дату на валидность, добавляет запись в БД
    В зависимости от используемой командной строки запрос может выглядеть так:
    /albums year=2010 "artist='John Dove'" genre='unknown' "album='new album'"
    Если в значении есть пробелы - используй кавычки вокруг всего параметра ("artist='John Dove'")

    """
    year   = user_data['year']  # в запросе year передавать как int, без кавычек
    artist = user_data['artist']
    genre  = user_data['genre']
    album  = user_data['album']
    if year.isdigit() and len(year) == 4:
        new_alb = work.Album(year=year, artist=artist, genre=genre, album=album)
    else:
        raise TypeError('Invalid arguments. Year should be in XXXX format')
    work.add(new_alb)


@route('/')
def hello():
    return f'Привет! Используй из терминала POST /albums/ year=год "artist=\'исполнитель'" \"genre='жанр'"' \
                     '"album='альбом' для записи нового альбома, " \
           "из браузера или из терминала GET /albums/artist для поиска существующих альбомов"


@route('/albums/', method='POST')  # ,
def album():
    """Для POST запросов использовать терминал. (http/httpie)"""
    try:
        album_data = {
            'year': request.forms.get('year'),
            'artist': request.forms.get('artist'),
            'genre': request.forms.get('genre'),
            'album': request.forms.get('album')
        }
        save_album(album_data)
    except AttributeError as er:
        print('Данные переданы в неверном формате. Проверь кавычки', er)
        return f'Данные переданы в неверном формате. Проверь кавычки "year=год" "artist=\'исполнитель'" \"genre='жанр'"' \
                     '"album='альбом''", f'<br>{er}'


@route('/albums/<artist>', method='GET')
def find_art(artist):
    """Функция поиска артиста через GET запрос"""
    albums_list = work.find(artist)
    if not albums_list:
        message = f'Альбомов {artist} не найдено'
        result = HTTPError(404, message)
        album_len = 'Количество альбомов - 0'
    else:
        album_names = [album.album for album in albums_list]
        result = f'<h2>Список альбомов {artist}:</h2><br>'
        result += f"<br>".join(album_names)
        album_len = f'<br>Количество альбомов - {len(album_names)}'
    return result, album_len


"""!!!Используется сервер paste, возможно придется установить его (pip install paste)"""

if __name__ == '__main__':
    try:
        run(server='paste', host='localhost', port=8090, debug=True)
    except OSError as oe:
        print('Change port for server', oe)
