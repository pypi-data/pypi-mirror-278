from openai import OpenAI
from openai import OpenAIError


def call_ai(client_gpt, model="gpt-3.5-turbo", system_content="", text="", seed=None, temperature=0.7, max_tokens=64, top_p=1, response_json=False):
    """
    This function calls the OpenAI API to generate a response.
    Args:
        :client_gpt: The OpenAI client.
        :model: The model to use. default = "gpt-3.5-turbo"
        :system_content: The system content.
        :text: The text to generate a response to.
        :seed: The seed to use, using the same int allow us to have output consistent request to request. @April 2024 Beta only work with "gpt-3.5-turbo-1106" & "gpt-4-1106-preview" models. default = None
        :temperature: The temperature of the response. default = 0.7
        :max_tokens: The maximum number of tokens to generate. default = 64
        :top_p: The top p value. default = 1
        :response_json: The response format True or False. default = False
    Returns:
        :response : The response from the API.
        :response.choices[0].message.content: The content response from the API.
    """
    
    try:
        if response_json == True:
            response = client_gpt.chat.completions.create(
                model=model,
                response_format={ "type": "json_object" },
                messages=[
                {
                "role": "system",
                "content": f"{system_content} your designed to output JSON."
                },
                {
                "role": "user",
                "content": f"{text}"
                }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                seed=seed
            )
        else:
            response = client_gpt.chat.completions.create(
                model=model,
                messages=[
                {
                "role": "system",
                "content": f"{system_content}"
                },
                {
                "role": "user",
                "content": f"{text}"
                }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                seed=seed
            )

        for resp in response.choices:
            print(f"Response: {resp.finish_reason}")
            response_status_check(resp.finish_reason)
        return response
    except OpenAIError as e:
        print(f"An error occurred: {e}")

def response_status_check(response):
    """
    This function checks the status of the response.
    Every response will include a finish_reason. The possible values for finish_reason are:
    - stop: API returned complete message, or a message terminated by one of the stop sequences provided via the stop parameter
    - length: Incomplete model output due to max_tokens parameter or token limit
    - function_call: The model decided to call a function
    - content_filter: Omitted content due to a flag from our content filters
    - null: API response still in progress or incomplete
        
        
    Args:
        :response: The response to check.
    """
    if response == "stop":
        print(" API returned complete message, or a message terminated by one of the stop sequences provided via the stop parameter")
    if response == "length":
        print("Incomplete model output due to max_tokens parameter or token limit")
    if response == "function_call":
        print("The model decided to call a function")
    if response == "content_filter":
        print("Omitted content due to a flag from our content filters")
    if response == "null":
        print("API response still in progress or incomplete")

def corrige_mon_français(client_gpt, text, model= "gpt-3.5-turbo", max_tokens=64, seed=None, full_content = False, response_json=False):
    """
    Cette fonction permet de corriger un texte en français.
    Args:
        :client_gpt: The OpenAI client.
        :text: The text to correct.
        :model: The model to use. default = "gpt-3.5-turbo"
        :max_tokens: The maximum number of tokens to generate. default = 64
        :seed: The seed to use, using the same int allow us to have output consistent request to request. @April 2024 Beta only work with "gpt-3.5-turbo-1106" & "gpt-4-1106-preview" models. default = None
        :full_content: The full content of the response. default = False
        :response_json: The response format True or False. default = False
    """
    system = "Je suis en train de rédiger un texte en français et j'aimerais que vous m'aidiez à vérifier l'orthographe. Ne prends pas en compte les balises html s'il y en a conserve les. Le format de sortie sera 'Need:':True or False, and 'text_corrected': 'texte corrigé'"
    text_to_check = text
    resp = call_ai(
        client_gpt,
        model=model,
        system_content=system,
        text=text,
        max_tokens=max_tokens,
        seed=seed,
        response_json=response_json)
    if full_content:
        return resp
    else:
        return resp.choices[0].message.content