import discord
from discord.ext import commands
import os

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="퀴즈1")
    async def play_quiz1(self, ctx):
        """싱글 플레이: 나락 퀴즈쇼"""
        if not self.base_url: 
            return await ctx.send("⚠️ GAME_URL 설정 필요")
        
        embed = discord.Embed(title="🎮 나락 퀴즈쇼", description="도덕성 테스트를 시작합니다.", color=0xff0000)
        url = f"{self.base_url}/quiz/index.html"
        embed.add_field(name="🔗 링크", value=f"[지옥 입장하기]({url})")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Quiz(bot))
