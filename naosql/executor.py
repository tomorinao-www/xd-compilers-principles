import os
from storage import load_table, save_table, get_table_path
from catalog import (
    create_database as _create_db,
    drop_database as _drop_db,
    use_database as _use_db,
    load_meta,
    save_meta,
)


# ========== 数据库相关 ==========


def create_database(db_name):
    _create_db(db_name)


def drop_database(db_name):
    _drop_db(db_name)


def use_database(db_name):
    _use_db(db_name)


def create_table(name, columns):
    meta = load_meta()
    if name in meta:
        raise Exception("表已存在")
    meta[name] = columns
    save_meta(meta)
    save_table(name, [])
    print(f"表 {name} 创建成功")


def drop_table(name):
    meta = load_meta()
    if name not in meta:
        raise Exception("表不存在")
    del meta[name]
    save_meta(meta)
    os.remove(get_table_path(name))
    print(f"表 {name} 删除成功")


def show_tables():
    meta = load_meta()
    print("当前数据库中的表：")
    for table in meta:
        print(f" - {table}")


def insert_into(table_name, values):
    meta = load_meta()
    if table_name not in meta:
        raise Exception("表不存在")
    schema = meta[table_name]
    if len(values) != len(schema):
        raise Exception("字段数量不匹配")

    row = {}
    for (col_name, typ), val in zip(schema, values):
        if typ == "INT":
            row[col_name] = int(val)
        elif typ.startswith("CHAR"):
            limit = int(typ[5:-1])
            row[col_name] = str(val)[:limit]
        else:
            raise Exception(f"未知字段类型 {typ}")

    data = load_table(table_name)
    data.append(row)
    save_table(table_name, data)
    print(f"插入成功：{row}")


def select_all(table_name):
    data = load_table(table_name)
    if not data:
        print("（无记录）")
    else:
        for row in data:
            print(row)


def delete_from(table_name, where=None):
    data = load_table(table_name)
    src_len = len(data)
    if where is None:
        deleted = len(data)
        data = []
    else:
        key, val = where
        data = [row for row in data if not match(row, key, val, deleted)]
        deleted = src_len - len(data)

    save_table(table_name, data)
    print(f"已删除 {deleted} 条记录")


def update_table(table_name, set_key, set_val, where=None):
    data = load_table(table_name)
    count = 0
    for row in data:
        if where is None or str(row.get(where[0])) == str(where[1]):
            row[set_key] = set_val
            count += 1
    save_table(table_name, data)
    print(f"更新了 {count} 条记录")


def match(row, key, val, deleted_counter=None):
    if str(row.get(key)) == str(val):
        if deleted_counter is not None:
            deleted_counter += 1
        return True
    return False
