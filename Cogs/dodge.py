import discord
from discord.ext import commands
import os

class DodgeAndSurvive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="닷지", aliases=["닷지앤서바이브", "탄막피하기"])
    async def play_dodge(self, ctx):
        """실시간 탄막 회피 아케이드 게임 '닷지 앤 서바이브' 로비 링크 생성"""
        if not self.base_url: 
            return await ctx.send("⚠️ GAME_URL 환경 변수 설정이 필요합니다.")

        embed = discord.Embed(
            title="⚡ 닷지 앤 서바이브 아케이드",
            description="기본 화면(360x360)과 큰 화면(720x720) 모드를 지원하는 실시간 탄막 회피 생존 게임입니다!",
            color=0x22d3ee
        )

        # 웹 서버 경로에 맞게 수정 (예: /dodge/index.html 또는 /index.html)
        game_url = f"{self.base_url}/dodge/index.html"

        embed.add_field(name="🎮 게임 로비 접속", value=f"[웹사이트 접속하기]({game_url})", inline=False)
        embed.add_field(
            name="📌 이용 방법", 
            value=(
                "1. 링크를 눌러 웹사이트에 접속합니다.\n"
                "2. 로비에서 **기본 화면** 또는 **큰 화면** 모드를 선택합니다.\n"
                "3. 마우스, 터치, 또는 WASD/방향키로 파란 원을 조작해 탄막을 피하세요!"
            ), 
            inline=False
        )
        
        embed.set_footer(text="최고 기록은 브라우저(LocalStorage)에 자동으로 저장됩니다.")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DodgeAndSurvive(bot))
