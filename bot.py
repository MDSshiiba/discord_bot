import discord
import os
import openai
from discord import app_commands

TOKEN = "" #discordトークン
os.environ["OPEN_API_KEY"] = "" #openaiトークン

openai.api_key = os.environ["OPEN_API_KEY"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()

@client.event
async def on_message(message):
    def check(msg):
        return msg.author == message.author
    if message.author == client.user:
        return
    if message.content.startswith('/hello'):
        await message.channel.send('Hello!')
    if message.content == '/exit':
        exit()

@tree.command(
    name="gpt",
    description="テストコマンドです。観光地の情報について解答します"
)
@app_commands.describe(
    text="観光地を書いてね" # 引数名=説明
)
async def test_command(interaction: discord.Interaction,text:str):
    await interaction.response.defer()
    if text == "/fin":
        await interaction.followup.send("bye")
        exit()
    else:
        #以下chatGPTに関する記述
        #入力内容の設定
        messages = [
          {"role": "system", "content":"""あなたはトラベルライターです．
トラベルライターとして[観光地]について，300字程度のレビューを書いてください．

レビューは
～タイトル～
から始めてください


"""},
          {"role": "user", "content": "[観光地]="+text}
        ]
        #出力内容の設定
        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=messages,
          max_tokens = 8000  #トークン量/一回のやり取り の制限
        )
        await interaction.followup.send(response["choices"][0]["message"]["content"])    #AIからの返答
        await interaction.followup.send("token="+str(response["usage"]["total_tokens"]))  #使用トークン量の出力

@tree.command(
    name="decider",
    description="テストコマンドです。GPT-4でこたえます"
)
@app_commands.describe(
    text="聞きたいことを書いてね" # 引数名=説明
)
async def test_command2(interaction: discord.Interaction,text:str):
    await interaction.response.defer()
    if text == "/fin":
        await interaction.followup.send("bye")
        exit()
    else:
        #以下chatGPTに関する記述
        #入力内容の設定
        messages = [
          {"role": "user", "content": text}
        ]
        #出力内容の設定
        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=messages,
          max_tokens = 8000  #トークン量/一回のやり取り の制限
        )
        await interaction.followup.send(response["choices"][0]["message"]["content"])    #AIからの返答
        await interaction.followup.send("token="+str(response["usage"]["total_tokens"]))  #使用トークン量の出力

@tree.command(
    name="keywords",
    description="テストコマンドです。文章からキーワードを取り出します"
)
@app_commands.describe(
    text="文章を書いてね" # 引数名=説明
)
async def test_command2(interaction: discord.Interaction,text:str):
    await interaction.response.defer()
    if text == "/fin":
        await interaction.followup.send("bye")
        exit()
    else:
        #以下chatGPTに関する記述
        #入力内容の設定
        messages = [
          {"role": "system", "content":"Extract keywords from this text:"},
          {"role": "user", "content": text}
        ]
        #出力内容の設定
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages,
          max_tokens = 2000  #トークン量/一回のやり取り の制限
        )
        await interaction.followup.send(response["choices"][0]["message"]["content"])    #AIからの返答
        await interaction.followup.send("token="+str(response["usage"]["total_tokens"]))  #使用トークン量の出力
client.run(TOKEN)
