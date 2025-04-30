import asyncio
from urllib.parse import urlparse
from core.modules.database import *

async def runCommand(cmd, type):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
        addScannerOutput(type, stdout)
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme in ('http', 'https'), parsed.netloc])