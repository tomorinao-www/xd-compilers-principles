import ply.yacc as yacc
from lexer import tokens  # 从 lexer.py 中引入 tokens
import executor

# -------------------------------
# 顶层支持多个语句
# -------------------------------

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    pass

# 支持每条语句后可以跟 SEMICOLON，也可以不加
def p_statement(p):
    '''statement : command SEMICOLON
                 | command'''
    pass

# -------------------------------
# 所有 SQL 命令
# -------------------------------

def p_command(p):
    '''command : create_database
               | use_database
               | create_table
               | show_tables
               | insert
               | select
               | update
               | delete
               | drop_table
               | drop_database
               | exit'''
    pass

# -------------------------------
# 1. CREATE DATABASE
# -------------------------------

def p_create_database(p):
    "create_database : CREATE DATABASE ID"
    executor.create_database(p[3])

# -------------------------------
# 2. USE DATABASE
# -------------------------------

def p_use_database(p):
    "use_database : USE ID"
    executor.use_database(p[2])

# -------------------------------
# 3. CREATE TABLE
# -------------------------------

def p_create_table(p):
    "create_table : CREATE TABLE ID LPAREN column_def_list RPAREN"
    executor.create_table(p[3], p[5])

def p_column_def_list(p):
    '''column_def_list : column_def
                       | column_def_list COMMA column_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_column_def(p):
    '''column_def : ID INT
                  | ID CHAR LPAREN NUMBER RPAREN'''
    if len(p) == 3:
        p[0] = (p[1], 'INT')
    else:
        p[0] = (p[1], f"CHAR({p[4]})")

# -------------------------------
# 4. SHOW TABLES
# -------------------------------

def p_show_tables(p):
    "show_tables : SHOW TABLES"
    executor.show_tables()

# -------------------------------
# 5. INSERT
# -------------------------------

def p_insert(p):
    "insert : INSERT INTO ID VALUES LPAREN value_list RPAREN"
    executor.insert_into(p[3], p[6])

def p_value_list(p):
    '''value_list : value
                  | value_list COMMA value'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_value(p):
    '''value : NUMBER
             | STRING'''
    p[0] = p[1]

# -------------------------------
# 6. SELECT
# -------------------------------

def p_select(p):
    "select : SELECT STAR FROM ID"
    executor.select_all(p[4])

# -------------------------------
# 7. UPDATE
# -------------------------------

def p_update(p):
    "update : UPDATE ID SET ID EQ value where_clause_opt"
    executor.update_table(p[2], p[4], p[6], p[7])

# -------------------------------
# 8. DELETE
# -------------------------------

def p_delete(p):
    "delete : DELETE FROM ID where_clause_opt"
    executor.delete_from(p[3], p[4])

# -------------------------------
# 9. DROP TABLE
# -------------------------------

def p_drop_table(p):
    "drop_table : DROP TABLE ID"
    executor.drop_table(p[3])

# -------------------------------
# 10. DROP DATABASE
# -------------------------------

def p_drop_database(p):
    "drop_database : DROP DATABASE ID"
    executor.drop_database(p[3])

# -------------------------------
# 11. EXIT
# -------------------------------

def p_exit(p):
    "exit : EXIT"
    executor.exit()

# -------------------------------
# WHERE 可选子句
# -------------------------------

def p_where_clause_opt(p):
    '''where_clause_opt : WHERE ID EQ value
                        | empty'''
    if len(p) == 5:
        p[0] = (p[2], p[4])
    else:
        p[0] = None

# -------------------------------
# 空
# -------------------------------

def p_empty(p):
    'empty :'
    pass

# -------------------------------
# 错误处理
# -------------------------------

def p_error(p):
    if p:
        print(f"语法错误：非法符号 {p.value}")
    else:
        print("语法错误：可能输入不完整")

# -------------------------------
# 构建 parser
# -------------------------------

parser = yacc.yacc()
