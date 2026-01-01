import asyncio

from pywizlight import wizlight, PilotBuilder, discovery, bulb

"""
WiZ experiment
Note example on https://github.com/sbidy/pywizlight SEEMS to make a distinction between `light`
and `bulb` but these are both both pywizlight.bulb.wizlight objects, so look to be the same.
"""


async def get_bulbs(broadcast_space: str = "192.168.0.255") -> list[bulb.wizlight]:
    "Find WiZ bulbs available on LAN"
    bulbs =  await discovery.discover_lights(broadcast_space=broadcast_space)
    return bulbs


async def colour_strobe(bulb: bulb.wizlight,
                        colours: list[tuple[int, int, int]],
                        delay: int | float = 0.5):
    """
    colours is list of tuples with RGB values e,g. [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    """
    for colour in colours:
        await bulb.turn_on(PilotBuilder(rgb = colour))
        await asyncio.sleep(delay)
        

async def main():
    print("Looking for WiZ lights")
    bulbs = await get_bulbs()
    

    if bulbs:
        # Don't need the below - can directly update bulb
        ## light = wizlight(bulbs[0].ip)
        
        print(f"Found {len(bulbs)} lights")
        for bulb in bulbs:
            print(bulb)
        print("Strobe!")
        bulb = bulbs[0]
        colours = [(0, 0, 255), (0, 128, 128), (0, 255, 0), (128 , 128, 0), (255, 0, 0), (128, 0, 128)] * 10
        await colour_strobe(bulb, colours, 0.1)
    else:
        print("No WiZ lights found")
    print("End")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

