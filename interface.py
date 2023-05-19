import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime
from core import tools
# from operator import itemgetter
from config import  community_token
import base
import core
from random import randrange
import psycopg2
conn = psycopg2.connect(database="postgres", user="postgres", password="38621964")

class BotInterface:

    def __init__(self, token):
        self.bot = vk_api.VkApi(token=token)

    def message_send(self, user_id, message=None, attachment=None):
        self.bot.method('messages.send',
                  {'user_id': user_id,
                   'message': message,
                   'attachment': attachment,
                   'random_id': randrange(10 ** 7)
                   }
                  )

    def handler(self):
        longpull = VkLongPoll(self.bot)
        for event in longpull.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                base.base.delete_tables(conn)
                base.base.create_db(conn)
                info=tools.get_profile_info(event.user_id)
                bdate_year = info.get('bdate').split('.')[2]
                now = datetime.now().strftime('%Y')
                age = int(now) - int(bdate_year)
                city_id = info.get('city').get('id')
                age_from = age  - 5
                age_to = age + 5
                status = 6
                sex = info.get('sex')

                if event.text.lower() == 'привет':
                    self.message_send(event.user_id, 'Привет, напиши поиск, чтобы найти пару!')

                if bdate_year is None:
                    self.message_send(event.user_id, 'Укажите год рождения в вашем профиле и начните заново')

                if city_id is None:
                    self.message_send(event.user_id, 'Укажите город в вашем профиле и начните заново')
                if sex is None:
                    self.message_send(event.user_id, 'Укажите ваш пол вашем профиле и начните заново')

                if event.text.lower() == 'поиск' and sex == 1:
                    sex = 2
                    self.message_send(event.user_id, 'Начинаем искать вам мужчину!')
                elif event.text.lower() == 'поиск' and sex == 2:
                    sex = 1
                    self.message_send(event.user_id, 'Начинаем искать вам женщину!')

                list_profiles = tools.user_search(city_id, age_from, age_to, sex)

                for a in list_profiles:
                    user_search_id = a.get('id')
                    name = a.get('name')
                    list_profiles_base = base.base.insert_profiles(conn, user_search_id, name)

                select = base.base.select_profiles(conn, user_search_id)
                # print(select)
                for x in select:
                    user = x[0]
                    select_id = []
                    select_id.append(user)
                    for id in select_id:
                        self.message_send(event.user_id, 'https://vk.com/id' + str(id))
                        top_photos = tools.photos_get(id)
                    # for c, d in top_photos:
                        self.message_send(event.user_id, 'Топ фотографии:' + str(top_photos))


bot = BotInterface(community_token)
bot.handler()


