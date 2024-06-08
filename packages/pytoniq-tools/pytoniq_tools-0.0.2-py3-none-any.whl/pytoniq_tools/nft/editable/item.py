from __future__ import annotations

from pytoniq_core import Address, Cell, begin_cell

from ..base.item import Item
from ..content import OffchainContent
from ..data import ItemData
from ..op_codes import *

CODE_HEX = "b5ee9c7241020d010001d0000114ff00f4a413f4bcf2c80b0102016203020009a11f9fe0050202ce050402012008060201200907001d00f232cfd633c58073c5b3327b552000113e910c1c2ebcb85360003b3b513434cffe900835d27080269fc07e90350c04090408f80c1c165b5b6002d70c8871c02497c0f83434c0c05c6c2497c0f83e903e900c7e800c5c75c87e800c7e800c3c00812ce3850c1b088d148cb1c17cb865407e90350c0408fc00f801b4c7f4cfe08417f30f45148c2ea3a1cc840dd78c9004f80c0d0d0d4d60840bf2c9a884aeb8c097c12103fcbc200b0a00727082108b77173505c8cbff5004cf1610248040708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb0001f65135c705f2e191fa4021f001fa40d20031fa00820afaf0801ba121945315a0a1de22d70b01c300209206a19136e220c2fff2e192218e3e821005138d91c85009cf16500bcf16712449145446a0708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb00104794102a375be20c0082028e3526f0018210d53276db103744006d71708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb0093303234e25502f003cc82807e"  # noqa


class ItemDataEditable(ItemData):
    ...


class ItemEditable(Item):

    def __init__(
            self,
            data: ItemDataEditable,
    ) -> None:
        self._data = data.serialize()
        self._code = Cell.one_from_boc(CODE_HEX)

    @classmethod
    def build_edit_content_body(
            cls,
            content: OffchainContent,
            query_id: int = 0,
    ) -> Cell:
        """
        Builds the body of the edit item content transaction.

        :param content: The new content to be set.
        :param query_id: The query ID. Defaults to 0.
        :return: The cell representing the body of the edit item content transaction.
        """
        return (
            begin_cell()
            .store_uint(EDIT_ITEM_CONTENT_OPCODE, 32)
            .store_uint(query_id, 64)
            .store_ref(content.serialize())
            .end_cell()
        )

    @classmethod
    def build_change_editorship_body(
            cls,
            editor_address: Address,
            response_address: Address = None,
            custom_payload: Cell = Cell.empty(),
            forward_payload: Cell = Cell.empty(),
            forward_amount: int = 0,
            query_id: int = 0,
    ) -> Cell:
        """
        Builds the body of the change item editorship transaction.

        :param editor_address: The address of the new editor.
        :param response_address: The address to respond to. Defaults to the editor address.
        :param custom_payload: The custom payload. Defaults to an empty cell.
        :param forward_payload: The payload to be forwarded. Defaults to an empty cell.
        :param forward_amount: The amount of coins to be forwarded. Defaults to 0.
        :param query_id: The query ID. Defaults to 0.
        :return: The cell representing the body of the change item editorship transaction.
        """
        return (
            begin_cell()
            .store_uint(CHANGE_ITEM_EDITORSHIP_OPCODE, 32)
            .store_uint(query_id, 64)
            .store_address(editor_address)
            .store_address(response_address or editor_address)
            .store_maybe_ref(custom_payload)
            .store_coins(forward_amount)
            .store_maybe_ref(forward_payload)
            .end_cell()
        )
