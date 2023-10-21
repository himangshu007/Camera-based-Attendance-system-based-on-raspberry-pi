import matplotlib.pyplot as plt

def create_attendance_chart(attendance_records):
    """
    Create a bar chart to visualize attendance data.

    Args:
        attendance_records (list of dict): List of attendance records, where each record is a dictionary.
    """
    names = [record['name'] for record in attendance_records]
    timestamps = [record['timestamp'] for record in attendance_records]

    # Convert timestamps to the number of occurrences (attendance)
    from collections import Counter
    attendance_counts = dict(Counter(names))

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(attendance_counts.keys(), attendance_counts.values())
    plt.xlabel('Names')
    plt.ylabel('Attendance Count')
    plt.title('Attendance Chart')
    plt.xticks(rotation=45)  # Rotate x-axis labels for readability

    plt.show()

# Example usage:
# If you have attendance records, you can call create_attendance_chart(records) with your data.
