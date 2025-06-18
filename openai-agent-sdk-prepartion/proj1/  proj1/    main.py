async def run_panacloud_agent(prompt):
    response = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    async for event in response.stream_events():
        print(f"Image generated: {event.item.output}")

async def main():
    await run_panacloud_agent("Generate an image of a sunset over the ocean.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())