import discord
from discord.ext import commands
import os

class GameLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 호스팅 사이트에 등록한 기본 주소: https://connect-four-28818.web.app
        self.base_url = os.getenv("GAME_URL")

    def create_single_game_embed(self, game_name, folder_name, description):
        """싱글 플레이 게임용 임베드 생성 함수"""
        if not self.base_url:
            return discord.Embed(description="⚠️ 환경 변수 'GAME_URL'이 설정되지 않았습니다.", color=discord.Color.red())

        embed = discord.Embed(
            title=f"🎮 {game_name}",
            description=description,
            color=0xff0000  # 나락 퀴즈쇼에 어울리는 빨간색
        )

        # 실제 접속 주소 조립
        game_url = f"{self.base_url}/{folder_name}/index.html"
        
        embed.add_field(name="🔗 게임 링크", value=f"[지옥 입장하기]({game_url})", inline=False)
        embed.set_footer(text="클릭하면 웹 브라우저에서 게임이 실행됩니다.")
        
        return embed

    @commands.command(name="퀴즈1")
    async def play_quiz1(self, ctx):
        """quiz 폴더: 나락 퀴즈쇼"""
        description = "당신의 도덕성을 시험하는 12개의 질문에 답하세요."
        await ctx.send(embed=self.create_single_game_embed("나락 퀴즈쇼", "quiz", description))

    @commands.command(name="퀴즈2")
    async def play_quiz2(self, ctx):
        """quiz2 폴더: 두 번째 퀴즈"""
        description = "두 번째 준비된 퀴즈 게임에 참여하세요!"
        await ctx.send(embed=self.create_single_game_embed("두 번째 퀴즈", "quiz2", description))

async def setup(bot):
    await bot.add_cog(GameLink(bot))
