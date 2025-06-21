import ply.lex as lex

# ========== 1. 关键字 ==========

keywords = {
    'create': 'CREATE',
    'database': 'DATABASE',
    'use': 'USE',
    'table': 'TABLE',
    'show': 'SHOW',
    'tables': 'TABLES',
    'insert': 'INSERT',
    'into': 'INTO',
    'values': 'VALUES',
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'update': 'UPDATE',
    'set': 'SET',
    'delete': 'DELETE',
    'drop': 'DROP',
    'exit': 'EXIT',
    'int': 'INT',
    'char': 'CHAR',
}

# ========== 2. token 列表 ==========

tokens = [
    'ID',           # 标识符（表名、列名、数据库名）
    'NUMBER',       # 整数常量
    'STRING',       # 字符串常量
    'LPAREN', 'RPAREN',  # ( )
    'COMMA', 'SEMICOLON',  # , ;
    'EQ', 'GT', 'LT', 'GE', 'LE', 'NE',  # 比较运算符
    'STAR',         # *
] + list(keywords.values())  # 把关键字 token 加进去

# ========== 3. 正则规则 ==========

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COMMA     = r','
t_SEMICOLON = r';'
t_EQ        = r'='
t_GT        = r'>'
t_LT        = r'<'
t_GE        = r'>='
t_LE        = r'<='
t_NE        = r'<>|!='
t_STAR      = r'\*'

t_ignore = ' \t'

# ========== 4. 标识符和关键字 ==========

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = keywords.get(t.value.lower(), 'ID')  # 区分关键字和标识符
    return t

# ========== 5. 数字常量（整数） ==========

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# ========== 6. 字符串常量（单引号） ==========

def t_STRING(t):
    r"'([^']*)'"
    t.value = t.value[1:-1]  # 去掉引号
    return t

# ========== 7. 换行处理 ==========

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ========== 8. 错误处理 ==========

def t_error(t):
    print(f"非法字符：'{t.value[0]}'")
    t.lexer.skip(1)

# ========== 9. 测试函数 ==========

def test_lexer(data):
    lexer = lex.lex()
    lexer.input(data)
    for tok in lexer:
        print(tok)

# ========== 10. 用于 import 的默认构造 ==========

lexer = lex.lex()
