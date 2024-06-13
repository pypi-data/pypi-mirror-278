import json
from typing import List, Dict, Any
from aily_core import action

OQL_API_NAME = 'action:brn:cn:spring:all:all:connector_action_runtime:/spring_sdk_oql_exec'
SQL_API_NAME = 'action:brn:cn:spring:all:all:connector_action_runtime:/spring_sdk_sql_exec'


def execute_oql(oql: str, args: list = None, named_args: dict = None) -> List[Dict[str, Any]]:
    """
    执行OQL查询,用于查询数据表的内容。

    Args:
        oql (str): 要执行的OQL查询语句。
        args:
        named_args:
    Returns:
        List[Dict[str, Any]]: 查询结果,每个字典代表一行数据。
            - 字典的键为列名(str)
            - 字典的值为对应的数据(Any)

    """
    # 执行OQL查询并获取结果
    response = action.call_action(OQL_API_NAME, {
        "query": oql,
        "args": args or [],
        "namedArgs": named_args or {}
    })

    rows = []
    for row in json.loads(response['rows']):
        rows.append(row)
    return rows


def execute_sql(sql: str) -> List[Dict[str, Any]]:
    """
    执行SQL查询,用于查询分析表的内容。

    Args:
        sql (str): 要执行的SQL查询语句。

    Returns:
        List[Dict[str, Any]]: 查询结果,每个字典代表一行数据。
            - 字典的键为列名(str)
            - 字典的值为对应的数据(Any)
    """
    # 执行SQL查询并获取结果
    response = action.call_action(SQL_API_NAME, {"query": sql})

    rows = []
    for row in response['data']:
        row_data = json.loads(row)
        rows.append(row_data)
    return rows
