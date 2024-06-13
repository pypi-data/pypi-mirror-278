# SB_ORM

`sb_orm` 是一个简单灵活的 Python 库，使用 SQLAlchemy ORM 与 MySQL 数据库进行交互。它提供了一个易于使用的接口，用于执行常见的数据库操作，例如 `SELECT`、`INSERT`、`UPDATE` 和 `DELETE`。

## 特性

- 为常见的数据库操作简化了查询接口。
- 支持条件查询、排序和限制结果。
- 数据库会话管理采用单例模式。
- 使用 SQLAlchemy ORM 进行可靠的数据库交互。

## 更新
### - 20240613
1. 【优化】数据库连接的正确关闭：使用上下文管理器来确保数据库会话在使用完毕后正确关闭，避免资源泄漏。
2. 【新增】【优化】异步任务处理：将任务请求和处理逻辑分离，便于维护和扩展。
3. 【优化】更好的错误处理：增加了对于不支持的HTTP方法的处理，避免程序因未知方法崩溃。
4. 【优化】代码可读性提升：重构部分代码，使逻辑更清晰，易于理解和维护。

## 安装

你可以使用 `pip` 从 PyPI 安装 `sb-orm`：

```bash
pip install sb-orm
```

## 使用
### 配置
首先，需要配置数据库连接的环境变量(.env)。确保以下变量已设置：
```
DB_USER: 数据库用户名
DB_PASSWORD: 数据库密码
DB_HOST: 数据库主机 (例如 localhost)
DB_NAME: 数据库名称
DB_PREFIX: (可选) 表名前缀
```

### 基本操作
初始化数据库会话
```python
from sb_orm.Db import DatabaseSession

db_session = DatabaseSession()

### 查询数据

query = db_session.db('your_table_name').where({'column_name': 'value'}).order_by('id', descending=True).limit(10)
results = query.select()
print(results)

### 插入数据

data = {'column1': 'value1', 'column2': 'value2'}
db_session.db('your_table_name').insert(data)

### 更新数据

query = db_session.db('your_table_name').where({'id': 1})
data = {'column1': 'new_value'}
query.update(data)

### 删除数据

query = db_session.db('your_table_name').where({'id': 1})
query.delete()
```
## 贡献
欢迎贡献！请 fork 仓库并提交 pull request 以进行任何改进或错误修复。

## 联系
如有任何问题或疑问，请在 GitHub https://github.com/idcim/sb_orm 仓库 上打开 issue。