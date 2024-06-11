
# CD Multi Tasker

`cd_multi_tasker` is a Python package designed to handle multiple concurrent tasks efficiently. It supports both CPU-bound and I/O-bound tasks, using multiprocessing for CPU-intensive operations and multithreading for I/O-bound operations.

## Features

- **Multiprocessing** for CPU-bound tasks such as file processing.
- **Multithreading** for I/O-bound tasks such as HTTP requests.
- Easy-to-use interface for running concurrent tasks.

## Installation

To install the package, use:

```bash
pip install cd_multi_tasker
```

## Usage

### Importing the Package

```python
from cd_multi_tasker.cd_multi_tasker import MultiTasking
```

### Example: CPU-bound Tasks (File Processing)

```python
# Initialize the MultiTasking class
multitasker = MultiTasking(max_workers=4)

# Define a sample task function for file processing
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

# List of file paths to process
file_paths = ["/path/to/file1", "/path/to/file2", "/path/to/file3"]

# Run the tasks
results = multitasker.run_cpu_bound_tasks(file_paths, process_file)
print("File processing results:", results)
```

### Example: I/O-bound Tasks (HTTP Requests)

```python
# Initialize the MultiTasking class
multitasker = MultiTasking(max_workers=4)

# Define a sample task function for HTTP requests
def fetch_data(url):
    """
    Dummy function to simulate fetching data from a URL.
    Replace with actual HTTP request logic.
    
    Parameters:
        url (str): URL to fetch data from.
    
    Returns:
        str: Dummy response message.
    """
    return f"Fetched data from {url}"

# List of URLs to fetch data from
urls = ["http://example.com/data1", "http://example.com/data2"]

# Run the tasks
results = multitasker.run_io_bound_tasks(urls, fetch_data)
print("HTTP fetching results:", results)
```

## Class and Methods

### `MultiTasking`

#### `__init__(self, max_workers)`

- Initializes the MultiTasking class with the maximum number of workers.
- **Parameters**:
  - `max_workers` (int): Maximum number of concurrent tasks.

#### `run_cpu_bound_tasks(self, tasks, task_func, *args, **kwargs)`

- Executes multiple CPU-bound tasks concurrently using multiprocessing.
- **Parameters**:
  - `tasks` (list): List of tasks to be processed (e.g., file paths for processing).
  - `task_func` (callable): Function to run for each task.
  - `*args`: Variable length argument list for the task function.
  - `**kwargs`: Arbitrary keyword arguments for the task function.
- **Returns**:
  - `list`: Results of the tasks.

#### `run_io_bound_tasks(self, tasks, task_func, *args, **kwargs)`

- Executes multiple I/O-bound tasks concurrently using multithreading.
- **Parameters**:
  - `tasks` (list): List of tasks to be processed (e.g., URLs for web requests).
  - `task_func` (callable): Function to run for each task.
  - `*args`: Variable length argument list for the task function.
  - `**kwargs`: Arbitrary keyword arguments for the task function.
- **Returns**:
  - `list`: Results of the tasks.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
```

## cd_multi_tasker.py

Here's the code for `cd_multi_tasker.py`:

```python
import concurrent.futures

class MultiTasking:
    def __init__(self, max_workers):
        """
        Initialize the MultiTasking class with the maximum number of workers.
        
        Parameters:
            max_workers (int): Maximum number of concurrent tasks.
        """
        self.max_workers = max_workers

    def run_cpu_bound_tasks(self, tasks, task_func, *args, **kwargs):
        """
        Executes multiple CPU-bound tasks concurrently using multiprocessing.
        
        Parameters:
            tasks (list): List of tasks to be processed (e.g., file paths for processing).
            task_func (callable): Function to run for each task.
            *args: Variable length argument list for the task function.
            **kwargs: Arbitrary keyword arguments for the task function.
        
        Returns:
            list: Results of the tasks.
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {executor.submit(task_func, task, *args, **kwargs): task for task in tasks}
            results = []
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append(f"Task {task} resulted in error: {str(e)}")
        return results

    def run_io_bound_tasks(self, tasks, task_func, *args, **kwargs):
        """
        Executes multiple I/O-bound tasks concurrently using multithreading.
        
        Parameters:
            tasks (list): List of tasks to be processed (e.g., URLs for web requests).
            task_func (callable): Function to run for each task.
            *args: Variable length argument list for the task function.
            **kwargs: Arbitrary keyword arguments for the task function.
        
        Returns:
            list: Results of the tasks.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {executor.submit(task_func, task, *args, **kwargs): task for task in tasks}
            results = []
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append(f"Task {task} resulted in error: {str(e)}")
        return results
```

