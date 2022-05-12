from icecream import ic
from postgres_to_es.elasticsearch.elasticsearch import BaseElasticsearch
from icecream import ic

from postgres_to_es.elasticsearch.elasticsearch import BaseElasticsearch

es = BaseElasticsearch(host="127.0.0.1")
index = "genre"
count = es.get_count_documents(index)
ic(f"Кол-вло записей: {es.get_count_documents(index)}")
assert 26 == count, 'Количества записей elastic не соответствует ожиданиям'
