from nemoguardrails import LLMRails, RailsConfig
from functions import return_representations, query_db_recipe, rag_response, query_db_food_plan
import warnings
warnings.filterwarnings("ignore")

config = RailsConfig.from_path('sample')
rails = LLMRails(config)

rails.register_action(action = return_representations, name = 'return_representation')
rails.register_action(action = query_db_food_plan, name = 'query_db_food_plan')
rails.register_action(action = query_db_recipe, name = 'query_db_recipe')
rails.register_action(action = rag_response, name = 'rag')
messages = []
while True:
    user_message = input("Type message: ")
    messages.append({
        "role":"user",
        "content": user_message
        })
    new_message = rails.generate(messages=messages)
    print(new_message['content'])
    messages.append(new_message)
