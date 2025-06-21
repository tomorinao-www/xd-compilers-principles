# shell.py
from parser import parser
from catalog import get_current_db


def run_shell():
    while True:  # 语句外循环，每个循环接收一条语句
        try:
            # 获取当前数据库名称
            current_db = ""
            try:
                current_db = get_current_db()
            except Exception:
                pass
            # 打印提示符
            prompt = f"naoSQL({current_db})" if current_db else "naoSQL"
            print(prompt, end="")
            sql = ""
            while True:
                # 语句内循环，直到用户输入完整的 SQL 语句
                sql += input("> ")
                if sql.strip().endswith(";"):
                    break
            if sql.strip().startswith("EXIT") or sql.strip().startswith("exit"):
                print("退出 naoSQL。")
                break
            parser.parse(sql)
        except Exception as e:
            print(f"执行错误：type={type(e).__name__}, message={str(e)}")


if __name__ == "__main__":
    run_shell()
