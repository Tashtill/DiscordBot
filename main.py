import os
from dotenv import load_dotenv
import discord
import random
import emoji
import datetime



#自分のBotのアクセストークンを取得
load_dotenv()
token = os.getenv("DiscordBot_token")
#接続に必要なクライアントを作成
client = discord.Client(intents=discord.Intents.all())
#スラッシュコマンドの情報をもつコンテナを作成
tree = discord.app_commands.CommandTree(client)

#各サーバーやチャンネルのID
guild_id_personnal = int(os.getenv("guild_id_personnal")) #個人サーバー
channel_id_bot_notice = int(os.getenv("channel_id_bot_notice"))  #個人サーバー,Bot通知チャンネル
channel_id_vc_general = int(os.getenv("channel_id_vc_general")) #個人サーバー,一般vc
guild_id_lab_room = int(os.getenv("guild_id_lab_room")) #らぼべやサーバー
guild_id_pair = int(os.getenv("guild_id_pair")) #2人用サーバー

#受信メッセージをターミナルにprintする機能のオンオフ
print_message = False


#イベント内で使用する関数
#サーバー内のVCから全メンバーを退出させる
async def close_vc(guild):
  voice_channels = guild.voice_channels
  for vc in voice_channels:
    print(vc)
    for member in vc.members:
      await member.move_to(None) #move_to(None)で切断
      print(f"{member}を退出させました")



#起動時に動作する処理
@client.event
async def on_ready():
  print(f"We have logged in as {client.user}")
  dt_now_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
  channel_bot_notice = client.get_channel(channel_id_bot_notice)
  await channel_bot_notice.send(f"オンラインになりました\n現在時刻は{dt_now_jst}です")

  await tree.sync() #スラッシュコマンドの同期



#メッセージ受信時に動作する処理群
@client.event
async def on_message(message):

  #メッセージ受信者がbotの場合無視する
  if message.author.bot:
    return

  #受信メッセージをターミナルで確認
  if print_message:
    print("受信メッセージ:" + message.content)

  #「にゃーん」と発言したら「にゃーん」を返す
  if message.content == "にゃーん":
    await message.channel.send("にゃーん")

  #💩の絵文字が入力されたら、トイレットペーパーを投げる
  demojized_message = emoji.demojize(
    message.content)
  if ":pile_of_poo:" in demojized_message:
    if message.guild.id == guild_id_lab_room:  #らぼべやでのみ動作
     await message.channel.send("(っ'-')╮=͟͟͞͞  :roll_of_paper:")

  #「うんち」の文字列があったら💩のリアクションをつける
  emoji_poop = "💩"
  if "うんち" in message.content:
    await message.add_reaction(emoji_poop)
    
  #「おはよ」の文字列があると挨拶する
  if "おはよ" in message.content:
    flg_greet = True
    if "おはようんち" in message.content:
      if random.choice([1,2,3]) == 1:
        await message.channel.send("あんまり外でそういうこと言っちゃだめだよ")
        flg_greet = False 
    if flg_greet:
      await message.channel.send("おはようございます。良い一日を。")

  #「/おやすみ」と発言したらペアサーバーの全員を退出させる
  #ペアサーバーでのみ機能する
  if message.content == "/おやすみ":
    if message.guild.id == guild_id_pair: 
      await close_vc(message.guild)
    
  #オウム返し
  """
  if message.guild.id == guild_id_personnal: #個人サーバーでのみ動作
    await message.channel.send(message.content)
    print(message.content)
  """



#スラッシュコマンド
#テスト
@tree.command(name="test", description="スラッシュコマンドのテスト")
async def test(interaction:discord.Interaction):
  await interaction.response.send_message("これはスラッシュコマンドのテストです")

#ボイスチャットの解散
@tree.command(name="close_vc", description="VCから全員を退出させます")
async def close_voice_chat(interaction:discord.Interaction):
  await close_vc(interaction.guild)
  await interaction.response.send_message("ボイスチャットを解散しました")

#6面ダイスを振る
@tree.command(name="roll", description="サイコロを振ります")
async def roll(interaction:discord.Interaction):
  number = random.randint(1,6)
  await interaction.response.send_message(f"{number}の目が出ました")



#Botの起動とDiscordサーバーへの接続
client.run(token)