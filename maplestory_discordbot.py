import discord
import json
from datetime import datetime
# External File
# Define the prefix. All command can call after prefix.
def get_token():
    with open('D:\개발중\Discord Bot\discord_bot_tokken_parameter.json', 'r') as file:
        json_data = json.load(file)
    file.close()
    return json_data['bot-token']
#on_ready
    # This event runs when load the bot or re-load.
    # :return: None
class MyClient(discord.Client):
    #onready
    async def on_ready(self): 
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))

    """
        This event runs when receive message. but It has no restriction of prefix.
        :param message: discord.Message
        :return: None
        """
    async def on_message(self, message):
        if message.author == self.user:
            return 
        if message.content == '!ping':
            await message.channel.send('pong{0.author.mention}'.format(message))
        else:
            answer= self.get_answer(message.content)
            await message.channel.send(answer)
    def get_day(self):
        day_list = ['월', '화', '수', '목', '금', '토', '일']
        weekday = day_list[datetime.today().weekday()]
        date = datetime.today.strftime("%Y년 %m월 %d일")
        result = '{}({})'.format(date, weekday)
        return result
    def get_time(self):
        return datetime.today().strftime("%H시 %M분 %S초")
    
    def get_answer(self,text):
        trim_text = text.replace(" ", "")
        answer_dick = {
            '안녕': '안녕하세요. 명섭의 노예입니다.',
            '요일': ':calendar: 오늘은 {}입니다'.format(self.get_day_of_week()),
            '시간': ':clock9: 현재 시간은 {}입니다.'.format(self.get_time()),
            '꺼져':'꺼지겠습니다',
        }
        if trim_text == '' or None:
            return "알 수 없는 질의입니다. 답변을 드릴 수 없습니다."
        elif trim_text in answer_dick.keys():
            return answer_dick[trim_text]
        else:
            for key in answer_dick.keys():
                if key.find(trim_text) != -1:
                    return "연관 단어 [" + key + "]에 대한 답변입니다.\n" + answer_dick[key]

            for key in answer_dick.keys():
                if answer_dick[key].find(text[1:]) != -1:
                    return "질문과 가장 유사한 질문 [" + key + "]에 대한 답변이에요.\n" + answer_dick[key]

        return text + "은(는) 없는 질문입니다."
    
intents = discord.Intents.default()
intents.message_content=True
clinet = MyClient(intents=intents)
clinet.run(get_token())