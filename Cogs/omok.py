import discord
from discord.ext import commands
import os
import random

class Omok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="오목")
    async def play_omok(self, ctx):
        """싱글(AI) 설정 및 멀티 플레이 링크 생성"""
        if not self.base_url: 
            return await ctx.send("⚠️ GAME_URL 설정 필요")

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
    await bot.add_cog(Omok(bot))
