from dataclasses import dataclass
from icecream import ic
from loguru import logger
from pathlib import Path
from typing import Optional, Any
import pandas as pd
import sys
import tomli  # Python3.9対応のためtomliを使う

# import tomllib  # TODO: いずれtomllibに置き換える
from pydantic import BaseModel

ic.configureOutput(prefix=f"{__name__}: ")


@dataclass
class RunData:
    """
    ランの設定をまとめる用のクラス

    :Parameters:
    - run_id(int): ラン番号
    - read_from(str): 入力ディレクトリ名
    - srcf(str): 入力ファイル（の形式）
    - interval(int): サンプリング間隔（秒）。デフォルトは ``600`` （10分）
    - datetime_offset(int): 測定機器の時刻と実時刻の時間差（秒）。デフォルトは0秒
    - description(str): ランの簡単な説明。詳しい説明は別に用意したGoogleスプレッドシートに書き込む
    - skip(bool): 除外する場合は ``True`` にする。デフォルトは ``False``
    - nfiles(int): 読み込んだファイルの数。デフォルトは ``0``
    - raw2gz(str): リサンプルせず ``.csv.gz`` として書き出すァイル名。ファイル名を指定しない場合（ ``""`` or ``None`` ）は、ファイルに書き出さない
    - raw2csv(str): リサンプルして ``.csv`` として書き出すファイル名。ファイル名を指定しない場合（ ``""`` or ``None`` ）は、ファイルに書き出さない

    :Returns:
    - run(RunData): ランデータ

    """

    run_id: int
    description: str = ""
    read_from: str = ""
    srcf: str = "*.csv"
    interval: int = 600
    datetime_offset: int = 0
    skip: bool = False
    nfiles: int = 0
    raw2gz: str = ""
    raw2csv: str = ""
    query: str = ""

    def __post_init__(self) -> None:
        self.name = f"Run{self.run_id}"
        self.fnames = self.get_fnames()
        self.nfiles = len(self.fnames)

    def get_fnames(self) -> list[Path]:
        """該当するランのファイル名（ ``pathlib.Path`` ）の一覧を取得する

        :Returns:
        - fnames(list[Path]): ファイル名（Pathオブジェクト）のリスト

        :Notes:
        - 設定ファイルの ``srcd`` / ``srcf`` から該当するファイルの一覧を取得する
        - ``srcd`` が存在しない場合は終了する
        """

        read_from = Path(self.read_from).expanduser()
        srcf = self.srcf

        if not read_from.exists():
            error = f"No directory found : {read_from}"
            logger.error(error)
            sys.exit()

        fnames = sorted(read_from.glob(srcf))
        return fnames

    def _load_gzip(self) -> Optional[pd.DataFrame]:
        """gzipで保存したデータを読み込む

        ``raw2gz``で指定したファイル名をデータフレームとして読み込む。
        ファイルが存在しない場合は終了する。

        :Returns:
        - data(pd.DataFrame | None): データフレーム
        """
        p = Path(self.raw2gz)
        if p.exists():
            data = pd.read_csv(self.raw2gz, parse_dates=["time"])
            return data
        else:
            error = f"File not found. {p}"
            logger.error(error)
            sys.exit()

    def _load_csv(self) -> Optional[pd.DataFrame]:
        """csvで保存したデータを読み込む

        ``raw2csv``で指定したファイル名をデータフレームとして読み込む。
        ファイルが存在しない場合は終了する。

        :Returns:
        - data(pd.DataFrame | None) : データフレーム
        """
        p = Path(self.raw2csv)
        if p.exists():
            data = pd.read_csv(self.raw2csv, parse_dates=["time"])
            return data
        else:
            error = f"File not found. {p}"
            logger.error(error)
            sys.exit()

    def load_data(self, kind: str) -> Optional[pd.DataFrame]:
        """保存形式（"csv" or "gzip"）を指定してデータを読み込む

        :Parameters:
        - kind(str): 保存したデータの形式（"csv" or "gzip")

        :Returns:
        - data(pd.DataFrame): データフレーム
        """
        if kind == "csv":
            return self._load_csv()
        elif kind == "gzip":
            return self._load_gzip()
        else:
            fmt = ["csv", "gzip"]
            error = f"Wrong file type : {kind}. Choose from {fmt}."
            logger.error(error)
            sys.exit()


@dataclass
class Config:
    """設定ファイル用のクラス

    :Returns:
    - config(Config): 設定
    """

    fname: str = "config.toml"

    def __post_init__(self) -> None:
        """
        - ``self.config``
        - ``self.rules``
        - ``self.runs``
        """
        self.config = self.load_config()
        self.rules = self.get_rules()
        self.runs = self.get_runs()
        self.labels = self.get_labels()

    def load_config(self) -> dict:
        """設定ファイルを読み込む

        :Returns:
        - config(dict) : 設定

        :Notes:
        - デフォルトの設定ファイル名は `config.toml`
        - 設定ファイルの名前は変更することができる
        - 設定ファイルが見つからない場合は、エラーを表示してスキップ（早期リターン）する
        - 設定ファイルは辞書型で読み込む
        """
        p = Path(self.fname)

        if not p.exists():
            error = f"No file found : {p}"
            logger.error(error)
            sys.exit()

        with p.open("rb") as f:
            config = tomli.load(f)
        return config

    def get_rules(self) -> dict:
        """イベント条件に関する設定を取得する

        :Returns:
        - rules(dict): {イベント名 : イベント条件}

        :Notes:
        - 設定ファイルの ``[rules]`` セクションの内容を取得する
        - ``条件名 = 条件式`` の辞書型（map型）で定義されている

        """
        rules = self.config.get("rules")
        return rules  # type: ignore

    def get_labels(self) -> Optional[dict]:
        """カラム名を取得する

        ``[labels]`` のセクションに、カラム名に対応した日本語を記述する

        """
        labels = self.config.get("labels")
        return labels

    def get_run(self, run_id: int) -> RunData:
        """ラン番号を指定してラン情報を取得する"""
        for run in self.runs:
            if run.run_id == run_id:
                return run
        msg = f"Run #{run_id} is out of range. Add to config."
        logger.error(msg)
        sys.exit()

    def get_runs(self) -> list[RunData]:
        """ランに関係する設定を取得する

        :Returns:
        - runs(list[RunData]): ランごとに設定をまとめたリスト

        :Notes:
        - 設定ファイルの ``[[rawdata]]`` セクションの内容を ``RunData`` クラスにまとめる
        - 除外するランがある場合は ``skip = true`` を設定する
        """
        runs = []
        rundata = self.config["rundata"]
        for data in rundata:
            if data.get("skip") is None:
                run = data.get("run")
                error = f"Run{run} : No configuration found for 'skip'"
                logger.error(error)
                sys.exit()

            if not data.get("skip"):
                _data = RunData(
                    run_id=data["run"],
                    read_from=data["read_from"],
                    srcf=data["srcf"],
                    interval=data["interval"],
                    datetime_offset=data.get("datetime_offset", 0),
                    description=data["desc"],
                    skip=data["skip"],
                    raw2gz=data.get("raw2gz"),
                    raw2csv=data.get("raw2csv"),
                    query=data.get("query"),
                )
                runs.append(_data)
        return runs


@dataclass
class Daq:
    "Configuration of DAQ"

    saved: str = "."
    prefix: str = "data"
    suffix: str = ".csv"
    skip: int = 10
    max_rows: int = 10000
    max_files: int = 100
    quiet: bool = False
    append: bool = False
    device: str = "/dev/ttyUSB0"
    baudrate: int = 115200
    timeout: int = 1000
    fname_logs: str = "threshold_logs.csv"
    fname_scan: str = "threshold_scan.csv"

    def load_toml(self, fname: str) -> None:
        "Load DAQ configuration from TOML"
        p = Path(fname)
        with p.open("rb") as f:
            _config = tomli.load(f)

        # logger.debug(_config)
        self.saved = _config.get("saved", ".")
        self.prefix = _config.get("prefix", "data")
        self.suffix = _config.get("suffix", ".csv")
        self.skip = _config.get("skip", 10)
        self.max_rows = _config.get("max_rows", 10000)
        self.max_files = _config.get("max_files", 100)
        self.quiet = _config.get("quiet", False)
        self.append = _config.get("append", False)
        self.device = _config.get("device", "/dev/ttyUSB0")
        self.baudrate = _config.get("baudrate", 115200)
        self.timeout = _config.get("timeout", 1000)
        self.fname_logs = _config.get("fname_logs", "threshold_logs.csv")
        self.fname_scan = _config.get("fname_scan", "threshold_scan.csv")


class UserSettings(BaseModel):
    """ユーザー設定用のクラス

    ``read_from`` に指定したファイルからユーザー設定を読み込みます。
    設定ファイルはTOML形式で作成してください。
    その他の形式に対応する予定はいまのところありません。
    また、読み込み時のファイル形式のチェックもしていません。

    :versionadded: `0.12.0`

    :Example:

    ```python
    >>> s = UserSettings("../sandbox/hnw.toml")
    >>> s.settings
    {
        'default': {'saved': '', 'suffix': '.csv', 'skip': 10, 'max_rows': 1000},
        'device': {'port': '/dev/ttyUSB0', 'baudrate': 115200, 'timeout': 100},
        'daq': {'prefix': 'osechi_data', 'max_files': 1000},
        'scan': {'prefix': 'scan_data', 'max_files': 10, 'timeout': 10},
        'threshold': {'logs': {'fname': 'threshold_logs.csv',
        'names': ['time', 'ch', 'vth', 'success']},
        'scan': {'fname': 'threshold_scan.csv',
        'names': ['time', 'duration', 'ch', 'vth', 'events']
    }

    >>> s.sections
    dict_keys(
        ['default', 'device', 'daq', 'scan', 'threshold', 'loguru']
    )
    ```

    """

    load_from: str
    settings: dict = {}
    sections: list = []

    def model_post_init(self, __context: Any) -> None:
        settings = self.load_toml(self.load_from)
        self.settings = settings
        self.sections = list(settings.keys())
        return super().model_post_init(__context)

    def load_toml(self, load_from: str) -> dict:
        """設定をTOMLファイルから読み込んで、辞書型に変換する

        UserSettingsクラスのオブジェクトを生成するときに ``__post_init__``の中で実行している。
        プロダクション環境では、このメソッドをわざわざ実行する必要はありません。

        新しい設定ファイルを作成した場合の内容確認のために使えると思います。

        :Args:
        - load_from(str): ファイル名

        :Returns:
        - settings(dict): ユーザー設定

        ```

        """
        p = Path(load_from)
        with p.open("rb") as f:
            settings = tomli.load(f)
        return settings

    def _get_settings(self, keys: list) -> dict:
        """設定を取得する

        :Example:
        >>> us = UserSettings(load_from="../sandbox/hnw.toml")
        >>> keys = ["default", "device", "scan", "threshold"]
        >>> settings = s._get_settings(keys)
        """
        settings = {}
        for key in keys:
            d = self.settings.get(key)
            if d is None:
                pass
            else:
                settings.update(d)
        return settings

    def get_daq_settings(self) -> dict:
        """DAQに必要な設定を取得する

        :Returns:
        - settings(dict): DAQの設定に必要な項目

        :Example:

        ```python
        >>> us = UserSettings(load_from="../sandbox/hnw.toml")
        >>> settings = us.get_daq_settings()
        >>> settings
        {
            'saved': '',
            'suffix': '.csv',
            'skip': 10,
            'max_rows': 1000,
            'port': '/dev/ttyUSB0',
            'baudrate': 115200,
            'timeout': 100,
            'prefix': 'osechi_data',
            'max_files': 1000
        }
        ```

        """
        keys = ["default", "device", "daq"]
        settings = self._get_settings(keys)
        return settings

    def get_scan_settings(self) -> dict:
        """スレッショルド測定に必要は設定を取得する

        :Returns:
        - settings(dict): スレッショルド測定に必要な項目

        :Example:

        ```python
        >>> us = UserSettings(load_from="../sandbox/hnw.toml")
        >>> settings = us.get_scan_settings()
        >>> settings
        {
            'saved': '',
            'suffix': '.csv',
            'skip': 10,
            'max_rows': 1000,
            'port': '/dev/ttyUSB0',
            'baudrate': 115200,
            'timeout': 10,
            'prefix': 'scan_data',
            'max_files': 10,
            'logs': {'fname': 'threshold_logs.csv', 'names': ['time', 'ch', 'vth', 'success']},
            'scan': {'fname': 'threshold_scan.csv', 'names': ['time', 'duration', 'ch', 'vth', 'events']},
            'fit': {'fname': 'threshold_fit.csv', 'names': ['time', 'ch', '0sigma', '1sigma', '3sigma', '5sigma']}
        }
        ```

        """

        keys = ["default", "device", "scan", "threshold"]
        settings = self._get_settings(keys)
        return settings

    def get_loguru(self, level: str = "DEBUG") -> logger:
        """ロガーを初期化する

        loguruパッケージを使ったロガーを初期化します。
        ``level`` オプションで指定したログレベルで、標準エラー出力（``sys.stderr``）のハンドラーを作成します。

        以下のような ``[loguru]`` セクションを作成することで、ファイル出力のハンドラーを追加できます。
        このハンドラーのログレベルは``DEBUG``、出力形式はJSON形式にハードコードしています。

        ```toml
        [loguru]
        sink = "required"
        format = "required"
        retention = "optional"
        rotation = "optional"
        ```

        :Args:
        - level(str): 標準エラー出力のログレベル

        :Returns:
        - logger(loguru.logger): ロガー

        :Example:

        ```python
        >>> s = UserSettings("../sandbox/hnw.toml")
        >>> logger = s.get_loguru()
        >>> logger.info("ロガーを初期化した")
        ```
        """
        # ロガーの既定値をリセット
        logger.debug("ロガーをリセットする")
        logger.remove()

        # 標準エラー（sys.stderr）出力のハンドラーを追加
        logger.add(
            sys.stderr,
            format="{time:YYYY-MM-DDTHH:mm:ss} | <level>{level:8}</level> | <level>{message}</level>",
            level=level,
        )
        logger.debug(f"標準エラー出力のハンドラーを追加した（{level=}）")

        # ファイル出力のハンドラーを追加
        section = self.settings.get("loguru")

        if section is None:
            return logger

        # ファイルから読み込んだ値を設定
        logger.add(
            sink=section.get("sink"),
            format=section.get("format"),
            level="DEBUG",
            retention=section.get("retention"),
            rotation=section.get("rotation"),
            serialize=True,
        )
        logger.info("ファイル出力のハンドラーを追加した")
        return logger


if __name__ == "__main__":
    """configモジュールの動作確認用

    $ python3 config.py

    - 設定ファイルの内容がきちんと読み込まれているか確認する
    - Configクラスのインスタンス変数を修正した場合に動作確認する
    - RunDataクラスのインスタンス変数を修正した場合に動作確認する
    """

    c = Config("../sandbox/config.toml")
    ic(c.fname)
    ic(type(c.rules))
    # ic(c.runs)
    # for run in c.runs:
    #     ic(run.name)
    #     ic(run.runid)
    #     ic(run.fnames)
