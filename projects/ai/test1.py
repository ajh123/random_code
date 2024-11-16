# pip install -U g4f[all]
import asyncio
from g4f.client import Client
import datetime

# Avoid a RuntimeWarning.
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

model = "gpt-4o-mini"

# Read context
files = [
    "instructions.md",
    "samland.md",
    "miners-online.md"
]

# Initialize the GPT client with the desired provider
client = Client()

# Initialize an empty conversation history
messages = []

for path in files:
    with open(path) as f:
        content = f.read()
        context = ""
        if path == "instructions.md":
            context = f"{content}"
        else:
            context = f"<document path=\"{path}\" format=\"markdown\">\n{content}\n</document>"
        messages.append({"role": "system", "content": f"{context}"})

dt_now = datetime.datetime.now(datetime.timezone.utc)
date_instruction = f"The conversation start date is {dt_now.strftime('%YYYY-%m-%d')} in Year-Month-Day format. Always respond with this date for any question about the date, and explain it is 'the date the conversation started' and may not be the current date."
messages.append({"role": "system", "content": f"{date_instruction}"})

while True:
    # Get user input
    user_input = input("You: ")

    # Check if the user wants to exit the chat
    if user_input.lower() == "exit":
        print("Exiting chat...")
        break  # Exit the loop to end the conversation

    # Update the conversation history with the user's message
    messages.append({"role": "user", "content": user_input})

    try:
        # Get GPT's response
        response = client.chat.completions.create(
            messages=messages,
            model=model,
        )

        # Extract the GPT response and print it
        gpt_response = response.choices[0].message.content
        print(f"Bot: {gpt_response}")

        # Update the conversation history with GPT's response
        messages.append({"role": "assistant", "content": gpt_response})

    except Exception as e:
        print(f"An error occurred: {e}")