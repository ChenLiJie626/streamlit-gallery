from io import StringIO
import json
import random
import streamlit as st

from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace

from .dashboard import Dashboard, Editor, Card, DataGrid, Radar, Pie, Player
from streamlit_echarts import st_echarts

# ECharts 配置
def get_echarts_options(accuracy_data):
    return {
        "title": {"text": "训练准确率"},
        "xAxis": {"type": "category", "data": [f"epoch{i}" for i in range(1, len(accuracy_data) + 1)]},
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": accuracy_data,
                "type": "line",
            }
        ],
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},

    }

def main():
    if "w" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            editor=Editor(board, 0, 0, 6, 11, minW=3, minH=3),
            player=Player(board, 0, 12, 6, 7, minH=4),
            pie=Pie(board, 6, 0, 6, 7, minW=3, minH=4),
            radar=Radar(board, 0, 0, 12, 7, minW=4, minH=4),
            card=Card(board, 6, 7, 3, 7, minW=2, minH=4),
            data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
        )
        state.w = w

        w.editor.add_tab("Card content", Card.DEFAULT_CONTENT, "plaintext")
        w.editor.add_tab("Data grid", json.dumps(DataGrid.DEFAULT_ROWS, indent=2), "json")
        w.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")
        w.editor.add_tab("Pie chart", json.dumps(Pie.DEFAULT_DATA, indent=2), "json")
    else:
        w = state.w

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            # w.editor()
            w.player()
            # w.pie(w.editor.get_content("Pie chart"))
            # w.card(w.editor.get_content("Card content"))
            w.data_grid(w.player.get_content())
    
    col1, col2 = st.columns(2)
    
    log_buffer = StringIO()
    with col1:
        log_placeholder = st.empty()  # 日志输出区域
    with col2:
        chart_placeholder = st.empty()  # 图表输出区域
    accuracy_data = []
    for epoch in range(1, 50):  
        accuracy = random.uniform(70, 100)
        accuracy_data.append(accuracy)

        # 更新日志
        log_message = f"Epoch {epoch}: Train Accuracy: {accuracy:.2f}%\n"
        log_buffer.write(log_message)
        log_placeholder.text_area("训练日志", log_buffer.getvalue(), height=250)


        # 更新图表，使用占位符更新同一个图表
        with chart_placeholder:
            st_echarts(get_echarts_options(accuracy_data))

    st.success("训练完成！")


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
