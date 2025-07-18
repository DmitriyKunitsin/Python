from FitnesBot import FitnessBot
import myLibary as lib
async def main():
    
    lib.nest_asyncio.apply()
    bot = FitnessBot(lib.TOKEN, persistence_path="arbitrarycallbackdatabot")
    lib.asyncio.run(bot.run())
    

if __name__ == "__main__":
    lib.asyncio.run(main())