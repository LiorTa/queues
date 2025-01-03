# FastAPI Queue Server


This FastAPI server provides a simple REST API to manage message queues with basic authentication.

Endpoints

	1.	POST /api/{queue_name}
	•	Adds a message to the specified queue.
	•	Request Body: JSON format message (e.g., {"message": "Your message here"})
	•	Authentication required.
	2.	GET /api/{queue_name}?timeout={ms}
	•	Retrieves the next message from the queue.
	•	Optional query parameter timeout: Timeout in milliseconds (default: 10000ms).
	•	Returns 204 No Content if no messages are available within the timeout.
	•	Authentication required.

Authentication

	•	Basic HTTP Authentication.
	•	Username: admin
	•	Password: password123

Prerequisites

	•	Python 3.7+ installed.
	•	pip for package management.

Installation

	1.	Clone this repository.
   2.	pip install -r requirements.txt
