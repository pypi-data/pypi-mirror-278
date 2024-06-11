"""compatibility layer to match the kkroening library.
@TODO: better docstrings"""

from typing import List
from typing import Tuple

from zprp_ffmpeg.base_connector import BaseConnector

from .filter_graph import Filter
from .filter_graph import FilterOption
from .filter_graph import SinkFilter
from .filter_graph import SourceFilter
from .filter_graph import Stream
from .process_connector import ProcessConnector


# this one is unique, creates the Stream object
def input(filename: str) -> Stream:
    source = SourceFilter(filename)
    return Stream().append(source)


def filter(stream_spec: Stream, filter_name: str, *args, **kwargs) -> Stream:
    """Applies a custom filter"""
    options = []
    for arg in args:
        options.append(FilterOption(arg, None))
    for name, value in kwargs.items():
        options.append(FilterOption(name, value))
    stream_spec.append(Filter(filter_name, params=options))
    return stream_spec


def output(stream: Stream, filename: str) -> Stream:
    sink = SinkFilter(filename)
    stream.append(sink)
    return stream


def global_args(stream: Stream, *args) -> Stream:
    new_args: List[str] = []
    for arg in args:
        new_args.append(str(arg))
    stream.global_options = new_args
    return stream


def get_args(stream: Stream, overwrite_output: bool = False) -> List[str]:
    """Build command-line arguments to be passed to ffmpeg."""
    args = ProcessConnector.compile(stream).split()
    if overwrite_output:
        args += ["-y"]
    return args


def compile(stream: Stream, cmd: str = "ffmpeg", overwrite_output: bool = False) -> List[str]:
    """Returns command-line for invoking ffmpeg split by space"""
    return [cmd, *get_args(stream, overwrite_output)]


# this api always uses process
def run(stream: Stream, extra_options: str = "") -> Tuple[bytes, bytes]:
    """Returns (stdout,stderr) tuple"""
    return ProcessConnector.run(stream, extra_options).communicate()


# this api always uses process
def run_async(stream: Stream) -> BaseConnector:
    """Returns handle to a process. Can raise an exception if script tries to terminate before ffmpeg is done."""
    return ProcessConnector.run(stream)


def overwrite_output(stream: Stream) -> Stream:
    stream.global_options.append("-y")
    return stream
