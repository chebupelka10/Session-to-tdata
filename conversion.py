from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession

import asyncio
import shutil

async def create_tdata(session_name):
	try:
		client = TelegramClient(f"Session/{session_name}")
		tdesk = await client.ToTDesktop(flag=UseCurrentSession)
		tdesk.SaveTData(f'TData/{session_name.split(".")[0]}/tdata/tdata')

		shutil.make_archive(f'TData/{session_name.split(".")[0]}/tdata',
							'zip',
							f'TData/{session_name.split(".")[0]}/tdata')

		return True
	except:
		return False
	finally:
		await client.disconnect()
