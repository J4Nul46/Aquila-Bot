import discord
from discord.ext import commands

# 봇 설정
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents)

# 공지 채널 저장용 딕셔너리 (서버마다 저장)
channel_settings = {}

@bot.event
async def on_ready():
    print(f"✅ 로그인 성공: {bot.user}")

# /일정채널 - 공지 채널 설정
@bot.command()
async def 일정채널(ctx):
    guild = ctx.guild
    channels = guild.text_channels  # 서버의 텍스트 채널 리스트 가져오기
    channel_list = "\n".join([f"{channel.name} (ID: {channel.id})" for channel in channels])

    embed = discord.Embed(title="📢 공지 채널 선택", description="공지 채널을 설정할 채널의 ID를 입력하세요.", color=0x00ff00)
    embed.add_field(name="채널 목록", value=channel_list, inline=False)

    await ctx.send(embed=embed)

    # 입력 받을 함수
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and int(msg.content) in [ch.id for ch in channels]

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        channel_settings[ctx.guild.id] = int(msg.content)
        await ctx.send(f"✅ 공지 채널이 <#{msg.content}>로 설정되었습니다!")
    except:
        await ctx.send("⏳ 시간이 초과되었습니다. 다시 시도해주세요.")

# /일정 - 비행 일정 입력
@bot.command()
async def 일정(ctx):
    if ctx.guild.id not in channel_settings:
        return await ctx.send("⚠️ 먼저 `/일정채널` 명령어로 공지 채널을 설정해주세요.")

    questions = ["✈️ 비행 시작 시간을 입력하세요 (예: 18:00)", "🛫 출발 공항을 입력하세요", "🛬 도착 공항을 입력하세요", "🛩 기종을 입력하세요"]
    answers = []

    # 입력 받기 함수
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    for question in questions:
        await ctx.send(question)
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            answers.append(msg.content)
        except:
            return await ctx.send("⏳ 시간이 초과되었습니다. 다시 시도해주세요.")

    flight_time, departure, arrival, aircraft = answers
    announcement_channel = bot.get_channel(channel_settings[ctx.guild.id])

    embed = discord.Embed(title="**비행 일정이 잡혔습니다!**", color=0x3498db)
    embed.add_field(name="> 비행 시작 시간", value=flight_time, inline=False)
    embed.add_field(name="> 노선", value=f"{departure} → {arrival}", inline=False)
    embed.add_field(name="> 기종", value=aircraft, inline=False)

    await announcement_channel.send(embed=embed)
    await ctx.send("✅ 일정이 공지 채널에 등록되었습니다!")

# / - 명령어 미리보기
@bot.command(name="")
async def show_commands(ctx):
    embed = discord.Embed(title="📌 사용 가능한 명령어", color=0x00ff00)
    embed.add_field(name="/일정채널", value="📢 공지를 보낼 채널을 설정합니다.", inline=False)
    embed.add_field(name="/일정", value="📝 비행 일정을 입력하여 공지합니다.", inline=False)
    
    await ctx.send(embed=embed)

# 실행
bot.run("MTM0MzIyNjIzNzAxNTAzMTgyMQ.Ge8qmn.8kaAXnw4sgRSrDqbIg54Pu09IsdVAxNqjn-sss")