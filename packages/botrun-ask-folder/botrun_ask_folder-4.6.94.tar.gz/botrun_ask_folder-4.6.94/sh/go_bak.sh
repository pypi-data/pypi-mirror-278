# qdrant
# http://localhost:6333/dashboard

source venv/bin/activate
ulimit 99999
sh/qdrant.sh

# 001 tree, 60 directories, 1651 files, real	5m36.046s
#time python run_split_txts.py --input_folder "./data"

# 002, max_tasks 10, real	10m45.899s
#time python run_async_summary.py --input_folder "./data" --max_tasks 100

# 003
#sh/qdrant.sh
#time python embeddings_to_qdrant.py --input_folder "./data" --collection_name "collection_1" --max_tasks 30

#time python query_qdrant.py --collection collection_1 --top_k 20 --query '
#那個什麼我想問，農村的人跟那個農村的老年人的補貼的政策或者津貼等等的有哪些？
#'

#time python query_qdrant.py --collection collection_1 --top_k 20 --query '
#請問一下山上有火怎麼辦
#'

#time python query_qdrant.py --collection collection_1 --top_k 20 --query '
#你那個雞蛋的價格，一直控制不下來，你想怎樣？
#'

#time python query_qdrant.py --collection collection_1 --top_k 20 --query '
#食物存放應該怎樣才能確保安全？
#'

#time python query_qdrant.py --collection collection_1 --top_k 12 --query '
#若戰爭的話，那時食物怎樣存放才安全？
#'

#time python query_qdrant.py --collection collection_1 --top_k 12 --query '
#若戰爭的話，那時食物怎樣存放才安全？
#'

#time python query_qdrant.py --collection collection_1 --top_k 4 --query '
#動物進口台灣的相關規定？尤其是長頸鹿的爭議是什麼？清楚說明
#'

#time python query_qdrant.py --collection collection_1 --top_k 12 --query '
#講一下河流生態環境保護的政策，整治河川怎麼做？
#'

#time python query_qdrant.py --collection collection_1 --top_k 12 --query '
#老年農民福利津貼應每年檢討
#'

#time python query_qdrant.py --collection collection_1 --top_k 12 --query '
#海風一吹常種植不了植物,怎麼辦?
#'

#time python query_qdrant.py --collection collection_1 --top_k 4 --query '
#升格之後，成立「資源永續利用司」,用途是啥？
#'

#time python query_qdrant.py --collection collection_1 --top_k 4 --query '
#為什麼六月就知道巴西有禽流感了，八月還有雞蛋在臺灣賣？
#'

#time python query_qdrant.py --collection collection_1 --top_k 4 --query '
#我阿伯ㄏㄡ，鄰居阿伯辛苦在種鳳梨，啊，這種農作物，是不是符合農業部說的具有外銷潛力的？還是一般作物，啊如果有外銷潛力，他要怎樣得到政府補助？阿伯的田不大，大約有三甲地，這樣有多少補助？
#'

#time python query_qdrant.py --collection collection_1 --top_k 20 --query '
#啊我阿伯的外銷的，轉作的獎勵，有三甲地的話，既然我阿伯的鳳梨有外銷潛力，轉做的補助，三甲地可以補助多少？
#'

#time python query_qdrant.py --collection collection_1 --top_k 12 --query '
#立委質詢：妳用錢補助進口的雞蛋，受害的是我們自己，我們國內的雞農怎麼辦？
#'

#time python query_qdrant.py --collection collection_1 --top_k 12 --query '
#是否把國軍當農委會的工具人？請拿出跟國
#軍的雞蛋合約。如果國軍沒有缺雞蛋，為何要提供豆漿給國
#軍?
#'

#time python query_qdrant.py --collection collection_1 --top_k 1 --query '
#我想問ㄏㄡ，那個ㄏㄡ，你們農業部的政策，對於我們農民種大豆、黑豆，有沒有什麼獎勵之類的？
#'

#time python query_qdrant.py --collection collection_1 --top_k 1 --chat_model openai/gpt-4-turbo-preview --query '
#是否把國軍當農委會的工具人？請拿出跟國
#軍的雞蛋合約。如果國軍沒有缺雞蛋，為何要提供豆漿給國
#軍?
#'

#echo openai/gpt-4-turbo-preview
#time python query_qdrant.py --collection collection_1 --top_k 12 --chat_model openai/gpt-4-turbo-preview --query '
#老農津貼是有多少？是不是應該增加更多金錢了？
#'
#
#echo mistral/mistral-tiny
#time python query_qdrant.py --collection collection_1 --top_k 12 --chat_model mistral/mistral-tiny --query '
#老農津貼是有多少？是不是應該增加更多金錢了？
#'
#
#echo mistral/mistral-medium
#time python query_qdrant.py --collection collection_1 --top_k 12 --chat_model mistral/mistral-medium --query '
#老農津貼是有多少？是不是應該增加更多金錢了？
#'

#echo mistral/mistral-small
#time python query_qdrant.py --collection collection_1 --top_k 12 --chat_model mistral/mistral-small --query '
#老農津貼是有多少？是不是應該增加更多金錢了？
#'

#python find_unprocessed_files.py


time python embeddings_to_qdrant_txt.py --input_folder "./data" --collection_name "collection_3" --max_tasks 50

