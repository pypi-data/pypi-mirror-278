import pickle
from ast import literal_eval
from datetime import datetime
from importlib import util, reload
from os import environ, mkdir, symlink, scandir, remove
from os import listdir
from pathlib import Path
from re import finditer
from sys import argv as _argv
from time import time
from urllib.parse import unquote

from config import color_theme
from . import rconfig, plugin
from .rconfig import *

argv = _argv[1:]


def _path(*elem):
    return str("/").join(elem)


_file_rc = "rconfig.py"
_file_cc = "colors.py"
_file_plugin = "plugin.py"
_inactive_prefix = "#"
_file_journal = "journal.pkl"
_file_history = "history.pkl"
_file_position_colors = "position-colors.pkl"
_file_column_state = "column-state.pkl"
_file_clean_time = "cleaner.timestamp"
_folder_trash = "cleaner.trash"
_folder_file_clones = "clones"
_folder_profile_assets = "files"
_file_rc_css = ".rc.css"
_file_rc_js = ".rc.js"
_file_favicon = ".favicon.ico"
_userhome = str(Path.home())
_default_install_root = _userhome
_proj_root = str(Path(__file__).parent.parent)
_proj_things = _path(_proj_root, "things")
_env = _path(_proj_root, "__env__")
_profiles_home_folder = "Trading-Journals.srtj"
_profile_prefix = "%"
_profiles_home_path_file = _path(_userhome, ".srtj")
_demo_env = _path(_proj_root, "__env__", "#demo")
_demo_profiles_home_folder = "#demo"


def _make_profile(profile_path: str, force: bool = False):
    print(f"[ PROFILE ]/make:", profile_path)
    try:
        mkdir(profile_path)
    except FileExistsError:
        if not force:
            raise

    profile_rc = _path(profile_path, _inactive_prefix + _file_rc)
    with open(_path(_env, _file_rc)) as _if, open(profile_rc, "w") as _of:
        _of.write(_if.read())

    profile_cc = _path(profile_path, _inactive_prefix + _file_cc)
    with open(_path(_env, _file_cc)) as _if, open(profile_cc, "w") as _of:
        _of.write(_if.read())

    profile_plugin = _path(profile_path, _inactive_prefix + _file_plugin)
    with open(_path(_env, _file_plugin)) as _if, open(profile_plugin, "w") as _of:
        _of.write(_if.read())

    try:
        mkdir(_path(profile_path, _folder_profile_assets))
    except FileExistsError:
        pass
    try:
        mkdir(_path(profile_path, _folder_profile_assets, _folder_file_clones))
    except FileExistsError:
        pass
    try:
        mkdir(_path(profile_path, _folder_trash))
    except FileExistsError:
        pass

    with open(_path(profile_path, _file_clean_time), "w") as f:
        f.write(str(int(time())))

    for file in scandir(_proj_things):
        try:
            symlink(file.path, _path(profile_path, _folder_profile_assets, file.name))
        except FileExistsError:
            pass
    return profile_path


def _demo_init():
    print(f"[ DEMO ]/init:", "@", __demo_home__)

    _make_profile(__demo_home__, force=True)

    demo_rc = _path(__demo_home__, _file_rc)
    with open(_path(_demo_env, _file_rc)) as _if, open(demo_rc, "w") as _of:
        _of.write(_if.read())

    demo_plugin = _path(__demo_home__, _file_plugin)
    with open(_path(_demo_env, _file_plugin)) as _if, open(demo_plugin, "w") as _of:
        _of.write(_if.read())

    demo_journal = _path(__demo_home__, _file_journal)
    with open(_path(_demo_env, _file_journal), "rb") as _if, open(demo_journal, "wb") as _of:
        _of.write(_if.read())

    demo_file_clones = _path(__demo_home__, _folder_profile_assets, _folder_file_clones)
    for e in scandir(_path(_demo_env, _folder_profile_assets, _folder_file_clones)):
        with open(e.path, "rb") as _if, open(_path(demo_file_clones, e.name), "wb") as _of:
            _of.write(_if.read())


def _install(profiles_root: str):
    global __profiles_home__
    __profiles_home__ = _path(profiles_root, _profiles_home_folder)
    print("[ INSTALL ] @", __profiles_home__)
    _make_profile(__profiles_home__)

    with open(_profiles_home_path_file, "w") as f:
        f.write(__profiles_home__)

    _demo_init()


def _autoclean(journal_data):
    t = int(time())
    __file_clean_time = _path(__profile_folder__, _file_clean_time)
    print(f"[ CLEAN ]/load", __file_clean_time)
    with open(__file_clean_time) as __f:
        clean_time = int(__f.read())
    remain = (clean_time + autocleanIntervalS) - t
    print(f"[ CLEAN ]/load ->", f"{remain=}s")
    if remain <= 0:
        with open(__file_clean_time, "w") as __f:
            __f.write(str(t))

        journal_datas = [journal_data]

        def scan_for_globals(attr_name, default_is_glob):
            gval = globals()[attr_name]
            print(f"[ CLEAN ]/scan_for_globals:", attr_name, "is", repr(gval))
            if gval == "global":
                for profile in scandir(__profiles_home__):
                    if profile.name.startswith(_profile_prefix):
                        spec = util.spec_from_file_location("", _path(profile.path, _file_rc))
                        _rc = util.module_from_spec(spec)
                        spec.loader.exec_module(_rc)
                        try:
                            is_glob = getattr(_rc, attr_name) == "global"
                        except AttributeError:
                            is_glob = default_is_glob
                        if is_glob:
                            print(f"[ CLEAN ]/scan_for_globals/add:", profile.name)
                            with open(_path(__profiles_home__, profile.name), "rb") as f:
                                journal_datas.append(pickle.load(f))

        if fileclones := listdir(FILE_CLONES):
            scan_for_globals(
                f"{noteFileDropCloner=}".split("=")[0],
                noteFileDropCloner == "global"
            )
            for data in journal_datas:
                for row in data:
                    if note := row.get("Note"):
                        for m in finditer("(\\[[^\\]*]\\])(\\([^\\)]+\\))", note):
                            link = unquote(m.group(2))
                            try:
                                fileclones.remove(link)
                            except ValueError:
                                if not fileclones:
                                    break

            if noteFileDropCloner == "global":
                trash = _path(__profiles_home__, _folder_trash)
            else:
                trash = _path(__profile_folder__, _folder_trash)

            print(f"[ CLEAN ]/flush trash @", trash)
            for e in listdir(trash):
                remove(_path(trash, e))

            if noteFileDropClonerFlushTrashing:
                print(f"[ CLEAN ]/trashing:", fileclones)
                for fileclone in fileclones:
                    with open(path := _path(FILE_CLONES, fileclone), "rb") as _if:
                        with open(_path(trash, fileclone), "wb") as _of:
                            _of.write(_if.read())
                    remove(path)
            else:
                print(f"[ CLEAN ]/flushing:", fileclones)
                for fileclone in fileclones:
                    remove(_path(FILE_CLONES, fileclone))

        journal_datas = [journal_data]
        scan_for_globals(
            f"{statisticsUsePositionColorCache=}".split("=")[0],
            statisticsUsePositionColorCache == "global"
        )
        ids = set()
        id_fields = ("Name", "Symbol", "Type", "Sector", "Category")
        for data in journal_datas:
            for row in data:
                for field in id_fields:
                    ids.add(row.get(field))
        with open(COLOR_CACHE, "rb") as f:
            _color_cache = pickle.load(f)
        color_cache = dict()
        for _id in ids:
            try:
                color_cache[_id] = _color_cache[_id]
            except KeyError:
                pass
        with open(COLOR_CACHE, "wb") as f:
            pickle.dump(color_cache, f)


PROFILE: str = ""
__profile_folder__: str = ""

_globals = globals()


def _load_profile(profile):
    global __profile_folder__, PROFILE
    if profile:
        PROFILE = profile
        __profile_folder__ = _path(__profiles_home__, _profile_prefix + profile)
        print(f"[ PROFILE ]/load:", profile, "@", __profile_folder__)
    else:
        __profile_folder__ = __profiles_home__
    if not Path(__profile_folder__).exists():
        _make_profile(__profile_folder__)
    if (p := Path(_path(__profile_folder__, _file_rc))).exists():
        print(f"[ PROFILE ]/load:", p)
        spec = util.spec_from_file_location("rc", p)
        _rc = util.module_from_spec(spec)
        spec.loader.exec_module(_rc)
        for attr in _rc.__dir__():
            if attr.startswith("_"):
                continue
            _globals[attr] = getattr(_rc, attr)
    if (p := Path(_path(__profile_folder__, _file_plugin))).exists():
        print(f"[ PROFILE ]/load:", p)
        spec = util.spec_from_file_location("plugin", p)
        _plugin = util.module_from_spec(spec)
        spec.loader.exec_module(_plugin)
        for attr in _plugin.__dir__():
            if attr.startswith("_"):
                continue
            setattr(plugin, attr, getattr(_plugin, attr))


def _load_colors():
    color_theme._load_theme(colorTheme)
    if (p := Path(_path(__profile_folder__, _file_cc))).exists():
        print(f"[ PROFILE ]/load:", p)
        spec = util.spec_from_file_location("cc", p)
        _cc = util.module_from_spec(spec)
        spec.loader.exec_module(_cc)
        for attr in _cc.__dir__():
            if attr.startswith("_"):
                continue
            setattr(color_theme, attr, getattr(_cc, attr))


def _cmdline():
    if argv:
        if len(argv) == 1:
            _load_profile(argv[0])
        else:
            print(f"[ CMDLINE ]/parse:", argv)
            _config_key = argv.pop(0)
            if _config_key == "/":
                _load_profile(argv.pop(0))
            while argv:
                if _config_key.endswith("]"):
                    _config_key, _idx = _config_key[:-1].split("[")
                    _attr = getattr(rconfig, _config_key)
                    _attr.__setitem__(int(_idx), type(_attr[0])(argv.pop(0)))
                elif (_attrt := type(_attr := getattr(rconfig, _config_key))) is list:
                    _arg = argv.pop(0)
                    if not _arg.startswith("["):
                        raise ValueError(f"{_config_key!r} requires a value of type <list> whose pattern corresponds to [1, 2, ...]. {_arg!r} is received.")
                    while not _arg.endswith("]"):
                        _arg += argv.pop(0)
                    _globals[_config_key] = literal_eval(_arg)
                else:
                    _globals[_config_key] = _attrt(argv.pop(0))
                try:
                    _config_key = argv.pop(0)
                except IndexError:
                    break


try:
    if argv[0] == "install":
        argv.pop(0)
        try:
            _install(argv[0])
            argv.pop(0)
        except IndexError:
            _install(_default_install_root)
except IndexError:
    pass

try:
    with open(_profiles_home_path_file) as _f:
        __profiles_home__ = _f.read()
        if not Path(__profiles_home__).exists():
            raise FileNotFoundError
except FileNotFoundError:
    _install(_default_install_root)

__demo_home__ = _path(__profiles_home__, _demo_profiles_home_folder)

try:
    if argv[0] == "demo":
        argv.pop(0)
        PROFILE = "#demo"
        if argv[0] == "init":
            argv.pop(0)
            _demo_init()
        __profiles_home__ = __demo_home__
except IndexError:
    pass


_load_profile(None)
try:
    _load_profile(environ["SRTJ"])
except KeyError:
    pass
_cmdline()
_load_colors()


DASH_ASSETS = _path(__profile_folder__, "files")
FILE_CLONES = _path(DASH_ASSETS, _folder_profile_assets, _folder_file_clones)
FILE_CLONES_URL = _path(".", "files", _folder_file_clones)

if noteFileDropCloner == "own":
    PROFILE_FILE_CLONES = _path(__profile_folder__, _folder_profile_assets, _folder_file_clones)
else:
    PROFILE_FILE_CLONES = _path(__profiles_home__, _folder_profile_assets, _folder_file_clones)
if statisticsUsePositionColorCache == "own":
    COLOR_CACHE = _path(__profile_folder__, _file_position_colors)
else:
    COLOR_CACHE = _path(__profiles_home__, _file_position_colors)
if columnStateCache == "own":
    COLUMN_CACHE = _path(__profile_folder__, _file_column_state)
else:
    COLUMN_CACHE = _path(__profiles_home__, _file_column_state)

dateFormat = {"ISO 8601": "ydm", "american": "mdy", "international": "dmy"}.get(dateFormat, dateFormat)
timeFormatTransaction, timeFormatHistory, timeFormatDaterange, timeFormatLastCalc = {
    "ydm": ("%y/%d/%m %H:%M", "\u2007\u2007%a. %y/%d/%m %H:%M.%S", "YY/DD/MM", "%y / %d / %m"),
    "mdy": ("%m/%d/%y %H:%M", "\u2007\u2007%a. %m/%d/%y %H:%M.%S", "MM/DD/YY", "%m / %d / %y"),
    "dmy": ("%d/%m/%y %H:%M", "\u2007\u2007%a. %d/%m/%y %H:%M.%S", "DD/MM/YY", "%d / %m / %y"),
}[dateFormat]

with open(_path(DASH_ASSETS, _file_rc_js), "w") as f:
    f.write(
        "// [do not change] this file is created by `rc'\n"
        f"const {gridDefWidthScale=};"
        f"const {gridMinWidthScale=};"
        f"const {gridRow3Height=};"
        f"const {dateFormat=};"
        f"const ccCopy = {bindKeyCodes[0]!r};"
        f"const ccCut = {bindKeyCodes[1]!r};"
        f"const ccPaste = {bindKeyCodes[2]!r};"
        f"const ccCopyRow1 = {bindKeyCodes[3]!r};"
        f"const ccCopyRow2 = {bindKeyCodes[4]!r};"
        f"const ccCopyRow3 = {bindKeyCodes[5]!r};"
        f"const ccAComplete = {bindKeyCodes[6]!r};"
        f"const ccNote = {bindKeyCodes[7]!r};"
        f"const ccNoteBack = {bindKeyCodes[8]!r};"
        f"const ccMark = {bindKeyCodes[9]!r};"
        f"const {noteCellVariableFormatter=};"
        f"const {noteUnifying=};"
        f"const noteLinkDropPattern=/{noteLinkDropPattern}/;"
        f"const notePathDropPattern=/{notePathDropPattern}/;"
    )

if statisticsIdBySymbol:
    statisticsGroupId = "Symbol"
else:
    statisticsGroupId = "Name"

if gridSideSizeInitScale:
    gridSideSizeInitValue = int(gridSideSizeInitScale * 100)
    c2Width = f"{gridSideSizeInitValue}%"
    c1Width = f"{100 - gridSideSizeInitValue}%"
    sideInitBalanceValue = sideInitBalance
    sideInitStatisticValue = int(not sideInitBalance)
else:
    gridSideSizeInitValue = 0
    c2Width = "0%"
    c1Width = "100%"
    sideInitBalanceValue = 0
    sideInitStatisticValue = 0

_colorCache = dict()
if statisticsUsePositionColorCache and statisticsUsePositionColorCache != '0':
    def _dump_color_cache():
        with open(COLOR_CACHE, "wb") as __f:
            pickle.dump(_colorCache, __f)


    try:
        with open(COLOR_CACHE, "rb") as __f:
            _colorCache = pickle.load(__f)
    except FileNotFoundError:
        _dump_color_cache()
else:
    def _dump_color_cache():
        pass

_colorPalette = color_theme.color_palette_positions.copy()


def get_position_color(__key):
    global _colorPalette
    try:
        return _colorCache[__key]
    except KeyError:
        try:
            color = _colorPalette.pop(0)
        except IndexError:
            _colorPalette = color_theme.color_palette_positions.copy()
            color = _colorPalette.pop(0)
        _colorCache[__key] = color
        _dump_color_cache()
        return color


COLUMN_CACHE_DATA: list[dict] | None = None


def dump_column_state(data):
    global COLUMN_CACHE_DATA
    COLUMN_CACHE_DATA = data
    with open(COLUMN_CACHE, "wb") as __f:
        pickle.dump(data, __f)


if columnStateCache := (columnStateCache and columnStateCache != '0'):

    try:
        with open(COLUMN_CACHE, "rb") as __f:
            COLUMN_CACHE_DATA = pickle.load(__f)
    except FileNotFoundError:
        dump_column_state(None)

cellRendererChangeTakeAmount = ({"cellRenderer": "agAnimateShowChangeCellRenderer"} if cellRendererChangeTakeAmount else {})
cellRendererChangeTakeCourse = ({"cellRenderer": "agAnimateShowChangeCellRenderer"} if cellRendererChangeTakeCourse else {})
cellRendererChangePerformance = ({"cellRenderer": "agAnimateShowChangeCellRenderer"} if cellRendererChangePerformance else {})
cellRendererChangeProfit = ({"cellRenderer": "agAnimateShowChangeCellRenderer"} if cellRendererChangeProfit else {})

nStatisticsDrag = len(set(statisticsPerformanceOrder))

if useDefaultAltColors:
    color_theme.cell_negvalue = color_theme.alt_neg
    color_theme.cell_posvalue = color_theme.alt_pos
    color_theme.rating_scale = color_theme.alt_rating_scale


with open(_path(DASH_ASSETS, _file_rc_css), "w") as f:
    cont = "/* [do not change] this file is created by `rc' */\n"
    cont += """
/* agGrid Input color > */
.%s input[class^=ag-] {
  color: %s !important;
}
/* < agGrid Input color */
""" % (color_theme.table_theme, color_theme.table_fg_main)
    if useDefaultAltColors:
        cont += """
/* agGrid alt colors > */
.ag-alt-colors {
    --ag-value-change-delta-down-color: %s !important;
    --ag-value-change-delta-up-color: %s !important;
}
/* < agGrid alt colors */
""" % (color_theme.alt_neg, color_theme.alt_pos)
    cont += """
/* dataTable hover bg > */
.dt-table-container__row-1 .cell-table tbody tr:hover td {
  background-color: %s !important;
}
/* < dataTable hover bg */
""" % color_theme.sheet_hover_bg
    cont += """
/* notepaper > */
.notepaper a {
  color: %s !important;
}
/* < notepaper */
""" % color_theme.notepaper_link
    cont += """
/* note editor > */
.CodeMirror {
  height: 100%%;
  width: 100%%;
  background-color: %s;
}
.CodeMirror-gutters {
  background-color: %s;
}
/* < note editor */
""" % (
        color_theme.notebook_bg + (color_theme.notebook_def_transparency if noteEditorDefaultTransparency else ""),
        color_theme.notebook_gutter_bg + (color_theme.notebook_def_gutter_transparency if noteEditorDefaultTransparency else ""),
    )
    if checkboxLongShortStyling and checkboxLongShortStyling != '0':
        cont += """
/* Short > */
.ag-checkbox-input-wrapper.ag-indeterminate::before {
  border-width: 0 !important;
}
.ag-checkbox-input-wrapper.ag-indeterminate::after {
  color: transparent !important;
}
.ag-checkbox-input-wrapper.ag-checked::before {
  border: solid %s;
  border-width: 0 3px 3px 0;
  display: inline-block;
  margin: 3px;
  transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
  opacity: 0.5 !important;
}
.ag-checkbox-input-wrapper.ag-checked::after {
  color: transparent !important;
}
.ag-checkbox-input-wrapper::before {
 %s border: solid %s;
  border-width: 0 3px 3px 0;
  display: inline-block;
  margin: 3px;
  transform: rotate(-135deg);
  -webkit-transform: rotate(-135deg);
  opacity: 0.5 !important;
}
.ag-checkbox-input-wrapper::after {
  color: transparent !important;
}
.ag-theme-balham, .ag-theme-balham-dark, .ag-theme-balham-auto-dark {
  --ag-checkbox-border-radius: 10px !important;
  --ag-checkbox-background-color: transparent !important;
}
/* < Short */
""" % (color_theme.cell_negvalue, ("//" if checkboxLongShortStyling == "s" else ""), color_theme.cell_posvalue)
    cont += """
/* Row Mark > */
.row-mark::before {
  content: "";
  background-color: %s;
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}
/* < Row Mark */
""" % color_theme.row_mark
    f.write(cont)


_idx = 0


def get_footer_live_signal():
    global _idx
    _idx += 1
    if _idx % 2:
        return {"borderTop": "1px solid " + color_theme.footer_sig2}
    else:
        return {"borderTop": "1px solid " + color_theme.footer_sig1}


_d = dict()

if disableFooterLifeSignal:
    def get_footer_live_signal():
        return _d

if strictScopeByBoth:
    scope_by_both = "or+"
else:
    scope_by_both = "or"

JOURNAL_DATA: list[dict] = list()
HISTORY_DATA: dict = dict()
HISTORY_KEYS_X_TIME_REVSORT: list[tuple[int, int]] = list()
LAST_HISTORY_CREATION_TIME: int = 0

JOURNAL = _path(__profile_folder__, _file_journal)
HISTORY = _path(__profile_folder__, _file_history)

pickleProtocol = pickle.HIGHEST_PROTOCOL


def _init_data():
    global JOURNAL_DATA, HISTORY_DATA, HISTORY_KEYS_X_TIME_REVSORT, LAST_HISTORY_CREATION_TIME
    __firstrun = [{"id": 0, "n": 0, "InvestTime": datetime.now().strftime(timeFormatTransaction), "InvestAmount": 1}]
    t = int(time())
    try:
        print("[ INIT ]/journal/load:", JOURNAL)
        with open(JOURNAL, "rb") as __f:
            JOURNAL_DATA = pickle.load(__f)
    except FileNotFoundError:
        print("[ INIT ]/journal/first run:", __firstrun)
        JOURNAL_DATA = __firstrun
        dump_journal(JOURNAL_DATA)
    try:
        print("[ INIT ]/history/load:", HISTORY)
        with open(HISTORY, "rb") as __f:
            HISTORY_DATA = pickle.load(__f)
    except FileNotFoundError:
        print("[ INIT ]/history/first run:", __firstrun)
        HISTORY_DATA = {i: {"time": i, "data": __firstrun} for i in range(nHistorySlots)}

    print("[ INIT ]/plugin/call")
    do_dump = plugin.init_log(JOURNAL_DATA)
    make_hist = plugin.init_history(HISTORY_DATA)

    HISTORY_KEYS_X_TIME_REVSORT = list((k, v["time"]) for k, v in HISTORY_DATA.items())
    HISTORY_KEYS_X_TIME_REVSORT.sort(key=lambda x: x[1], reverse=True)

    def make_history():
        global LAST_HISTORY_CREATION_TIME
        LAST_HISTORY_CREATION_TIME = t
        HISTORY_DATA[HISTORY_KEYS_X_TIME_REVSORT[-1][0]] = {"time": LAST_HISTORY_CREATION_TIME, "data": JOURNAL_DATA}
        with open(HISTORY, "wb") as __f:
            pickle.dump(HISTORY_DATA, __f, pickleProtocol)

    if do_dump:
        print("[ INIT ]/plugin/journal -> dump")
        dump_journal(JOURNAL_DATA)
        make_history()
    elif make_hist:
        print("[ INIT ]/plugin/history -> dump")
        with open(HISTORY, "wb") as __f:
            pickle.dump(HISTORY_DATA, __f, pickleProtocol)
    else:
        newest_backup = HISTORY_DATA[HISTORY_KEYS_X_TIME_REVSORT[0][0]]["data"]

        if len(JOURNAL_DATA) != len(newest_backup):
            print("[ INIT ]/history/n-entries -> create+dump")
            make_history()
            return

        initdata = JOURNAL_DATA.copy()
        initdata.sort(key=lambda x: x["id"])
        newest_backup.sort(key=lambda x: x["id"])
        comp_keys = ("id", "Name", "n", "InvestTime", "InvestAmount", "TakeTime", "TakeAmount", "ITC", "Note")

        for ini, bku in zip(initdata, newest_backup):
            if tuple(ini.get(k) for k in comp_keys) != tuple(bku.get(k) for k in comp_keys):
                print("[ INIT ]/history/cell-contents -> create+dump")
                make_history()
                return

        print("[ INIT ]/history -> no changes")

    LAST_HISTORY_CREATION_TIME = HISTORY_DATA[HISTORY_KEYS_X_TIME_REVSORT[0][0]]["time"]
    
    return JOURNAL_DATA


def dump_journal(data: list[dict]):
    global JOURNAL_DATA
    JOURNAL_DATA = data
    with open(JOURNAL, "wb") as __f:
        pickle.dump(data, __f, pickleProtocol)


if pluginQuickDisable:
    reload(plugin)

_init_data()
_autoclean(JOURNAL_DATA)
