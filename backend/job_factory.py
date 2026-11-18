"""
job_factory.py
Factory for creating job objects.
"""

from models import EmailJob, DataProcessingJob, PriorityJob, RetryableJob

class JobFactory:

    @staticmethod
    def create_job(job_type, job_id, *args):

        if job_type == "email":
            return EmailJob(job_id, args[0])

        elif job_type == "data":
            return DataProcessingJob(job_id, args[0])

        elif job_type == "priority":
            return PriorityJob(job_id, args[0], args[1])

        elif job_type == "retry":
            return RetryableJob(job_id, args[0], args[1])

        raise ValueError(f"Unknown job type: {job_type}")