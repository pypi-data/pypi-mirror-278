from concurrent.futures import ThreadPoolExecutor, wait
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# 构建es客户端对象
def create_client(hosts,port):
    addrs = []
    for host in hosts:
        addr = {'host': host, 'port': port}
        addrs.append(addr)
    return Elasticsearch(addrs)

# es索引是否存在
def index_exists(es, index_name):
    return es.indices.exists(index=index_name)

# 创建索引
def create_index(es, index_name, mapping):
    res = es.indices.create(index=index_name, ignore=400, body=mapping)
    return res

# 删除索引
def delete_index(es, index_name):
    res = es.indices.delete(index=index_name)
    return res

# 多线程多批量写入向量数据
def write_index_bulk(es, vec_datas):
    pool = ThreadPoolExecutor(max_workers=8)
    tasks = []
    for vecs in vec_datas:
        tasks.append(pool.submit(write_bulk, es, vecs))
    wait(tasks)

# 批量写入向量数据
def write_bulk(es, vecs, timeout=3600):
    helpers.bulk(es, vecs, request_timeout=timeout)
