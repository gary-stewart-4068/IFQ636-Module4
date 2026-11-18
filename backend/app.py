""" app.py
Build a few jobs, register them, run them, print a summary.
"""

from job_factory import JobFactory
from task_manager import TaskManager
from executor import Executor

def build_jobs():
    return [
        JobFactory.create_job("email", 1, "user@example.com"),
        JobFactory.create_job("data", 2, "dataset_A" ),
        JobFactory.create_job("priority", 3, "Critical security alert", 10),
        JobFactory.create_job("priority", 4, "Urgent payroll processing", 5),
        JobFactory.create_job("email", 5, "admin@example.com"),
        JobFactory.create_job("data", 6, "dataset_B"),
        JobFactory.create_job("retry", 7, "Database backup", 3),
        JobFactory.create_job("retry", 8, "Cloud sync", 5 )
    ]

if __name__ == "__main__":
    jobs = []
    jobs = build_jobs()
    manager = TaskManager()
    for job in jobs:
        manager.add_job(job) # all start as 'pending'
    jobs = manager.get_jobs_in_priority_order()
    Executor(jobs).run()
    manager.refresh_statuses()
    print("\n=== SUMMARY ===")
    pending_jobs = [job for job in jobs if job.status == "pending"]
    completed_jobs = [job for job in jobs if job.status == "completed"]
    print(f"Pending: {len(pending_jobs)}")
    print(f"Completed: {len(completed_jobs)}")
    print(f"Pending: {len(manager.get_jobs_by_status('pending'))}")
    print(f"Completed: {len(manager.get_jobs_by_status('completed'))}")
    print("\n=== JOB LOGS ===")
    for job in jobs:
        print(f"\nJob {job.job_id}")
        duration = job.get_duration()
        if duration is not None:
            print(f"Duration: {duration:.2f} seconds")
        for log in job.get_logs():
            print(f"  - {log}")