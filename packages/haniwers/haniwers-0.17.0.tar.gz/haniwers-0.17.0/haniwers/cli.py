import platform
import sys
from pathlib import Path
from platformdirs import PlatformDirs
import pandas as pd
import pendulum
import typer
from loguru import logger

from . import __version__


def setup_logger(level="INFO") -> Path:
    """ロガーの設定"""

    format_short = (" | ").join(
        ["{time:YYYY-MM-DDTHH:mm:ss}", "<level>{level:8}</level>", "<level>{message}</level>"]
    )
    format_long = (" | ").join(
        [
            "{time:YYYY-MM-DDTHH:mm:ss}",
            "<level>{level:8}</level>",
            "<cyan>{name}.{function}:{line}</cyan>",
            "<level>{message}</level>",
        ]
    )

    # ロガーをリセット
    logger.remove()

    # stderr用
    if level in ["DEBUG"]:
        logger.add(
            sys.stderr,
            format=format_long,
            level=level,
        )
    else:
        logger.add(
            sys.stderr,
            format=format_short,
            level=level,
        )

    # ファイル出力用
    p = PlatformDirs(appname="haniwers", version=__version__)
    fname = p.user_log_path / "haniwers_log.json"
    logger.add(
        sink=fname,
        format=format_long,
        level="DEBUG",
        serialize=True,
        retention="10 days",
        rotation="1 MB",
    )
    return fname


app = typer.Typer()


@app.command()
def version(env: bool = False, log_level: str = "INFO"):
    """Show version."""

    fname = setup_logger(level=log_level)

    msg = f"haniwers {__version__}"
    print(msg)
    logger.debug(msg)

    if env:
        msg = f"Python: {platform.python_version()}"
        print(msg)
        logger.debug(msg)

        msg = f"System: {platform.system()}"
        print(msg)
        logger.debug(msg)

        msg = f"OS: {platform.platform()}"
        print(msg)
        logger.debug(msg)

        msg = f"Logs: {fname}"
        print(msg)
        logger.debug(msg)

        print("\n🤖 Please use 'poetry env info' to see more details.\n")

    return


@app.command()
def raw2tmp(
    read_from: str,
    search_pattern: str = "*.csv",
    interval: int = 600,
    offset: int = 0,
    tz: str = "UTC+09:00",
    log_level: str = "INFO",
) -> None:
    """Parse raw_data into CSV format. Should be used temporarily for quick analysis.

    宇宙線を測定したデータをその場で確認するために、生データを変換するための簡易コマンドです。
    必要最低限のオプションしか変更できないようになっています。
    出力ファイル名（``tmp_raw2tmp.csv``）は固定で、変更できません。
    きちんとしたデータ解析には ``haniwers run2csv`` を使って変換してください。

    :Args:
    - read_from (str): 測定データがあるディレクトリ名
    - search_pattern (str, optional): 検索パターン. Defaults to "*.csv".
    - interval (int, optional): リサンプルの間隔. Defaults to 600.
    - offset (int, optional): 測定時刻のオフセット. Defaults to 0.
    - tz (str, optional): 測定時刻のタイムゾーン. Defaults to "UTC+09:00".
    """
    from .preprocess import get_fnames, raw2csv

    setup_logger(level=log_level)

    logger.info(f"Read data from {read_from}")
    fnames = get_fnames(read_from, search_pattern)
    gzip, csv = raw2csv(fnames, interval, offset, tz)
    logger.debug(f"raw2gz = {len(gzip)}")
    logger.debug(f"raw2csv = {len(csv)}")

    fname = "tmp_raw2tmp.csv.gz"
    gzip.to_csv(fname, index=False, compression="gzip")
    logger.info(f"Save data to: {fname} ({len(gzip)} rows).")

    fname = "tmp_raw2tmp.csv"
    csv.to_csv(fname, index=False)
    logger.info(f"Save data to: {fname} ({len(csv)} rows).")


@app.command()
def run2csv(
    runid: int, save: bool = False, load_from: str = "config.toml", log_level: str = "INFO"
) -> None:
    """Parse raw_data into CSV format. Specify RunID.

    :Args:
    - runid (int): ラン番号
    - save (bool, optional): 保存ファイル名（CSV形式）. Defaults to False.
    - load_from (str, optional): RunDataの設定ファイル. Defaults to "config.toml".
    """
    from .config import Config
    from .preprocess import run2csv

    setup_logger(level="INFO")
    c = Config(load_from)
    msg = f"Load config from: {load_from}."
    logger.info(msg)

    msg = f"Get RunData: {runid}."
    logger.info(msg)

    run = c.get_run(runid)
    logger.info(f"description: {run.description}")
    logger.info(f"read_from: {run.read_from}")
    logger.debug(f"srcf: {run.srcf}")

    gzip, csv = run2csv(run)
    if save:
        fname = run.raw2gz
        gzip.to_csv(fname, index=False, compression="gzip")
        logger.info(f"Save data to: {fname} ({len(gzip)} rows).")
        fname = run.raw2csv
        csv.to_csv(fname, index=False)
        logger.info(f"Save data to: {fname} ({len(csv)} rows).")
    else:
        logger.warning("No data saved. Add --save to save data.")
        logger.debug(f"gzip: {len(gzip)}.")
        logger.debug(f"csv:  {len(csv)}.")


@app.command()
def ports(log_level: str = "INFO") -> None:
    """Search available ports and show device names.

    :Note:
    - Linuxの場合: `/dev/ttyUSB0`
    - macOSの場合: `/dev/cu.usbserial-*` （CP2102N USB to UART Bridge Controller）
    - Windowsの場合: `COM3`
    """

    setup_logger(level=log_level)

    from serial.tools import list_ports

    ports = list_ports.comports()
    n = len(ports)

    if n == 0:
        logger.warning("No ports found")
        return

    logger.info(f"Found {n} ports")

    for i, port in enumerate(ports):
        logger.info(f"Port{i}: {port}")

        logger.debug(f"{port.device=}")
        logger.debug(f"{port.name=}")
        logger.debug(f"{port.description=}")
        logger.debug(f"{port.usb_description()=}")
        logger.debug(f"{port.hwid=}")
        logger.debug(f"{port.usb_info()=}")
        logger.debug(f"{port.pid=}")
        logger.debug(f"{port.vid=}")
        logger.debug(f"{port.interface=}")
        logger.debug(f"{port.manufacturer=}")
        logger.debug(f"{port.product=}")
        logger.debug(f"{port.serial_number=}")

    for port in ports:
        if "UART" in port.description:
            logger.info(f"Please use '{port.device}' as your device path")


@app.command()
def vth(
    ch: int = 0,
    vth: int = 0,
    max_retry: int = 3,
    load_from: str = "daq.toml",
    log_level: str = "INFO",
) -> None:
    """Set threshold to each channel. 1step = 4mV.

    OSECHIの各チャンネルにスレッショルドを設定します。
    カレントディレクトリにある ``thresholds_latest.csv`` を参考に、
    スレッショルド値の最良推定値を設定します。
    1step = 4mVに相当します。

    原因がまだわかってないですが、スレッショルドの書き込みに失敗することがあります。
    その場合は、書き込みに成功するまで``max_retry``回リトライします。デフォルトは3回です。

    :Args:
    - ch (int, optional): チャンネル番号. Defaults to 0 (=all).
    - vth (int, optional): スレッショルド値. Defaults to 0 (=all).
    - max_retry (int, optional): スレッショルドの書き込みに失敗したときにリトライする回数. Defaults to 3.
    - load_from (str, optional): 設定ファイル. Defaults to "daq.toml".
    """

    from .config import Daq
    from .daq import set_vth_retry

    setup_logger(level=log_level)

    daq = Daq()
    daq.load_toml(load_from)

    now = pendulum.now().format("YYYYMMDD")
    daq.saved = str(Path(daq.saved) / now)

    # 個別のチャンネルにスレッショルドを設定する
    if ch in range(1, 4) and vth > 0:
        logger.debug(f"Set threshold to each channel: {ch} -> {vth}")
        set_vth_retry(daq, ch, vth, max_retry)
        return

    # 引数を指定しない場合は
    # すべてのチャンネルに規定のスレッショルドを設定する
    if ch == 0 and vth == 0:
        # スレッショルド値をファイルから読み込む
        fname = Path("thresholds_latest.csv")
        if not fname.exists():
            logger.error(f"No file found. Please create {fname}")
            return

        names = ["ch", "3sigma"]
        thresholds = pd.read_csv(fname)[names]

        for _, row in thresholds.iterrows():
            ch = int(row["ch"])
            vth = int(row["3sigma"])
            logger.debug(f"Set threshold to channels: {ch} -> {vth}")
            set_vth_retry(daq, ch, vth, max_retry)
        return

    # オプション指定が間違っている
    logger.error("Invalid arguments")
    return


@app.command()
def scan(
    ch: int = 0,
    duration: int = 10,
    step: int = 1,
    vmin: int = 250,
    vmax: int = 311,
    quiet: bool = False,
    load_from="scan.toml",
    log_level: str = "INFO",
) -> None:
    """スレッショルド曲線を測定する

    :Args:
    - ch (int, optional): チャンネル番号. Defaults to 0.
    - duration (int, optional): 1点あたりの測定時間（秒）. Defaults to 10.
    - step (int, optional): 測定間隔. Defaults to 1.
    - vmin (int, optional): 測定範囲（最小値）. Defaults to 250.
    - vmax (int, optional): 測定範囲（最大値）. Defaults to 311.
    - quiet (bool, optional): _description_. Defaults to False.
    - load_from (str, optional): 設定ファイル. Defaults to "scan.toml".
    """
    from .config import Daq
    from .threshold import scan_thresholds

    setup_logger(level=log_level)
    daq = Daq()
    daq.load_toml(load_from)
    daq.quiet = quiet

    now = pendulum.now().format("YYYYMMDD")
    daq.saved = str(Path(daq.saved) / now)

    if ch == 0:
        channels = [1, 2, 3]
    else:
        channels = [ch]

    thresholds = list(range(vmin, vmax, step))

    for ch in channels:
        msg = f"Running threshold scan on ch{ch}."
        logger.info(msg)
        scan_thresholds(daq, duration, ch, thresholds)

    return


@app.command()
def daq(
    quiet: bool = False,
    load_from: str = "daq.toml",
    log_level: str = "INFO",
) -> None:
    """Start DAQ. Set up with daq.toml.

    :Args:
    - quiet (bool, optional): quiet mode. Defaults to False.
    - load_from (str, optional): 設定ファイル. Defaults to "daq.toml".
    """
    from .config import Daq
    from .daq import run, open_serial_connection

    # ログレベルを設定
    setup_logger(level=log_level)

    # DAQの初期設定
    args = Daq()
    args.load_toml(load_from)
    args.quiet = quiet

    # データの保存先をymdに変更
    now = pendulum.now().format("YYYYMMDD")
    args.saved = str(Path(args.saved) / now)

    with open_serial_connection(args) as port:
        run(port, args)

    return


@app.command()
def mock_daq(quiet: bool = False, load_from: str = "daq.toml", log_level: str = "DEBUG"):
    from unittest.mock import MagicMock, patch
    from .config import Daq
    from .mimic import FakeEvent
    from .daq import run
    import serial

    # ログレベルを設定
    setup_logger(level=log_level)
    logger.debug("mock-daq")

    # DAQの初期設定
    args = Daq()
    args.load_toml(load_from)
    args.quiet = quiet

    # データの保存先をymdに変更
    now = pendulum.now().format("YYYYMMDD")
    args.saved = str(Path(args.saved) / now)
    args.max_rows = 10
    args.max_files = 5
    logger.debug(args)

    # シリアル通信をモック
    mock_port = MagicMock()
    mock_port.readline().decode.return_value = FakeEvent().to_mock_string()
    mock_port.name.return_value = "mock"

    with patch("serial.Serial", return_value=mock_port):
        with serial.Serial() as port:
            logger.debug(f"Port opened: {port.name}")
            run(port, args)
    logger.debug(f"Port closed: {port.name}")


@app.command()
def fit(
    read_from: str,
    search_pattern: str = "threshold_scan.csv",
    ch: int = 0,
    log_level: str = "INFO",
):
    """Get threshold recommendations.

    スレッショルドを測定したデータから、誤差関数を使って閾値の推定値を計算します。
    チャンネル番号を指定できます。
    デフォルトはすべてのチャンネルの推定値を計算します。
    計算するたびにその結果は``thresholds_history.csv``に追記されます。
    また、最新のフィット結果は``thresholds_latest.csv``に保存されます。
    このファイルを使ってスレッショルドを設定できるようになっています。

    :Args:
    - read_from (str): スレッショルド測定データがあるディレクトリ名を指定してください
    - search_pattern (str, optional): スレッショルド測定データのファイル名を変更できます。Defaults to "threshold_scan.csv".
    - ch (int, optional): チャンネル番号を変更できます。Defaults to 0.
    """
    import pandas as pd

    from .preprocess import get_fnames
    from .threshold import fit_thresholds

    setup_logger(level=log_level)

    logger.info(f"Read data from {read_from}")
    fnames = get_fnames(read_from, search_pattern)

    # ファイルが見つからない時は、なにもしない
    if len(fnames) == 0:
        logger.error("No files found.")
        return

    logger.debug(fnames)

    # チャンネル番号が範囲外のときは、なにもしない
    if ch > 3:
        logger.error(f"Out of range!: {ch}")
        return

    channels = [ch]
    if ch == 0:
        channels = [1, 2, 3]

    names = ["time", "duration", "ch", "vth", "events", "tmp", "atm", "hmd"]
    data = pd.read_csv(fnames[0], names=names, parse_dates=["time"])
    thresholds = fit_thresholds(data, channels)

    # 実行した時刻を上書きする
    now = pendulum.now()
    thresholds["timestamp"] = now
    print(thresholds)

    fname = "thresholds_history.csv"
    thresholds.to_csv(fname, index=False, mode="a", header=None)
    logger.info(f"Saved to {fname}")
    fname = "thresholds_latest.csv"
    thresholds.to_csv(fname, index=False)
    logger.info(f"Saved to {fname}")

    return


if __name__ == "__main__":
    app()
