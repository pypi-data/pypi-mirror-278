import argparse
import os
import sys

from litellm import completion, embedding
from qdrant_client import QdrantClient
from qdrant_client.http import models

DEFAULT_NOTICE_PROMPT = '''
請妳使用繁體中文回答，必須使用臺灣慣用語回答
請妳不可以使用簡體中文回答，不可以使用大陸慣用語回答
回答的最末端尾巴要附上妳引證的來源檔案名稱
如果妳不會回答的部分，不可以亂猜
'''


def query_qdrant_knowledge_base(qdrant_host,
                                qdrant_port,
                                collection_name,
                                user_input,
                                embedding_model,
                                top_k,
                                hnsw_ef) -> str:
    qdrant_client_instance = QdrantClient(qdrant_host, port=qdrant_port)
    query_vector = generate_embedding(embedding_model, user_input)
    search_params = models.SearchParams(hnsw_ef=hnsw_ef, exact=False)
    search_result = qdrant_client_instance.search(
        collection_name=collection_name,
        query_vector=query_vector['data'][0]['embedding'],
        search_params=search_params,
        limit=top_k,
        with_payload=True,
        with_vectors=True
    )

    str_knowledge_base = ""
    for idx, hit in enumerate(search_result, start=1):
        str_knowledge_base += (f"\n"
                               f"<a-rag-file>\n"
                               f"<file-path>\n"
                               f"{hit.payload['file_path']}\n"
                               f"</file-path>\n")
        str_knowledge_base += (f"<text-content>\n"
                               f"{hit.payload['text_content']}"
                               f"</text-content>\n"
                               f"</a-rag-file>\n"
                               )
    os.makedirs("./users/botrun_ask_folder", exist_ok=True)
    open("./users/botrun_ask_folder/str_knowledge_base.txt", "w").write(str_knowledge_base)
    return str_knowledge_base


def query_qdrant_and_llm(qdrant_host, qdrant_port, collection_name, user_input,
                         embedding_model, top_k, notice_prompt,
                         chat_model,
                         hnsw_ef):
    str_knowledge_base = query_qdrant_knowledge_base(
        qdrant_host, qdrant_port, collection_name, user_input,
        embedding_model, top_k, hnsw_ef)
    if not notice_prompt:
        notice_prompt = DEFAULT_NOTICE_PROMPT
    str_message = f'''
    <知識庫RAG搜索到的內容>
    {str_knowledge_base}
    </知識庫RAG搜索到的內容>

    <回答時請妳注意>
    {notice_prompt}
    </回答時請妳注意>

    <使用者提問請妳回答>
    {user_input}
    </使用者提問請妳回答>
    '''
    return completion_call(chat_model, str_message)


def completion_call(model, message):
    try:
        response = completion(
            model=model,
            messages=[{"content": message, "role": "user"}],
            stream=True
        )
        for part in response:
            delta_content = part.choices[0].delta.content
            if delta_content:
                yield delta_content
    except Exception as e:
        print(f"query_qdrant.py, completion_call, exception: {e}")


def generate_embedding(model, text):
    embedding_response = embedding(model=model, input=[text])
    return embedding_response


def query_qdrant_and_llm_print(qdrant_host, qdrant_port, collection_name, user_input,
                               embedding_model, top_k, notice_prompt,
                               chat_model, hnsw_ef):
    for fragment in query_qdrant_and_llm(qdrant_host, qdrant_port, collection_name, user_input,
                                         embedding_model, top_k, notice_prompt,
                                         chat_model, hnsw_ef):
        print(fragment, end="")
        sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search documents in Qdrant using natural language query.")
    parser.add_argument("--query")
    parser.add_argument("--collection", default="collection_1")
    parser.add_argument("--embedding_model", default="openai/text-embedding-3-large")
    parser.add_argument("--top_k", default=12)
    parser.add_argument("--notice_prompt", default=DEFAULT_NOTICE_PROMPT)
    parser.add_argument("--chat_model", default="gpt-4-turbo-preview")
    parser.add_argument("--hnsw_ef", default=256)
    args = parser.parse_args()

    qdrant_host = os.getenv('QDRANT_HOST', 'localhost')
    qdrant_port = int(os.getenv('QDRANT_PORT', '6333'))
    query_qdrant_and_llm_print(qdrant_host, qdrant_port, args.collection, args.query,
                               args.embedding_model, args.top_k,
                               args.notice_prompt, args.chat_model,
                               args.hnsw_ef)
