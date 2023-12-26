from account import Account
from applicant import Applicant
from candidate import Candidate
from company import Company
from job import Job
from database import db

from faker import Faker
import random

fake = Faker()

def create_fake_job(company):
    title = fake.job()
    description = fake.text()
    requirements = fake.text()
    salary = round(random.uniform(30000, 100000), 2)
    location = fake.city()

    job = Job(
        title=title,
        description=description,
        requirements=requirements,
        salary=salary,
        location=location,
        company=company
    )
    return job

def create_fake_data():
    companies = [Company(name=fake.company(), description=fake.text(), location=fake.city()) for _ in range(5)]
    db.session.add_all(companies)
    db.session.commit()

    for company in companies:
        for _ in range(4):
            job = create_fake_job(company)
            db.session.add(job)

    db.session.commit()

if __name__ == '__main__':
    create_fake_data()
