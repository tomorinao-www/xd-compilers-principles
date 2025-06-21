import os
import json
import shutil

DATA_ROOT = "data"
current_db = None

def get_current_db():
    if not current_db:
        raise Exception("当前未选择数据库")
    return os.path.join(DATA_ROOT, current_db)

def create_database(name):
    path = os.path.join(DATA_ROOT, name)
    if os.path.exists(path):
        raise Exception("数据库已存在")
    os.makedirs(path)
    with open(os.path.join(path, "meta.json"), "w") as f:
        json.dump({}, f)
    print(f"数据库 {name} 创建成功")

def use_database(name):
    global current_db
    path = os.path.join(DATA_ROOT, name)
    if not os.path.exists(path):
        raise Exception("数据库不存在")
    current_db = name
    print(f"已切换至数据库 {name}")

def drop_database(name):
    path = os.path.join(DATA_ROOT, name)
    if not os.path.exists(path):
        raise Exception("数据库不存在")
    shutil.rmtree(path)
    global current_db
    if current_db == name:
        current_db = None
    print(f"数据库 {name} 删除成功")

def load_meta():
    path = os.path.join(get_current_db(), "meta.json")
    with open(path) as f:
        return json.load(f)

def save_meta(meta):
    path = os.path.join(get_current_db(), "meta.json")
    with open(path, "w") as f:
        json.dump(meta, f, indent=2)
