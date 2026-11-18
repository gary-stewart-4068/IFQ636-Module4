"""
task_manager.py
Tracks jobs by status using defaultdict(list) to avoid KeyErrors and boilerplate.
"""

from collections import defaultdict
from typing import Dict, List
from models import Job

class TaskManager: 
    def __init__(self) -> None:
        self.jobs_by_status: Dict[str, List[Job]] = defaultdict(list)

    def add_job(self, job: Job) -> None:
        self.jobs_by_status[job.status].append(job)

    def get_all(self) -> Dict[str, List[Job]]:
        return self.jobs_by_status

    def get_jobs_by_status(self, status: str) -> List[Job]: 
        return list(self.jobs_by_status.get(status, []))

    def get_all_jobs_sorted(self) -> List[Job]:
        jobs = []
        for status_jobs in self.jobs_by_status.values():
            jobs.extend(status_jobs)
        jobs.sort(
            key=lambda job: getattr(job, "priority", 0),
            reverse=True
        )
        return jobs

    def get_jobs_in_priority_order(self):
        jobs = []
        for status_jobs in self.jobs_by_status.values():
            jobs.extend(status_jobs)
        return sorted(
            jobs,
            key=lambda job: getattr(job, "priority", 0),
            reverse=True
        )