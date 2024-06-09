from dash import callback, Output, Input, State, no_update, callback_context

import __env__
import layout

if __env__.columnStateCache:

    @callback(
        Output(layout.tradinglog, "columnState"),
        Output(layout.tradinglog, "columnDefs", allow_duplicate=True),
        Output(layout.init_done_trigger2, "n_clicks", allow_duplicate=True),
        Input(layout.init_done_trigger2, "n_clicks"),
        State(layout.tradinglog, "columnDefs"),
        Input(layout.tradinglog, "dashGridOptions"),
        Input(layout.tradinglog, "columnState"),
        config_prevent_initial_callbacks=True
    )
    def call(n, col_defs, grid_opts, _state):
        if callback_context.triggered_id == layout.init_done_trigger2.id:
            n += 1
            if __env__.COLUMN_CACHE_DATA:
                widths = {c["colId"]: c["width"] for c in __env__.COLUMN_CACHE_DATA}
                for _col_def in col_defs:
                    try:
                        _col_def["width"] = widths[_col_def["field"]]
                    except KeyError:
                        try:
                            for child in _col_def["children"]:
                                child["width"] = widths[child["field"]]
                        except KeyError:
                            pass
                return __env__.COLUMN_CACHE_DATA, col_defs, n
            else:
                return no_update, no_update, n
        else:
            if n == 2:
                __env__.dump_column_state(_state)
            return __env__.COLUMN_CACHE_DATA, no_update, no_update


@callback(
    Output(layout.tradinglog, "columnDefs", allow_duplicate=True),
    Output(layout.tradinglog, "resetColumnState"),
    Input(layout.header.reset_columns_button, "n_clicks"),
    config_prevent_initial_callbacks=True
)
def reset(_):
    __env__.dump_column_state(None)
    return layout.log.columnDefs, True
