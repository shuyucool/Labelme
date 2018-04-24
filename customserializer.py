'''
为了解决dumps中出现不可序列化的数据时会报错的问题，
比如：raise TypeError(repr(o) + " is not JSON serializable")
TypeError: xxxxx is not JSON serializable.
主要是将不能序列化的数据转成list，int，dict，float等基本类型，保证数据的可序列化，
数据的转换由下面第一个定义的函数 to_json() 实现
'''

import pickle
import json
import time
import numpy as np
def to_json(python_object):
    if isinstance(python_object, np.uint8):   # 我的数据类型是uint8或者uint16，将其转为float类型
        return float(python_object)
    if isinstance(python_object, np.uint16):
        return float(python_object)
    if isinstance(python_object, time.struct_time):
        return {'__class__': 'time.asctime',
                '__value__': time.asctime(python_object)}
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': list(python_object)}
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def from_json(json_object):
    if '__class__' in json_object:
        if json_object['__class__'] == 'time.asctime':
            return time.strptime(json_object['__value__'])
        if json_object['__class__'] == 'bytes':
            return bytes(json_object['__value__'])
    return json_object

if __name__ == '__main__':
    entry = {}
    entry['title'] = 'Dive into history, 2009 edition'
    entry['article_link'] = 'http://diveintomark.org/archives/2009/03/27/dive-into-history-2009-edition'
    entry['comments_link'] = None
    entry['internal_id'] = b'\xDE\xD5\xB4\xF8'
    entry['tags'] = ('diveintopython', 'docbook', 'html')
    entry['published'] = True
    entry['published_date'] = time.strptime('Fri Mar 27 22:20:42 2009')
    
    with open('entry.pickle', 'wb') as f:
        pickle.dump(entry, f)

    with open('entry.pickle', 'rb') as f:
        entry2 = pickle.load(f)

    print(entry == entry2)
    print(type(entry['tags']))
    print(type(entry2['tags']))

    with open('entry.json', 'w', encoding='utf-8') as f:
        json.dump(entry, f, default=to_json)

    with open('entry.json', 'r', encoding='utf-8') as f:
        entry2 = json.load(f, object_hook=from_json)

    print(entry == entry2)
    print(type(entry['tags']))
    print(type(entry2['tags']))
