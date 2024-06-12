import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
from PIL import Image, ImageTk
import customtkinter
import traceback

def generate_graphs(HomePage):
    try:
        selected_graph = HomePage.graph_selector_value.get()
        info = HomePage.option_manager.get_project_data()
        folder = os.path.join(info['path'], info['name'])
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        if (selected_graph == "Best Cost Stacked"):
            HomePage.selected_graph_name = "best_cost_stacked"
            best_cost_stacked(HomePage.running_config['steps'], HomePage.progress_data, HomePage.option_manager)
        elif (selected_graph == "Best Cost by Round"):
            HomePage.selected_graph_name = "best_cost_by_round"
            best_cost_by_round(HomePage.running_config['steps'], HomePage.progress_data, HomePage.option_manager)
        elif (selected_graph == "Iteration Table"):
            HomePage.selected_graph_name = "table"
            table(HomePage.running_config['steps'], HomePage.progress_data, HomePage.option_manager)
        elif (selected_graph == "Calibrated Parameters"):
            HomePage.selected_graph_name = "calibrated_params_by_round"
            calibrated_params_by_round(HomePage.running_config['steps'], HomePage.calibration_data, HomePage.option_manager)
        elif (selected_graph == "Custom CSV"):
            HomePage.selected_graph_name = "custom_csv"
            custom_csv(HomePage, HomePage.option_manager)
        elif (selected_graph == "Compare CSV"):
            HomePage.selected_graph_name = "compare_csv"
            compare_csv(HomePage, HomePage.option_manager)
            
        image_path = os.path.join(folder, HomePage.selected_graph_name + ".png")
        
        if not os.path.exists(image_path):
            image_path = os.path.join("./images", "up.png")
        
        HomePage.graph_image_obj = Image.open(image_path)
        HomePage.graph_image = customtkinter.CTkImage(HomePage.graph_image_obj, size=(HomePage.image_width * HomePage.image_scale, HomePage.image_height * HomePage.image_scale))
        HomePage.graph_label.configure(image=HomePage.graph_image)
    except Exception as e:
        print(f"An exception occurred in Graph Generator: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        print("Traceback:")
        traceback.print_exc()

def best_cost_stacked(config, data, option_manager):
    fig = go.Figure()
        
    total_steps = len(config)
    
    # Get unique values from the round_step column of the dataframe
    for round_step in data.keys():
        fig.add_trace(go.Scatter(x=data[round_step]["percent"], y=data[round_step]["best_cost"], name=round_step))

    fig.update_layout(
        title="",
        xaxis_title="Iteration",
        yaxis_title="Best Cost",
        font=dict(color='white'),
        paper_bgcolor='rgba(42, 42, 42, 0)',
        plot_bgcolor='rgb(62, 62, 62)',
        xaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=1
        ),
        yaxis=dict(
            range=[0, 0.6],
            autorange=True,
            gridcolor='rgb(72, 72, 72)',
            gridwidth=0.1
        )
    )
    
    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "best_cost_stacked.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "best_cost_stacked.html"), include_plotlyjs='cdn', auto_open=False)
    with open(os.path.join(folder, "best_cost_stacked.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "best_cost_stacked.html"), "w") as f:
        f.write(html)

    
        return fig

def table(config, dataframe, option_manager):
    # Create a plotly table with the values in the dataframe
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(dataframe.columns),
            font=dict(color='black'),
            align="left"
        ),
        cells=dict(
            values=[dataframe[k].tolist() for k in dataframe.columns],
            font=dict(color='black'),
            align = "left")
    )])
    
    fig.update_layout(
        title="",
        xaxis_title="Iteration",
        yaxis_title="Best Cost",
        font=dict(color='white'),
        paper_bgcolor='rgba(42, 42, 42, 0)',
        plot_bgcolor='rgb(62, 62, 62)',
        xaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=1
        ),
        yaxis=dict(
            range=[0, 0.6],
            autorange=True,
            gridcolor='rgb(72, 72, 72)',
            gridwidth=0.1
        )
    )

    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "table.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "table.html"), include_plotlyjs='cdn', auto_open=False)
    with open(os.path.join(folder, "table.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "table.html"), "w") as f:
        f.write(html)
    
    return fig

def best_cost_by_round(config, data, option_manager):
    fig = go.Figure()
        
    total_steps = len(config)
    
    # Get unique values from the round_step column of the dataframe
    for round_step in data.keys():
    #for iteration in dataframe['round_step'].unique():
        # Get best_cost and completed rounds rows for this iteration

        round_index = int(round_step.split(" -")[0].replace("Round: ", "")) - 1

        #df = dataframe[dataframe['round_step'] == iteration]
        
        #step_index = ((iteration) % total_steps)
        #round_index = ((iteration) // total_steps)

        fig.add_trace(go.Scatter(x=np.array(data[round_step]['percent']) + (100 * round_index), y=data[round_step]['best_cost'], name=round_step))
        
        #fig.add_trace(go.Scatter(x=df['completed_rounds'] + (df['total_rounds'] * round_index), y=df['best_cost'], name='Group ' + str(step_index + 1)))
        
        xx = np.max(np.array(data['percent']) + (100 * round_index))
        fig.add_shape(
            type='line',
            x0=xx,
            y0=0,
            x1=xx,
            y1=1,
            yref='paper',
            line=dict(
                color='rgb(102, 102, 102)',
                width=2
            )
        )
        
        fig.add_annotation(
            x=xx + 0.5,
            y=1,
            yref='paper',
            text='Round ' + str(round_index + 1),
            showarrow=False,
            yshift=-10
        )

    fig.update_layout(
        title="",
        xaxis_title="Iteration",
        yaxis_title="Best Cost",
        font=dict(color='white'),
        paper_bgcolor='rgba(42, 42, 42, 0)',
        plot_bgcolor='rgb(62, 62, 62)',
        xaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=1
        ),
        yaxis=dict(
            range=[0, 0.6],
            autorange=True,
            gridcolor='rgb(72, 72, 72)',
            gridwidth=0.1
        )
    )
    
    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "best_cost_by_round.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "best_cost_by_round.html"), include_plotlyjs='cdn', auto_open=False)
    with open(os.path.join(folder, "best_cost_by_round.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "best_cost_by_round.html"), "w") as f:
        f.write(html)
    
    return fig

def calibrated_params_by_round(config, list_of_objs, option_manager):
    fig = go.Figure()
        
    total_steps = len(config)
    
    datalines = {"step": [], "round": []}
    step = 1
    round = 1
    for index, obj in enumerate(list_of_objs):
        if (obj == {}):
            continue
        for key in obj.keys():
            if key not in datalines:
                datalines[key] = []
            datalines[key].append(obj[key])
        datalines["step"].append(step)
        datalines['round'].append(round)
        step += 1
        if (step > total_steps):
            step = 1
            round += 1
    
    # Get unique values from the round_step column of the dataframe
    for key in datalines.keys():
        # Get best_cost and completed rounds rows for this iteration
        if key == 'step' or key == 'round':
            continue
        
        fig.add_trace(go.Scatter(x=datalines['round'], y=datalines[key], name=key))

    fig.update_layout(
        title="",
        xaxis_title="Round",
        yaxis_title="Particle Parameters",
        font=dict(color='white'),
        paper_bgcolor='rgba(42, 42, 42, 0)',
        plot_bgcolor='rgb(62, 62, 62)',
        xaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=1
        ),
        yaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=0.1
        )
    )

    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "calibrated_params_by_round.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "calibrated_params_by_round.html"), include_plotlyjs='cdn', auto_open=False)
    with open(os.path.join(folder, "calibrated_params_by_round.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "calibrated_params_by_round.html"), "w") as f:
        f.write(html)

    return fig

def custom_csv(homepage, option_manager):
    fig = go.Figure()

    data = homepage.csv_data["data"]

    x = homepage.csv_x_selector.get()
    val = homepage.csv_y1_selector.get()
    val2 = homepage.csv_y2_selector.get()
    
    xx = None
    if x == "time":
        xx = pd.to_datetime(data["time"], format='%Y-%m-%d', errors='coerce')
    elif x == "date":
        xx = pd.to_datetime(data["date"], format='%d-%m-%Y', errors='coerce')
    else:
        xx = pd.to_numeric(data[x], errors="coerce")
        
    yy = pd.to_numeric(data[val], errors="coerce")
    
    yy_unit = "-"
    if "Unit" in homepage.csv_data["data_attributes"]:
        yy_unit = homepage.csv_data["data_attributes"]["Unit"][val]
    
    yy2 = pd.to_numeric(data[val2], errors="coerce")
    
    yy2_unit = "-"
    if "Unit" in homepage.csv_data["data_attributes"]:
        yy2_unit = homepage.csv_data["data_attributes"]["Unit"][val2]

    fig.add_trace(go.Scatter(x=xx, y=yy, name=val))
    fig.add_trace(go.Scatter(x=xx, y=yy2, name=val2, yaxis='y2'))

    fig.update_layout(
        title="",
        xaxis_title=x,
        yaxis_title=val,
        font=dict(color='white'),
        paper_bgcolor='rgba(42, 42, 42, 0)',
        plot_bgcolor='rgb(62, 62, 62)',
        xaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=1
        ),
        yaxis=dict(
            title=val + " (" + str(yy_unit) + ")",
            autorange=True,
            gridcolor='rgb(72, 72, 72)',
            gridwidth=0.1
        ),
        yaxis2=dict(
            title=val2 + " (" + str(yy2_unit) + ")",
            overlaying='y',
            side='right'
        )
    )

    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "custom_csv.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "custom_csv.html"), include_plotlyjs='cdn', auto_open=False)
    with open(os.path.join(folder, "custom_csv.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "custom_csv.html"), "w") as f:
        f.write(html)

    return fig

def compare_csv(homepage, option_manager):
    fig = go.Figure()

    data = homepage.csv_data["data"]
    data2 = homepage.csv_data2["data"]

    x = homepage.csv_x_selector.get()
    val = homepage.csv_y1_selector.get()
    val2 = homepage.csv_y2_selector.get()
    
    xx = None
    if x == "time":
        xx = pd.to_datetime(data["time"], format='%Y-%m-%d', errors='coerce')
    elif x == "date":
        xx = pd.to_datetime(data["date"], format='%d-%m-%Y', errors='coerce')
    else:
        xx = pd.to_numeric(data[x], errors="coerce")
        
    yy = pd.to_numeric(data[val], errors="coerce")
    
    xx2 = None
    if x == "time":
        xx2 = pd.to_datetime(data2["time"], format='%Y-%m-%d', errors='coerce')
    elif x == "date":
        xx2 = pd.to_datetime(data2["date"], format='%d-%m-%Y', errors='coerce')
    else:
        xx2 = pd.to_numeric(data2[x], errors="coerce")
    
    yy_unit = "-"
    if "Unit" in homepage.csv_data["data_attributes"]:
        yy_unit = homepage.csv_data["data_attributes"]["Unit"][val]
    
    yy2 = pd.to_numeric(data[val2], errors="coerce")
    
    yy2_unit = "-"
    if "Unit" in homepage.csv_data["data_attributes"]:
        yy2_unit = homepage.csv_data["data_attributes"]["Unit"][val2]

    fig.add_trace(go.Scatter(x=xx, y=yy, name=val))
    fig.add_trace(go.Scatter(x=xx2, y=yy2, name=val2, yaxis='y2'))

    fig.update_layout(
        title="",
        xaxis_title=x,
        yaxis_title=val,
        font=dict(color='white'),
        paper_bgcolor='rgba(42, 42, 42, 0)',
        plot_bgcolor='rgb(62, 62, 62)',
        xaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=1
        ),
        yaxis=dict(
            title=val + " (" + str(yy_unit) + ")",
            autorange=True,
            gridcolor='rgb(72, 72, 72)',
            gridwidth=0.1
        ),
        yaxis2=dict(
            title=val2 + " (" + str(yy2_unit) + ")",
            overlaying='y',
            side='right'
        )
    )

    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "compare_csv.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "compare_csv.html"), include_plotlyjs='cdn', auto_open=False)
    with open(os.path.join(folder, "compare_csv.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "compare_csv.html"), "w") as f:
        f.write(html)

    return fig