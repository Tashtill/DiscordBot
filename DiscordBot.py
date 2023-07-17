import os
from dotenv import load_dotenv
import discord
import random
import emoji
import datetime

#gitlens revert test


#自分のBotのアクセストークンを取得
load_dotenv()
token = os.getenv("DiscordBot_token")
#接続に必要なクライアントを作成
client = discord.Client(intents=discord.Intents.all())

#各サーバーやチャンネルのID
guild_id_personnal = int(os.getenv("guild_id_personnal")) #個人サーバー
channel_id_bot_notice = int(os.getenv("channel_id_bot_notice"))  #個人サーバー,Bot通知チャンネル
channel_id_vc_general = int(os.getenv("channel_id_vc_general")) #個人サーバー,一般vc
guild_id_lab_room = int(os.getenv("guild_id_lab_room")) #らぼべやサーバー
guild_id_pair = int(os.getenv("guild_id_pair")) #2人用サーバー


#受信メッセージをターミナルにprintする機能のオンオフ
print_message = False


#起動時に動作する処理
@client.event
async def on_ready():
  print(f"We have logged in as {client.user}")
  dt_now_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
  channel_bot_notice = client.get_channel(channel_id_bot_notice)
  await channel_bot_notice.send(f"オンラインになりました\n現在時刻は{dt_now_jst}です")



#メッセージ受信時に動作する処理群
@client.event
async def on_message(message):

  #各種フラグの初期化
  flg_ohayo = True

  #メッセージ受信者がbotの場合無視する
  if message.author.bot:
    return

  #受信メッセージをターミナルで確認
  if print_message:
    print("受信メッセージ:" + message.content)

  #「/neko」と発言したら「にゃーん」を返す
  if message.content == "/neko":
    await message.channel.send("にゃーん")

  #「/roll」と発言したらサイコロを振る
  if message.content == "/roll":
    number = random.randint(1, 6)
    await message.channel.send(number)

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
    
    if "おはようんち" in message.content:
      if random.choice([1,2,3]) == 1:
        flg_ohayo = False
        await message.channel.send("あんまり外でそういうこと言っちゃだめだよ")

  #「おはよ」の文字列があると挨拶する
  if "おはよ" in message.content:
    if flg_ohayo:
      await message.channel.send("おはようございます。良い一日を。")

  #「/close_vc」と発言したら全メンバーをボイスチャットから退出させる
  if message.content == "/close_vc":
    voice_channels = message.guild.voice_channels
    for vc in voice_channels:
      print(vc)
      for member in vc.members:
        print(f"{member}を退出させました")
        await member.move_to(None) #move_to(None)で切断

  #「/おやすみ」と発言したらペアサーバーの全員を退出させる
  #ペアサーバーでのみ機能する
  if message.content == "/おやすみ":
    if message.guild.id == guild_id_pair: 
      voice_channels = message.guild.voice_channels
      for vc in voice_channels:
        print(vc)
        for member in vc.members:
          await member.move_to(None) #move_to(None)で切断
          print(f"{member}を退出させました")
    
  #オウム返し
  """
  if message.guild.id == guild_id_personnal: #個人サーバーでのみ動作
    await message.channel.send(message.content)
    print(message.content)
  """





#Botの起動とDiscordサーバーへの接続
client.run(token)