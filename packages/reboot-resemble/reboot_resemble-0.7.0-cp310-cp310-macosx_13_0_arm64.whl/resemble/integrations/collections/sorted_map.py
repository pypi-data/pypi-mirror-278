from google.protobuf.empty_pb2 import Empty
from resemble.aio.contexts import ReaderContext, WriterContext
from resemble.integrations.collections.v1.sorted_map_rsm import (
    Entry,
    InsertRequest,
    InsertResponse,
    RangeRequest,
    RangeResponse,
    RemoveRequest,
    RemoveResponse,
    SortedMap,
)


class SortedMapServicer(SortedMap.Interface):

    async def Insert(
        self,
        # TODO: Once https://github.com/reboot-dev/respect/issues/2918 is fixed
        # this method should become a Transaction, which will be a backwards
        # compatible change.
        context: WriterContext,
        state: Empty,
        request: InsertRequest,
    ) -> SortedMap.InsertEffects:
        return SortedMap.InsertEffects(
            state=state,
            response=InsertResponse(),
            _interleaved_upserts=list(request.entries.items()),
        )

    async def Remove(
        self,
        # TODO: Once https://github.com/reboot-dev/respect/issues/2918 is fixed
        # this method should become a Transaction, which will be a backwards
        # compatible change.
        context: WriterContext,
        state: Empty,
        request: RemoveRequest,
    ) -> SortedMap.RemoveEffects:
        return SortedMap.RemoveEffects(
            state=state,
            response=RemoveResponse(),
            _interleaved_upserts=list((k, None) for k in request.keys),
        )

    async def Range(
        self,
        context: ReaderContext,
        state: Empty,
        request: RangeRequest,
    ) -> RangeResponse:
        if request.limit == 0:
            raise ValueError("Range requires a non-zero `limit` value.")

        assert self._middleware is not None

        page = await self._middleware._state_manager.interleaved_range(
            context,
            start=(
                request.start_key if request.HasField('start_key') else None
            ),
            end=(request.end_key if request.HasField('end_key') else None),
            limit=request.limit,
        )

        return RangeResponse(entries=[Entry(key=k, value=v) for k, v in page])
