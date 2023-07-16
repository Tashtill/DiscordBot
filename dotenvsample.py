from dotenv import load_dotenv
import os

load_dotenv()

sam = os.getenv("Sample")
prnit(sam)