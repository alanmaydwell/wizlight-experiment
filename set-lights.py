#!/usr/bin/env python3

import asyncio


from pywizlight import wizlight, PilotBuilder, discovery, bulb
from pywizlight.exceptions import WizLightConnectionError


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
        print("Found the following bulbs:")
        for bulb in bulbs:
            print(f"\t{bulb}")
    return bulbs


async def set_bulb_colour(bulb: bulb.wizlight,
                          rgb: tuple[int, int, int] = (255, 255, 255)) -> bool:
    success = True
    try:
        await bulb.turn_on(PilotBuilder(rgb = rgb))
    except WizLightConnectionError as e:
        success = False
        print(f"Failed to connect to {bulb}")
    return success


async def main():
    bulbs = await get_bulbs()
    if not bulbs:
        print("Ending as no bulbs found.")
        return

    iteration = 0
    while True:
        # The async behaviour here is not ideal. If we have two bulbs that
        # are being updated but then one of them is turned off, the updates
        # to the remaining bulb are repeatedly paused. Likely due to timeout
        # time from attempt to update the turned-off bulb, and that `gather`
        # awaits all responses before advancing to next step.
        bulb_coroutines = [set_bulb_colour(bulb, get_rgb(iteration + 3*bi))
                           for bi, bulb in enumerate(bulbs)]
        results = await asyncio.gather(*bulb_coroutines)
        if True not in results:
            print("Ending as all bulb updates failed.")
            return
        await asyncio.sleep(0.4)
        iteration += 1


if __name__ == "__main__":
    # using the two lines below instead of just `asyncio.get_event_loop()` stops the
    # `DeprecationWarning: There is no current event loop` message but this might depend
    # on Python version
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
