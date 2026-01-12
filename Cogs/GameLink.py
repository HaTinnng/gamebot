import discord
from discord.ext import commands
import os
import random

class GameLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 환경변수 예시: https://your-project.web.app
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
        """멀티 플레이: 커넥트 포"""
        if not self.base_url: return await ctx.send("⚠️ GAME_URL 설정 필요")

        room_id = random.randint(1000, 9999)
        embed = discord.Embed(
            title="🔵 커넥트 포 멀티플레이", 
            description=f"방 번호: **{room_id}**\n상대방과 다른 색깔 링크를 눌러주세요!",
            color=0x0055ff
        )

        red_url = f"{self.base_url}/connect4/index.html?room={room_id}&color=red"
        yellow_url = f"{self.base_url}/connect4/index.html?room={room_id}&color=yellow"

        embed.add_field(name="🔴 1번 플레이어", value=f"[Red 접속]({red_url})", inline=True)
        embed.add_field(name="🟡 2번 플레이어", value=f"[Yellow 접속]({yellow_url})", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="오목")
    async def play_omok(self, ctx):
        """싱글(AI) 설정 및 멀티 플레이 링크 생성"""
        if not self.base_url: return await ctx.send("⚠️ GAME_URL 설정 필요")

        room_id = random.randint(1000, 9999)

        embed = discord.Embed(
            title="⚫⚪ 오목 게임 라운지",
            description=f"**방 번호: {room_id}**\n원하는 모드를 선택하세요!",
            color=0xdeb887 
        )

        # 1. 싱글 플레이 링크 (모드 파라미터 추가)
        single_url = f"{self.base_url}/omok/index.html?mode=single"
        
        # 2. 멀티 플레이 링크 (흑/백 고정)
        black_url = f"{self.base_url}/omok/index.html?mode=multi&room={room_id}&color=black"
        white_url = f"{self.base_url}/omok/index.html?mode=multi&room={room_id}&color=white"

        embed.add_field(name="🤖 혼자 하기", value=f"[싱글 플레이 설정]({single_url})", inline=False)
        embed.add_field(name="⚔️ 멀티 플레이 (P1)", value=f"[⚫ 흑돌로 시작]({black_url})", inline=True)
        embed.add_field(name="⚔️ 멀티 플레이 (P2)", value=f"[⚪ 백돌로 시작]({white_url})", inline=True)
        
        embed.set_footer(text="버그 발생 시 화면 하단의 로그를 확인하세요.")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GameLink(bot))
