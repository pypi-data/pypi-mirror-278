from cd_multi_tasker.cd_multi_tasker import MultiTasking

multitasker = MultiTasking(max_workers=4)


# Example task function for file processing
def process_file(file_path):
    """
    Dummy function to simulate file processing.
    Replace with actual file processing logic.

    Parameters:
        file_path (str): Path to the file to process.

    Returns:
        str: Dummy result message.
    """
    return f"Processed file {file_path}"


# Example list of file paths to process
file_paths = ["/path/to/file1", "/path/to/file2", "/path/to/file3"]
results = multitasker.run_cpu_bound_tasks(file_paths, process_file)
print("File processing results:", results)
