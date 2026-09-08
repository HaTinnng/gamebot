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
        """실시간 오목 게임 라운지 링크 생성"""
        if not self.base_url: 
            return await ctx.send("⚠️ GAME_URL 환경 변수 설정이 필요합니다.")

        # 현재 웹 코드에 맞게 6자리 랜덤 방 번호 생성
        room_id = random.randint(100000, 999999)

        embed = discord.Embed(
            title="⚫⚪ 실시간 오목 온라인",
            description=f"**방 코드: `{room_id}`**\n아래 버튼을 눌러 게임에 접속하세요!",
            color=0xdeb887 
        )

        # 현재 웹 구조에 맞는 URL 경로 설정 (필요시 폴더 구조에 맞게 수정)
        game_url = f"{self.base_url}/omok/index.html"

        embed.add_field(name="🎮 오목 게임 바로가기", value=f"[게임 접속하기]({game_url})", inline=False)
        embed.add_field(name="📌 안내", value=f"멀티 플레이 시 위 방 코드(`{room_id}`)를 입력해 입장하세요.", inline=False)
        
        embed.set_footer(text="버그 발생 시 브라우저 개발자 도구 콘솔을 확인하세요.")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Omok(bot))
