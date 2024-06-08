import asyncio

from pytoniq import LiteBalancer, WalletV4R2

from pytoniq_tools.nft.standard.collection import CollectionStandard

IS_TESTNET = True

MNEMONICS = "a b c ..."  # noqa


async def main() -> None:
    provider = await get_provider()
    wallet = await get_wallet(provider)

    from_index = 1
    body = CollectionStandard.build_butch_mint_body(
        index=index,
        owner_address=OWNER_ADDRESS,
        content=OffchainCommonContent(
            uri=f"{index}.json"
        ),
    )

    await wallet.transfer(
        destination=COLLECTION_ADDRESS,
        body=body,
        amount=int(0.02 * 1e9),
    )

    item = ItemStandard(
        data=ItemDataStandard(
            index=index,
            collection_address=COLLECTION_ADDRESS,
        )
    )

    print(f"Minted item: {item.address.to_str()}")

async def get_provider() -> LiteBalancer:
    if IS_TESTNET:
        provider = LiteBalancer.from_testnet_config(
            trust_level=2,
        )
    else:
        provider = LiteBalancer.from_mainnet_config(
            trust_level=2,
        )

    await provider.start_up()
    return provider


async def get_wallet(provider: LiteBalancer) -> WalletV4R2:
    return await WalletV4R2.from_mnemonic(
        provider=provider,
        mnemonics=MNEMONICS.split(" "),
    )


if __name__ == "__main__":
    asyncio.run(main())
