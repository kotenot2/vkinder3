import vk_api
from config import acces_token
from vk_api.exceptions import ApiError
# from vk_api.utils import get_random_id
# from operator import itemgetter

class VkTools():

    def __init__(self, token):
        self.ext_api = vk_api.VkApi(token=token)

    def get_profile_info(self, user_id):
        try:
            info = self.ext_api.method('users.get',
                                       {'user_id': user_id,
                                        'fields': 'bdate,city,sex,first_name,last_name'
                                       }
                                       )[0]
        except ApiError:
            return 'Ошибка get_profile_info'
        city_id = info.get('city').get('id')
        return info

    def user_search(self, city_id, age_from, age_to, sex):
        profiles = self.ext_api.method('users.search',
                                       {'city_id': city_id,
                                        'age_from': age_from,
                                        'age_to': age_to,
                                        'sex': sex,
                                        'count': 100,
                                        'has_photo': 1,
                                       }
                                       )
        profiles = profiles['items']
        result = []
        for profile in profiles:
            if profile['is_closed'] == False:
                result.append({'name': profile.get('first_name')  + ' ' + profile.get('last_name'),
                               'id': profile['id']
                               }
                              )
        return result
    # получение 3 топ фото
    def photos_get(self, user_id):
        photos = self.ext_api.method('photos.get',
                                      {'album_id': 'profile',
                                       'owner_id': user_id,
                                       'extended': 1,
                                       'count': 100,

                                      }
                                      )
        try:
            photos = photos['items']
        except KeyError:
            return 'Ошибка photos_get '
        result = []
        for photo in photos:
            result.append([photo['likes']['count'], 'vk.com/photo' + str(photo['owner_id']) + '_' + str(photo['id'])])

        result = sorted(result, reverse=True)[0:3]
        #
        # result1 = result[0][1]
        # result2 = result[1][1]
        # result3 = result[2][1]

        # return result1,result2,result3
        return result


tools = VkTools(acces_token)


# a = tools.photos_get(43119218)
# print(a)