import requests
import json
import streamlit as st
import base64
from PIL import Image
from io import BytesIO
from time import sleep

#验证登录
key = st.text_input('请输入密码',value=None)  
true_key = 'ytf19961227'

@st.cache_data
def ask_ques(address,message):
    url = address
    #注意message必须是奇数条
    payload = json.dumps({"messages":message})
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.request("POST", url, headers=headers, data=payload).json()
    return res['result']
    
def main(address):
    messages = []
    i = 0
    while True:
        # 获取用户输入
        i = i+1
        user_input = st.text_input('请输入你的问题：'+':red[更换AI模型前务必刷新整个页面！！]',value=None,key=i)
        if user_input != None:
            d = {"role":"user","content":user_input}
            # 将用户输入添加到messages中
            messages.append(d)
            text = ask_ques(address,messages)
            d = {"role":"assistant","content":text}
            st.write(':green[AI：]'+text+'\n')
            messages.append(d)
        else :
            sleep(300)
            st.write(':red[您输入了太久！]')
            break
        
def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
    
def AI_draw(ques,url):

    payload = json.dumps({
        "prompt": "%s"%(str(ques)),
        "size": "1024x1024",
        "n": 1,
        "steps": 20,
        "sampler_index": "Euler a"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    res = requests.request("POST", url, headers=headers, data=payload).json()
    dic = res['data']
    b64code = dic[0]["b64_image"]
    img_data = base64.b64decode(b64code)
    image = Image.open(BytesIO(img_data))
    st.image(image)
    image.save("./ai.jpg")

if key == true_key:
    API_KEY = "LQIuATY8Ozjb2tcYfpAXwY8T"
    SECRET_KEY = "GHjTSHgtF9vEhx3dMkZFA0HeGp5x6m1I"
    access_token = get_access_token()

    ERNIE_Bot = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + access_token
    ERNIE_Bot_turbo = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token="+ access_token
    Llama_2_70b = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/llama_2_70b?access_token="+ access_token
    Qianfan_Chinese_Llama_2_7B = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/qianfan_chinese_llama_2_7b?access_token="+ access_token
    Qianfan_BLOOMZ_7B_compressed = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/qianfan_bloomz_7b_compressed?access_token=" + access_token
    ChatGLM2_6B_32K = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatglm2_6b_32k?access_token=" + access_token
    ERNIE_Bot_4  = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token
    Stable_Diffusion_XL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/text2image/sd_xl?access_token=" + access_token
    #选择使用功能
    op_func =['ERNIE_Bot','ERNIE_Bot_turbo','Llama_2_70b','Qianfan_Chinese_Llama_2_7B','Qianfan_BLOOMZ_7B_compressed','ChatGLM2_6B_32K','ERNIE_Bot_4','Stable_Diffusion_XL']
    Help = ['百度自行研发的大语言模型免费版（不推荐）','百度自行开发的模型，响应速度更快（推荐）','Meta AI研发并\
            开源，在编码、推理及知识应用等场景表现优秀，Llama-2-70b-chat是高精度效果的原生开源版本（英文输出）','Llama-2-7b模型的中文版，在CMMLU、C-EVAL等中文数据集上表现优异。','BLOOMZ-7B的中文版，融合量化、稀疏化\
            等技术，显存占用低。','智谱AI与清华KEG实验室发布的中英双语对话模型，强化了对于长文本的理解能力，能够\
            更好的处理最多32K长度的上下文。','文心一言4.0版本，更智能（收费高）','业内知名的跨模态大模型，由StabilityAI研发并开源，建议采用英文描述(仅该模型可绘图)']
    
    choose_func = st.radio(':rainbow[请选择AI模型]',op_func,captions=Help,index=0)
    if choose_func == op_func[0]:
        ip = ERNIE_Bot
        main(ip)
    if choose_func == op_func[1]:
        ip = ERNIE_Bot_turbo
        main(ip)
    if choose_func == op_func[2]:
        ip = Llama_2_70b
        main(ip)
    if choose_func == op_func[3]:
        ip = Qianfan_Chinese_Llama_2_7B
        main(ip)
    if choose_func == op_func[4]:
        ip = Qianfan_BLOOMZ_7B_compressed
        main(ip)
    if choose_func == op_func[5]:
        ip = ChatGLM2_6B_32K
        main(ip)
    if choose_func == op_func[6]:
        ip = ERNIE_Bot_4
        main(ip)
    if choose_func == op_func[7]:
        ip = Stable_Diffusion_XL
        ask = st.text_input('你想要AI作什么样的图？')
        if st.button("确认绘图"):
            AI_draw(ask,ip)

else:
    st.write('请输入正确的密码！')
