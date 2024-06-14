from importlib.util import find_spec
from pathlib import Path
from pkg_resources import get_distribution, DistributionNotFound

_dist = get_distribution("qchaindym_ta")
try:
    # Normalize case for Windows systems
    here = Path(_dist.location) / __file__
    if not here.exists():
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = "请使用setup.py安装此，或使用 \'pip install qchaindym_ta\'进行安装"

version = __version__ = _dist.version

Imports = {
    "alphaVantage-api": find_spec("alphaVantageAPI") is not None,
    "matplotlib": find_spec("matplotlib") is not None,
    "mplfinance": find_spec("mplfinance") is not None,
    "numba": find_spec("numba") is not None,
    "yaml": find_spec("yaml") is not None,
    "scipy": find_spec("scipy") is not None,
    "sklearn": find_spec("sklearn") is not None,
    "statsmodels": find_spec("statsmodels") is not None,
    "stochastic": find_spec("stochastic") is not None,
    "talib": find_spec("talib") is not None,
    "tqdm": find_spec("tqdm") is not None,
    "vectorbt": find_spec("vectorbt") is not None,
    "yfinance": find_spec("yfinance") is not None,
    "pandas_ta":find_spec("pandas_ta") is not None
}

Category = {
    # Candles
    "candles": [
        "cdl_pattern", "cdl_z", "ha"
    ],
    # Cycles
    "cycles": ["ebsw"],
    # Momentum
    "momentum": [
        "ao", "apo", "bias", "bop", "brar", "cci", "cfo", "cg", "cmo",
        "coppock", "cti", "er", "eri", "fisher", "inertia", "kdj", "kst", "macd",
        "mom", "pgo", "ppo", "psl", "pvo", "qqe", "roc", "rsi", "rsx", "rvgi",
        "slope", "smi", "squeeze", "squeeze_pro", "stc", "stoch", "stochrsi", "td_seq", "trix",
        "tsi", "uo", "willr"
    ],
    # Overlap
    "overlap": [
        "alma", "dema", "ema", "fwma", "hilo", "hl2", "hlc3", "hma", "ichimoku",
        "jma", "kama", "linreg", "mcgd", "midpoint", "midprice", "ohlc4",
        "pwma", "rma", "sinwma", "sma", "ssf", "supertrend", "swma", "t3",
        "tema", "trima", "vidya", "vwap", "vwma", "wcp", "wma", "zlma"
    ],
    # Performance
    "performance": ["log_return", "percent_return"],
    # Statistics
    "statistics": [
        "entropy", "kurtosis", "mad", "median", "quantile", "skew", "stdev",
        "tos_stdevall", "variance", "zscore"
    ],
    # Trend
    "trend": [
        "adx", "amat", "aroon", "chop", "cksp", "decay", "decreasing", "dpo",
        "increasing", "long_run", "psar", "qstick", "short_run", "tsignals",
        "ttm_trend", "vhf", "vortex", "xsignals"
    ],
    # Volatility
    "volatility": [
        "aberration", "accbands", "atr", "bbands", "donchian", "hwc", "kc", "massi",
        "natr", "pdist", "rvi", "thermo", "true_range", "ui"
    ],

    # Volume, "vp" or "Volume Profile" is unique
    "volume": [
        "ad", "adosc", "aobv", "cmf", "efi", "eom", "kvo", "mfi", "nvi", "obv",
        "pvi", "pvol", "pvr", "pvt"
    ],
}

from qchaindym_ta.main import *
