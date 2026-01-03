#!/usr/bin/env python3

import asyncio


from pywizlight import wizlight, PilotBuilder, discovery, bulb


colours = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0),
           (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255),
           (0, 0, 255), (128, 0 , 255), (255, 0, 255), (255, 0, 128)
           ]


def get_rgb(pick: int = 0) -> tuple[int, int, int]:
    pick = pick % len(colours)
    return colours[pick]


async def get_bulbs(broadcast_space: str = "192.168.0.255", verbose=True) -> list[bulb.wizlight]:
    "Find WiZ bulbs available on LAN"
    bulbs =  await discovery.discover_lights(broadcast_space=broadcast_space)
    if verbose:
        for bulb in bulbs:
            print(bulb)
    return bulbs


async def set_bulb_colour(bulb: bulb.wizlight, rgb: tuple[int, int, int] = (255, 255, 255)):
    await bulb.turn_on(PilotBuilder(rgb = rgb))


async def main():
    bulbs = await get_bulbs()
    if not bulbs:
        return
    iteration = 0
    while True:
        bulb_coroutines = [set_bulb_colour(bulb, get_rgb(iteration + (3 * bi))) for bi, bulb in enumerate(bulbs)]
        await asyncio.gather(*bulb_coroutines)
        await asyncio.sleep(0.1)
        iteration += 1


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
