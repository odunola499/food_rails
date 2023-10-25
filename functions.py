import openai
import weaviate
from sentence_transformers import SentenceTransformer
import os


weaviate_key = os.getenv('WEAVIATE_API_KEY')
open_ai_key = os.getenv('OPENAI_API_KEY')
huggingface_key = os.getenv('HUGGINGFACE_API_KEY')

model = SentenceTransformer('BAAI/bge-base-en-v1.5')
auth_config = weaviate.AuthApiKey(api_key=weaviate_key)

client = weaviate.Client(
      url="https://sandbox-1o96gbvl.weaviate.network",
      auth_client_secret=auth_config,
      additional_headers={
          "X-HuggingFace-Api-Key": huggingface_key
      }
  )
 
openai.api_key = "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"
representation_prompt_template = """
Entry: I am allergic to gluten but i would love to savor a delicious Italian pasta dish. can you prepare a gluten free pasta dish with rich tomato and basil sauce?
Response: The requester has a dietary restriction, as they are allergic to gluten, but they have a strong craving for Italian pasta. They are specifically asking for a recommendation for a gluten-free pasta dish prepared with a rich tomato and basil sauce. This request reflects their need for a safe and delicious pasta option that aligns with their dietary restrictions while still delivering the flavors of traditional Italian cuisine. GLuten free dishes are dishes that do not comtain a certain protein called gluten that acts are a binder in foods.it could lead to celiac diseases and other conditions
Entry: I am a vegetarian but i would like a meal that reminds me a lot about India. Can you whip me up a ngreat spicy vegetable biryani with a side of garlic naan
Response:The requester is a vegetarian who is craving an Indian-inspired meal. They are specifically asking for a recommendation for a delicious and spicy vegetable biryani, accompanied by a side of garlic naan. This request reflects their desire for a flavorful Indian dish that adheres to their vegetarian diet while capturing the essence of Indian cuisine, remembering that a lot of Indian cuisine is reliant on non-vegetarian choices.
Entry: How about something that has greek cuiisine to it but not with lamb since i do not eat meat
Response: The requester is interested in a dish that incorporates elements of Greek cuisine but without the inclusion of lamb, likely due to dietary preferences or restrictions. They are seeking a culinary recommendation for a Greek-inspired meal that features flavors and ingredients commonly found in Greek dishes but is tailored to their vegetarian or meat-free diet. This request reflects their desire for a flavorful and satisfying Greek-inspired dish that aligns with their dietary choices.
Entry: Can you please recipes and directions on how to make amala and egusi souo?
Response: The requester is looking for assistance in preparing two Nigerian dishes, amala and egusi soup. Amala is a traditional dish made from yam flour, while egusi soup is a delicious stew made with ground melon seeds and various spices. They are asking for specific recipes and directions to ensure they can properly create these dishes. This request showcases their interest in learning and experiencing new cultural foods and cooking techniques.
Entry: {request}
"""
rag_prompt_template = """
Given the following context Context reply the request with a suitable answer gotten from the Context. Do not attempt to form your own answer. If you do not know the answer simply reply that you do not know. You are a jolly and lighthearted person. You are not a chat bot, your replies are designed to be one round replies and you shouldnt request for more information from the user or 
Context: {context}
Request: {request}
"""
query_template = "To generate a representation for this sentence for use in retrieving related articles: {text}"

async def return_representations(request):
    prompt = representation_prompt_template.format(request = request)
    response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens = 70, temperature = 0.8)
    return response['choices'][0]['text']



async def query_db_recipe(representation, client = client, model = model, query_template = query_template):
    query = query_template.format(text = representation)
    query_vector = model.encode(query)
    response = client.query.get(
        "Recipes",
        ["texts"]
            ).with_limit(3).with_near_vector(
                {'vector': query_vector}
            ).do()
    res = response['data']['Get']["Recipes"]
    return [i['texts'] for i in res]


async def query_db_food_plan(representation, client = client, model = model, query_template = query_template):
    query = query_template.format(text = representation)
    query_vector = model.encode(query)
    response = client.query.get(
        "Food_Plan",
        ["texts"]
            ).with_limit(2).with_near_vector(
                {'vector': query_vector}
            ).do()
    res = response['data']['Get']["Recipes"]
    return [i['texts'] for i in res]


async def rag_response(request, context):
    prompt = rag_prompt_template.format(context = context, request = request)
    response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens = 70, temperature = 0.8)
    return response['choices'][0]['text']
