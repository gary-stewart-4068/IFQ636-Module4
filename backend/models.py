""" models.py
Defines the Job hierarchy (parent + child classes).
Polymorphism: each subclass implements its own execute().
"""
from datetime import datetime

class Job:
    """Parent/base class shared by all job types."""
    def __init__(self, job_id: int, description: str) -> None:
        self.job_id = job_id
        self.description = description
        self.status = "pending"
        # encapsulated attribute
        self.__logs = []
        self.start_time = None
        self.end_time = None

    def execute(self) -> None:
        """Must be overridden by subclasses."""
        raise NotImplementedError("Each job must implement its own execution logic.")

    def mark_done(self) -> None: 
        self.status = "completed"
        self.add_log("Job completed successfully")

    def add_log(self, message: str) -> None:
        self.__logs.append(message)

    def get_logs(self) -> list:
        return list(self.__logs)

    def start(self) -> None:
        self.start_time = datetime.now()
        self.add_log(f"Started at {self.start_time}")

    def end(self) -> None:
        self.end_time = datetime.now()
        self.add_log(f"Ended at {self.end_time}")

    def get_duration(self):
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    def __repr__(self) -> str:
        return f"<Job id={self.job_id} status={self.status}desc='{self.description}'>"

class EmailJob(Job):
    """Child class: sends an email."""
    def __init__(self, job_id: int, recipient: str) -> None:
        # super() calls parent constructor (DRY)
        super().__init__(job_id, f"Send email to {recipient}") 
        self.recipient = recipient

    def execute(self) -> None:
        self.add_log(f"Email send started for {self.recipient}")
        print(f"Sending email to {self.recipient}...")
        self.mark_done()

class DataProcessingJob(Job):
    """Child class: processes a dataset.""" 
    def __init__(self, job_id: int, dataset: str) -> None:
        super().__init__(job_id, f"Process dataset {dataset}")
        self.dataset = dataset

    def execute(self) -> None:
        self.add_log(f"Process dataset {self.dataset}")
        print(f"Processing dataset {self.dataset}...")
        self.mark_done()

class PriorityJob(Job):
    """
    Child class: represents a high-priority job.
    """
    def __init__(self, job_id: int, description: str, priority: int) -> None:
        super().__init__(job_id, description)
        self.priority = priority

    def execute(self) -> None:
        self.add_log(f"Priority {self.priority} job started")
        print(f"Executing PRIORITY {self.priority} job: {self.description}")
        self.mark_done()

    def __repr__(self) -> str:
        return (f"<PriorityJob id={self.job_id} priority={self.priority} status={self.status}>")

class RetryableJob(Job):
    """
    Child class: retries execution when failures occur.
    """
    def __init__(self, job_id: int, description: str, max_retries: int = 3) -> None:
        super().__init__(job_id, description)
        self.max_retries = max_retries

    def execute(self) -> None:
        for attempt in range(1, self.max_retries + 1):
            try:
                self.add_log(f"Attempt {attempt} started")
                print(f"Job {self.job_id}: Attempt {attempt}")
                # Simulated failure
                import random
                if random.random() < 0.5:
                    raise Exception("Simulated failure")
                self.add_log(f"Attempt {attempt} succeeded")
                self.mark_done()
                return
            except Exception as e:
                self.add_log(f"Attempt {attempt} failed: {e}")
                print(f"Job {self.job_id} failed on attempt {attempt}")
        self.add_log(f"Failed after {self.max_retries} attempts")