from dataclasses import dataclass
from aily_core import action
from typing import List, Optional

KNOWLEDGE_API_NAME = 'action:brn:cn:spring:all:all:connector_action_runtime:/spring_sdk_wiki_recall'


@dataclass
class Chunk:
    content: str
    score: float
    chunk_id: str
    raw_data: dict
    title: Optional[str] = None
    link: Optional[str] = None


def retrieve(
        knowledge_id: str,
        query_text: str,
        top_k: int = 5,
        threshold: float = 0.5
) -> List[Chunk]:
    """
    在指定的知识库中查询与给定文本相似的条目。

    Args:
        knowledge_id (str): 要查询的知识库ID。
        query_text (str): 查询的文本内容。
        top_k (int, optional): 返回的最相似条目的数量。默认为5。
        threshold (float, optional): 相似度阈值,只返回相似度大于等于该阈值的条目。默认为0.5。

    Returns:
        List[Chunk]: 查询结果列表,每个元素是一个Chunk对象,包含以下字段:
            - content (str): 条目的内容。
            - title (str): 条目的标题。
            - score (float): 条目与查询文本的相似度得分。
            - link (str): 条目的链接。
            - chunk_id (str): 条目的ID。
    """
    if not knowledge_id:
        raise ValueError("知识库ID不能为空")

    if not query_text:
        raise ValueError("查询文本不能为空")

    if top_k <= 0:
        raise ValueError("top_k必须大于0")

    if threshold < 0 or threshold > 1:
        raise ValueError("threshold必须在[0, 1]范围内")

    response = action.call_action(KNOWLEDGE_API_NAME, {
        "apiName": knowledge_id,
        "key": query_text,
        "scoreThreshold": threshold,
        "topk": top_k,
    })
    results = []
    for chunk in response:
        source_value = chunk.get('source_value', {})
        results.append(
            Chunk(
                content=source_value.get('content'),
                title=source_value.get('doc', {}).get('title'),
                score=chunk.get('recall_score'),
                link=source_value.get('doc', {}).get('link'),
                chunk_id=chunk.get('id'),
                raw_data=chunk
            )
        )
    return results

