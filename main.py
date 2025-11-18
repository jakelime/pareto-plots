import random
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Since the 'pareto' library and 'utils.generate_toy_story_machine_names' are not standard,
# I will create a placeholder function for demonstration purposes.
def generate_toy_story_machine_names(count=100):
    return [f"Machine_{i + 1}" for i in range(count)]


random.seed(42)

names = generate_toy_story_machine_names(count=100)

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

# --- Create the combined figure with subplots ---

# A4 paper size in pixels (at 96 DPI) is approximately 794x1123.
# We will use this as a reference for the figure size.
A4_WIDTH_PX = 794
A4_HEIGHT_PX = 1123


# Create a figure with 2 rows of subplots
fig = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"secondary_y": True}], [{}]],
    subplot_titles=(
        "Pareto Analysis: Normalized Machine Utilization Rate",
        "Sorted Heatmap of Normalized Machine Utilization",
    ),
)


# --- Pareto Chart (First Subplot) ---
VALUE_COL = "under_utilized_rate_normalized"
df_pareto = df.sort_values(by=VALUE_COL, ascending=False).reset_index(drop=True)
total_sum = df_pareto["total_idle_pct"].sum()
df_pareto["cumulative_sum"] = df_pareto["total_idle_pct"].cumsum()
df_pareto["cumulative_percent"] = (df_pareto["cumulative_sum"] / total_sum) * 100

# Add Bar Chart
fig.add_trace(
    go.Bar(
        x=df_pareto["machine_name"],
        y=df_pareto[VALUE_COL],
        name="Under Utilized Rate",
        marker_color="darkred",
        hovertemplate="%{}: %{y:.2f}<extra></extra>",
    ),
    row=1,
    col=1,
    secondary_y=False,
)

# Add Line Chart
fig.add_trace(
    go.Scatter(
        x=df_pareto["machine_name"],
        y=df_pareto["cumulative_percent"],
        name="Cumulative Percentage",
        mode="lines+markers",
        line=dict(color="rgb(255, 69, 0)", width=3),
        marker=dict(symbol="circle", size=8),
        hovertemplate="Cumulative: %{y:.1f}%<extra></extra>",
    ),
    row=1,
    col=1,
    secondary_y=True,
)

# --- Heatmap (Second Subplot) ---
df_heatmap = df_raw.sort_values(
    by="utilization_rate_normalized", ascending=False
).reset_index(drop=True)

grid_size = 10
if len(df_heatmap) != grid_size * grid_size:
    raise ValueError(
        f"Number of machines must be {grid_size * grid_size} for a square grid."
    )

z_data = df_heatmap["utilization_rate_normalized"].values.reshape(grid_size, grid_size)
hover_text = [
    f"{name} - Normalized Utilization: {util_rate:.2f}"
    for name, util_rate in zip(
        df_heatmap["machine_name"], df_heatmap["utilization_rate_normalized"]
    )
]
hover_text = np.array(hover_text).reshape(grid_size, grid_size)


fig.add_trace(
    go.Heatmap(
        z=z_data,
        text=hover_text,
        hoverinfo="text",
        colorscale="RdYlGn",
        reversescale=False,
        zmid=0.8,
        zmax=1.0,
        zmin=0.5,
        colorbar=dict(title="Normalized<br>Utilization"),
    ),
    row=2,
    col=1,
)


# --- Customize Layout ---
fig.update_layout(
    height=A4_HEIGHT_PX,
    width=A4_WIDTH_PX,
    template="plotly_white",
    showlegend=False,
)

# Customize Pareto Axes
fig.update_xaxes(
    title_text="Machine Name (Sorted by Normalized Rate)",
    showticklabels=False,
    row=1,
    col=1,
)
fig.update_yaxes(
    title_text="Under Utilized Rate (Normalized)",
    secondary_y=False,
    row=1,
    col=1,
    showgrid=False,
)
fig.update_yaxes(
    title_text="Cumulative Percentage (%)",
    secondary_y=True,
    row=1,
    col=1,
    range=[0, 100],
    tickvals=list(range(0, 101, 10)),
    gridcolor="lightgray",
)

# Customize Heatmap Axes
fig.update_xaxes(showgrid=False, showticklabels=False, row=2, col=1)
fig.update_yaxes(
    showgrid=False, showticklabels=False, autorange="reversed", row=2, col=1
)


# Add 80/20 line to Pareto
fig.add_hline(
    y=80,
    line_dash="dash",
    line_color="red",
    secondary_y=True,
    row=1,
    col=1,
    annotation_text="80% Threshold",
    annotation_position="top right",
    annotation_font_size=12,
    annotation_font_color="red",
)

# Export to HTML
fig.write_html("combined_figure_a4.html")

print("Figure has been saved to combined_figure_a4.html")
