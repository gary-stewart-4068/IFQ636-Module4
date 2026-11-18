""" app.py
Build a few jobs, register them, run them, print a summary.
"""

from models import EmailJob, DataProcessingJob, PriorityJob
from task_manager import TaskManager
from executor import Executor

def build_jobs():
    return [
        EmailJob(1, "user@example.com"),
        DataProcessingJob(2, "dataset_A"),
        PriorityJob(3, "Critical Security Alert", 10),
        PriorityJob(4, "Urgent payroll processing", 5),
        EmailJob(5, "admin@example.com"),
        DataProcessingJob(6, "dataset_B"),
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
        for log in job.get_logs():
            print(f"  - {log}")