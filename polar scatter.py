import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

df = pd.read_csv("GlobalWeatherRepository.csv")

polar_scatter = px.scatter_polar(
    df,
    r='wind_mph',
    theta='wind_direction',
    title='Wind Speed by Direction',
    color='country'


)
polar_scatter.update_layout(showlegend=False)


# Define a callback function for filtering by moon phase
def filter_by_moon_phase(trace, points, selector):
    if not points.point_inds:
        return

    selected_moon_phase = df.iloc[points.point_inds[0]]['moon_phase']
    filtered_countries = df[df['moon_phase'] == selected_moon_phase]['country'].tolist()

    # Create a filtered trace based on the selected moon phase
    filtered_trace = go.Scatterpolar(
        r=df[df['moon_phase'] == selected_moon_phase]['wind_mph'],
        theta=df[df['moon_phase'] == selected_moon_phase]['wind_direction'],
        text=df[df['moon_phase'] == selected_moon_phase]['moon_phase'],
        mode='markers',
        marker=dict(size=8),
        customdata=filtered_countries
    )

    # Update the polar scatter plot with the filtered trace
    polar_scatter.data = [filtered_trace]

# Add a scatter plot trace for the callback function
scatter_trace = go.Scatterpolar(r=[0], theta=[0], mode='markers', marker=dict(size=0))
scatter_trace.on_click(filter_by_moon_phase)

# Add the scatter trace to the plot
polar_scatter.add_trace(scatter_trace)

# Show the polar scatter plot
polar_scatter.show()