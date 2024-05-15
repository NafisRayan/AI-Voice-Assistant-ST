from huggingface_hub import InferenceClient

def format_prompt(message, history):
    prompt = ""
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response} "
    prompt += f"[INST] {message} [/INST]"
    return prompt

def generate(prompt, history, temperature=0.9, max_new_tokens=1024, top_p=0.95, repetition_penalty=1.0):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=42,
    )

    formatted_prompt = format_prompt(prompt, history)

    client = InferenceClient(model= "mistralai/Mixtral-8x7B-Instruct-v0.1", token='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')
    stream = client.text_generation(formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
    output = ""

    for response in stream:
        output += response.token.text
    
    output = output.replace("<s>", "").replace("</s>", "")
    
    yield output
    return output


history = []
while True:
    user_input = input("You: ")
    if user_input.lower() == "off":
        break
    history.append((user_input, "")) 
    for response in generate(user_input, history):
        print("Bot:", response)
