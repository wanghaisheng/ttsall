import requests
import base64
import os
import time
from traceback import print_exc
import random
import json
from time import sleep
from requests.exceptions import Timeout

# 功能	限制说明	避免直接拼接json文本，尽量使用转换库，避免造成转义符等导致json格式错误
# 输入	文本内容	匹配发音人语种信息，不可读文本将会被过滤
# 文本长度

# 非流式场景下上限为 1000 个utf-8字符
# 流式场景下为 2000 个utf-8字符
# 包括空格、标点、汉字、字母等。超出上限会返回接口错误以及对应状态码



# 配置参数 #
# payload配置参数为json字符串格式

# 字段	描述	类型	是否必传	默认值
# text	输入文本	string	否。text与ssml字段至少一个非空，若二者都非空则按照ssml字段	-
# ssml	输入文本(SSML格式)，与text字段至少一个非空	string	否。text与ssml字段至少一个非空，若二者都非空则按照ssml字段	-
# speaker	发音人，具体见附录：发音人列表	string	是	-
# audio_config	补充参数	object	否	
# audio_config.format	输出音频编码格式，wav/mp3/aac	string	否	mp3
# audio_config.sample_rate	输出音频采样率，可选值 [8000,16000,22050,24000,32000,44100,48000]	number	否	24000
# audio_config.speech_rate	语速，取值范围[-50,100]，100代表2.0倍速，-50代表0.5倍数	number	否	0
# audio_config.pitch_rate	音调，取值范围[-12,12]	number	否	0
# audio_config.enable_timestamp	是否选择同时返回字与音素时间戳	bool	否	false


# tts_payload = json.dumps({
#     "text": "欢迎使用文本转语音服务。",
#     "speaker": "zh_female_qingxin",
#     "audio_config": {
#         "format": "wav",
#         "sample_rate": 24000,
#         "speech_rate": 0,
#     },
# })


# HTTP状态码
# 业务状态码	错误信息	错误说明	解决办法
# 400	40402004	TTSInvalidSpeaker	
# TTS发音人设置无效
# 检查TTS发音人是否正确设置
# 400	40402001	TTSEmptyText	TTS未设置文本	检查TTS文本是否设置
# 400	40402002	TTSInvalidText	TTS设置文本非法	检查TTS文本与发音人可能不匹配、无可读内容
# 400	40402003	
# TTSExceededTextLimit
# TTS文本长度超限	检查TTS文本是否超限。非流式接口上限为 1000 个utf-8字符；流式接口上限为 2000 个utf-8字符（包括空格、标点、汉字、字母等）

def speak(content,rate,voice,voiceidx):
    
    try: 
        headers = {
            'authority': 'translate.volcengine.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            # 'origin': 'chrome-extension://jmnhemdajboodicneejdlpanmijclhef',
            'accept-encoding': 'gzip, deflate, br',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'none',
            # 'cookie':'x-jupiter-uuid=1685206167481291; i18next=zh-CN; s_v_web_id=verify_li6888fu_E2yIFhRA_Amo7_42lt_93A0_OrjFArSkTope; ttcid=29381a8ff7874daea9f91f7bb6a91c4b41; isIntranet=-1; ve_doc_history=4640; tt_scid=QmoChhEFFYvYA9lNkQwiGu8VOuOiJDyGbcNg7Ysc9h4O-ceoZRVLq0cw5H4qbVSl79af; __tea_cache_tokens_3569={"web_id":"7237905415249118780","user_unique_id":"7237905415249118780","timestamp":1685208803602,"_type_":"default"}; referrer_title=音视频文件翻译API--机器翻译-火山引擎',
            'content-type':'application/json; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51',

        }

        json_data = {
            "text": content,
            "speaker":voice,
            "language":"zh",
            # "audio_config": {
            #         "format": "wav",
            #         "sample_rate": 24000,
            #         "speech_rate": 0,
            #     }
        }
        data=json.dumps(json_data)
        # json serializes Python dictionaries to JSON. data takes arbitrary bytes.

        max_retries = 3
        timeout = 15

        retry_count = 0
        while retry_count < max_retries:
            try:
                # fname=voice+'-'+str(voiceidx)+'-'+str(time.time())
                fname=voice+'-'+str(voiceidx)
                
                if not os.path.exists('./results/'+fname+'.mp3'):                
                    response = requests.post('https://translate.volcengine.com/crx/tts/v1/',  headers=headers, json= json_data,proxies={'http':None,'https':None}, timeout=timeout)
                    
                    # response = requests.post('https://translate.volcengine.com/crx/tts/v1/',  headers=headers, data= data,proxies={'http':None,'https':None}, timeout=timeout)
                    
                    response.raise_for_status()
                    print('Request successful!')
                    # print('Response:', response.text)
                    if response.json()['audio']['data']:                
                        b64=base64.b64decode(response.json()['audio']['data'])

                                
                        with open('./results/'+fname+'.mp3','wb') as ff:
                            ff.write(b64)
                    else:
                        print('response content has no audio data filed',response.text)
                        retry_count += 1
                        break
                                
                return ('./results/'+fname+'.mp3')                
                break
            except Timeout:
                print('Request timed out. Retrying...')
                retry_count += 1
            except requests.RequestException as e:
                print('An error occurred:', e)
                break

        if retry_count == max_retries:
            print('Maximum number of retries reached.')


        
    except:
        print_exc()
        return None

speakers=[
    #清新女声
"zh_female_qingxin",
"zh_male_chunhou",
"zh_female_zhixing",
"zh_male_qinqie",
"zh_female_qiaopi",
"zh_female_tianmei",
"zh_male_cartoonboy",
"zh_male_cartoonbaby",
"zh_male_rap",
"zh_female_sichuan",
"zh_female_mengyatou",
"zh_male_taiwan",
"zh_female_zhubo",
"zh_male_zhubo"]


speakersall=[
    #清新女声
"zh_female_qingxin",
"zh_male_chunhou",
"zh_female_zhixing",
"zh_male_qinqie",
"zh_female_qiaopi",
"zh_female_tianmei",
"zh_male_cartoonboy",
"zh_male_cartoonbaby",
"zh_male_rap",
"zh_female_sichuan",
"zh_female_mengyatou",
"zh_male_taiwan",
"zh_female_zhubo",
"zh_male_zhubo",
# 东北话
"tts.other.BV021_streaming",
#粤语男声
"tts.other.BV026_streaming",
#台湾女生
"tts.other.BV025_streaming",
#影视配音
"zh_male_xiaoming",

"zh_male_ad",
"zh_male_commentate",
#少儿故事
"zh_female_story", 
"tts.参考Q2.BV700_streaming",
"tts.other.BV406_streaming",
"tts.other.BV407_streaming",
"tts.参考Q2.BV001_streaming",
"tts.other.BV002_streaming",
"tts.BV701DialogMale.BV701_streaming",
"tts.BV123DialogMale.BV123_streaming",
"tts.BV120DialogMale.BV120_streaming",
"tts.BV119DialogMale.BV119_streaming",
"tts.BV115DialogFemale.BV115_streaming",
"tts.BV107DialogMale.BV107_streaming",
"tts.BV100DialogMale.BV100_streaming",
"tts.BV104DialogFemale.BV104_streaming",
"tts.BV004DialogMale.BV004_streaming",
"tts.BV113DialogFemale.BV113_streaming",
"tts.BV102DialogMale.BV102_streaming",
"tts.other.BV405_streaming",
"tts.other.BV007_streaming",
"tts.other.BV009_streaming",
"tts.other.BV419_streaming",
"tts.other.BV415_streaming",
"tts.other.BV008_streaming",
"tts.other.BV408_streaming",
"tts.other.BV403_streaming",
"tts.other.BV158_streaming",
"tts.other.BV157_streaming",
"tts.other.BR001_streaming",
"tts.other.BV410_streaming",
"tts.other.BV411_streaming",
"tts.other.BV412_streaming",
"tts.other.BV159_streaming",
"tts.other.BV418_streaming",
"tts.BV120DialogMale.BV120_streaming",
"tts.other.BV142_streaming",
"tts.other.BV143_streaming",
"tts.other.BV056_streaming",
"tts.other.BV005_streaming",
"tts.other.BV064_streaming",
"tts.other.BV051_streaming",
"tts.other.BV063_streaming",
"tts.other.BV417_streaming",
"tts.other.BV050_streaming",
"tts.other.BV061_streaming",
"tts.other.BV401_streaming",
"tts.other.BV402_streaming",
"tts.other.BV006_streaming",
"tts.other.BV011_streaming",
"tts.other.BV012_streaming",
"tts.other.BV034_streaming",
"tts.other.BV033_streaming",
"tts.other.BV511_streaming",
"tts.other.BV505_streaming",
"tts.other.BV516_streaming",
"tts.other.BV138_streaming",
"tts.other.BV027_streaming",
"tts.other.BV502_streaming",
"tts.other.BV503_streaming",
"tts.other.BV504_streaming",
"tts.other.BV421_streaming",
"tts.other.BV506_streaming",
"tts.other.BV040_streaming",
"tts.other.BV520_streaming",
"tts.other.BV523_streaming",
"tts.other.BV521_streaming",
"tts.other.BV421_streaming",
"tts.other.BV522_streaming",
"tts.other.BV524_streaming",
"tts.other.BV531_streaming",
"tts.other.BV530_streaming",
"tts.other.BV421_streaming",
"tts.other.BV065_streaming",
"tts.other.BV421_streaming",
"tts.other.BV421_streaming",
"tts.other.BV421_streaming",
"tts.other.BV421_streaming",
"tts.other.BV021_streaming",
"tts.other.BV020_streaming",
"tts.other.BV210_streaming",
"tts.other.BV217_streaming",
"tts.other.BV213_streaming",
"tts.other.BV025_streaming",
"tts.other.BV026_streaming",
"tts.other.BV424_streaming",
"tts.other.BV212_streaming",
"tts.other.BV019_streaming",
"tts.other.BV221_streaming",
"tts.other.BV423_streaming",
"tts.other.BV214_streaming",
]

en=[
    "en_male_adam",
"en_male_bob",
"en_female_kat",
"en_female_sarah",
"en_male_dryw",
"jp_female_mai",
"jp_female_hana",
"jp_female_yui",
"jp_male_satoshi",
"kr_male_kim",   
]
text="我们自豪地向您介绍火山写作：一款中英双语的AI写作助手。您可以使用它来撰写和润色您的论文、博客、电子邮件等！在写作英文时，火山写作会实时扫描您的文章供修改和增强建议，使您的英文表达更流畅、准确、恰当。如下所示："
# text=text.encode("utf-8")


text = "Sincerely, I have never used it. Its softness and moisturization make it feel great.Then my skin feels refreshed, hydrated, and doesn't really smell at all! I used lots of makeup wipes in the past- and Aveeno was my favorite (the no fragrance one). But THIS Neutrogena one is better than Aveeno!! It makes my skin feel better, and the wipes are a lot softer. My makeup comes off really easily, and it feels like a skin care wipe in a lot of ways. It doesn't feel like harsh chemicals or anything when I was taking off my mascara and eyeshadow. I saw Jenna Ortega advertise for them, and I had to try it LOL. Also the reviews were really good and it says "#1 best seller" on Amazon. I can see why! Only thing I would recommend is to make the wipes MORE hydrating. You can never get too much hydration! Also there is a slight scent, which smells good, but please make one with ZERO fragrance. Also on the Yuka app it says it has this Poly ingredient or something that's not super good for you (A LOT of makeup wipe brands have this ingredient), so please make ones without that! Lol. But yeah it gets all my makeup off pretty easily!"
unavailable=[]
supported=[]


supported_zh=['zh_female_qingxin', 'zh_male_chunhou', 'zh_male_rap', 'zh_female_sichuan', 'zh_female_zhubo', 'zh_male_zhubo', 'tts.other.BV021_streaming', 'tts.other.BV026_streaming', 'tts.other.BV025_streaming', 'zh_male_xiaoming', 'zh_female_story', 'tts.other.BV406_streaming', 'tts.other.BV407_streaming', 'tts.other.BV002_streaming', 'tts.BV701DialogMale.BV701_streaming', 'tts.BV123DialogMale.BV123_streaming', 'tts.BV120DialogMale.BV120_streaming', 'tts.BV119DialogMale.BV119_streaming', 'tts.BV115DialogFemale.BV115_streaming', 'tts.BV107DialogMale.BV107_streaming', 'tts.BV100DialogMale.BV100_streaming', 'tts.BV104DialogFemale.BV104_streaming', 'tts.BV004DialogMale.BV004_streaming', 'tts.BV113DialogFemale.BV113_streaming', 'tts.BV102DialogMale.BV102_streaming', 'tts.other.BV405_streaming', 'tts.other.BV007_streaming', 'tts.other.BV419_streaming', 'tts.other.BV415_streaming', 'tts.other.BV408_streaming', 'tts.other.BV403_streaming', 'tts.other.BV158_streaming', 'tts.other.BR001_streaming', 'tts.other.BV411_streaming', 'tts.other.BV412_streaming', 'tts.other.BV418_streaming', 'tts.BV120DialogMale.BV120_streaming', 'tts.other.BV142_streaming', 'tts.other.BV143_streaming', 'tts.other.BV005_streaming', 'tts.other.BV064_streaming', 'tts.other.BV051_streaming', 'tts.other.BV063_streaming', 'tts.other.BV417_streaming', 'tts.other.BV050_streaming', 'tts.other.BV061_streaming', 'tts.other.BV401_streaming', 'tts.other.BV402_streaming', 'tts.other.BV006_streaming', 'tts.other.BV011_streaming', 'tts.other.BV012_streaming', 'tts.other.BV034_streaming', 'tts.other.BV033_streaming', 'tts.other.BV511_streaming', 'tts.other.BV505_streaming', 'tts.other.BV516_streaming', 'tts.other.BV138_streaming', 'tts.other.BV027_streaming', 'tts.other.BV502_streaming', 'tts.other.BV503_streaming', 'tts.other.BV506_streaming', 'tts.other.BV520_streaming', 'tts.other.BV523_streaming', 'tts.other.BV521_streaming', 'tts.other.BV531_streaming', 'tts.other.BV530_streaming', 'tts.other.BV065_streaming', 'tts.other.BV021_streaming', 'tts.other.BV210_streaming', 'tts.other.BV217_streaming', 'tts.other.BV213_streaming', 'tts.other.BV025_streaming', 'tts.other.BV026_streaming', 'tts.other.BV424_streaming', 'tts.other.BV212_streaming', 'tts.other.BV221_streaming', 'tts.other.BV423_streaming', 'tts.other.BV214_streaming']

unavailable_zh=['zh_female_zhixing', 'zh_male_qinqie', 'zh_female_qiaopi', 'zh_female_tianmei', 'zh_male_cartoonboy', 'zh_male_cartoonbaby', 'zh_female_mengyatou', 'zh_male_taiwan', 'zh_male_ad', 'zh_male_commentate', 'tts.参考Q2.BV700_streaming', 'tts.参考Q2.BV001_streaming', 'tts.other.BV009_streaming', 'tts.other.BV008_streaming', 'tts.other.BV157_streaming', 'tts.other.BV410_streaming', 'tts.other.BV159_streaming', 'tts.other.BV056_streaming', 'tts.other.BV504_streaming', 'tts.other.BV421_streaming', 'tts.other.BV040_streaming', 'tts.other.BV421_streaming', 'tts.other.BV522_streaming', 'tts.other.BV524_streaming', 'tts.other.BV421_streaming', 'tts.other.BV421_streaming', 'tts.other.BV421_streaming', 'tts.other.BV421_streaming', 'tts.other.BV421_streaming', 'tts.other.BV020_streaming', 'tts.other.BV019_streaming']




supported_en=['zh_female_qingxin', 'zh_male_chunhou', 'zh_male_rap', 'zh_female_sichuan', 'zh_female_zhubo', 'zh_male_zhubo', 'tts.other.BV021_streaming', 'tts.other.BV026_streaming', 'tts.other.BV025_streaming', 'zh_male_xiaoming', 'zh_female_story', 'tts.other.BV406_streaming', 'tts.other.BV407_streaming', 'tts.other.BV002_streaming', 'tts.BV701DialogMale.BV701_streaming', 'tts.BV123DialogMale.BV123_streaming', 'tts.BV120DialogMale.BV120_streaming', 'tts.BV119DialogMale.BV119_streaming', 'tts.BV115DialogFemale.BV115_streaming', 'tts.BV107DialogMale.BV107_streaming', 'tts.BV104DialogFemale.BV104_streaming', 'tts.BV004DialogMale.BV004_streaming', 'tts.BV113DialogFemale.BV113_streaming', 'tts.BV102DialogMale.BV102_streaming', 'tts.other.BV405_streaming', 'tts.other.BV007_streaming', 'tts.other.BV419_streaming', 'tts.other.BV408_streaming', 'tts.other.BV403_streaming', 'tts.other.BV158_streaming', 'tts.other.BR001_streaming', 'tts.other.BV410_streaming', 'tts.other.BV411_streaming', 'tts.other.BV412_streaming', 'tts.BV120DialogMale.BV120_streaming', 'tts.other.BV142_streaming', 'tts.other.BV143_streaming', 'tts.other.BV056_streaming', 'tts.other.BV005_streaming', 'tts.other.BV064_streaming', 'tts.other.BV051_streaming', 'tts.other.BV063_streaming', 'tts.other.BV417_streaming', 'tts.other.BV050_streaming', 'tts.other.BV061_streaming', 'tts.other.BV402_streaming', 'tts.other.BV011_streaming', 'tts.other.BV012_streaming', 'tts.other.BV034_streaming', 'tts.other.BV033_streaming', 'tts.other.BV511_streaming', 'tts.other.BV505_streaming', 'tts.other.BV516_streaming', 'tts.other.BV027_streaming', 'tts.other.BV506_streaming', 'tts.other.BV523_streaming', 'tts.other.BV521_streaming', 'tts.other.BV065_streaming', 'tts.other.BV021_streaming', 'tts.other.BV210_streaming', 'tts.other.BV217_streaming', 'tts.other.BV213_streaming', 'tts.other.BV025_streaming', 'tts.other.BV026_streaming', 'tts.other.BV424_streaming', 'tts.other.BV212_streaming', 'tts.other.BV221_streaming', 'tts.other.BV423_streaming', 'tts.other.BV214_streaming']

unavailable_en=['zh_female_zhixing', 'zh_male_qinqie', 'zh_female_qiaopi', 'zh_female_tianmei', 'zh_male_cartoonboy', 'zh_male_cartoonbaby', 'zh_female_mengyatou', 'zh_male_taiwan', 'zh_male_ad', 'zh_male_commentate', 'tts.参考Q2.BV700_streaming', 'tts.参考Q2.BV001_streaming', 'tts.BV100DialogMale.BV100_streaming', 'tts.other.BV009_streaming', 'tts.other.BV415_streaming', 'tts.other.BV008_streaming', 'tts.other.BV157_streaming', 'tts.other.BV159_streaming', 'tts.other.BV418_streaming', 'tts.other.BV401_streaming', 'tts.other.BV006_streaming', 'tts.other.BV138_streaming', 'tts.other.BV502_streaming', 'tts.other.BV503_streaming', 'tts.other.BV504_streaming', 'tts.other.BV421_streaming', 'tts.other.BV040_streaming', 'tts.other.BV520_streaming', 'tts.other.BV421_streaming', 'tts.other.BV522_streaming', 'tts.other.BV524_streaming', 'tts.other.BV531_streaming', 'tts.other.BV530_streaming', 'tts.other.BV421_streaming', 'tts.other.BV421_streaming', 'tts.other.BV421_streaming', 'tts.other.BV421_streaming', 'tts.other.BV421_streaming', 'tts.other.BV020_streaming', 'tts.other.BV019_streaming']


supported_en=['en_male_adam', 'en_male_bob', 'en_female_sarah', 'jp_female_mai', 'jp_male_satoshi']


unavailable_en=['en_female_kat', 'en_male_dryw', 'jp_female_hana', 'jp_female_yui', 'kr_male_kim']

for speaker in supported_zh:
    print('choose speaker',speaker)
    with open('tests/口播.txt','r') as ff: 
        text_contents=ff.readlines()   
    for idx,text in enumerate(text_contents):
        print(str(idx),text)
        sleep_time = random.uniform(1, 5)
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)
        if text is not None:
            
            res= speak(text,'',speaker,idx)
            if res is None:
                unavailable.append(speaker)
            else:
                supported.append(speaker)
# print(
#     supported
# )
# print(
#     '==============\n'
# )

# print(
#     unavailable
# )
