import discord
from discord.ext import commands
import os

class PokerGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # main.py 또는 .env 파일에서 설정한 웹 호스팅 기본 주소 (예: https://my-game.web.app)
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="포커", aliases=["poker", "비디오포커", "1인포커!"])
    async def play_poker(self, ctx):
        """비디오 포커 게임 링크를 생성합니다."""
        
        # 환경변수 체크
        if not self.base_url:
            return await ctx.send("⚠️ 오류: `GAME_URL` 환경변수가 설정되지 않았습니다. 봇 관리자에게 문의하세요.")

        # 게임 접속 URL 설정 (Firebase Hosting의 poker 폴더 경로 기준)
        game_url = f"{self.base_url}/poker/index.html"

        # 임베드 생성
        embed = discord.Embed(
            title="🃏 비디오 포커 (Jacks or Better)",
            description=(
                "**매 판 베팅을 조절하며 즐기는 정통 비디오 포커 게임**\n\n"
                "💰 **베팅 시스템:** 매판 카드 받기 직전 원하시는 만큼 베팅 금액을 자유롭게 조절!\n"
                "🔄 **드로우 규칙:** 원하는 카드를 선택(DISCARD)하여 교체 후 최종 족보 결정\n"
                "📊 **배당표 안내:**\n"
                "• **로얄 플러시:** 250배\n"
                "• **스트레이트 플러시:** 50배\n"
                "• **포 카드:** 25배\n"
                "• **풀 하우스:** 9배 | **플러시:** 6배\n"
                "• **스트레이트:** 4배 | **트리플:** 3배\n"
                "• **투 페어:** 2배 | **잭스 오어 베터:** 1배"
            ),
            color=0xf1c40f # 게임 테마색 (Gold)
        )
        
        # 링크 버튼 추가
        embed.add_field(
            name="🚀 게임 접속", 
            value=f"**[👉 여기를 눌러 게임 시작하기]({game_url})**", 
            inline=False
        )
        
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PokerGame(bot))
