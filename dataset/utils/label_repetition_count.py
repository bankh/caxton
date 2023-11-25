import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def count_repetitions_and_plot(csv_filepath, output_image_path):
    # Load the dataset into a pandas DataFrame
    data = pd.read_csv(csv_filepath)

    # Define the columns that you want to check for repetitions
    class_columns = ['flow_rate_class', 'feed_rate_class', 'z_offset_class', 'hotend_class']

    # Count the repetitions of the class sets
    repetition_counts = data.groupby(class_columns).size().reset_index(name='repetitions')

    # Sort the dataframe based on the count of repetitions
    repetition_counts_sorted = repetition_counts.sort_values('repetitions', ascending=True)

    # Create a new column 'set' that concatenates the class values into a single string
    repetition_counts_sorted['set'] = (
        repetition_counts_sorted['flow_rate_class'].astype(str) + 
        repetition_counts_sorted['feed_rate_class'].astype(str) +
        repetition_counts_sorted['z_offset_class'].astype(str) +
        repetition_counts_sorted['hotend_class'].astype(str)
    )

    # Plotting with adjusted figure size for better y-axis readability
    plt.figure(figsize=(12, len(repetition_counts_sorted) * 0.3))  # Adjust the height dynamically based on the number of bars
    bars = plt.barh(repetition_counts_sorted['set'], 
                    repetition_counts_sorted['repetitions'], 
                    height=0.5,  # Adjust the height of the bars to reduce thickness
                    color='blue', 
                    edgecolor='black')

    # Increase space between bars for better readability
    # plt.gca().invert_yaxis()  # Invert y-axis to have the highest count at the top
    bar_width = 0.4
    plt.bar_label(bars, padding=3, fmt='%.0f', fontsize=10, color='black')

    # Gradient color - light to dark
    num_bars = len(bars)
    light_blue = (0.7, 0.85, 1.0)  # Light blue color
    dark_blue = (0, 0, 0.5)        # Dark blue color

    # Apply color gradient
    for i, bar in enumerate(bars):
        bar.set_color(((dark_blue[0] * i) / num_bars + light_blue[0] * (1 - i / num_bars),
                       (dark_blue[1] * i) / num_bars + light_blue[1] * (1 - i / num_bars),
                       (dark_blue[2] * i) / num_bars + light_blue[2] * (1 - i / num_bars)))

    # Add legend for class encoding
    legend_elements = [Patch(facecolor='orange', edgecolor='black', label='0: Low'),
                       Patch(facecolor='green', edgecolor='black', label='1: Good'),
                       Patch(facecolor='red', edgecolor='black', label='2: High')]
    plt.legend(handles=legend_elements, title='Class encoding (Order: flow_rate, feed_rate, z_offset, hotend_temperature)')

    plt.xlabel('Count')
    plt.ylabel('Set (flow_rate_class feed_rate_class z_offset_class hotend_class)')
    plt.title('Histogram of Repetitions')

    # Save the plot to a file
    plt.savefig(output_image_path, bbox_inches='tight')
    plt.close()

    # Return the sorted repetition counts
    return repetition_counts_sorted

# The path to the CSV file - provided as a variable
csv_filepath = '/caxton_dataset/caxton_dataset_final.csv'

# The path to save the output image - provided as a variable
output_image_path = 'image.png'

# Count the repetitions, plot the histogram, and save the image
repetitions_sorted = count_repetitions_and_plot(csv_filepath, output_image_path)

# Optionally, save the sorted repetition counts to a CSV file
repetitions_sorted.to_csv('repetitions_count_sorted.csv', index=False)


