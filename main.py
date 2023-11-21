import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random
import emoji
import datetime
import glob
import asyncio



#自分のBotのアクセストークンを取得
load_dotenv()
token = os.getenv("DiscordBot_token")
#ボットのインスタンスを作成
description = """このボットで使用可能なコマンドは以下のとおりです。
コマンドを使用する際は/helpのように頭に/をつけてください。"""
bot = commands.Bot(command_prefix="/", description = description, intents=discord.Intents.all())


#起動時に動作する処理
@bot.event
async def on_ready():
  print(f"We have logged in as {bot.user}")
  await bot.tree.sync() #コマンドを同期



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



#メッセージ受信時に動作する処理群
@bot.event
async def on_message(message):

  #メッセージ送信者がBot自身の場合、出力したメッセージをターミナルにprintし、以降の処理をスキップ
  if message.author == bot.user:
    print(f"[{message.guild}] OUTPUT : {message.content}")
    return

  #受信メッセージをターミナルで確認。demojizeで絵文字の文字化けを防ぐ
  print(f"[{message.guild}] {message.author} > {emoji.demojize(message.content)}")

  #メッセージが「にゃん」or「にゃーん」の場合「にゃーん」を返す
  if "にゃーん" in message.content or "にゃん" in message.content:
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

  #スラッシュコマンド対応用の確認項目
  if message.content == "コマンド表示":
    print(bot.tree.get_commands())

  if message.content == "コマンドリスト":
    for command in bot.commands:
      print(command)

  #スラッシュコマンドの処理に移行
  await bot.process_commands(message)



#スラッシュコマンド
@bot.command()
async def hello(ctx):
  """あいさつは、だいじ"""
  await ctx.reply("こんにちは")

#ボイスチャットの解散
@bot.command()
async def close(ctx):
  """サーバー内のボイスチャットを解散します"""
  await close_vc(ctx.guild)
  await ctx.send("ボイスチャットを解散しました")

timer_counter = 0

#ボイスチャットの解散タイマー
@bot.command()
async def closeIn(ctx, arg):
  """x分後にボイスチャットを解散します"""
  try:
    sec = int(arg)
    min = sec*60
    global timer_counter
    timer_counter += 1 #新規タイマーの作成前もしくはタイマーストップ時にtimer_counterを書き換えてタイマーを無効化する
    my_counter = timer_counter
    await ctx.send(f"{arg}分後にボイスチャットを解散します")
    await asyncio.sleep(min)
    if my_counter == timer_counter:
      await close_vc(ctx.guild)
      await ctx.send("ボイスチャットを解散しました")
    else:
      print(f"{arg}分前のタイマーは停止もしくはリセットされています")
  except ValueError:
    await ctx.send("数値は整数で入力してください")
#ボイスチャットのタイマー停止
@bot.command()
async def stop(ctx):
  """タイマーを停止します"""
  global timer_counter
  timer_counter += 1
  await ctx.send("ボイスチャット停止のタイマーを停止しました")

#6面ダイスを振る
@bot.command()
async def roll(ctx):
  """サイコロをふります"""
  number = random.randint(1,6)
  await ctx.send(f"{number}の目が出ました")

#動物の画像を送る
@bot.command()
async def animal(ctx):
  """動物の画像を送ります"""
  jpg_img_list = glob.glob(r"C:\Users\mhrt2\work\DiscordBot\animals\*.jpg")
  png_img_list = glob.glob(r"C:\Users\mhrt2\work\DiscordBot\animals\*.png")
  img_list = jpg_img_list + png_img_list
  img_path = random.choice(img_list)
  await ctx.send(file = discord.File(img_path))



#Botの起動とDiscordサーバーへの接続
bot.run(token)