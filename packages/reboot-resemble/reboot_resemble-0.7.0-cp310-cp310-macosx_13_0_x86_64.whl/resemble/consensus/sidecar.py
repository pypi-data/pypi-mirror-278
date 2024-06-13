import asyncio
import grpc
import uuid
from google.protobuf.descriptor_pb2 import FileDescriptorSet
from resemble.aio.contexts import Participants
# ISSUE(#2941) Because `isort` and `mypy` have different opinions on how to
# write the following import statement, we use a regular import and an
# assignment.
#
#from resemble.consensus.sidecar_native import \
#   SidecarServer as _SidecarServer  # type: ignore[import]
from resemble.consensus.sidecar_native import (  # type: ignore[import]
    SidecarServer,
)
from resemble.settings import MAX_SIDECAR_GRPC_MESSAGE_LENGTH_BYTES
from resemble.v1alpha1 import sidecar_pb2, sidecar_pb2_grpc, tasks_pb2
# TODO(benh): move this into a top-level 'grpc' module to be shared by
# both 'respect' and 'resemble'.
from respect.grpc.options import make_retry_channel_options
from typing import Optional

# ISSUE(#2941) Continuation of the above workaround for `isort` and `mypy`.
_SidecarServer = SidecarServer


# TODO: Refactor into an `exceptions` module.
class SidecarError(Exception):
    """Base exception for sidecar related errors."""


class SidecarServerFailed(SidecarError):
    """Raised when the sidecar server fails to start."""


class LoadError(SidecarError):
    """Base exception for errors related to loading state from the sidecar."""


class NonexistentTaskId(LoadError):
    """Raised when attempting to load a task response with a non-existent task
    id."""


def SidecarServer( # type: ignore[no-redef]
    *args, **kwargs
) -> 'SidecarServer':
    """Fake constructor for creating a SidecarServer instance. This is done to
    capture and cast exceptions thrown by the C++ sidecar server into more
    python friendly types.
    """
    try:
        return _SidecarServer(*args, **kwargs)
    except RuntimeError as e:
        raise SidecarServerFailed(str(e)) from e


# `SortedMap` is implemented using a series of special cases that we might
# selectively remove over time. See #2983 for more information.
#
# The state schema in the native sidecar bans use of `\x00` and `\x01` in all
# key components: see documentation on `STATE_CF_NAME` in `sidecar.cc`.
#
# This client prepends a type tag when storing data in the state schema, in order
# to support colocating any data type (recursively) under a state machine. In
# future, we expect to use _either_ varint or fixed length hashes for type tags:
# see #2972 for more information. For now, we use hardcoded varint type tags for
# the two types stored in the state schema. To support fixed length hashes in the
# future, we would reserve a particular prefix byte for the fixed length hash.
SORTED_MAP_TYPE_NAME = "resemble.integrations.collections.v1.SortedMap"
SORTED_MAP_TYPE_TAG = "\x02"
SORTED_MAP_ENTRY_TYPE_TAG = "\x03"


def _validate_state_key_component(component: str) -> None:
    if not component or component[0] not in (
        SORTED_MAP_TYPE_TAG, SORTED_MAP_ENTRY_TYPE_TAG
    ):
        raise ValueError(
            "A key used in the state schema must be prefixed with "
            f"a type tag. Got {component!r}"
        )
    if any(char in ("\x00", "\x01") for char in component):
        raise ValueError(
            "A key used in the state schema may not contain the bytes "
            f"\\x00 or \\x01. Got {component!r}"
        )


class SidecarClient:
    """Helper class for interacting with the resemble sidecar."""

    def __init__(self, target: str):
        self._target = target
        self._stub: Optional[sidecar_pb2_grpc.SidecarStub] = None

    async def interleaved_range(
        self,
        *,
        state_key: list[str],
        start: Optional[str] = None,
        end: Optional[str] = None,
        limit: int = 128,
        transaction: Optional[sidecar_pb2.Transaction] = None,
    ) -> list[tuple[list[str], bytes]]:
        """Attempt to load a page of interleaved state machines from the sidecar.

        NOTE: This method validates that keys are already prefixed with their type
        tags, as required by the partitioned state schema in the sidecar.
        """
        for component in state_key:
            _validate_state_key_component(component)
        if start is not None:
            _validate_state_key_component(start)
        if end is not None:
            _validate_state_key_component(end)

        stub = await self._get_sidecar_stub()
        response: sidecar_pb2.InterleavedRangeResponse = await stub.InterleavedRange(
            sidecar_pb2.InterleavedRangeRequest(
                state_key=sidecar_pb2.Key(components=state_key),
                start=start,
                end=end,
                transaction=transaction,
                limit=limit,
            )
        )
        assert len(response.keys) == len(response.values)
        return [
            (k.components, v) for k, v in zip(response.keys, response.values)
        ]

    async def load_actor_state(
        self,
        service: str,
        actor_id: str,
    ) -> Optional[bytes]:
        """Attempt to load state from sidecar. Return None if state
         has not (yet) been stored.
        """
        stub = await self._get_sidecar_stub()
        response: sidecar_pb2.LoadResponse = await stub.Load(
            sidecar_pb2.LoadRequest(
                actors=[sidecar_pb2.Actor(service=service, actor_id=actor_id)]
            )
        )
        if len(response.actors) > 1:
            raise LoadError(
                f'Expected one actor in LoadResponse; got {len(response.actors)}'
            )

        if len(response.actors) == 0:
            return None

        # Invariant: If an actor is filled in a LoadResponse, its state field is
        # also filled (although said state may itself be empty).
        assert response.actors[0].HasField('state')
        return response.actors[0].state

    async def load_task_response(
        self,
        task_id: tasks_pb2.TaskId,
    ) -> Optional[bytes]:
        """Attempt to load task response from sidecar. Return None if task
         has no response stored yet. If the task doesn't exist yet, throw an
         error.
        """
        stub = await self._get_sidecar_stub()
        response: sidecar_pb2.LoadResponse = await stub.Load(
            sidecar_pb2.LoadRequest(task_ids=[task_id])
        )
        if len(response.tasks) == 0:
            raise NonexistentTaskId()

        if len(response.tasks) > 1:
            raise LoadError(
                f'Expected one task in LoadResponse; got {len(response.tasks)}'
            )

        if response.tasks[0].status == sidecar_pb2.Task.Status.COMPLETED:
            # Invariant: once a Task's status is COMPLETED, the task response
            # field is filled (although the response itself may be empty).
            assert response.tasks[0].HasField('response')
            return response.tasks[0].response.SerializeToString()
        else:
            return None

    async def store(
        self,
        actor_upserts: list[sidecar_pb2.Actor],
        task_upserts: list[sidecar_pb2.Task],
        interleaved_upserts: list[sidecar_pb2.InterleavedUpsert],
        transaction: Optional[sidecar_pb2.Transaction] = None,
        idempotent_mutation: Optional[sidecar_pb2.IdempotentMutation] = None,
        file_descriptor_set: Optional[FileDescriptorSet] = None,
    ) -> None:
        """Store actor state and task upserts after method completion."""
        stub = await self._get_sidecar_stub()

        for iup in interleaved_upserts:
            for component in iup.key.components:
                _validate_state_key_component(component)

        request = sidecar_pb2.StoreRequest(
            actor_upserts=actor_upserts,
            task_upserts=task_upserts,
            interleaved_upserts=interleaved_upserts,
            transaction=transaction,
            idempotent_mutation=idempotent_mutation,
            file_descriptor_set=file_descriptor_set,
        )

        await stub.Store(request)

    async def transaction_coordinator_prepared(
        self,
        transaction_id: uuid.UUID,
        participants: Participants,
    ) -> None:
        """Called by a transaction coordinator after it has successfully
        prepared a transaction, i.e., completed the first phase of two
        phase commit. After this RPC returns we should always be able
        to tell all the transaction participants that the transaction
        has committed.
        """
        stub = await self._get_sidecar_stub()

        await stub.TransactionCoordinatorPrepared(
            sidecar_pb2.TransactionCoordinatorPreparedRequest(
                transaction_id=transaction_id.bytes,
                participants=participants.to_sidecar(),
            )
        )

    async def transaction_participant_prepare(
        self, service: str, actor_id: str
    ) -> None:
        """Called by a transaction participant when they are
        prepared. Guarantees that the preparedness of this participant
        is persisted when the RPC returns, meaning that until
        'TransactionParticipantCommit()' or '...Abort()' is called,
        any call to 'Recover()' is guaranteed to return this
        transaction's information.
        """
        stub = await self._get_sidecar_stub()

        await stub.TransactionParticipantPrepare(
            sidecar_pb2.TransactionParticipantPrepareRequest(
                service=service, actor_id=actor_id
            )
        )

    async def transaction_participant_commit(
        self, service: str, actor_id: str
    ) -> None:
        """Called by a transaction participant to commit its given
        transaction. The transaction must previously have been
        prepared via 'TransactionParticipantPrepare()'. The
        transaction is guaranteed to be persisted as committed when
        the RPC returns.
        """
        stub = await self._get_sidecar_stub()

        await stub.TransactionParticipantCommit(
            sidecar_pb2.TransactionParticipantCommitRequest(
                service=service, actor_id=actor_id
            )
        )

    async def transaction_participant_abort(
        self, service: str, actor_id: str
    ) -> None:
        """Called by a transaction participant to abort its given
        transaction. The transaction MAY or MAY NOT have been prepared
        via 'TransactionParticipantPrepare()'. The transaction is
        guaranteed to be persisted as aborted when the RPC returns.
        """
        stub = await self._get_sidecar_stub()

        await stub.TransactionParticipantAbort(
            sidecar_pb2.TransactionParticipantAbortRequest(
                service=service, actor_id=actor_id
            )
        )

    async def recover(self) -> sidecar_pb2.RecoverResponse:
        """Attempt to recover server state after a potential restart."""
        stub = await self._get_sidecar_stub()
        return await stub.Recover(sidecar_pb2.RecoverRequest())

    @classmethod
    async def _make_sidecar_channel(cls, target: str) -> grpc.aio.Channel:
        """Create a gRPC channel with options specific for the sidecar."""
        channel = grpc.aio.insecure_channel(
            target,
            options=make_retry_channel_options(
                max_send_message_length=MAX_SIDECAR_GRPC_MESSAGE_LENGTH_BYTES,
                max_receive_message_length=
                MAX_SIDECAR_GRPC_MESSAGE_LENGTH_BYTES,
            )
        )

        # See 'respect/clients/aio/object_store_client.py' for a
        # longer explanation of why we wait for 'channel_ready()'
        # here.
        await asyncio.wait_for(channel.channel_ready(), timeout=45)
        return channel

    async def _get_sidecar_stub(self) -> sidecar_pb2_grpc.SidecarStub:
        if self._stub is None:
            channel = await SidecarClient._make_sidecar_channel(self._target)
            self._stub = sidecar_pb2_grpc.SidecarStub(channel)
        return self._stub
