import mutagen.id3
from mutagen.id3 import ID3
import vk_api, csv
import time
import winsound
import pyperclip

# Оно, особо, никому не надо, даже мне, скрипт отработал,
# Посему оставлю в таком первозданно-костыльном виде,
# Вдруг кому пригодится :)

# ==================================================|  Data  |========================================================#

login, password = '', '' # Логин, пасс от вк
token = '' # Токен доступа
musicListId = r''# Путь до таблицы со списком загруженных песен
musicPathList = r''# Путь до списка с расположением локальных песен
playlistMusicList = r'' # Путь до таблицы с расположение песен для плейлиста
bannedMusicList = r'' # Путь до списка забаненных песен

ownerId = 272230679 # id владельца страницы вк
plstId = 0 # id плейлиста
delay = 2 # Задержка между сообщениями
isAdd = 0 # 0 - загрузка песен, 1 - добавление в плейлист

# ==================================================|  Functions  |=================================================== #

def captcha_handler(captcha):
    duration = 500
    freq = 500
    winsound.Beep(freq, duration)
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

def editCsv(title, artist, id, owner, path, musicListId):
    with open(musicListId, 'a', encoding='utf8') as file:
        file.write("{} - {},{},{},{}".format(title, artist, id, owner, path))
        file.write("\n")

def pause():
    print('Stopped: ')

    duration = 500
    freq = 500
    winsound.Beep(freq, duration)

    a = input()
    if a == 'q':
        a = nxt
    try:
        return int(a)
    except:
        pass

def msg(type, text):
    if type == 1:
        print("\033[1m\033[37m•[\033[35m{}\033[37m]: \033[32m✔\033[0m".format(text))
    else:
        print("\033[1m\033[37m•[\033[31m{}\033[37m]: \033[31m✘ Error\033[0m".format(text))

# ==================================================|  Auth  |======================================================== #

vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)
try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_session.get_api()
upload = vk_api.VkUpload(vk_session)

# ==================================================|  Main  |======================================================== #

if isAdd == 0: # def main(): Для лохов :) Если кому-то нужен хоть, черканите в лс vk.com/frvctv1, сделаю нормально, без костылей
    nxt = 0
    with open(musicPathList, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            skp = 0
            path = row['msc']
            print("\033[1m\033[36m{}\033[0m".format(path))
            tags = ID3(path)
            try:
                title = mutagen.File(path).get('TIT2')
                artist = mutagen.File(path).get('TPE1')
                msg(1, 'Tit2Tag')
            except:
                msg(0, 'Tit2Tag')
                pause()

            try:
                response = upload.audio(path, artist, title)
                msg(1, 'fUpload')
            except:
                msg(0, 'fUpload')
                pyperclip.copy(str(artist) + ' - ' + str(title))
                id = pause()
                owner = ownerId
                skp = 1

# =================================================|  Add Song  |===================================================== #

            if skp == 0:
                id = response['id']
                strId = response['id']
                owner = ownerId
                try:
                    if response['id'] != 0:
                        msg(1, 'msAdded')
                        nxt = int(id) + 1
                except:
                        msg(0, 'msAdded')

# =================================================|  Csv Write  |==================================================== #

            try:
                editCsv(title, artist, id, owner, path, musicListId)
                msg(1, 'CsvRecs')
            except:
                msg(0, 'CsvRecs')
                pause()

# =================================================|  Add Tags  |===================================================== #

            try:
                tags.add(mutagen.id3.TXXX(encoding=3, desc=u'id', text=str(id)))
                tags.add(mutagen.id3.TXXX(encoding=3, desc=u'owner_id', text=str(owner)))
                tags.save(path)
                msg(1, 'TxxxTag')
            except:
                msg(0, 'TxxxTag')
                pause()

# =================================================|  Results  |====================================================== #
            if skp == 0:
                print("\033[1m\033[37m[\033[35m{} \033[37m- \033[35m{}\033[37m] [\033[36m{} \033[37m- \033[36m{}\033[37m] [\033[35m{}\033[37m]\033[0m".format(id, owner, response['title'], response['artist'], mutagen.File(path).get('TXXX:id')))
            else:
                print("\033[1m\033[37m[\033[35m{} \033[37m- \033[35m{}\033[37m] [\033[36m{} \033[37m- \033[36m{}\033[37m] [\033[35m{}\033[37m]\033[0m".format(id, owner, title, artist, mutagen.File(path).get('TXXX:id')))

                time.sleep(delay)
else:
    try:
        with open(playlistMusicList, newline='', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            for row in reader:
                try:
                    path = row['msc']
                    print("\033[1m\033[36m{}\033[0m".format(path))
                    tags = ID3(path)
                    id2 = str(mutagen.File(path).get('TXXX:id'))
                    rspns = vk.audio.add(audio_id=int(id2), owner_id=272230679, playlist_id=plstId, access_token=token, v=5.126)
                    if rspns != 0:
                        print('\033[32m✔')
                    else:
                        print('\033[31m✘')
                        with open(bannedMusicList, 'a', encoding='utf8') as file:
                            file.write("{}".format(path))
                            file.write("\n")
                        pause()
                except:
                    print('\033[31m✘')
                    with open(bannedMusicList, 'a', encoding='utf8') as file:
                        file.write("{}".format(path))
                        file.write("\n")
                    pause()
    except:
        msg(0, 'msAdded')
        pause()
