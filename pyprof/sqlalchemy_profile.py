import argparse
import logging
import tempfile
from pathlib import Path

from memory_profiler import profile

from pyprof.entity import Block, Frame, Session

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


@profile
def run(count: int):
    session = Session()
    try:
        for i in range(count):
            frame = Frame(name=f"frame-{i:05}")
            frame.blocks = [Block(name=f"block-{i:05}-{j:05}") for j in range(3)]
            session.add(frame)
        session.commit()
    except Exception as ex:
        logger.exception(ex)
        session.rollback()


@profile
def flush_run(count: int):
    session = Session()
    try:
        for i in range(count):
            frame = Frame(name=f"frame-{i:05}")
            frame.blocks = [Block(name=f"block-{i:05}-{j:05}") for j in range(3)]
            session.add(frame)
            session.flush()
        session.commit()
    except Exception as ex:
        logger.exception(ex)
        session.rollback()


@profile
def del_run(count: int):
    session = Session()
    try:
        for i in range(count):
            frame = Frame(name=f"frame-{i:05}")
            frame.blocks = [Block(name=f"block-{i:05}-{j:05}") for j in range(3)]
            session.add(frame)
            del frame
        session.commit()
    except Exception as ex:
        logger.exception(ex)
        session.rollback()


@profile
def bulk_run(count: int):
    session = Session()
    try:
        for i in range(count):
            if i != 0 and i % 100 == 0:
                session.flush()
            frame = Frame(name=f"frame-{i:05}")
            frame.blocks = [Block(name=f"block-{i:05}-{j:05}") for j in range(3)]
            session.add(frame)
        session.commit()
    except Exception as ex:
        logger.exception(ex)
        session.rollback()


@profile
def attribute_run(count: int):
    class Attr:
        pass

    session = Session()
    try:
        for i in range(count):
            a = Attr()
            if i != 0 and i % 100 == 0:
                session.flush()
            frame = Frame(name=f"frame-{i:05}")
            frame.blocks = [Block(name=f"block-{i:05}-{j:05}") for j in range(3)]
            a.entity = frame
            session.add(frame)
        session.commit()
    except Exception as ex:
        logger.exception(ex)
        session.rollback()


@profile
def with_file_run(count: int):
    class Attr:
        pass

    session = Session()
    try:
        for i in range(count):
            a = Attr()
            a.filename = Path(tempfile.mktemp())
            create_file(a.filename)
            if i != 0 and i % 100 == 0:
                session.flush()
            frame = Frame(name=f"frame-{i:05}")
            frame.blocks = [Block(name=f"block-{i:05}-{j:05}") for j in range(3)]
            a.entity = frame
            session.add(frame)
        session.commit()
    except Exception as ex:
        logger.exception(ex)
        session.rollback()


@profile
def create_file(filename):
    filename = Path(tempfile.mktemp())
    with open(filename, "w") as f:
        f.write("This is test")


if __name__ == "__main__":
    logger.info("delete entities...")
    session = Session()
    frames = session.query(Frame).all()
    for f in frames:
        session.delete(f)
    session.commit()
    session.close()
    logger.info("finish to delete")
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument(
        "--run-type",
        type=str,
        required=True,
        choices=["run", "flush", "del", "bulk", "attr", "file"],
        default="run",
    )
    args = parser.parse_args()
    count = args.count
    run_type = args.run_type

    if run_type == "run":
        logger.info("run...")
        run(count)
    elif run_type == "flush":
        logger.info("flush run...")
        flush_run(count)
    elif run_type == "del":
        logger.info("delete run...")
        del_run(count)
    elif run_type == "bulk":
        logger.info("bulk run...")
        bulk_run(count)
    elif run_type == "attr":
        logger.info("attr run...")
        attribute_run(count)
    elif run_type == "file":
        logger.info("with file run...")
        with_file_run(count)
