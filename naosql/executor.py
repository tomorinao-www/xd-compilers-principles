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


# ====== 数据表 ======


def eval_expr(expr, row):
    if expr is None:
        return True
    etype = expr[0]
    if etype == "cmp":
        _, op, left, right = expr
        # 左右可以是列名也可以是常量
        left_val = row.get(left) if isinstance(left, str) and left in row else left
        right_val = row.get(right) if isinstance(right, str) and right in row else right
        return {
            "=": left_val == right_val,
            "!=": left_val != right_val,
            "<": left_val < right_val,
            "<=": left_val <= right_val,
            ">": left_val > right_val,
            ">=": left_val >= right_val,
        }[op]
    elif etype == "binop":
        _, op, left_expr, right_expr = expr
        if op == "AND":
            return eval_expr(left_expr, row) and eval_expr(right_expr, row)
        elif op == "OR":
            return eval_expr(left_expr, row) or eval_expr(right_expr, row)
    elif etype == "const":
        return expr[1]
    else:
        raise Exception(f"未知表达式类型: {etype}")


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
    new_data = []
    deleted = 0
    for row in data:
        if not eval_expr(where, row):
            new_data.append(row)
        else:
            deleted += 1
    save_table(table_name, new_data)
    print(f"删除了 {deleted} 条记录")

def update_table(table_name, set_key, set_val, where=None):
    data = load_table(table_name)
    updated = 0
    for row in data:
        if eval_expr(where, row):
            row[set_key] = set_val
            updated += 1
    save_table(table_name, data)
    print(f"更新了 {updated} 条记录")


def match(row, key, val, deleted_counter=None):
    if str(row.get(key)) == str(val):
        if deleted_counter is not None:
            deleted_counter += 1
        return True
    return False
