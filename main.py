import os
import discord
from discord.ext import commands
import asyncio

# 봇 권한 설정
intents = discord.Intents.default()
intents.message_content = True

# 봇 생성
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    """Cogs 폴더의 모든 파일을 로드합니다."""
    # Cogs 폴더가 없으면 에러가 날 수 있으니 체크
    if not os.path.exists("Cogs"):
        print("❌ Cogs 폴더를 찾을 수 없습니다.")
        return

    for filename in os.listdir("Cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"Cogs.{filename[:-3]}")
                print(f"✅ 로드 성공: {filename}")
            except Exception as e:
                print(f"❌ 로드 실패 ({filename}): {e}")

@bot.event
async def on_ready():
    print(f'🤖 봇이 준비되었습니다: {bot.user.name}')
    print(f'🆔 봇 ID: {bot.user.id}')
    await bot.change_presence(activity=discord.Game("게임 대기"))

async def main():
    async with bot:
        await load_extensions()
        
        # 환경변수에서 토큰 가져오기
        token = os.getenv("DISCORD_TOKEN")
        
        if not token:
            print("❌ 에러: 환경변수에 'DISCORD_TOKEN'이 없습니다.")
            return
            
        await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # 강제 종료 시 깔끔하게 닫기
        print("봇을 종료합니다.")
