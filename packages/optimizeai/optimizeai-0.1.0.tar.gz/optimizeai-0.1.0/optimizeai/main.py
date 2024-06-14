# main.py

from optimizeai.decorators.optimize import optimize
from optimizeai.config import Config
from dotenv import load_dotenv
import time
import os

load_dotenv()
llm = os.getenv("LLM")
key = os.getenv("API_KEY")
model = os.getenv("MODEL")
llm_config = Config(llm=llm, model= model, key=key, mode="online")
perfwatch_params = ["line", "cpu", "time"]

@optimize(config = llm_config, profiler_types=perfwatch_params)
def test():
    for _ in range(10):
        time.sleep(0.1)
        print("Hello World!")
        pass

if __name__ == "__main__":
    test()
