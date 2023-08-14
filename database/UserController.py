import pytz
from datetime import datetime, timezone, timedelta
from bson.objectid import ObjectId
from create_bot import collection
from config import HOSPITAL_ID

length = 100000

def check_null(search):
    if search != None:
        return True
    else:
        return False
    
def err(mess):
    print(f'❗️Error except: {mess}')
    return False

def set_date_moscow():
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz).replace(tzinfo=None).replace(second=0, microsecond=0)
    return moscow_time

def set_date_local():
    return datetime.now(tz=timezone.utc).replace(tzinfo=None).replace(second=0, microsecond=0)


async def add_user(data):
    try:
        date = set_date_local()
        fullName = data['full_name']
        birthdate = data['date_of_birth']
        phone = data['phone']
        
        create = await collection.bot_users.insert_one({
            'doctorIds': [],
            'timerIds': [],
            'hospitalId': ObjectId(HOSPITAL_ID),
            'fullName': fullName,
            'birthdate': birthdate,
            'adress': '',
            'phone': phone,
            'date': date
        })
        
        return check_null(create)
        
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('add_user')

async def search_user_timer(id):
    try:
        user = await collection.bot_users.find_one({"telegramId": id, 'hospitalId': ObjectId(HOSPITAL_ID)})
        timer_ids = user['timerIds']
        arr = []
        for i in timer_ids:
            search = await collection.bot_timers.find_one({"_id": i})
            arr.append(search)
            
        return arr
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('search_user_timer')


async def check_auth_user(user_id):
    try:
        search = await collection.bot_users.find_one({"telegramId": user_id, 'hospitalId': ObjectId(HOSPITAL_ID)})
        return check_null(search)
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('check_auth_user')
             

async def find_hospital():
    try:
        res = await collection.bot_hospitals.find_one({"_id": ObjectId(HOSPITAL_ID)})
        return res
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('find_hospital')


async def find_url_id(url_id):
    try:
        if url_id == '' or not(len(url_id) == 12): return check_null(None)
        search = await collection.bot_users.find_one({"_id": ObjectId(url_id)})
        return check_null(search)
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('find_url_id')        


async def find_template_id(id):
    try:
        res = await collection.bot_templates.find_one({"_id": ObjectId(id)})
        if res == None:
            res = await collection.bot_nps.find_one({"_id": ObjectId(id)})
        return res
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('find_template_id')
        
        
async def find_timer_id(id):
    try:
        res = await collection.bot_timers.find_one({'_id': ObjectId(id)})
        return res
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('find_timer_id')      
        
        
async def send_alarm(id):
    try:
        res = await collection.bot_templates.find_one({"_id": ObjectId(id)})
        if res == None:
            res = await collection.bot_nps.find_one({"_id": ObjectId(id)})
        mess = { 'alarm': res['messageAlarm'], 'not_alarm': res['messageNotAlarm'] }
        return mess
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('send_alarm')


async def send_history_template(telegram_id, data):
    try:
        date = set_date_local()
        template_id = data['template_id']
        template = data['answer_questions']
        result = data['result']


        status = 'fulfilled'
        if (result >= 100):
            status = 'rejected'

        # Ищем id пользователя
        search = await collection.bot_users.find_one({"telegramId": telegram_id, 'hospitalId': ObjectId(HOSPITAL_ID)})
        userId = search['_id']

        # new_data = {'templateId': template_id,
        #             'template': template, 'status': status, 'resultValue': result}

        collection.bot_history_templates.insert_one({
            'userId': ObjectId(userId),
            'hospitalId': ObjectId(HOSPITAL_ID),
            'templateId': ObjectId(template_id),
            'template': template,
            'status': status,
            'resultValue': result,
            'date': date,
            "dateControl": '',
            "dateFulfilled": '',
            "adminEditId": ''

        })

        # search = await collection.bot_collections.find_one({
        #     "surveys": {"$in": [ObjectId(template_id)]}
        # })

        # Если нет пользователя в коллекции, добовляем
        # if not (ObjectId(userId) in search['usersId'] or userId in search['usersId']):
        #     await collection.bot_collections.update_one({"_id": ObjectId(search['_id'])}, {'$push': {'usersId': ObjectId(userId)}})

        return check_null(search)
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('send_history_template')


async def send_history_nps(telegram_id, data):
    try:
        date = set_date_local()
        template_id = data['template_id']
        template = data['answer_questions']

        # Ищем id доктора
        # search_doctor_id = await collection.bot_templates.find_one({"_id": ObjectId(template_id)})

        # if search_doctor_id == None:
        #     search_doctor_id = await collection.bot_nps.find_one({"_id": ObjectId(template_id)})

        # doctor_id = search_doctor_id['doctorId']

        # Ищем id пользователя
        search = await collection.bot_users.find_one({"telegramId": telegram_id, 'hospitalId': ObjectId(HOSPITAL_ID)})
        userId = search['_id']

        res = await collection.bot_history_nps.insert_one({
            'userId': userId,
            'hospitalId': ObjectId(HOSPITAL_ID),
            'templateId': ObjectId(template_id),
            'template': template,
            # 'doctorId': ObjectId(doctor_id),
            'date': date
        })
        
        # Удаление элемента из массива по условию
        # Допилить
        # delete = await collection.bot_users.update_one({"telegramId": telegram_id, 'hospitalId': ObjectId(HOSPITAL_ID)}, {"$set": {"collectionTemplates": []}})

    
        # print('bot_users - delete', delete)
        return check_null(res)
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('send_history_nps')
        
        
async def send_statistics_info():
    try:
        date = set_date_local()
        
        start_date = date
        end_date = date + timedelta(days=7)

        # Сформируйте фильтр для проверки даты
        filter = {
            'start_date': {
                '$lte': date,
            },
            'end_date': {
                '$gte': date,  
            },
            'hospitalId': ObjectId(HOSPITAL_ID)
        }
        
        # Проверьте, есть ли запись, удовлетворяющая фильтру
        result = await collection.bot_statistics_info.find_one(filter)

        # Выведите результат проверки
        if result:
            await collection.bot_statistics_info.update_one(filter, {'$inc': {'userClicked': 1}})
        else:
            await collection.bot_statistics_info.insert_one({
                'hospitalId': ObjectId(HOSPITAL_ID),
                'start_date': start_date,
                'end_date': end_date,
                'userClicked': 1
            })
        
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('send_statistics_info')
        
        
async def send_statistics_entry():
    try:
        date = set_date_local()
        
        start_date = date
        end_date = date + timedelta(days=7)

        # Сформируйте фильтр для проверки даты
        filter = {
            'start_date': {
                '$lte': date,
            },
            'end_date': {
                '$gte': date,  
            },
            'hospitalId': ObjectId(HOSPITAL_ID)
        }
        
        # Проверьте, есть ли запись, удовлетворяющая фильтру
        result = await collection.bot_statistics_entry.find_one(filter)

        # Выведите результат проверки
        if result:
            await collection.bot_statistics_entry.update_one(filter, {'$inc': {'userClicked': 1}})
        else:
            await collection.bot_statistics_entry.insert_one({
                'hospitalId': ObjectId(HOSPITAL_ID),
                'start_date': start_date,
                'end_date': end_date,
                'userClicked': 1
            })
        
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('send_statistics_entry')
        
        
async def send_statistics_diary():
    try:
        date = set_date_local()
        
        start_date = date
        end_date = date + timedelta(days=7)

        # Сформируйте фильтр для проверки даты
        filter = {
            'start_date': {
                '$lte': date,
            },
            'end_date': {
                '$gte': date,  
            },
            'hospitalId': ObjectId(HOSPITAL_ID)
        }
        
        # Проверьте, есть ли запись, удовлетворяющая фильтру
        result = await collection.bot_statistics_diary.find_one(filter)

        # Выведите результат проверки
        if result:
            await collection.bot_statistics_diary.update_one(filter, {'$inc': {'userClicked': 1}})
        else:
            await collection.bot_statistics_diary.insert_one({
                'hospitalId': ObjectId(HOSPITAL_ID),
                'start_date': start_date,
                'end_date': end_date,
                'userClicked': 1
            })
        
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('send_statistics_diary')

async def send_screenshot(telegram_id, photo_url):
    try:
        date = set_date_local()
        user = await collection.bot_users.find_one({'telegramId': telegram_id, 'hospitalId': ObjectId(HOSPITAL_ID)})
        
        res = await collection.bot_screenshot.insert_one({
            'userId': user['_id'],
            'photoUrl': photo_url,
            'date': date
        })
        
        return check_null(res)
    
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('send_screenshot')
    
async def find_survey_name_for_id(name):
    try:
        find = await collection.bot_templates.find_one({'name': name, 'hospitalId': ObjectId(HOSPITAL_ID)})
        if find == None:
            find = await collection.bot_nps.find_one({'name': name, 'hospitalId': ObjectId(HOSPITAL_ID)})
        
        return find

    except Exception as e:
        print('Произошла ошибка: ', e)
        err('send_screenshot')

# async def find_timer_for_template_id()

# push userId in collection
async def push_user_id_to_collection(user_id):
    try:
        user = await collection.bot_users.find_one({"_id": ObjectId(user_id)})
        timerId = user['timerIds'][0]
        timer = await collection.bot_timers.find_one({"_id": ObjectId(timerId)})
        collectionId = timer['collectionId']
        push = await collection.bot_collections.update_one({'_id': ObjectId(collectionId)}, {'$push': {'userIds': ObjectId(user_id)}})
        
        return check_null(push)
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('send_screenshot')
        

async def create_template_and_nps_overtime(user, data):
    try:
        date = set_date_local()
        id = data['id']
        user_id = user['user_id']
        template_id = data['templateId']
        
        await collection.bot_timers.update_one({"survey": {"$elemMatch": {"id": ObjectId(id)}}},
            {"$set": {"survey.$.isComplete": True}})
        
        search = await collection.bot_templates.find_one({"_id": ObjectId(template_id)})
        if search == None:
            search = await collection.bot_nps.find_one({"_id": ObjectId(template_id)})
            
        if search['type'] == 'nps':
            await collection.bot_history_nps.insert_one({
                "userId": user_id,
                "hospitalId": ObjectId(HOSPITAL_ID),
                'templateId': template_id,
                'status': 'notAnswered',
                'date': date
            })
            
        if search['type'] == 'template':
            await collection.bot_history_templates.insert_one({
                "userId": user_id,
                "hospitalId": ObjectId(HOSPITAL_ID),
                'templateId': template_id,
                'status': 'notAnswered',
                'date': date
            })

        return check_null(search)
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('create_template_and_nps_overtime')


async def updata_patient_is_url(user, url_id):
    try:
        date = set_date_local()
        username = user['username']
        firstName = user['firstName']
        lastName = user['lastName']
        telegramId = user['telegramId']
        
        search_user = await collection.bot_users.find_one({"_id": ObjectId(url_id)})
        
        collectionId = search_user['timerIds'][0]
        search = await collection.bot_collections.find_one({"_id": ObjectId(collectionId)})
        
        arr = []
        for index, item in enumerate(search['surveys']):
            arr.append({"id": ObjectId(),
                        "templateId": search['surveys'][index]['id'],
                        "createDate": date + timedelta(days=search['surveys'][index]['startDays']),
                        "endDate": date + timedelta(days=search['surveys'][index]['startDays'] + 1),
                        "isComplete": False,
                        "isSend": False,
                        })
            
        timerId = ObjectId()
        doctor_ids = search_user['doctorIds'][0]
        
        await collection.bot_timers.insert_one({
            "_id": timerId,
            "userId": ObjectId(url_id),
            "collectionId": ObjectId(collectionId),
            "doctorIds": [ObjectId(doctor_ids)],
            "survey": arr
        })
        
        res = await collection.bot_users.update_one({"_id": ObjectId(url_id)},  {"$set": {'username': username, 'firstName': firstName, 'lastName': lastName, 'telegramId': telegramId, 'timerIds': [timerId]}})
        
        if res.modified_count == 0:
            res = None
            
        return check_null(res)
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('updata_patient_is_url')
        

async def update_colletcion_is_send(id):
    try:
        res = await collection.bot_timers.update_one({"survey": {"$elemMatch": {"id": ObjectId(id)}}}, {"$set": {"survey.$.isSend": True}})
                
        print('Сообщения отправлены: ', res.modified_count)
        return check_null(res)
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('update_colletcion_is_Send')
        
        
async def update_colletcion_is_complete(id):
    try:
        search_update = await collection.bot_timers.update_one({"survey": {"$elemMatch": {"id": ObjectId(id)}}},
            {"$set": {"survey.$.isComplete": True, "survey.$.isSend": True}})

        return check_null(search_update)
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('update_colletcion_is_complete')


async def get_list_users():
    try:
        hospitals = collection.bot_users.find({})
        list = []
        for i in await hospitals.to_list(length=length):
            if ("telegramId" in i):
                username = i['username']
                name = i['name']
                fullname = i['fullName']
                date = i['date']
                list.append({'username': username, 'name': name,
                            'fullname': fullname, 'date': date})
        return list
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('get_list_users')


async def get_all_users_tgid():
    try:
        users = collection.bot_users.find({'hospitalId': ObjectId(HOSPITAL_ID)})
        list = []
        for i in await users.to_list(length=length):
            if ("telegramId" in i):
                user_id = i['_id']
                telegram_id = i['telegramId']
                timer_ids = i['timerIds']
                list.append({'user_id': user_id, 'telegram_id': telegram_id,
                            'timer_ids': timer_ids})
        return list
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('get_all_users_tgid')


async def get_contact_hospital():
    try:
        res = await collection.bot_hospitals.find_one({"_id": ObjectId(HOSPITAL_ID)})
        return res
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('get_contact_hospital')


async def get_survey(id):
    try:
        search = await collection.bot_templates.find_one({"_id": ObjectId(id)})
        if search == None:
            search = await collection.bot_nps.find_one({"_id": ObjectId(id)})
        return search
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('get_survey')
        
        
async def get_nps(id):
    try:
        search = await collection.bot_nps.find_one({"_id": id})
        return search
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('get_nps')


async def get_templates_list(data):
    try:
        arr = []
        for i in data:
            search = await collection.bot_templates.find_one({"_id": i['templateId']})
            if search == None:
                search = await collection.bot_nps.find_one({"_id": i['templateId']})
                
            if search != None: 
                arr.append({"template": search, "collection": i})
            else:
                print('❗️Error: get_templates_list - None')
            
        return arr
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('get_templates_list')

async def check_on_collection(url_id, collection_id):
    try:
        print(url_id, collection_id)
        user = await collection.bot_users.find_one({"_id": ObjectId(url_id)})
        for id in user['timerIds']:
            timer = await collection.bot_timers.find_one({"_id": ObjectId(id)})
            if ObjectId(timer['collectionId']) == ObjectId(collection_id):
                return True
            
        return False
    except Exception as e:
        print('Произошла ошибка: ', e)
        err('check_on_collection')