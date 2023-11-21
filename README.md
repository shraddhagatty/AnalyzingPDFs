# AnalyzingPDFs-Serverless

## Overview

This project implements an Analyzing PDFs Application, built as a serverless and event-driven solution on the AWS platform. The application allows users to upload PDFs to an S3 bucket, trigger an analysis process, and retrieve the results. The analysis is performed by Lambda functions, and the user and job information is stored in a MySQL database on Amazon RDS.

## Project Structure

The application comprises two main components: Lambda functions and an API Gateway. The Lambda functions are designed to handle different aspects of the application, from managing users and jobs to uploading, analyzing, and downloading PDFs.

### Lambda Functions

1. **compute (Event-Driven Lambda):**
   - Triggered automatically when a PDF is dropped into the configured S3 bucket.
   - Downloads and analyzes the PDF, writing the results back to S3 as a .txt file.

2. **users:**
   - Returns all users from the MySQL database.

3. **jobs:**
   - Returns all jobs from the MySQL database.

4. **upload:**
   - Uploads a PDF to S3.
   - Inserts job information into the MySQL database.
   - Returns the job ID.

5. **download:**
   - Given a job ID, checks the status of the job.
   - If completed, downloads the analysis results.

6. **reset:**
   - Resets the database to its original state, removing all jobs.

### Database

- A MySQL database named "benfordapp" in RDS is used to store user information and job status.

## Getting Started

To set up and deploy the Analyzing PDFs Application, follow these steps:

1. **Database Setup:**
   - Create a MySQL database named "benfordapp" using the provided SQL script.

2. **Lambda Functions:**
   - Deploy the Lambda functions using the AWS Lambda service.
   - Ensure proper configurations, especially for the S3 bucket trigger in `compute`.

3. **API Gateway:**
   - Configure API Gateway to invoke the Lambda functions based on specific endpoints.
   - Map API functions to corresponding Lambda functions:
     - `/users` to `users`
     - `/jobs` to `jobs`
     - `/upload` to `upload`
     - `/download` to `download`
     - `/reset` to `reset`

4. **Testing:**
   - Test the application by uploading PDFs through the API and checking the status and results using the provided endpoints.

## Additional Notes

- Ensure proper IAM roles and permissions for Lambda functions to interact with S3, RDS, and other AWS services.
- Monitor AWS CloudWatch logs for Lambda functions for troubleshooting and performance optimization.
- This README serves as a high-level guide
