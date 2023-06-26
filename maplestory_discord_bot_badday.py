import discord
import yt_dlp as youtube_dl
import numpy as np
from discord.ext import commands
from discord_bot_tokken_parameter import Token
import asyncio
import urllib.request

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
    async def 시드하(self, ctx):
        result = self.green_jade_ha()
        await ctx.send(embed=discord.Embed(title='녹옥의 보스 반지 상자 (하급) 사용결과', description=f'{result}가 나왔습니다.',color=0x55efc4))
        # await ctx.send(f'녹옥의 보스 반지 상자 (하급) 사용결과 : {result} 가 나왔습니다. ')
    @commands.command()
    async def 테스트(self, ctx):
        await ctx.send(embed=discord.Embed(title="디스코드 봇", description="명령어 테스트",colour=0x00FFFF))
    
    @commands.command()
    async def 시드중(self, ctx):
        result = self.red_jade_ha()
        await ctx.send(embed=discord.Embed(title='홍옥의 보스 반지 상자 (중급) 사용결과', description=f'{result}가 나왔습니다.',color=0xd63031))
    @commands.command()
    async def 시드상(self, ctx):
        result = self.black_jade_ha()
        await ctx.send(embed=discord.Embed(title='흑옥의 보스 반지 상자 (상급) 사용결과', description=f'{result}가 나왔습니다.',color=0x636e72))
    @commands.command()
    async def 시드최상(self, ctx):
        result = self.white_jade_ha()
        await ctx.send(embed=discord.Embed(title='백옥의 보스 반지 상자 (최상급)', description=f'{result}가 나왔습니다.',color=0xdfe6e9))
        
    @commands.command()
    async def 시드상자드랍(self, ctx):
        await ctx.send(f'녹옥의 보스 반지 상자 (하급) \n 스우 (노멀) §   데미안 (노멀) §   가디언 엔젤 슬라임 (노멀)\n루시드 (이지, 노멀) §   윌 (이지, 노멀) §   더스크 (노멀)\n 듄켈 (노멀)\n\n홍옥의 보스 반지 상자 (중급)\n§   스우 (하드) §   데미안 (하드) §   루시드 (하드)§   윌 (하드) §   진 힐라 (노멀) \n\n흑옥의 보스 반지 상자 (상급)\n§   더스크 (카오스) §   듄켈 (하드) §   가디언 엔젤 슬라임 (카오스)\n§   진 힐라 (하드) §   선택받은 세렌 (노멀) -       백옥의 보스 반지 상자 (최상급)\n\n§   검은 마법사 (하드, 익스트림) §   선택받은 세렌 (하드, 익스트림)\n§   감시자 칼로스 (카오스) §   카링 (노멀)')
    #----------------------시드--------------------------#
    @commands.command()
    async def 키워드(self, ctx):
            embed = discord.Embed(title='음악봇 관련', description='!help')
            await ctx.send(embed=embed)
            embed = discord.Embed(title='메이플봇 - 시드시뮬레이션', \
            description='!시드하 : 녹옥의 보스 반지 상자 (하급)\n1개를 개봉합니다\n\n!시드중: 홍옥의 보스 반지 상자 (중급)\n1개를 개봉합니다.\n\n!시드상: 흑옥의 보스 반지 상자 (상급)\n 1개를 개봉합니다.\n\n!시드최상: 백옥의 보스 반지 상자 (최상급)\n 1개를 개봉합니다.\n\n!시드상자드랍: 난이도별 보스 반지 상자 드랍구간을 알려줍니다.')
            await ctx.send(embed=embed)
            embed = discord.Embed(title='메이플봇 - 농장관련',\
            description='\n농장 도우미 추가예정, 로얄스타일, 골드애플, 큐브 시뮬추가예정,\n주간보스 드랍템 입력 및 정산기능 추가예정')
            await ctx.send(embed=embed)
    # await ctx.send(embed=embed)
    #     await ctx.send(embed=discord.Embed(title='음악봇 관련' description='!help'))
    #     await ctx.send(embed=discord.Embed(title='메이플봇 관련' description='!시드하 : 녹옥의 보스 반지 상자 (하급)1개를 개봉합니다\n!시드중: 홍옥의 보스 반지 상자 (중급)1개를 개봉합니다. \n !시드상:흑옥의 보스 반지 상자 (상급) 1개를 개봉합니다.\n !시드최상:백옥의 보스 반지 상자 (최상급) 1개를 개봉합니다.\n!시드상자드랍: 난이도별 보스 반지 상자 드랍구간을 알려줍니다.\n농장 도우미 추가예정, 로얄스타일, 골드애플, 큐브 시뮬추가예정,\n주간보스 드랍템 입력 및 정산기능 추가예정'))
        # await ctx.send(f'음악봇 관련 : !help \n\n메이플봇 관련 : !시드하 : 녹옥의 보스 반지 상자 (하급)1개를 개봉합니다\n!시드중: 홍옥의 보스 반지 상자 (중급)1개를 개봉합니다. \n !시드상:흑옥의 보스 반지 상자 (상급) 1개를 개봉합니다.\n !시드최상:백옥의 보스 반지 상자 (최상급) 1개를 개봉합니다.\n!시드상자드랍: 난이도별 보스 반지 상자 드랍구간을 알려줍니다.\n농장 도우미 추가예정, 로얄스타일, 골드애플, 큐브 시뮬추가예정,\n주간보스 드랍템 입력 및 정산기능 추가예정')
#-------------main--------------#
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.add_cog(MapleStory_Seedring_Simul(bot))
        await bot.start(Token)

asyncio.run(main())