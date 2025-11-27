import altair as alt
import pandas as pd

# Load your data
df = pd.read_csv('fastfood.csv')

# Calculate averages for all nutritional metrics per restaurant
avg_nutrition = df.groupby('restaurant').agg({
    'calories': 'mean',
    'cal_fat': 'mean',
    'total_fat': 'mean',
    'sat_fat': 'mean',
    'trans_fat': 'mean',
    'cholesterol': 'mean',
    'sodium': 'mean',
    'total_carb': 'mean',
    'fiber': 'mean',
    'sugar': 'mean',
    'protein': 'mean',
    'vit_a': 'mean',
    'vit_c': 'mean',
    'calcium': 'mean'
}).reset_index()

# Reshape data for radio button selection
nutrition_long = avg_nutrition.melt(
    id_vars=['restaurant'],
    value_vars=['calories', 'cal_fat', 'total_fat', 'sat_fat', 'trans_fat', 
                'cholesterol', 'sodium', 'total_carb', 'fiber', 'sugar', 
                'protein', 'vit_a', 'vit_c', 'calcium'],
    var_name='metric',
    value_name='value'
)

# Create radio button widget (changed from dropdown)
metric_radio = alt.binding_radio(
    options=['calories', 'cal_fat', 'total_fat', 'sat_fat', 'trans_fat', 
             'cholesterol', 'sodium', 'total_carb', 'fiber', 'sugar', 
             'protein', 'vit_a', 'vit_c', 'calcium'],
    labels=['Calories', 'Calories from Fat', 'Total Fat (g)', 'Saturated Fat (g)', 
            'Trans Fat (g)', 'Cholesterol (mg)', 'Sodium (mg)', 'Total Carbs (g)', 
            'Fiber (g)', 'Sugar (g)', 'Protein (g)', 'Vitamin A (%)', 
            'Vitamin C (%)', 'Calcium (%)'],
    name='Select Nutritional Metric: '
)

metric_selection = alt.selection_point(
    fields=['metric'],
    bind=metric_radio,
    value='calories'
)

# Create the chart - restaurants stay in same position
chart = alt.Chart(nutrition_long).mark_bar().encode(
    x=alt.X('restaurant:N', 
            sort=None,  # No sorting - keeps original order
            axis=alt.Axis(title='Restaurant', labelAngle=-45)),
    y=alt.Y('value:Q', 
            axis=alt.Axis(title='Average Value')),
    color=alt.Color('value:Q',
                    scale=alt.Scale(scheme='redyellowgreen', reverse=True),
                    legend=alt.Legend(title='Value')),
    tooltip=[
        alt.Tooltip('restaurant:N', title='Restaurant'),
        alt.Tooltip('metric:N', title='Metric'),
        alt.Tooltip('value:Q', format='.2f', title='Value')
    ]
).transform_filter(
    metric_selection
).add_params(
    metric_selection
).properties(
    width=800,
    height=500,
    title='Average Nutritional Content by Fast Food Restaurant'
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16,
    anchor='middle'
)

# Save as HTML
chart.save('graph1.html')
print("Interactive chart with radio buttons saved as graph1.html!")