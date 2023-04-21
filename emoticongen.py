import os, openai, requests, sys, urllib.request, json

from PIL import Image
from io import BytesIO

openai.api_key = "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"
client_id = "ChhQ0rmphSByTOqwQdPV"
client_secret = "JqdiGwWrAv"

def clova_papago(encText = ""):
    if encText == "":
        encText = urllib.parse.quote(input())
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        data = json.loads(response_body.decode('utf-8'))
        print(data['message']['result']['translatedText'])
        chat_gpt(data['message']['result']['translatedText'])
    else:
        print("Error Code:" + rescode)

def chat_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role":"system", "content": "You are a helpful describer for AI image generator"},
        {"role":"user", "content": "students studying at school"},
        {"role":"assistant", "content": "Students studying at school are typically seen sitting at desks in a classroom."},
        {"role":"user", "content":"Please describe \"" + prompt + "\", answer your description only and if you are unable to describe, text \"error\" first"}
        ],
        max_tokens = 2048
    )
    error_list = ["Error", "I'm s"]
    if response['choices'][0]['message']['content'][0:5] in error_list :
        print(clova_papago(response['choices'][0]['message']['content']))
        dall_e(prompt)
        return 0
    answer_gpt_detail = response['choices'][0]['message']['content']
    print(answer_gpt_detail)

    dall_e(answer_gpt_detail)

def dall_e(prompt):
    response = openai.Image.create(
        prompt = prompt,
        n = 4,
        size = "1024x1024"
    )

    for i in range(4):
        image_url = response['data'][i]['url']
        res = requests.get(image_url)
        img = Image.open(BytesIO(res.content))
        img.show()

print("키워드를 입력해주세요.")
clova_papago()