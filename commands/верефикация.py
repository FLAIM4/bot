import random
import disnake
from disnake.ext import commands
from disnake import ui
from captcha.image import ImageCaptcha
from disnake import TextInputStyle

class Button1(disnake.ui.View):
    def __init__(self, rnd):
        super().__init__()
        self.rnd = rnd

    @ui.button(label='Пройти', custom_id='id_2', style=disnake.ButtonStyle.secondary)
    async def button1(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(VerifyModal(self.rnd))
        await interaction.delete_original_message()

class Button(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.rnd = random.randint(1000, 9999)
        super().__init__(timeout=None)

    @ui.button(label='Получить полный доступ', custom_id='id_1', style=disnake.ButtonStyle.secondary)
    async def button1(self, button: ui.Button, interaction: disnake.Interaction):
        image = ImageCaptcha(fonts=['font.ttf'])
        data = image.generate(f'{self.rnd}')
        image.write(f'{self.rnd}', 'out.png')
        embed = disnake.Embed(
            title="Capcha",
            description=">>> Просим вас записать числовые значения,\nпредставленные на изображении.",
            color=0x2F3136
        )
        embed.set_author(
            name="FUNMINE STUDIO",
            icon_url="https://cdn.discordapp.com/attachments/1071030207726755882/1139948382933221396/sefsfef.png",
        )
        file = disnake.File("out.png", filename="out.png")
        embed.set_image(url="attachment://out.png")
        embed.set_thumbnail(url=interaction.user.avatar.url)
        view = Button1(self.rnd) 
        await interaction.response.send_message(embed=embed, file=file, view=view, ephemeral=True)

class VerifyModal(disnake.ui.Modal):
    def __init__(self,rnd):
        self.rnd = rnd
        components = [
            disnake.ui.TextInput(label="Введите код", placeholder=rnd, custom_id="code")
        ]
        super().__init__(title="Верификация", components=components, custom_id="verify_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        if self.rnd == int(interaction.text_values["code"]):
            role = interaction.guild.get_role(1140196270280032308)
            await interaction.author.add_roles(role)
            embed = disnake.Embed(
                title="Успешно",
                description="Вы успешно прошли верификацию!",
                color=0x2F3136,
            )
            embed.set_author(
            name="FUNMINE STUDIO",
            icon_url="https://cdn.discordapp.com/attachments/1071030207726755882/1139948382933221396/sefsfef.png",
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = disnake.Embed(
                title="Отмена",
                description="Неверный код!",
                color=0x2F3136,
            )
            embed.set_author(
            name="FUNMINE STUDIO",
            icon_url="https://cdn.discordapp.com/attachments/1071030207726755882/1139948382933221396/sefsfef.png",
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

class Верификация(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.command()
    async def test(self, ctx: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="Верификация",
            description=">>> Для того чтобы осуществить доступ ко всем чатам, просьба нажать на предоставленную ниже кнопку. Это мероприятие нацелено на предотвращение потока ботов и их нежелательной активности.",
            color=0x2F3136
        )

        embed.set_author(
            name="FUNMINE STUDIO",
            icon_url="https://cdn.discordapp.com/attachments/1071030207726755882/1139948382933221396/sefsfef.png",
        )

        embed.set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1138791961193623673/awawdawd-1.png")

        view = Button()
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return
        
        self.bot.add_view(Button(), message_id=1140208798506700800)

def setup(bot):
    bot.add_cog(Верификация(bot))
