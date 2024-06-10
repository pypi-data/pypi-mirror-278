from typing import Iterable, Iterator, TypeVar, cast

from streamable import _util, functions
from streamable.stream import (
    AForeachStream,
    AMapStream,
    CatchStream,
    FilterStream,
    FlattenStream,
    ForeachStream,
    GroupStream,
    LimitStream,
    MapStream,
    ObserveStream,
    SlowStream,
    Stream,
)
from streamable.visitor import Visitor

T = TypeVar("T")
U = TypeVar("U")


class IteratorVisitor(Visitor[Iterator[T]]):
    def visit_catch_stream(self, stream: CatchStream[T]) -> Iterator[T]:
        return functions.catch(
            stream.upstream.accept(self),
            stream.predicate,
            raise_at_exhaustion=stream.raise_at_exhaustion,
        )

    def visit_filter_stream(self, stream: FilterStream[T]) -> Iterator[T]:
        return filter(
            _util.reraise_as(
                stream.predicate, StopIteration, functions.WrappedStopIteration
            ),
            cast(Iterable[T], stream.upstream.accept(self)),
        )

    def visit_flatten_stream(self, stream: FlattenStream[T]) -> Iterator[T]:
        return functions.flatten(
            stream.upstream.accept(IteratorVisitor[Iterable]()),
            concurrency=stream.concurrency,
        )

    def visit_foreach_stream(self, stream: ForeachStream[T]) -> Iterator[T]:
        return self.visit_map_stream(
            MapStream(
                stream.upstream,
                _util.sidify(stream.func),
                stream.concurrency,
            )
        )

    def visit_aforeach_stream(self, stream: AForeachStream[T]) -> Iterator[T]:
        return self.visit_amap_stream(
            AMapStream(
                stream.upstream,
                _util.async_sidify(stream.func),
                stream.concurrency,
            )
        )

    def visit_group_stream(self, stream: GroupStream[U]) -> Iterator[T]:
        return cast(
            Iterator[T],
            functions.group(
                stream.upstream.accept(IteratorVisitor[U]()),
                stream.size,
                stream.seconds,
                stream.by,
            ),
        )

    def visit_limit_stream(self, stream: LimitStream[T]) -> Iterator[T]:
        return functions.limit(
            stream.upstream.accept(self),
            stream.count,
        )

    def visit_map_stream(self, stream: MapStream[U, T]) -> Iterator[T]:
        return functions.map(
            stream.func,
            stream.upstream.accept(IteratorVisitor[U]()),
            concurrency=stream.concurrency,
        )

    def visit_amap_stream(self, stream: AMapStream[U, T]) -> Iterator[T]:
        return functions.amap(
            stream.func,
            stream.upstream.accept(IteratorVisitor[U]()),
            concurrency=stream.concurrency,
        )

    def visit_observe_stream(self, stream: ObserveStream[T]) -> Iterator[T]:
        return functions.observe(
            stream.upstream.accept(self),
            stream.what,
            stream.colored,
        )

    def visit_slow_stream(self, stream: SlowStream[T]) -> Iterator[T]:
        return functions.slow(stream.upstream.accept(self), stream.frequency)

    def visit_stream(self, stream: Stream[T]) -> Iterator[T]:
        iterable = stream._source() if callable(stream._source) else stream._source
        _util.validate_iterable(iterable)
        return iter(iterable)
