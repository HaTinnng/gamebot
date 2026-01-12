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

    # --- 추가된 오목 코드 ---
    @commands.command(name="오목")
    async def play_omok(self, ctx):
        """멀티 플레이: 실시간 오목"""
        if not self.base_url: return await ctx.send("⚠️ GAME_URL 설정 필요")

        # 1. 방 번호 생성
        room_id = random.randint(1000, 9999)

        # 2. 임베드 생성 (나무색 느낌의 색상 코드 사용)
        embed = discord.Embed(
            title="⚫⚪ 실시간 오목 대전",
            description=f"방 번호: **{room_id}**\n흑돌이 선공입니다. 친구와 링크를 나눠 가지세요!",
            color=0xdeb887 
        )

        # 3. URL 생성 (omok 폴더 경로 가정)
        # HTML 파일이 호스팅된 경로가 /omok/index.html 이라고 가정합니다.
        black_url = f"{self.base_url}/omok/index.html?room={room_id}&color=black"
        white_url = f"{self.base_url}/omok/index.html?room={room_id}&color=white"

        # 4. 버튼(링크) 추가
        embed.add_field(name="⚫ 1번 플레이어 (선공)", value=f"[흑돌로 접속]({black_url})", inline=True)
        embed.add_field(name="⚪ 2번 플레이어 (후공)", value=f"[백돌로 접속]({white_url})", inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GameLink(bot))
