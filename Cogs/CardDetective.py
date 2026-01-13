import discord
from discord.ext import commands
import os

class CardDetective(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # main.py 또는 .env 파일에서 설정한 웹 호스팅 기본 주소 (예: https://my-game.web.app)
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="카드추리", aliases=["card", "카드게임", "카드"])
    async def play_cardgame(self, ctx):
        """심리전 카드 게임 링크를 생성합니다."""
        
        # 환경변수 체크
        if not self.base_url:
            return await ctx.send("⚠️ 오류: `GAME_URL` 환경변수가 설정되지 않았습니다. 봇 관리자에게 문의하세요.")

        # 게임 접속 URL 설정
        # Firebase Hosting의 public 폴더 구조에 맞춰 경로를 수정하세요. 
        # 예: public/cardgame/index.html 에 파일을 넣었다면 아래와 같습니다.
        game_url = f"{self.base_url}/cardgame/index.html"

        # 임베드 생성
        embed = discord.Embed(
            title="🃏 THE CARD GAME (심리전 카드 추리)",
            description=(
                "**숫자와 심리를 이용한 고도의 전략 카드 게임**\n\n"
                "🃏 **덱 구성:** 1~20 숫자 카드 + 특수(⭐) 카드 총 22장\n"
                "👀 **진행 방식:**\n"
                "1. 자신만의 덱에서 카드 2장을 선택합니다.\n"
                "2. 상대에게 보여줄 카드 1장을 공개합니다.\n"
                "3. 공개된 정보를 바탕으로 **Call** 또는 **Die**를 결정합니다.\n\n"
                "🔥 **특수 승리 규칙:**\n"
                "• **기본:** 숫자가 높은 쪽이 승리\n"
                "• **역상성:** `20`은 `1`에게 무조건 패배합니다!\n"
                "• **스타:** 같은 숫자 대결 시 `⭐` 카드가 승리합니다.\n\n"
                "🤖 **싱글플레이:** 7단계 난이도 AI와 대결\n"
                "👥 **멀티플레이:** 실시간 방 생성 및 친구와 대결"
            ),
            color=0xf1c40f # 게임 테마색 (Gold)
        )
        
        # 썸네일 설정 (카드 게임 아이콘 등 이미지 URL이 있다면 추가)
        # embed.set_thumbnail(url="https://example.com/card_icon.png")

        # 링크 버튼 추가
        embed.add_field(
            name="🚀 게임 접속", 
            value=f"**[👉 여기를 눌러 게임 시작하기]({game_url})**", 
            inline=False
        )
        
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CardDetective(bot))
