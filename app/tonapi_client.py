import aiohttp
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class TonAPIClient:
    def __init__(self):
        self.api_key = os.getenv("TONAPI_KEY")
        self.base_url = "https://tonapi.io/v2"
        self.mainnet_contract = "EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt"
        self.rate_limit_delay = 0.1

    async def get_swap_transactions(self, wallet_address: str):
        transactions = []
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{self.base_url}/blockchain/accounts/{wallet_address}/transactions?limit=100"
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        print(f"Ошибка API: {await response.text()}")
                        return transactions
                    data = await response.json()
                    for tx in data.get("transactions", []):
                        if any(msg.get("destination") == self.mainnet_contract for msg in tx.get("out_msgs", [])):
                            operation = await self._parse_swap_operation(tx)
                            if operation:
                                transactions.append(operation)
                        await asyncio.sleep(self.rate_limit_delay)
            except Exception as e:
                print(f"Ошибка при получении транзакций: {e}")
        return transactions

    async def _parse_swap_operation(self, tx):
        for msg in tx.get("out_msgs", []):
            if msg.get("destination") == self.mainnet_contract:
                return {
                    "transaction_hash": tx.get("hash"),
                    "pool_address": msg.get("destination"),
                    "amount_in": float(msg.get("value", 0)) / 1_000_000_000,
                    "amount_out": 0.0,
                    "token_in": "TON",
                    "token_out": "Unknown",
                    "timestamp": datetime.fromtimestamp(tx.get("utime")),
                    "status": "success" if tx.get("success", True) else "failed"
                }
        return None