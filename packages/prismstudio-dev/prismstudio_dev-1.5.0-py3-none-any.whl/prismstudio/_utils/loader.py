import time
import logging
import requests
from itertools import cycle
from threading import Thread
from tqdm.auto import tqdm
from shutil import get_terminal_size

from .._common.config import ModeSetting

logger = logging.getLogger()


class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        ms = ModeSetting()
        self.quiet_mode = ms.QUIET_MODE
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread = Thread(target=self._animate, daemon=True)
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            time.sleep(self.timeout)

    def __enter__(self):
        if not self.quiet_mode:
            self.start()
        return self

    def stop(self, exce=True):
        self.done = True
        if self.quiet_mode:
            return
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, flush=True)
        if exce:
            print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        self.stop(exce=False)


def download(links):
    ms = ModeSetting()
    r = requests.get(url=links, stream=(not ms.QUIET_MODE))
    if ms.QUIET_MODE:
        result = r.content
    else:
        print("\r")
        print("\rData Fetching Done!")
        print(" " * 30)
        print("Start downloading data...")
        r.raise_for_status()
        result = []
        with tqdm(total=int(r.headers["content-length"]), unit="B", unit_scale=True, unit_divisor=1024) as pbar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk is not None:  # filter out keep-alive new chunks
                    result.append(chunk)
                    pbar.update(len(chunk))
        result = b"".join(result)
        print("Download Completed!")
    return result
