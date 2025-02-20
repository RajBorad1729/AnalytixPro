import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def create_visualizations(data):
    # Convert date to datetime and create Month-Year column
    data["Date"] = pd.to_datetime(data["Date"])
    data["Month"] = data["Date"].dt.to_period("M").astype(str)
    
    # Group data by month
    monthly_data = data.groupby("Month")[["Sales", "Profit", "Quantity"]].sum().reset_index()

    # Graph 1: Monthly Analysis of Sales and Profit
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(
        go.Scatter(
            x=monthly_data["Month"], y=monthly_data["Sales"], name="Sales",
            mode='lines+markers', line=dict(color='blue', width=2)
        ),
        secondary_y=False,
    )
    fig1.add_trace(
        go.Scatter(
            x=monthly_data["Month"], y=monthly_data["Profit"], name="Profit",
            mode='lines+markers', line=dict(color='green', width=2, dash='dot')
        ),
        secondary_y=True,
    )
    fig1.update_layout(
        title="Analysis of Sales and Profit",
        xaxis_title="Month",
        template="plotly_dark",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Graph 2: Monthly Analysis of Quantity
    fig2 = px.line(monthly_data, x="Month", y="Quantity", title="Analysis of Quantity",template="plotly_dark")

    # Graph 3: Pie chart (Category vs Quantity)
    fig3 = px.pie(data, names="Category", values="Quantity", title="Category-wise Quantity",template="plotly_dark")

    # Graph 4: Pie chart (Sub-Category vs Quantity)
    fig4 = px.pie(data, names="SubCategory", values="Quantity", title="Sub-Category-wise Quantity",template="plotly_dark")

    # Graph 5: Bar chart (Sub-Category-wise Profit and Sales)
    bar_data = data.groupby("SubCategory")[["Sales", "Profit"]].sum().reset_index()
    fig5 = go.Figure()
    fig5.add_trace(
        go.Bar(
            x=bar_data["SubCategory"], y=bar_data["Sales"], name="Sales",
            marker=dict(color='rgba(0, 123, 255, 0.7)'),
        )
    )
    fig5.add_trace(
        go.Bar(
            x=bar_data["SubCategory"], y=bar_data["Profit"], name="Profit",
            marker=dict(color='rgba(40, 167, 69, 0.7)'), width=0.5,
        )
    )
    fig5.update_layout(
        title="Sub-Category-wise Profit and Sales",
        barmode="overlay",
        xaxis_title="Sub-Category",
        yaxis_title="Values",
        template="plotly_dark",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Graph 6: Correlation Heatmap
    # Graph 6: Correlation Heatmap with Annotations
    correlation_matrix = data[["Sales", "Profit", "Quantity"]].corr()

    fig6 = go.Figure(go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale="Viridis",
        zmin=-1, zmax=1,  # Optional: for color normalization
    ))

    # Add annotations manually
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            fig6.add_annotation(
                x=correlation_matrix.columns[j],
                y=correlation_matrix.columns[i],
                text=f'{correlation_matrix.iloc[i, j]:.2f}',
                showarrow=False,
                font=dict(size=10, color='black')
            )

    fig6.update_layout(
        title="Correlation Heatmap of Sales, Profit, and Quantity",
        xaxis_title="Metrics",
        yaxis_title="Metrics",
        template="plotly_dark"
    )
 
    
    
    df_agg = data.groupby(["Category", "Region"], as_index=False)[["Sales", "Profit", "Quantity"]].sum()

# Pivot the data for the heatmap
    heatmap_data = df_agg.pivot(index="Category", columns="Region", values="Sales")
    
    fig7 = go.Figure(
    data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale="Viridis",
        colorbar={"title": "Sales"}
    )
)
    for i in range(heatmap_data.shape[0]):
        for j in range(heatmap_data.shape[1]):
            fig7.add_annotation(
            x=heatmap_data.columns[j],
            y=heatmap_data.index[i],
            text=f'{heatmap_data.values[i][j]:.2f}',
            showarrow=False,
            font=dict(color="black", size=12)
        )
    fig7.update_layout(
    title="Sales Heatmap with Annotations",
    xaxis_title="Region",
    yaxis_title="Category",
    template="plotly_dark"
)




    # Graph 9: Top Categories by Sales
    category_data = data.groupby("Category")[["Sales", "Profit"]].sum().reset_index()

    # Creating the figure for Category-wise Sales and Profit
    fig9 = go.Figure()

    # Add a bar trace for 'Sales'
    fig9.add_trace(
        go.Bar(
            x=category_data["Category"], y=category_data["Sales"], name="Sales",
            marker=dict(color='rgba(0, 123, 255, 0.7)'),
        )
    )

    # Add a bar trace for 'Profit' with smaller width for overlap effect
    fig9.add_trace(
        go.Bar(
            x=category_data["Category"], y=category_data["Profit"], name="Profit",
            marker=dict(color='rgba(40, 167, 69, 0.7)'), width=0.5,
        )
    )

    # Update layout to match your desired configuration
    fig9.update_layout(
        title="Category-wise Profit and Sales",
        barmode="overlay",  # Overlay bars (Sales and Profit) on top of each other
        xaxis_title="Category",
        yaxis_title="Values",
        template="plotly_dark",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Return all visualizations and statistics
    return {
        'fig1': fig1.to_html(),
        'fig2': fig2.to_html(),
        'fig3': fig3.to_html(),
        'fig4': fig4.to_html(),
        'fig6': fig5.to_html(),
        'fig7': fig6.to_html(),
        'fig8': fig7.to_html(),
        'fig5': fig9.to_html(),
    }
