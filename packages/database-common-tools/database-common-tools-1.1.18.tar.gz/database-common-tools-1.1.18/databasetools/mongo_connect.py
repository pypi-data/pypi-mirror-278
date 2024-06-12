# -*- coding: utf-8 -*-

from pymongo import MongoClient, UpdateOne


##################################################
# mongo function
##################################################

def mongo_bulk(collection, docs):
    datas = list()
    for key, doc in docs.items():
        query = dict()
        query['_id'] = key
        bson = dict()
        bson['$set'] = doc
        datas.append(UpdateOne(query, bson, upsert=True))
    return collection.bulk_write(datas)


def mongo_collection(database, collection):
    return database[collection]


def mongo_collection_try(database, collection, indexes):
    if collection not in database.list_collection_names():
        for index in indexes:
            database[collection].create_index(index)
    return database[collection]


def mongo_connect(url):
    return MongoClient(url)


def mongo_database(connect, database):
    return connect[database]


def mongo_find_gt(collection, key, value):
    return collection.find({key: {'$gt': value}})


def mongo_find_gte(collection, key, value):
    return collection.find({key: {'$gte': value}})


def mongo_find_in(collection, key, values):
    return collection.find({key: {'$in': values}})


def mongo_find_all(collection):
    return collection.find()


def mongo_find_query(collection, query):
    return collection.find(query)


def mongo_find_query_show(collection, query=dict(), show=dict()):
    return collection.find(query,show)


def mongo_find_page(collection, page, size):
    skip = (page - 1) * size
    return collection.find().skip(skip).limit(size)


def mongo_count_total(collection):
    return collection.count_documents({})


def mongo_count_total_query(collection, query=dict()):
    return collection.count_documents(query)


def mongo_find_start(collection, start, size):
    return collection.find().skip(start).limit(size)


def mongo_find_query_start(collection, query, start, size):
    return collection.find(query).skip(start).limit(size)


def mongo_find_query_filter_start(collection, query, filter, start, size):
    return collection.find(query, filter).skip(start).limit(size)


def paginated_query(collection, query={}, field_show={}, page_size=10):
    """
    高性能分页查询函数

    Args:
        collection: MongoDB 集合对象
        query (dict): 查询条件，默认为空字典表示查询所有文档
        page_size (int): 每页文档数量，默认为 10

    Returns:
        generator: 生成器对象，用于逐页返回文档

    使用示例:
    # 连接到 MongoDB 数据库
    client = MongoClient('localhost', 27017)
    db = client['your_database']
    collection = db['your_collection']

    # 执行分页查询
    for doc in paginated_query(collection, query={}, page_size=10):
        print(doc)
    """
    # 查询第一页数据
    cursor = None
    if field_show:
        cursor = collection.find(query, field_show).limit(page_size)
    else:
        cursor = collection.find(query).limit(page_size)
    last_doc_id = None

    while True:
        # 检查是否有文档返回
        if cursor.count() == 0:
            break

        # 遍历当前页的文档
        for doc in cursor:
            # 返回当前页的文档
            yield doc

        # 获取当前页最后一个文档的 ID
        last_doc = cursor[page_size - 1]
        last_doc_id = last_doc['_id']

        # 查询下一页数据，指定起始位置为当前页最后一个文档的 ID
        cursor = collection.find({'_id': {'$gt': last_doc_id}}).limit(page_size)

        # 游标超过最后一页时退出循环
        if cursor.count() == 0:
            break


##################################################
# mongo connect
##################################################
# url 连接mongo域名
# db  连接mongo 数据库
# tb  连接mongo 数据表
def mongo_conn(url, db, tb):
    return mongo_collection(mongo_database(mongo_connect(url), db), tb)


# url 连接mongo域名
# db  连接mongo 数据库
# tb  连接mongo 数据表
# ti  连接mongo 数据表索引
def mongo_conn_try(url, db, tb, ti):
    return mongo_collection_try(mongo_database(mongo_connect(url), db), tb, ti)
