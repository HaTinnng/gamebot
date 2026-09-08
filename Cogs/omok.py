import discord
from discord.ext import commands
import os

class Omok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="오목")
    async def play_omok(self, ctx):
        """실시간 오목 온라인 게임 로비 링크 생성"""
        if not self.base_url: 
            return await ctx.send("⚠️ GAME_URL 환경 변수 설정이 필요합니다.")

        embed = discord.Embed(
            title="⚫⚪ 실시간 오목 온라인",
            description="정교한 Minimax AI 대전 및 6자리 방 코드를 통한 실시간 멀티플레이를 지원합니다!",
            color=0xdeb887 
        )

        game_url = f"{self.base_url}/omok/index.html"

        embed.add_field(name="🎮 오목 게임 로비", value=f"[웹사이트 접속하기]({game_url})", inline=False)
        embed.add_field(name="📌 이용 방법", value="1. 링크를 눌러 웹사이트에 접속합니다.\n2. **싱글 플레이** 또는 **멀티 플레이**를 선택합니다.\n3. 멀티 시 방 코드를 직접 만들거나 입력해 친구와 대전하세요!", inline=False)
        
        embed.set_footer(text="버그 발생 시 브라우저 개발자 도구 콘솔을 확인하세요.")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Omok(bot))
