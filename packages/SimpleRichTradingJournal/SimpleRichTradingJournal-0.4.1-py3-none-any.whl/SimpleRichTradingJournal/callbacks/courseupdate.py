from sys import stderr
from traceback import print_exception

from dash import callback, Output, Input, State, no_update

import __env__
import layout
from config import styles
from callbacks import main


@callback(
    Output(layout.tradinglog, "rowTransaction", allow_duplicate=True),
    Output(layout.summary_footer, "children", allow_duplicate=True),
    Output(layout.statistics.open_positions_graph, "figure", allow_duplicate=True),
    Output(layout.statistics.all_positions_graph, "figure", allow_duplicate=True),
    Output(layout.statistics.performance_graph, "figure", allow_duplicate=True),
    Output(layout.statistics.drag_container, "style", allow_duplicate=True),
    Output(layout.balance.balance_content, "children", allow_duplicate=True),
    Output(layout.header.update_interval, "disabled", allow_duplicate=True),
    Output(layout.summary_footer, "style", allow_duplicate=True),
    ##############################################################################################
    Input(layout.header.update_interval_trigger, "n_clicks"),
    State(layout.header.with_open_trigger, "n_clicks"),
    State(layout.statistics.performance_size_slider, "value"),
    State(layout.statistics.performance_steps, "value"),
    State(layout.statistics.performance_trailing_frame, "value"),
    State(layout.statistics.performance_trailing_interval, "value"),
    State(layout.statistics.performance_range, "value"),
    State(layout.statistics.drag_container, "style"),
    State(layout.drag_event_receiver, "value"),
    State(layout.statistics.STATISTICS, "style"),
    State(layout.balance.BALANCE, "style"),
    State(layout.balance.T_trigger_, "n_clicks"),
    State(layout.balance.C_trigger_, "n_clicks"),
    State(layout.balance.Y_trigger_, "n_clicks"),
    State(layout.balance.Q_trigger_, "n_clicks"),
    State(layout.header.scope_by_button, "n_clicks"),
    State(layout.drag_event_receiver2, "value"),
    State(layout.summary_footer, "style"),
    [State(i, "value") for i in layout.statistics._group_by_checks],
    State(layout.statistics.show_all, "value"),
    config_prevent_initial_callbacks=True
)
def course_update(
        _,
        i_with_open_value,
        i_performance_size_slider_value,
        i_performance_steps_value,
        i_performance_trailing_frame_value,
        i_performance_trailing_interval_value,
        i_performance_range_value,
        i_drag_container_style,
        i_drag_event_receiver_value,
        i_STATISTICS_style,
        i_BALANCE_style,
        i_T_trigger_,
        i_C_trigger_,
        i_Y_trigger_,
        i_Q_trigger_,
        i_scope_by_button_n_clicks,
        i_drag_event_receiver2_value,
        i_summary_footer_style,
        i_group_by_short,
        i_group_by_type,
        i_group_by_sector,
        i_group_by_category,
        i_group_by_id,
        i_group_by_show_all,
):
    o_summary_footer_style = o_tradinglog_rowTransaction = o_summary_footer_children = o_open_positions_graph_figure = o_all_positions_graph_figure = o_performance_graph_figure = o_drag_container_style = o_BALANCE_children = o_update_interval_disabled = no_update
    try:
        o_tradinglog_rowTransaction = {"update": main.__lc__.update_course()}
        o_update_interval_disabled = False
        if main.__lc__._calc_with_open_positions:
            main.__lc__.__f_reset_calc__()
            o_tradinglog_rowTransaction["update"] += [d.data for d in main.__lc__.frame_deposits]

            if i_scope_by_button_n_clicks % 2:
                scope_by_attr = "idx"
            else:
                scope_by_attr = __env__.scope_by_both

            i_STATISTICS_style = not i_STATISTICS_style.get("display")
            i_BALANCE_style = not i_BALANCE_style.get("display")

            o_summary_footer_children = layout.make.make_footer(main.__lc__)
            (o_open_positions_graph_figure,
             o_all_positions_graph_figure,
             o_performance_graph_figure,
             o_BALANCE_children,
             o_drag_container_style) = main.new_side(
                i_drag_event_receiver2_value,
                i_group_by_type,
                i_group_by_short,
                i_group_by_sector,
                i_group_by_category,
                i_group_by_id,
                i_group_by_show_all,
                scope_by_attr,
                i_performance_steps_value,
                i_performance_trailing_frame_value,
                i_performance_trailing_interval_value,
                i_performance_range_value,
                i_drag_event_receiver_value,
                i_drag_container_style,
                i_performance_size_slider_value,
                i_Y_trigger_,
                i_Q_trigger_,
                i_T_trigger_,
                i_C_trigger_,
                i_STATISTICS_style,
                i_BALANCE_style
            )
    except Exception as e:
        print_exception(e)
        print("[Error]", e, flush=True, file=stderr)
        o_summary_footer_style = i_summary_footer_style | styles.misc.summary_error
        o_tradinglog_rowTransaction = no_update
    else:
        o_summary_footer_style = i_summary_footer_style | styles.misc.summary_error_reset | __env__.get_footer_live_signal()

    return (
        o_tradinglog_rowTransaction,
        o_summary_footer_children,
        o_open_positions_graph_figure,
        o_all_positions_graph_figure,
        o_performance_graph_figure,
        o_drag_container_style,
        o_BALANCE_children,
        o_update_interval_disabled,
        o_summary_footer_style,
    )
