# Aily Code SDK

## 调用LLM
```python
from aily.server_sdk import llm

message = llm.generate(messages=[
{"role": "user", "content": "Hello world"}
], model="BYOM-pro")
print(message.content)

message = llm.generate(messages=[
{"role": "user", "content": "Hello world"}
], model=llm.LLMModel.BYOM_PRO)
print(message.content)
```
## 发送消息

```
from aily.server_sdk.conversation import send_message, update_message

message_id = send_message('xxx')
print(message_id)
```

## 数据查询
### 执行OQL
```python
from aily.server_sdk.data import execute_oql

oql_query = "SELECT * FROM data_table"
oql_results = execute_oql(oql_query)
print(f"OQL查询结果: {oql_results}")

from aily.server_sdk.data import execute_sql

# 执行SQL查询
sql_query = "SELECT * FROM analytics_table"
sql_results = execute_sql(sql_query)
print(f"SQL查询结果: {sql_results}")
```


## 知识库查询
```python
from aily.server_sdk import knowledge

knowledge_id = "my_knowledge_base"
query_text = "如何获取飞书多维表格的高阶权限协作者?"

results = knowledge.retrieve(knowledge_id, query_text, top_k=3, threshold=0.7)

```
