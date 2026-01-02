#!/usr/bin/env python3

import asyncio

from pywizlight import wizlight, PilotBuilder, discovery, bulb

"""
WiZ experiment
Note example on https://github.com/sbidy/pywizlight SEEMS to make a distinction between `light`
and `bulb` but these are both both pywizlight.bulb.wizlight objects, so look to be the same.
"""


def get_rgbs(pick: int, repeat: int = 10) -> list[tuple[int, int, int]]:
    "Hasty bodge for returning two sequences of RGB values"
    colours1 = [(0, 0, 255), (0, 128, 128), (0, 255, 0), (128 , 128, 0), (255, 0, 0), (128, 0, 128)] * repeat
    colours2 = colours1[::-1]  # reversed
    colours = [colours1, colours2]
    pick = pick % len(colours)
    return colours[pick]
    

async def get_bulbs(broadcast_space: str = "192.168.0.255") -> list[bulb.wizlight]:
    "Find WiZ bulbs available on LAN"
    bulbs =  await discovery.discover_lights(broadcast_space=broadcast_space)
    return bulbs


async def colour_strobe(bulb: bulb.wizlight,
                        colours: list[tuple[int, int, int]],
                        delay: int | float = 0.5):
    """
    Send sequence of colour changes to WiZ bulb.
    colours is list of tuples with RGB values e,g. [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    """
    for colour in colours:
        await bulb.turn_on(PilotBuilder(rgb = colour))
        await asyncio.sleep(delay)
        

async def main():
    print("Looking for WiZ lights")
    bulbs = await get_bulbs()
    if bulbs:
        print(f"Found {len(bulbs)} lights:")
        for bulb in bulbs:
            print(bulb)
        
        print("Strobe!")
        strobe_coroutines = [colour_strobe(bulb, get_rgbs(bi), 0.1) for bi, bulb in enumerate(bulbs)]
        await asyncio.gather(*strobe_coroutines)
    else:
        print("No WiZ lights found")
    print("End")


if __name__ == "__main__":
    # Note using `asyncio.run(main())` leads to `RuntimeError: Event loop is closed` at end
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
