import discord
import yt_dlp as youtube_dl
import numpy as np
from discord.ext import commands
from discord_bot_tokken_parameter import Token
import asyncio
import urllib.request
from PIL import Image
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


# youtube 음악과 로컬 음악의 재생을 구별하기 위한 클래스 작성.
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


# 음악 재생 클래스. 커맨드 포함.
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    status=discord.Status.online, activity=discord.Game("도움말 명령어는 !키워드"),
    description='Relatively simple music bot example',
    intents=intents,
)
# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Red', description='Your favourite colour is red', emoji='🟥'),
            discord.SelectOption(label='Green', description='Your favourite colour is green', emoji='🟩'),
            discord.SelectOption(label='Blue', description='Your favourite colour is blue', emoji='🟦'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose your favourite colour...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(Dropdown())
        
@bot.command(aliases=['color'])
async def colour(ctx):
    """Sends a message with our dropdown containing colours"""

    # Create the view containing our dropdown
    view = DropdownView()

    # Sending a message containing our view
    await ctx.send('Pick your favourite colour:', view=view)

class MapleStory_Seedring_Simul(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def green_jade_ha(self):
        box_count=1
        seedring_list=["리스트레인트링","컨티뉴어스 링","웨폰퍼프 - S링","웨폰퍼프 - I링","웨폰퍼프 - L링","웨폰퍼프 - D링","얼티메이덤 링","리스크테이커 링","링 오브 썸 링","크리데미지 링","크라이시스 - HM링","버든리프트 링","오버패스 링","레벨퍼프 - S링","레벨퍼프 - I링","레벨퍼프 - L링","레벨퍼프 - D링","헬스컷 링","크리디펜스 링","리밋 링","듀라빌리티 링","리커버디펜스 링","실드스와프 링","마나컷 링","크라이시스 - H링","크라이시스 - M링","크리쉬프트 링","스탠스쉬프트 링","리커버스텐스 링","스위프트 링","리플렉티브 링"]
        seedring_choice_list_green_jade_ha = np.random.choice(seedring_list, box_count, p=[0.02112678732392759, 0.02112678732392759, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.028168983098610118, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265, 0.03521127887323265])
        seedring_level_list=["Lv1","Lv2","Lv3"]
        seedring_level_choice_list_green_jade_ha=np.random.choice(seedring_level_list, box_count, p=[0.5, 0.41, 0.09])
        result = str(seedring_choice_list_green_jade_ha[0] +" "+ seedring_level_choice_list_green_jade_ha[0] )
        return result
    
    def black_jade_ha(self):
        box_count=1
        seedring_list=['리스트레인트 링', '컨티뉴어스 링', '웨폰퍼프 - S링', '웨폰퍼프 - I링', '웨폰퍼프 - L링', '웨폰퍼프 - D링', '얼티메이덤 링', '리스크테이커 링', '링 오브 썸', '크리데미지 링', '크라이시스 - HM링']
        seedring_choice_list_red_jade_ha = np.random.choice(seedring_list, box_count, p=[0.1250000375000112, 0.1250000375000112, 0.08333332499999747, 0.08333332499999747, 0.08333332499999747, 0.08333332499999747, 0.08333332499999747, 0.08333332499999747, 0.08333332499999747, 0.08333332499999747, 0.08333332499999747])
        seedring_level_list=["Lv1","Lv2","Lv3","Lv4"]
        seedring_level_choice_list_green_jade_ha=np.random.choice(seedring_level_list, box_count, p=[0.25, 0.25, 0.30,0.2])
        result = str(seedring_choice_list_red_jade_ha[0] +" "+ seedring_level_choice_list_green_jade_ha[0] )
        # select_seedring_result = str(seedring_choice_list_green_jade_ha, seedring_level_choice_list_green_jade_ha)
        return result
    
    def white_jade_ha(self):
        box_count=1
        seedring_list=['리스트레인트 링', '컨티뉴어스 링', '웨폰퍼프 - S링', '웨폰퍼프 - I링', '웨폰퍼프 - L링', '웨폰퍼프 - D링', '얼티메이덤 링', '리스크테이커 링', '링 오브 썸', '크리데미지 링', '크라이시스 - HM링']
        seedring_choice_list_red_jade_ha = np.random.choice(seedring_list, box_count, p=[0.14285708571429143, 0.14285708571429143, 0.0793650920634908, 0.0793650920634908, 0.0793650920634908, 0.0793650920634908, 0.0793650920634908, 0.0793650920634908, 0.0793650920634908, 0.0793650920634908, 0.0793650920634908])
        seedring_level_list=["Lv3","Lv4"]
        seedring_level_choice_list_green_jade_ha=np.random.choice(seedring_level_list, box_count, p=[0.65,0.35])
        result = str(seedring_choice_list_red_jade_ha[0] +" "+ seedring_level_choice_list_green_jade_ha[0] )
        # select_seedring_result = str(seedring_choice_list_green_jade_ha, seedring_level_choice_list_green_jade_ha)
        return result
    
    def red_jade_ha(self):
        box_count=1
        seedring_list=["리스트레인트링","컨티뉴어스 링","웨폰퍼프 - S링","웨폰퍼프 - I링","웨폰퍼프 - L링","웨폰퍼프 - D링","얼티메이덤 링","리스크테이커 링","링 오브 썸 링","크리데미지 링","크라이시스 - HM링","버든리프트 링","오버패스 링","레벨퍼프 - S링","레벨퍼프 - I링","레벨퍼프 - L링","레벨퍼프 - D링","헬스컷 링","크리디펜스 링","리밋 링","듀라빌리티 링","리커버디펜스 링","실드스와프 링","마나컷 링","크라이시스 - H링","크라이시스 - M링","크리쉬프트 링","스탠스쉬프트 링","리커버스텐스 링","스위프트 링","리플렉티브 링"]
        seedring_choice_list_red_jade_ha = np.random.choice(seedring_list, box_count, p=[0.06923079307692072, 0.06923079307692072, 0.06153849384615064, 0.06153849384615064, 0.06153849384615064, 0.06153849384615064, 0.06153849384615064, 0.06153849384615064, 0.06153849384615064, 0.06153849384615064, 0.06153849384615064, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016, 0.01538459846154016])
        seedring_level_list=["Lv1","Lv2","Lv3","Lv4"]
        seedring_level_choice_list_green_jade_ha=np.random.choice(seedring_level_list, box_count, p=[0.4, 0.3, 0.2,0.1])
        result = str(seedring_choice_list_red_jade_ha[0] +" "+ seedring_level_choice_list_green_jade_ha[0] )
        return result
    
    @commands.command()
    async def 하(self, ctx):
        result = self.green_jade_ha()
        urllib.request.urlretrieve(f'https://raw.githubusercontent.com/Bad-day/discord_MapleStoryBot/main/img/%EB%85%B9%EC%98%A5.png', "explain.png")
        image = Image.open('explain.png')
        image = image.resize((1000,1000))
        image.save("green_jade.png")
        green_jade = discord.File("green_jade.png", filename='green_jade.png')
        embed=discord.Embed(title='녹옥의 보스 반지 상자 (하급) 사용결과', description=f'{result}가 나왔습니다.',color=0x55efc4)
        embed.set_thumbnail(url='attachment://green_jade.png')
        # embed.add_field(name='이름',vlaue='값',inline=True)
        await ctx.send(embed=embed,file=green_jade)
    @commands.command()
    async def 중(self, ctx):
        result = self.red_jade_ha()
        urllib.request.urlretrieve(f'https://raw.githubusercontent.com/Bad-day/discord_MapleStoryBot/main/img/%ED%99%8D%EC%98%A5.png', "explain.png")
        image = Image.open('explain.png')
        image = image.resize((1000,1000))
        image.save("red_jade.png")
        red_jade = discord.File("red_jade.png", filename='red_jade.png')
        embed=discord.Embed(title='홍옥의 보스 반지 상자 (중급) 사용결과', description=f'{result}가 나왔습니다.',color=0xd63031)
        embed.set_thumbnail(url='attachment://red_jade.png')
        # embed.add_field(name='이름',vlaue='값',inline=True)
        await ctx.send(embed=embed,file=red_jade)
    @commands.command()
    async def 상(self, ctx):
        result = self.black_jade_ha()
        urllib.request.urlretrieve(f'https://raw.githubusercontent.com/Bad-day/discord_MapleStoryBot/main/img/%ED%9D%91%EC%98%A5.png', "explain.png")
        image = Image.open('explain.png')
        image = image.resize((1000,1000))
        image.save("black_jade.png")
        black_jade = discord.File("black_jade.png", filename='black_jade.png') 
        embed=discord.Embed(title='흑옥의 보스 반지 상자 (상급) 사용결과', description=f'{result}가 나왔습니다.',color=0x636e72)
        embed.set_thumbnail(url='attachment://black_jade.png')
        # embed.add_field(name='이름',vlaue='값',inline=True)
        await ctx.send(embed=embed,file=black_jade)
    @commands.command()
    async def 최상(self, ctx):
        result = self.white_jade_ha()
        urllib.request.urlretrieve(f'https://raw.githubusercontent.com/Bad-day/discord_MapleStoryBot/main/img/%EB%B0%B1%EC%98%A5.png', "explain.png")
        image = Image.open('explain.png')
        image = image.resize((1000,1000))
        image.save("white_jade.png")
        white_jade = discord.File("white_jade.png", filename='white_jade.png')
        embed=discord.Embed(title='백옥의 보스 반지 상자 (최상급)', description=f'{result}가 나왔습니다.',color=0xdfe6e9) 
        embed.set_thumbnail(url='attachment://white_jade.png')
        # embed.add_field(name='이름',vlaue='값',inline=True)
        await ctx.send(embed=embed,file=white_jade)
        
    @commands.command()
    async def 시드상자드랍(self, ctx):
        await ctx.send(f'녹옥의 보스 반지 상자 (하급) \n 스우 (노멀) §   데미안 (노멀) §   가디언 엔젤 슬라임 (노멀)\n루시드 (이지, 노멀) §   윌 (이지, 노멀) §   더스크 (노멀)\n 듄켈 (노멀)\n\n홍옥의 보스 반지 상자 (중급)\n§   스우 (하드) §   데미안 (하드) §   루시드 (하드)§   윌 (하드) §   진 힐라 (노멀) \n\n흑옥의 보스 반지 상자 (상급)\n§   더스크 (카오스) §   듄켈 (하드) §   가디언 엔젤 슬라임 (카오스)\n§   진 힐라 (하드) §   선택받은 세렌 (노멀) -       백옥의 보스 반지 상자 (최상급)\n\n§   검은 마법사 (하드, 익스트림) §   선택받은 세렌 (하드, 익스트림)\n§   감시자 칼로스 (카오스) §   카링 (노멀)')
    #----------------------시드--------------------------#
    @commands.command()
    async def 키워드(self, ctx):
            embed = discord.Embed(title='음악봇 관련', description='!help')
            await ctx.send(embed=embed)
            embed = discord.Embed(title='메이플봇 - 시드시뮬레이션', \
            description='!하 : 녹옥의 보스 반지 상자 (하급)\n1개를 개봉합니다\n\n!중: 홍옥의 보스 반지 상자 (중급)\n1개를 개봉합니다.\n\n!상: 흑옥의 보스 반지 상자 (상급)\n 1개를 개봉합니다.\n\n!최상: 백옥의 보스 반지 상자 (최상급)\n 1개를 개봉합니다.\n\n!시드상자드랍: 난이도별 보스 반지 상자 드랍구간을 알려줍니다.')
            await ctx.send(embed=embed)
            embed = discord.Embed(title='메이플봇 - 농장관련',\
            description=' !필수농장 : 낑선 기준 필수로 뽑아야할 농장 몬스터 리스트를 출력합니다. \n\n!기간: 현재 뽑은 농장몬스터의 옵션 기간을 출력합니다.\n\n!농장킵: 농장몬스터를 뽑으며 필요하여 킵해야할 몬스터들 리스트를 출력합니다.\n\n!농장유지: 농장 몬스터를 뽑기위해 필수로 유지해야할 몬스터 리스트를 출력합니다.\n\n!공마:공격력/마력 을 증가시키는 몬스터 리스트를 출력합니다.\n\n!데미지: 데미지를 증가시키는 몬스터 리스트를 출력합니다.\n\n벞지: 버프지속시간을 증가시키는 몬스터 리스트를 출력합니다.\n\n!보공: 보스공격력을 증가시키는 몬스터 리스트를 출력합니다.\n\n!사냥: 경험치 획득량을 증가시키는 몬스터 리스트를 출력합니다.\n\n!스탯:STR/DEX/INT/LUK/올스탯을 증가시키는 몬스터 리스트를 출력합니다.\n\n크뎀: 크리티컬데미지를 증가시키는 몬스터 리스트를 출력합니다.\n\n기타: 재사용, 파이널어택 데미지 등 기타 사항 몬스터 리스트를 출력합니다.')
            await ctx.send(embed=embed)
            embed = discord.Embed(title='기타 추가사항',\
            description='농장 도우미 추가예정, 로얄스타일, 골드애플, 큐브 시뮬추가예정,\n주간보스 드랍템 입력 및 정산기능 추가예정')
            await ctx.send(embed=embed)
class MapleStory_farm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def 필수농장(self,ctx):
        embed = discord.Embed(title='낑선 기준 필수농장', description=f'<공/마>\n검그,미르,어둠루미,이퀄루미\n\n<데미지>\n검바,허수아비,쁘띠시그\n\n<크확>\n라즐리,팬텀\n\n<방무>\n라피스,쁘띠매,양철나무꾼\n\n<보공>\n쁘띠랑,반레온\n\n<크뎀>\n쁘띠힐라\n\n<기타>\n쁘띠은월-재사용\n\n<스탯류>\n라니아 올20(루미다있으면),성장한미르 올20,일반몬스터SS(개, 소),베릴',color=0xd63031)
        await ctx.send(embed=embed)
    @commands.command()
    async def 공마(self,ctx):
        await ctx.send(embed=discord.Embed(title='농장 공격력 / 마력 리스트', description=f'검은마법사의 그림자 -  공격력/마력 +6\n\n무공의분신 - 공격력+3\n\n미르 - 공격력/마력 +5\n\n루미너스(어둠) - 공격력/마력 +5\n\n루미너스(이퀄브리엄) - 20렙당 공격력/마력 + 1',color=0xdfe6e9))
    @commands.command()
    async def 스탯(self,ctx):
        await ctx.send(embed=discord.Embed(title='농장 스탯류 리스트', description=f'*스페셜기준입니다.\n\n\n마스터레드너그 - 힘 +15\n\n마스터렐릭 - 민첩 +15\n\n마스터 마르가나 - 지능+ 15\n\n마스터잭슨 - 올스텟 +5\n\n마스터 히삽 - 럭 + 15\n\n쁘띠 라니아 - 올스텟 + 20(쁘띠루미너스 전체 보유 시)\n\n성장한미르 - 올스텟 +20',color=0xdfe6e9))
    @commands.command()
    async def 벞지(self,ctx):
        await ctx.send(embed=discord.Embed(title='농장 버프지속시간 리스트', description=f'반반  - 버프지속시간 + 5%\n\n 쁘띠 아카이럼 -  버프지속시간 +5%\n\n군단장 윌 - 버프지속시간 +6%',color=0xdfe6e9))
    
    @commands.command()
    async def 보공(self,ctx):
        await ctx.send(embed=discord.Embed(title='농장 보공  리스트', description=f'쁘띠 랑 - 보공 +8% (쁘띠 은월 보유시)\n\n쁘띠 반레온 - 보공 + 5%',color=0xdfe6e9))
    @commands.command()
    async def 기타(self,ctx):
        await ctx.send(embed=discord.Embed(title='농장 기타(재사용, 파이널어택, 내성 등)  리스트', description=f'피에르 - 파이널어택류 데미지 + 15%\n\n성장중인 미르 - 내성 + 5\n\n쁘띠 은월 -  재사용 대기시간 미적용 확률 + 4%\n\n큰 운영자의 벌룬 재사용 대기시간 미적용 확률 + 2%',color=0xdfe6e9))
    @commands.command()
    async def 크뎀(self,ctx):
        await ctx.send(embed=discord.Embed(title='농장 크뎀  리스트', description=f'쁘띠 힐라 - 크리티컬데미지 +2% ',color=0xdfe6e9))
    @commands.command()
    async def 사냥(self,ctx):
        await ctx.send(embed=discord.Embed(title='농장 사냥(경험치 획득) 리스트', description=f'쁘띠 메르세데스 - 경험치 획득량 + 3%\n\n쁘띠 오르카 - 경험치 획득량 +3%',color=0xdfe6e9))
    @commands.command()
    async def 데미지(self,ctx):
        await ctx.send(embed=discord.Embed(title="농장 데미지 리스트",description='검은 바이킹 -데미지 +2%, 민첩 + 6\n\n허수아비 - 데미지 +4%\n\n쁘띠 시그너스 - 데미지 +3%\n\n핑크빈 - 데미지 +2%', color=0xdfe6e9))
    @commands.command()
    async def 농장유지(self,ctx):
        await ctx.send(embed=discord.Embed(title='농장 보관함포함 유지해야할 목록', description=f'베릴(S) - 강력한 베릴유지용 + 올스텟\n\n파풀라투스의 시계(S) - 루미너스(어둠) 유지용\n\n프랑켄로이드(A+) - 주스텟 스페셜\n\n진지한바이킹(S) or 바이킹군단(S) -검은바이킹 유지용\n\n도둑까마귀(B+) - 허수아비 유지용\n\n푸소 (S) - 쁘띠 매그너스 유지용\n\n월묘도둑 (S) - 쁘띠 팬텀 유지용\n\n쌍둥이 월묘(A+) - 쁘띠 오르카 or 쁘띠랑',color=0xdfe6e9))      
    @commands.command()
    async def 농장킵(self,ctx):
        await ctx.send(embed=discord.Embed(title='농장 하다 킵 할 리스트', description=f'구미호(SS) - 개(힘/행훈) + 쁘띠 랑 유지용\n\n\크레스크레스(SS) - 힘\n\n이프리트(SS) - 라피스 유지용\n\n이상한 몬스터(SS) - 내면의 분노 + 빅터 -> 양철나무꾼 유지용\n\n마스터오멘(SS) - 검은마법사의 그림자 유지용\n\n내면의분노(SS) - 양철나무꾼 유지용\n\n빅터(SS) - 양철나무꾼 유지용\n\n루팡돼지(SS) - 미르세트 유지용\n\n마뇽(SS) - 미르세트 유지용',color=0xdfe6e9))
    @commands.command()
    async def 기간(self,ctx):
        await ctx.send(embed=discord.Embed(title='농장 효과 유지 까지 기간',description=f'2023년 8월 31일 마감 예정 따라서 2023년 8월 30일 농장시작하길 권장합니다.'))

    
#-------------main--------------#
@bot.event
async def on_ready():
    print(f'로그인 중 {bot.user} (ID: {bot.user.id})')
    print('Success')

async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.add_cog(MapleStory_Seedring_Simul(bot))
        await bot.add_cog(MapleStory_farm(bot))
        await bot.start(Token)

asyncio.run(main())