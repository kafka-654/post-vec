from gen_ai_hub.proxy.native.openai import embeddings
def get_embedding(input, model="text-embedding-ada-002")->str:
    response = embeddings.create(
        model_name = model,
        input = input
    )
    return response.data
