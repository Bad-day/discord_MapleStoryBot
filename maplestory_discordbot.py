import discord
import json
import numpy as np
import asyncio
from datetime import datetime
from discord.ext import commands
# External File
# Define the prefix. All command can call after prefix.
# client = commands.Bot(command_prefix='!')
#on_ready
    # This event runs when load the bot or re-load.
    # :return: None
    
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("도움말 명령어는 !키워드"))

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content == 'ping':
            await message.channel.send('pong {0.author.mention}'.format(message))
        else:
            answer = self.get_answer(message.content)
            await message.channel.send(answer)
        # if message.content.startswith ("!청소"): # '!청소'를 입력한다면

        #     amount = message.content[4:] # '!청소 숫자' 에서 숫자를 인식하여 amount의 값을 넣는다.
        #     await message.delete()
        #     await message.channel.purge(limit=int(amount))
    def get_day_of_week(self):
        weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

        weekday = weekday_list[datetime.today().weekday()]
        date = datetime.today().strftime("%Y년 %m월 %d일")
        result = '{}({})'.format(date, weekday)
        return result

    def get_time(self):
        return datetime.today().strftime("%H시 %M분 %S초")
    
    # def Weapone_additional_Options(self):
    def royal_style_simul(self):
        royal_list=["[스페셜 라벨] 스파이럴 펑크","[스페셜 라벨] 스파이럴 플라이","[스페셜 라벨] 스파이럴 구두 (남) / 스파이럴 힐 (여)","[스페셜 라벨] 스파이럴 쇼크 (남) / 스파이럴 시크 (여)","[스페셜 라벨] 닥터 스파이럴","암흑 실크햇|암흑 레이스",
                    "고결한 암흑 (남) / 우아한 암흑 (여)","암흑 사박 (남) / 암흑 사뿐 (여)","암흑의 균열","암흑 감시자","펑크 고글","펑크 태엽","펑크 모노클","펑크 배낭","루시드 페도라 / 루시드 실크햇","루시드 드림 (남) / 루시드 드림 (여)"	
                    ,"꿈결"	,"새장 속 영혼"	,"자유로운 영혼","퍼피 레글런티","파깅스","[30일] 스파이럴 말풍선 반지 교환권","[30일] 스파이럴 명찰 반지 교환권"	,"박쥐의 주인 이펙트 교환권","스카우터"]
        choice_result = np.random.choice(royal_list, 1, p=[0.025, 0.03, 0.032, 0.032, 0.031, 0.04,0.015,0.05,0.04,0.04,0.04,0.05,0.04,0.05,0.035,0.02,0.03,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05])
        return choice_result
        
    def cube_simul(self):
        emblem_1 = ["STR : +12%","DEX : +12%","INT : +12%","LUK : +12%","공격력 : +12%","마력 : +12%","크리티컬 확률 : +12%","데미지 : +12%","올스탯 : +9%","캐릭터 기준 10레벨 당 공격력 : +1","캐릭터 기준 10레벨 당 마력 : +1","몬스터 방어율 무시 : +35%","몬스터 방어율 무시 : +40%"]
        emblem_2 = ["STR : +9%","DEX : +9%","INT : +9%","LUK : +9%","공격력 : +9%","마력 : +9%","크리티컬 확률 : +9%","데미지 : +9%","올스탯 : +6%","몬스터 방어율 무시 : +30%","STR : +12%","DEX : +12%","INT : +12%","LUK : +12%","공격력 : +12%","마력 : +12%","크리티컬 확률 : +12%","데미지 : +12%","올스탯 : +9%","캐릭터 기준 10레벨 당 공격력 : +1","캐릭터 기준 10레벨 당 마력 : +1","몬스터 방어율 무시 : +35%","몬스터 방어율 무시 : +40%"]
        emblem_3 = ["STR : +9%","DEX : +9%","INT : +9%","LUK : +9%","공격력 : +9%","마력 : +9%","크리티컬 확률 : +9%","데미지 : +9%","올스탯 : +6%","몬스터 방어율 무시 : +30%","STR : +12%","DEX : +12%","INT : +12%","LUK : +12%","공격력 : +12%","마력 : +12%","크리티컬 확률 : +12%","데미지 : +12%","올스탯 : +9%","캐릭터 기준 10레벨 당 공격력 : +1","캐릭터 기준 10레벨 당 마력 : +1","몬스터 방어율 무시 : +35%","몬스터 방어율 무시 : +40%"]
        # emblem_exe_num = int(input("시행 횟수 입력 : "))
        emblem_exe_num = 1
        choice_result1 = np.random.choice(emblem_1, emblem_exe_num, p=[0.114285,0.114285,0.114286,0.114286,0.057143,0.057143,0.057143,0.057143,0.085714,0.057143,0.057143,0.057143,0.057143])
        choice_result2 = np.random.choice(emblem_2, emblem_exe_num, p=[0.1125,0.1125,0.1125,0.1125,0.0675,0.0675,0.09,0.0675,0.09,0.0675,0.011429,0.011429,0.011429,0.011429,0.005714,0.005714,0.005714,0.005714,0.008572,0.005714,0.005714,0.005714,0.005714])
        choice_result3 = np.random.choice(emblem_3, emblem_exe_num, p=[0.12375,0.12375,0.12375,0.12375,0.07425,0.07425,0.099,0.07425,0.099,0.07425,0.001143,0.001143,0.001143,0.001143,0.000571,0.000571,0.000571,0.000571,0.00086,0.000571,0.000571,0.000571,0.000571])
        # for i in range(emblem_exe_num):
        return choice_result1,'\n',choice_result2,'\n',choice_result3
    
    def green_jade_ha(self):
        box_count=1
        seedring_list=["리스트레인트링","컨티뉴어스 링","웨폰퍼프 - S링","웨폰퍼프 - I링","웨폰퍼프 - L링","웨폰퍼프 - D링","얼티메이덤 링","리스크테이커 링","링 오브 썸 링","크리데미지 링","크라이시스 - HM링","버든리프트 링","오버패스 링","레벨퍼프 - S링","레벨퍼프 - I링","레벨퍼프 - L링","레벨퍼프 - D링","헬스컷 링","크리디펜스 링","리밋 링","듀라빌리티 링","리커버디펜스 링","실드스와프 링","마나컷 링","크라이시스 - H링","크라이시스 - M링","크리쉬프트 링","스탠스쉬프트 링","리커버스텐스 링","스위프트 링","리플렉티브 링"]
        seedring_choice_list_green_jade_ha = np.random.choice(seedring_list, box_count, p=[0.02112678732392759, 0.02112678732392759, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265])
        seedring_level_list=["LV1","LV2","LV3"]
        seedring_level_choice_list_green_jade_ha=np.random.choice(seedring_level_list, box_count, p=[0.5, 0.41, 0.09])
        result = str(seedring_choice_list_green_jade_ha[0] +" "+ seedring_level_choice_list_green_jade_ha[0] )
        # select_seedring_result = str(seedring_choice_list_green_jade_ha, seedring_level_choice_list_green_jade_ha)
        return result


    
    def get_answer(self, text):
        trim_text = text.replace(" ", "")
        
        
        answer_dict = {
            '안녕': '안녕하세요. 명섭의 노예입니다.',
            '요일': ':calendar: 오늘은 {}입니다'.format(self.get_day_of_week()),
            '시간': ':clock9: 현재 시간은 {}입니다.'.format(self.get_time()),
            '꺼져':':thinking:  ',
            '키워드':'안녕 : 인사해줍니다. \n요일: 오늘의 요일을 알려줍니다\n시간: 현재 시간을 알려줍니다. \n꺼져 : 꺼집니다\n로얄스타일: 로얄스타일 1개 개봉. \n 큐브: 큐브 1개를 사용한 결과 \n 시드링하급:녹옥의 반지 상자(하급) 1개를 개봉합니다',
            '로얄스타일': '결과 : {}'.format(self.royal_style_simul()),
            '큐브': '결과 : {}'.format(self.cube_simul()),
            '시드링하급': '결과 : {}'.format(self.green_jade_ha())
        }
        return answer_dict[trim_text]
        # if trim_text == '' or None:
        #     return "알 수 없는 질의입니다. 답변을 드릴 수 없습니다."
        # elif trim_text in answer_dict.keys():
        #     return answer_dict[trim_text]
        # else:
        #     for key in answer_dict.keys():
        #         if key.find(trim_text) != -1:
        #             return "연관 단어 [" + key + "]에 대한 답변입니다.\n" + answer_dict[key]

        #     for key in answer_dict.keys():
        #         if answer_dict[key].find(text[1:]) != -1:
        #             return "질문과 가장 유사한 질문 [" + key + "]에 대한 답변이에요.\n" + answer_dict[key]

        # return text + "은(는) 없는 질문입니다."

def get_token():
    with open('D:\개발중\Discord Bot\discord_bot_tokken_parameter.json', 'r') as file:
        json_data = json.load(file)
    file.close()
    return json_data['bot-token']
intents = discord.Intents.default()
intents.message_content=True
clinet = MyClient(intents=intents)
clinet.run(get_token())

# 추가할 기능
# 무기 추옵계산
# 유니온 성능,링크
# 골드애플 시뮬
# 주간보스 장부
# 극딜순서
#https://velog.io/@eastminn/discord-2 <- 삭제 관련