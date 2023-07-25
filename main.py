import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random
import emoji
import datetime



#自分のBotのアクセストークンを取得
load_dotenv()
token = os.getenv("DiscordBot_token")
#ボットのインスタンスを作成
description = """このボットで使用可能なコマンドは以下のとおりです。
コマンドを使用する際は/helpのように頭に/をつけてください。"""
bot = commands.Bot(command_prefix="/", description = description, intents=discord.Intents.all())


#各サーバーやチャンネルのID
guild_id_personnal = int(os.getenv("guild_id_personnal")) #個人サーバー
channel_id_bot_notice = int(os.getenv("channel_id_bot_notice"))  #個人サーバー,Bot通知チャンネル
channel_id_vc_general = int(os.getenv("channel_id_vc_general")) #個人サーバー,一般vc
guild_id_lab_room = int(os.getenv("guild_id_lab_room")) #らぼべやサーバー
guild_id_pair = int(os.getenv("guild_id_pair")) #2人用サーバー



#イベント内で使用する関数
#サーバー内のVCから全メンバーを退出させる
async def close_vc(guild):
  voice_channels = guild.voice_channels
  for vc in voice_channels:
    for member in vc.members:
      await member.move_to(None) #move_to(None)で切断
      print(f"{vc}から{member}を退出させました")



#起動時に動作する処理
@bot.event
async def on_ready():
  print(f"We have logged in as {bot.user}")
  dt_now_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
  channel_bot_notice = bot.get_channel(channel_id_bot_notice)
  await channel_bot_notice.send(f"オンラインになりました\n現在時刻は{dt_now_jst}です")




#メッセージ受信時に動作する処理群
@bot.event
async def on_message(message):

  #メッセージ送信者がBot自身の場合、出力したメッセージをターミナルにprintし、以降の処理をスキップ
  if message.author == bot.user:
    print(f"[{message.guild}] OUTPUT : {message.content}")
    return

  #受信メッセージをターミナルで確認。絵文字を処理できるようにdemojizeしておく
  print(f"[{message.guild}] {message.author} > {emoji.demojize(message.content)}")

  #「にゃーん」と発言したら「にゃーん」を返す
  if message.content == "にゃーん":
    await message.channel.send("にゃーん")

  #💩の絵文字が入力されたら、トイレットペーパーを投げる
  demojized_message = emoji.demojize(message.content)
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

  #「？おやすみ」と発言したらペアサーバーの全員を退出させる
  #ペアサーバーでのみ機能する
  if message.content == "？おやすみ":
    if message.guild.id == guild_id_pair: 
     await close_vc(message.guild)

  #スラッシュコマンドの処理に移行
  await bot.process_commands(message)



#スラッシュコマンド

@bot.command()
async def hello(ctx):
  """あいさつは、だいじ"""
  await ctx.reply("こんにちは")

#ボイスチャットの解散
@bot.command()
async def close_voice_chat(ctx):
  """サーバー内のボイスチャットを解散します"""
  await close_vc(ctx.guild)
  await ctx.send("ボイスチャットを解散しました")

#6面ダイスを振る
@bot.command()
async def roll(ctx):
  """サイコロをふります"""
  number = random.randint(1,6)
  await ctx.send(f"{number}の目が出ました")



#Botの起動とDiscordサーバーへの接続
bot.run(token)