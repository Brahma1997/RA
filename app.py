import streamlit as st
import time
import random

# Sorting Algorithm Implementations
def bubble_sort_with_animation(array):
    steps = []
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            explanation = f"Comparing {array[j]} and {array[j + 1]}"
            steps.append((array.copy(), explanation, j, j + 1, False))
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                explanation = f"Swapping {array[j]} and {array[j + 1]}"
                steps.append((array.copy(), explanation, j, j + 1, True)) 
                
    return steps

def insertion_sort_with_animation(array):
    steps = []
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            explanation = f"Moving {array[j]} to the right to insert {key}"
            steps.append((array.copy(), explanation, j, i, False))
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
        explanation = f"Inserted {key} at the correct position"
        steps.append((array.copy(), explanation, j + 1, i, True))
    return steps

def selection_sort_with_animation(array):
    steps = []
    n = len(array)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            explanation = f"Comparing {array[min_idx]} and {array[j]}"
            steps.append((array.copy(), explanation, min_idx, j, False))
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        explanation = f"Swapping {array[i]} with {array[min_idx]}"
        steps.append((array.copy(), explanation, i, min_idx, True))
    return steps

def merge_sort_with_equal_split(array):
    steps = []

    def merge_sort_recursive(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            explanation = f"Splitting: Left = {arr[left:mid + 1]}, Right = {arr[mid + 1:right + 1]}"
            steps.append((arr.copy(), explanation, left, right, False))
            merge_sort_recursive(arr, left, mid)  # Sort the left half
            merge_sort_recursive(arr, mid + 1, right)  # Sort the right half
            merge(arr, left, mid, right)  # Merge the two halves

    def merge(arr, left, mid, right):
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]

        explanation = f"Start merging: Left = {left_part}, Right = {right_part}"
        steps.append((arr.copy(), explanation, left, right, False))

        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            explanation = f"Merging: Comparing {left_part[i]} and {right_part[j]}"
            steps.append((arr.copy(), explanation, k, k, False))
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            k += 1

        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1

        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1

        explanation = f"Merged: {arr[left:right + 1]}"
        steps.append((arr.copy(), explanation, left, right, True))

    merge_sort_recursive(array, 0, len(array) - 1)
    return steps

# Convert array to a text-based representation with colored rectangles
def array_to_colored_rectangles(array, highlight_indices=None, swap=False):
    if highlight_indices is None:
        highlight_indices = []
    result = []
    for i, num in enumerate(array):
        if i in highlight_indices:
            if swap:
                result.append(
                    f"<span style='display: inline-block; padding: 10px; border: 2px solid red; background-color: pink; font-weight: bold; color: black;'>{num}</span>"
                )
            else:
                result.append(
                    f"<span style='display: inline-block; padding: 10px; border: 2px solid orange; background-color: lightyellow; font-weight: bold; color: black;'>{num}</span>"
                )
        else:
            result.append(
                f"<span style='display: inline-block; padding: 10px; border: 1px solid gray; background-color: white; font-weight: bold; color: black;'>{num}</span>"
            )
    return " ".join(result)

# Algorithm Descriptions
ALGORITHM_DESCRIPTIONS = {
    "Bubble Sort": "Bubble Sort repeatedly compares adjacent elements and swaps them if they are in the wrong order. It is a simple but inefficient sorting algorithm with O(n^2) time complexity.",
    "Insertion Sort": "Insertion Sort builds the sorted array one item at a time by inserting each element into its correct position. It is efficient for small datasets and partially sorted arrays.",
    "Selection Sort": "Selection Sort divides the array into a sorted and unsorted region, repeatedly finding the minimum element from the unsorted region and placing it in the sorted region.",
    "Merge Sort": "Merge Sort is a divide-and-conquer algorithm that recursively divides the array into halves, sorts them, and merges them back together. It has a time complexity of O(n log n)."
}

# Streamlit Interface
st.title("Step-by-Step Sorting Visualizer with Rectangles")

# User Inputs
sorting_algorithm = st.selectbox("Choose Sorting Algorithm", ["Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort"])
array_size = st.slider("Array Size", min_value=5, max_value=15, value=8)
speed = st.slider("Visualization Speed (seconds per step)", min_value=0.1, max_value=1.0, value=0.5)

# Algorithm Description
st.subheader("Algorithm Description")
st.write(ALGORITHM_DESCRIPTIONS[sorting_algorithm])

# Generate a Random Array
if "array" not in st.session_state or st.button("Generate New Array"):
    st.session_state.array = random.sample(range(1, 100), array_size)

array = st.session_state.array  # Current array to sort

# Display the Initial Array
st.subheader("Initial Array")
st.markdown(array_to_colored_rectangles(array), unsafe_allow_html=True)

# Start Sorting Visualization
if st.button("Start Sorting"):
    # Perform the selected sorting algorithm with animation
    if sorting_algorithm == "Bubble Sort":
        steps = bubble_sort_with_animation(array)
    elif sorting_algorithm == "Insertion Sort":
        steps = insertion_sort_with_animation(array)
    elif sorting_algorithm == "Selection Sort":
        steps = selection_sort_with_animation(array)
    elif sorting_algorithm == "Merge Sort":
        steps = merge_sort_with_equal_split(array)

    # Display each step with explanation and colorful animation
    for step_array, explanation, i, j, swap in steps:
        # Show the explanation
        st.write(f"Step: {explanation}")
        
        # Show the animated state of the array with colored rectangles
        st.markdown(array_to_colored_rectangles(step_array, highlight_indices=[i, j], swap=swap), unsafe_allow_html=True)
        
        # Add a delay for visualization
        time.sleep(speed)

    # Final Sorted Array
    st.success("Sorting Completed!")
    st.subheader("Sorted Array:")
    st.markdown(array_to_colored_rectangles(array), unsafe_allow_html=True)
