from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from decouple import config
from sqlalchemy import create_engine
from db import Base, User, Post
from sqlalchemy.pool import NullPool
from cores.databases.connection import get_db


router = APIRouter(
    # dependencies=[Depends(authorization_helper.check_access)],
    prefix='/justdont',
    tags=['kkk'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

@router.get('/list_endpoints/')
def list_endpoints(request: Request):
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return url_list


@router.get('/create_tables')
def create_tables(password: str):
    if password == '123':
        _host = config('db_host')
        _username = config('db_username')
        _password = config('db_password') 
        _database = config('db_database')
        engine = create_engine(
            f'mysql+pymysql://{_username}:{_password}@{_host}/{_database}?charset=utf8mb4', echo=False, poolclass=NullPool, isolation_level="READ UNCOMMITTED")
        Base.metadata.create_all(engine)
        return 'OK'
    else: 
        return 'No'

@router.get('/drop_db')
def drop_db(password: str):
    if password == '123':
        _host = config('db_host')
        _username = config('db_username')
        _password = config('db_password') 
        _database = config('db_database')
        engine = create_engine(
            f'mysql+pymysql://{_username}:{_password}@{_host}/{_database}?charset=utf8mb4', echo=False, poolclass=NullPool, isolation_level="READ UNCOMMITTED")
        Base.metadata.drop_all(engine)
        return 'OK'
    else: 
        return 'No'
    
@router.get('/huhu')
def create_tables(password: str):
    session = next(get_db())
    if password == '123':
        u1 = User(username='playboicarti', email='u1@gmail.com', full_name='Playboi Ca Mau', 
                  avatar='/files/avatars/u1.jpg', avatar_2nd = '/files/covers/c1.jpg', bio = 'lam di', location = 'Mars',
                  phone='03123123', dob='2000-3-8', gender='Male', password='passpass', is_verified=True)
        u2 = User(username='kanyewest', email='u2@gmail.com', full_name='Chu Kanye', 
                  avatar='/files/avatars/u2.jpg', avatar_2nd = '/files/covers/c2.jpg', bio = 'lam di', location = 'Moon',
                  phone='03123123', dob='2000-3-8', gender='Male', password='passpass', is_verified=True)
        u3 = User(username='liluzineku', email='u3@gmail.com', full_name='Tieu^~ Uzi', 
                  avatar='/files/avatars/u3.jpg', avatar_2nd = '/files/covers/c3.jpg', bio = 'lam di', location = 'O2O',
                  phone='03123123', dob='2000-3-8', gender='Male', password='passpass', is_verified=True)
        u4 = User(username='lilyatchy', email='u4@gmail.com', full_name='Lil Yatchy', 
                  avatar='/files/avatars/u4.jpg', avatar_2nd = None, bio = 'lam di', location = 'Suburb',
                  phone='03123123', dob='2000-3-8', gender='Male', password='passpass', is_verified=True)
        u5 = User(username='kencarson', email='u5@gmail.com', full_name='Ken Carson', 
                  avatar='/files/avatars/u5.jpg', avatar_2nd = None, bio = 'lam di', location = 'Teen Titan Headquarter',
                  phone='03123123', dob='2000-3-8', gender='Male', password='passpass', is_verified=True)
        u6 = User(username='NAV', email='u6@gmail.com', full_name='Navi No1', 
                  avatar='/files/avatars/u6.jpg', avatar_2nd = None, bio = 'lam di', location = 'Not Africa',
                  phone='03123123', dob='2000-3-8', gender='Male', password='passpass', is_verified=True)
        u7 = User(username='popsmoke', email='u7@gmail.com', full_name='Pop Smoke', 
                  avatar='/files/avatars/u7.jpg', avatar_2nd = None, bio = 'lam di', location = 'New York',
                  phone='03123123', dob='2000-3-8', gender='Male', password='passpass', is_verified=True)
        u8 = User(username='mck', email='u8@gmail.com', full_name='Ghe Tlinh', 
                  avatar='/files/avatars/u8.jpg', avatar_2nd = None, bio = 'lam di', location = 'Not that H-Town',
                  phone='03123123', dob='2000-3-8', gender='Male', password='passpass', is_verified=True)
        u9 = User(username='sol7', email='u9@gmail.com', full_name='Su phu 7', 
                  avatar='/files/avatars/u9.jpg', avatar_2nd = None, bio = 'lam di', location = 'It"s Jail Time',
                  phone='03123123', dob='2000-3-8', gender='Male', password='passpass', is_verified=True)
        u10 = User(username='Lukaku', email='u10@gmail.com', full_name='Lukaku', 
                  avatar='/files/avatars/u10.jpg', avatar_2nd = None, bio = 'lam di', location = 'MU',
                  phone='03123123', dob='2000-3-8', gender='Male', password='passpass', is_verified=True)
         
        users = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
        for user in users:
            try:
                session.add(user)
                session.commit()
                session.refresh(user)

            except Exception:
                pass
                
        p1 = Post(
            user_id = u1.id, 
            content='Once upon a time, there was a talking dog named Frank. One day, Frank decided to go on a road trip with his owner. During the trip, Frank started telling jokes to pass the time. Unfortunately, all of his jokes were so bad that his owner had to pull over and ask him to stop before they crashed from laughing too hard.', 
            picture= None
        )
        p2 = Post(
            user_id = u2.id, 
            content="I am so clever that sometimes I don't understand a single word of what I am saying.", 
            picture= '/files/posts/p2.jpg'
        )
        p3 = Post(
            user_id = u3.id, 
            content="John was a clumsy guy. He couldn't walk down the street without tripping over something. One day, he was walking his dog when he tripped over a crack in the sidewalk and fell into a puddle. His dog looked at him with a sigh and said, 'I think it's time for you to invest in some better shoes.'", 
            picture= None
        )
        p4 = Post(
            user_id = u4.id, 
            content="I'm not lazy, I'm just on energy-saving mode.", 
            picture= '/files/posts/p4.jpg'
        )
        p5 = Post(
            user_id = u5.id, 
            content='Tom and Jerry were two mice who lived in a house with a cat named Fluffy. They were always getting into trouble, but they loved each other like brothers. One day, Fluffy caught Tom and was about to eat him when Jerry jumped on Fluffy"s back and started tickling him. Fluffy laughed so hard', 
            picture= None
        )
        p6 = Post(
            user_id = u6.id, 
            content="I'm not arguing, I'm just explaining why I'm right.", 
            picture= '/files/posts/p6.jpg'
        )
        posts = [p1, p2, p3, p4, p5, p6]
        for post in posts:
            try:
                session.add(post)
                session.commit()
            except Exception:
                pass
        return 'Done'
    else:
        return 'No'
    
# @router.get('/create_es')
# def create_es(password: str):
#     if password == '123':
#         from cores.elasticsearch.es_helper import ElasticSearch
#         from cores.elasticsearch import es_base
#         from enums.db import table_name_enum
#         es = ElasticSearch()
#         indices = [
#             table_name_enum.USER,
#         ]
#         mappings = [
#             user.mapping,
#             # link_mapping.mapping
#         ]
#         for index, mapping in zip(indices, mappings):
#             try:
#                 if es.check_index_is_exists(index):
#                     es.delete_index(index)
#                 if mapping:
#                     index_setting = es_base.get_setting_to_create_index(mapping)
#                 else:
#                     index_setting = None
#                 es.create_index(index_name=index, index_body=index_setting)
#             except Exception as e: 
#                 print(f'index {index}:: {e}')
#                 pass
#         return 'OK'
#     else: 
#         return 'No'