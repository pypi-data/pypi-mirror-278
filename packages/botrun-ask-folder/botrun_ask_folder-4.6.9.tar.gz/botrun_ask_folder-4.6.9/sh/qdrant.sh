# qdrant
# http://localhost:6333/dashboard

docker run -d -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    --name qdrant_container \
    qdrant/qdrant
