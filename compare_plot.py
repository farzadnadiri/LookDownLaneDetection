import matplotlib.pyplot as plt
import numpy as np

# Function to generate plot from CSV files
def generate_plot(file1, file2):
    # Read the saved data from the CSV files
    projected_data_1 = np.loadtxt(file1, delimiter=',')
    projected_data_2 = np.loadtxt(file2, delimiter=',')

    # Generate the x-axis data for both lines
    x_data_1 = np.linspace(0, len(projected_data_1), len(projected_data_1))
    x_data_2 = np.linspace(0, len(projected_data_2), len(projected_data_2))

    # Create a new plot
    plt.figure(figsize=(10, 6))

    # Plot both `projected_car_line` data sets
    plt.plot(x_data_1, projected_data_1, label="Projected Car Line - Look Ahead", color="orange")
    plt.plot(x_data_2, projected_data_2, label="Projected Car Line - Look Down", color="purple")

    # Add labels and title
    plt.title("Projected Car Position from Two Methods")
    plt.xlabel("Time")
    plt.ylabel("Projected Car Position")

    # Add a legend
    plt.legend()

    # Display the merged graph
    plt.show()

# If running directly, you can pass filenames
if __name__ == "__main__":
    # Use the generated CSV files
    generate_plot('look_ahead.csv', 'look_down.csv')
