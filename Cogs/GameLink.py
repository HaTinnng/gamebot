import discord
from discord.ext import commands
import os
import random

class GameLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 환경변수: https://connect-four-28818.web.app
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="퀴즈1")
    async def play_quiz1(self, ctx):
        """싱글 플레이: 나락 퀴즈쇼"""
        if not self.base_url: return await ctx.send("⚠️ GAME_URL 설정 필요")
        
        embed = discord.Embed(title="🎮 나락 퀴즈쇼", description="도덕성 테스트를 시작합니다.", color=0xff0000)
        url = f"{self.base_url}/quiz/index.html"
        embed.add_field(name="🔗 링크", value=f"[지옥 입장하기]({url})")
        await ctx.send(embed=embed)

    @commands.command(name="커넥트포")
    async def play_connect4(self, ctx):
        """멀티 플레이: 커넥트 포 (방 번호 포함)"""
        if not self.base_url: return await ctx.send("⚠️ GAME_URL 설정 필요")

        # 여러 팀이 겹치지 않게 랜덤 방 번호 생성
        room_id = random.randint(1000, 9999)
        embed = discord.Embed(
            title="🔵 커넥트 포 멀티플레이", 
            description=f"방 번호: **{room_id}**\n상대방과 다른 색깔 링크를 눌러주세요!",
            color=0x0055ff
        )

        # connect4 폴더 경로 사용
        red_url = f"{self.base_url}/connect4/index.html?room={room_id}&color=red"
        yellow_url = f"{self.base_url}/connect4/index.html?room={room_id}&color=yellow"

        embed.add_field(name="🔴 1번 플레이어", value=f"[Red 접속]({red_url})", inline=True)
        embed.add_field(name="🟡 2번 플레이어", value=f"[Yellow 접속]({yellow_url})", inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GameLink(bot))
