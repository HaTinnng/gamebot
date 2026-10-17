import discord
from discord.ext import commands
import os

class NightHunter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="밤의사냥꾼", aliases=["사냥꾼", "나이트헌터", "뱀서"])
    async def play_night_hunter(self, ctx):
        """실시간 괴물 사냥 생존 아케이드 게임 '밤의 사냥꾼' 로비 링크 생성"""
        if not self.base_url: 
            return await ctx.send("⚠️ GAME_URL 환경 변수 설정이 필요합니다.")

        embed = discord.Embed(
            title="🦇 밤의 사냥꾼 아케이드",
            description="몰려오는 괴물을 쓰러뜨리고 경험치를 모아 무기를 강화하며 새벽까지 살아남는 생존 아케이드 게임입니다!",
            color=0xfbbf24
        )

        # 웹 서버 경로에 맞게 수정 (예: /night_hunter/index.html)
        game_url = f"{self.base_url}/night_hunter/index.html"

        embed.add_field(name="🎮 게임 로비 접속", value=f"[웹사이트 접속하기]({game_url})", inline=False)
        embed.add_field(
            name="📌 이용 방법", 
            value=(
                "1. 링크를 눌러 웹사이트에 접속합니다.\n"
                "2. 난이도(쉬움 / 보통 / 어려움)를 선택하고 사냥을 시작합니다.\n"
                "3. WASD/방향키 또는 마우스·터치로 이동하며, 자동 공격과 레벨업 강화로 살아남으세요!"
            ), 
            inline=False
        )
        
        embed.set_footer(text="난이도별 최고 생존 기록은 브라우저(LocalStorage)에 자동으로 저장됩니다.")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NightHunter(bot))
