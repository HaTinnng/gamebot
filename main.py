import os
import discord
from discord.ext import commands
import asyncio
import motor.motor_asyncio

intents = discord.Intents.default()
intents.message_content = True

# 기존 봇 설정 유지
bot = commands.Bot(command_prefix="/", intents=intents)

# 사이트(호스팅) 환경 변수에서 직접 불러오기
MONGODB_URI = os.getenv("MONGODB_URI")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = mongo_client["discordbot"]

async def load_extensions():
    """Cogs 폴더 내의 모든 확장을 로드합니다."""
    # 기존 코드의 비활성화 목록 체크 로직 포함 가능
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"Cogs.{cog_name}")
                print(f"✅ {cog_name}.py 로드 성공")
            except Exception as e:
                print(f"❌ {cog_name}.py 로드 실패: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game("게임 링크 제공"))

async def main():
    # 봇 실행 전 확장 로드
    async with bot:
        await load_extensions()
        # 사이트 설정창에 등록된 DISCORD_TOKEN을 불러옵니다.
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
