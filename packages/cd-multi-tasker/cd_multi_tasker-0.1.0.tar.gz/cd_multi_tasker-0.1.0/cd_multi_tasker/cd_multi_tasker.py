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

