import discord
from discord.ext import commands
import os

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="타입퀴즈", aliases=["포켓몬타입", "타입"])
    async def play_quiz(self, ctx):
        """인물보고 타입맞추기 퀴즈 프레젠테이션 링크 생성"""
        if not self.base_url: 
            return await ctx.send("⚠️ GAME_URL 환경 변수 설정이 필요합니다.")

        embed = discord.Embed(
            title="🚀 포켓몬 타입 퀴즈 프레젠테이션",
            description="전신 사진을 보고 타입을 맞추는 인터랙티브 퀴즈입니다!",
            color=0x4f46e5 # 웹사이트 테마 색상과 맞춤
        )

        # 퀴즈 HTML 파일이 배포된 경로에 맞춰 수정하세요 (예: /quiz/index.html 또는 루트 경로)
        game_url = f"{self.base_url}/quiz3/index.html"

        embed.add_field(name="🎮 퀴즈 플레이", value=f"[웹사이트 접속하기]({game_url})", inline=False)
        embed.add_field(name="📌 이용 방법", value="1. 링크를 눌러 퀴즈 웹사이트에 접속합니다.\n2. **퀴즈 시작하기** 버튼을 눌러 슬라이드를 진행하세요!\n3. 누가 가장 맞추는지 겨루어보세요!.", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Quiz(bot))
