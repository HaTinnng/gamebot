import discord
from discord.ext import commands
import os

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # main.py에서 설정한 환경변수(Firebase 주소)를 가져옵니다.
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="틱택토", aliases=["tictactoe", "틱"])
    async def play_tictactoe(self, ctx):
        """네온 무한 틱택토 게임 링크를 생성합니다."""
        
        # 환경변수 체크
        if not self.base_url:
            return await ctx.send("⚠️ 오류: `GAME_URL` 환경변수가 설정되지 않았습니다.")

        # Firebase Hosting 경로 설정
        # (주의: public/tictactoe 폴더 안에 index.html이 있어야 함)
        game_url = f"{self.base_url}/tictactoe/index.html"

        # 임베드 생성
        embed = discord.Embed(
            title="🎮 Neon Infinite Tic-Tac-Toe",
            description=(
                "**3x3 무한 틱택토 (네온 에디션)**\n\n"
                "⚡ **규칙:** 돌은 3개까지만 유지됩니다.\n"
                "4번째 돌을 두면 가장 오래된 돌이 사라집니다!\n\n"
                "🤖 **싱글플레이:** 5단계 난이도 AI\n"
                "⚔️ **멀티플레이:** 방 만들기 & 실시간 대결"
            ),
            color=0x00f3ff # 네온 블루 색상
        )
        
        # 링크 버튼처럼 보이게 링크 추가
        embed.add_field(
            name="🚀 게임 접속", 
            value=f"**[👉 여기를 눌러 게임 시작하기]({game_url})**", 
            inline=False
        )
        
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TicTacToe(bot))
