from msoc import search, engines
import asyncio


async def main():
    # async for sound in search("Его Крид"):
    #     print(f"Name: {sound.name}, URL: {sound.url}")
    print(engines())
    

asyncio.run(main())