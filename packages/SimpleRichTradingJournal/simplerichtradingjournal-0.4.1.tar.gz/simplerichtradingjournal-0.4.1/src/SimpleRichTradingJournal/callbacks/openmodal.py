from __future__ import annotations

from dash import callback, Output, Input, State, callback_context

import layout
from config import styles


@callback(
    Output(layout.history.MODAL, "is_open"),
    Input(layout.header.history_button, "n_clicks"),
    State(layout.history.MODAL, "is_open"),
    config_prevent_initial_callbacks=True
)
def open_backup_modal(_, is_open):
    return not is_open


@callback(
    Output(layout.statistics.group_by_settings, "style"),
    Output(layout.statistics.framing_settings, "style"),
    Output(layout.statistics.group_by_button, "style"),
    Output(layout.statistics.framing_button, "style"),
    Input(layout.statistics.group_by_button, "n_clicks"),
    Input(layout.statistics.framing_button, "n_clicks"),
    State(layout.statistics.group_by_settings, "style"),
    State(layout.statistics.framing_settings, "style"),
    State(layout.statistics.group_by_button, "style"),
    State(layout.statistics.framing_button, "style"),
    config_prevent_initial_callbacks=True
)
def open_group_by(g_n, f_n, g_style, f_style, g_b_style, f_b_style):
    if callback_context.triggered_id == layout.statistics.framing_button.id:
        g_style |= {"zIndex": -3}
        g_b_style |= styles.misc.group_by_options_off
        if f_style["zIndex"] == -3:
            f_style |= {"zIndex": 15}
            f_b_style |= styles.misc.framing_options_on
        else:
            f_style |= {"zIndex": -3}
            f_b_style |= styles.misc.framing_options_off
    else:
        f_style |= {"zIndex": -3}
        f_b_style |= styles.misc.framing_options_off
        if g_style["zIndex"] == -3:
            g_style |= {"zIndex": 15}
            g_b_style |= styles.misc.group_by_options_on
        else:
            g_style |= {"zIndex": -3}
            g_b_style |= styles.misc.group_by_options_off
    return g_style, f_style, g_b_style, f_b_style
