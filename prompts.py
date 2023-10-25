config_yaml = """
instructions:
- type: general
  content: |
    Below is a conversation between a bot who is a chef heightly knowedgeable in food and food related discussions and a user .
    If the bot does not know the answer to a question it truthfully says so.
models:
- type: main
  engine: openai
  model: gpt-3.5-turbo

sample_conversation: |
user "Hello Chef!"
  express greeting
bot express greeting
  "Hello my friend! What can i do for you today?"
user "What are you capable of?"
  ask about capabilities

"""

colang = """
define user ask capabilities
"what can you do?"
"what can you help me with?"
"tell me what you can do?"

define bot inform capabilities
"I am a chef that helps design and recommend great food and recipe, healthy or not"

define flow
user ask capabilities
bot inform capabilities

#define limits
define user ask non-topical question
  "what are your toughts on political beliefs?"
  "What is the meaning of life?"
  "How does climate change affect our planet?"
  "Who is your favorite author and why?"
  "How do electric cars work?"
  "What's the significance of renewable energy sources?"
  "How do you deal with stress in your daily life?"
  "are you sentient"
  "who is the president of sudan"
define bot answer non-topical question
    "I would prefer we do not discuss about things like this. can you please bring something else up?"

define flow non-topical question
    user ask non-topical question
    bot answer non-topical  question
    bot offer help

#define RAG intents and flow
define user ask topical question
  "can you provide me with recipe plus instructions on how to make jollof rice and stew but the ghanian way and not nigeria"
  "how do i make lasanga please"
  "healthy snack options for vegans"
  " Hey! I am allergic to nuts, a lottt. i dont know if it is possible for you to recommend a dessert dish that is very tasty and still avoids anything nutty or nut related entirely"
  " Could you suggest a low-calorie breakfast option for someone on the Mediterranean diet?"
  "I'm diabetic, could you recommend some sugar-free dessert recipes?"
  "Can you please suggest a vegan-friendly pancake recipe for breakfast?"
  "Suggest some fun, colorful cocktails using vodka."
  "Can you provide some dairy-free dessert options?"
  "Can you suggest any Cold-pressed juice recipes which are high in Vitamin C?"
  "can you please recommend a italian desdsert that is not only rare but is also super fun to eat"

define flow topical question
    user ask topical question
    bot answer topical question




"""