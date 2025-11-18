import random

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from pareto import utils

random.seed(42)

names = utils.generate_toy_story_machine_names(count=100)


df = pd.DataFrame(names, columns=["machine_name"])
df["target_util_rate"] = random.choices(
    [0.3, 0.4, 0.5], k=len(names)
)  # Adjusted for higher utilization
df["total_hours_year"] = 8760


# Parameters for generating IDLE hours using a Pareto distribution
shape_param = 3.7  # Shape parameter 'a'. Controls the tail of the idle time.
min_idle_hours = 50  # Minimum idle hours for any machine.
scale_factor = 8000  # Scales the idle hours distribution.

# Generate idle hours following a Pareto distribution
# Most machines will have few idle hours, a few will have many.
df["idle_hours_year"] = (
    np.random.pareto(shape_param, len(names)) * scale_factor + min_idle_hours
).astype(int)
# Calculate utilized hours by subtracting idle hours from the total
df["utilized_hours_year"] = df["total_hours_year"] - df["idle_hours_year"]

# IMPORTANT: Clip the values to ensure they are realistic (0 <= hours <= 8760)
df["utilized_hours_year"] = df["utilized_hours_year"].clip(
    lower=0, upper=df["total_hours_year"]
)


df["utilization_rate"] = df["utilized_hours_year"] / df["total_hours_year"]
df["utilization_rate_normalized"] = df["utilization_rate"] / df["target_util_rate"]
df["under_utilized_rate_normalized"] = 1 - df["utilization_rate_normalized"]

total_idle_hours = df["idle_hours_year"].sum()

df["total_idle_pct"] = df["idle_hours_year"] / total_idle_hours * 100

df_raw = df.copy()
df_raw.to_csv("output-machine_utilization_inverted_pareto.csv", index=False)


VALUE_COL = "under_utilized_rate_normalized"
TITLE = "Pareto Analysis: Normalized Machine Utilization Rate"

df_pareto = df.sort_values(by=VALUE_COL, ascending=False).reset_index(drop=True)

# 2. Calculate the cumulative sum and cumulative percentage
total_sum = df_pareto["total_idle_pct"].sum()
df_pareto["cumulative_sum"] = df_pareto["total_idle_pct"].cumsum()
df_pareto["cumulative_percent"] = (df_pareto["cumulative_sum"] / total_sum) * 100

# 3. Create the Plotly figure with two y-axes
fig = make_subplots(specs=[[{"secondary_y": True}]])

# 4. Add the Bar Chart (Primary Y-axis)
fig.add_trace(
    go.Bar(
        x=df_pareto["machine_name"],
        y=df_pareto[VALUE_COL],
        name=VALUE_COL,
        marker_color="darkred",  # Forest Green for resource usage
        hovertemplate="%{x}: %{y:.2f}<extra></extra>",
    ),
    secondary_y=False,
)

# 5. Add the Line Chart (Secondary Y-axis for Cumulative Percentage)
fig.add_trace(
    go.Scatter(
        x=df_pareto["machine_name"],
        y=df_pareto["cumulative_percent"],
        name="Cumulative Percentage",
        mode="lines+markers",
        line=dict(color="rgb(255, 69, 0)", width=3),  # Red/Orange for focus line
        marker=dict(symbol="circle", size=8),
        hovertemplate="%{x}: %{y:.1f}%",
    ),
    secondary_y=True,
)

# 6. Customize Layout
fig.update_layout(
    title={
        "text": TITLE,
        "y": 0.95,
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top",
        "font": dict(size=20, family="Inter, sans-serif"),
    },
    xaxis_title="Machine Name (Sorted by Normalized Rate)",
    margin=dict(l=40, r=40, t=60, b=40),
    template="plotly_white",
)

# Set y-axes titles and ranges
fig.update_yaxes(
    title_text=f"{VALUE_COL}",
    secondary_y=False,
    range=[0, df_pareto[VALUE_COL].max() * 1.05],  # Slight buffer
    showgrid=False,
)
fig.update_yaxes(
    title_text="Cumulative Percentage (%)",
    secondary_y=True,
    range=[0, 100],
    tickvals=list(range(0, 101, 10)),
    gridcolor="lightgray",
)

# Add 80/20 line
fig.add_hline(
    y=80,
    line_dash="dash",
    line_color="red",
    secondary_y=True,
    annotation_text="80% Threshold",
    annotation_position="top right",
    annotation_font_size=12,
    annotation_font_color="red",
)

# Hide x-axis tick labels if there are too many (100 labels look messy)
if len(df_pareto) > 50:
    fig.update_xaxes(showticklabels=False)


df = df_raw.sort_values(
    by="utilization_rate_normalized", ascending=False, inplace=False
)
df.reset_index(drop=True, inplace=True)

grid_size = 10
if len(df) != grid_size * grid_size:
    raise ValueError(
        f"Number of machines must be {grid_size * grid_size} for a square grid."
    )

z_data = df["utilization_rate_normalized"].values.reshape(grid_size, grid_size)

hover_text = []
for i, name in enumerate(df["machine_name"]):
    util_rate = df["utilization_rate_normalized"].iloc[i]
    hover_text.append(f"{name} - Normalized Utilization: {util_rate:.2f}")
hover_text = np.array(hover_text).reshape(grid_size, grid_size)

# Create the heatmap figure
fig = go.Figure(
    data=go.Heatmap(
        z=z_data,
        text=hover_text,
        hoverinfo="text",
        colorscale="RdYlGn",
        reversescale=False,
        zmid=0.8,
        zmax=1.0,
        zmin=0.5,
        colorbar=dict(title="Normalized<br>Utilization"),
    )
)

fig.update_layout(
    title_text="<b>Sorted Heatmap of Normalized Machine Utilization</b>",
    xaxis=dict(showgrid=False, showticklabels=False),
    yaxis=dict(showgrid=False, showticklabels=False, autorange="reversed"),
    plot_bgcolor="#444",
    width=600,
    height=600,
    autosize=False,
)
