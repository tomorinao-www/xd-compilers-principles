# 西电 编译原理 实验 数据库系统 DBMS 的设计与实现

<img src="https://img.shields.io/badge/Python-3.10+-666?style=flat&logo=Python&logoColor=fc5&labelColor=3776AB" alt="Python 3.10+">

## 依赖

uv:

```
pip install uv
```

## 开始

1. 创建虚拟环境

```
uv venv
```

2. 激活虚拟环境

<details open>
<summary>
Windows:
</summary>

```
.venv\Scripts\activate
```

</details>

<details open>
<summary>
Linux / macOS:
</summary>

```
source .venv/bin/activate
```

</details>

3. 安装依赖

```
uv sync
```

4. 运行

<details open>
<summary>
使用 uv:
</summary>

```
cd naosql
uv run shell.py
```

</details>

<details open>
<summary>
使用 python:
</summary>

```
cd naosql
python shell.py
```

</details>

## 报告

实验报告在 `doc/`

## 测试

提供几句SQL用于测试：
```sql
CREATE DATABASE db1;
USE db1;

CREATE TABLE users (
    id INT,
    name CHAR(50)
);
INSERT INTO users VALUES (1, 'Alice');
INSERT INTO users VALUES (2, 'Bob');
INSERT INTO users VALUES (3, 'Peter');
INSERT INTO users VALUES (4, 'Eve');

SELECT * FROM users;
SELECT name FROM users WHERE name = 'Alice';
SELECT id, name FROM users WHERE id <= 2 OR name = 'Eve';

UPDATE users SET name = 'Charlie' WHERE id = 1;

DELETE FROM users WHERE id = 4;
SELECT * FROM users;

DROP TABLE users;
DROP DATABASE db1;
```