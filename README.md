# Project Title: Delivery Fee Calculator

## Overview
This project implements a delivery fee calculator for a delivery service. The calculator takes into account various factors like cart value, delivery distance, number of items, and time of order to calculate the total delivery fee.
## Introduction
This project is built using FastAPI, focusing on efficient data handling and validation with an emphasis on minimalistic and effective coding practices.

## Validation
As I transitioned from Django REST Framework to FastAPI for this project, I encountered a learning curve. Initially, I faced a challenge with Pydantic due to the 422 error code "Unprocessable Entity". However, I preferred the 400 status code, which indicates a "Bad Request" from the user's side. To address this, I developed custom data validation functions. This approach not only resolved the ambiguity of the errors but also made the error messages more informative and user-friendly. However, it's worth noting that this enhancement resulted in an increase in the overall size of the codebase.

After a thorough review and considering the requirement for concise code, I refined my approach. I limited custom data validation exclusively to the 'time' item, entrusting Pydantic with the remainder of data validation tasks. This shift not only aligned with the project's guidelines for lean code but also leveraged Pydantic's robust built-in capabilities for efficient and accurate data validation.

It is important to note that Pydantic, a data validation and settings management library in Python, automatically converts data types based on the annotations you provide in your model. If you define a model attribute as an int, but pass a string that can be converted to an integer, Pydantic will attempt to convert that string to an integer during model instantiation.

For instance in this project, I used BaseModel to define the data model for the request body. The model attributes are annotated with the data type of each attribute. When the API receives a request, Pydantic will automatically convert the request body to the model object, and if the request body contains an invalid data type, Pydantic will raise an error.

For integer items, I used int = Field(..., gt=0) to ensure that the value is greater than zero. Similarly, for other interger items, I used the same approach. But for time, I used a custom validation function to ensure that the time is in UTC and the date is not before a specific historical date (e.g., the founding of the Wolt company).

Every functions they have their own docstring to explain what the function does and what are the parameters and return values.

## Files Description
1. **calculation.py**: Contains the `FeeCalculator` class which implements methods to calculate the total delivery fee based on cart items. It includes functions for calculating fees based on cart value, delivery distance, and number of items, as well as applying a rush hour multiplier.

2. **constants.py**: Defines various constants used in the fee calculation, such as thresholds for free delivery, minimum purchase requirements, and maximum delivery fee.

3. **main.py**: The main script that uses FastAPI to create an API endpoint `/calculate_cost/`. It receives cart items details, validates the time format using ISO 8601, checks the date-time validity, and calculates the delivery fee.

4. **time_validity.py**: Contains a function to validate the datetime object ensuring it is in UTC and the date is not before a specific historical date (e.g., the founding of the Wolt company).

5. **test.py**: Contains a comprehensive suite of automated tests designed to ensure the reliability and correctness of the Delivery Fee Calculator's functionality.

6. **requirements.txt**: Contains the list of dependencies to be installed using pip.

7. **Dockerfile**: Contains the instructions to build a Docker image for the project.

8. **docker-compose.yml**: Contains the instructions to run the project in a Docker container.

## Testing

The `test.py` file contains a comprehensive suite of automated tests designed to ensure the reliability and correctness of the Delivery Fee Calculator's functionality. The tests are implemented using FastAPI's `TestClient`, facilitating the simulation of API requests and responses without the need for a running server.

### Test Structure

The tests are organized within the `TestCalculateCost` class, which encapsulates various test scenarios to verify the calculator's behavior under different conditions. These scenarios include:

- **No Payload**: Validates the API's response when no data is submitted.
- **Correct Data Variants**: Tests various combinations of input data to ensure the calculator returns the correct delivery fee.
- **Missing Required Fields**: Checks the API's error handling when required fields are omitted in the request.
- **Incorrect Field Names**: Verifies that the API correctly identifies requests with incorrect field names.
- **Invalid Field Values**: Ensures that the API handles cases where input fields have invalid values, such as negative numbers.
- **Date-Related Errors**: Tests the API's response to date and time-related errors, such as requests with dates before the company's founding or incorrectly formatted timezone information.
- **Correct Time Format**: Confirms that the API correctly processes requests with valid date and time formats.

Each test case within these scenarios uses a helper function, `post_calculate_cost`, to send POST requests to the `/calculate_cost/` endpoint and assert the expected outcomes based on status codes, response payloads, and error messages.

## Project Usage
For macOS, linux and windows users, the following commands can be used to run the project:

### Without Docker
**Prerequisites**
* Python 3.10 or later: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Pipenv: [https://pipenv.pypa.io/en/latest/installation.html](https://pipenv.pypa.io/en/latest/installation.html)

** Steps to run the project:**

Make sure you have pipenv installed. If not, run the following command:

Windows users can use the following command to install 'pipenv' after installing Python.

    ```bash
    pip install pipenv
    ```

Linux/Mac Users can use the following command to install 'pipenv' after installing LinuxBrew.

    ```bash
    brew install pipenv
    ```

1. Make sure you are in the root folder of "My assignment"

    ```bash
    pipenv shell       # this command creates a virtual environment
    pipenv install      # this command installs all the requirements from requirements.txt
    uvicorn app.main:app --reload   #if you are in the root folder of "My assignment" use this command
    uvicorn main:app --reload   # if you are in the app folder, use this command
    ```

2. To execute `test.py`:

    ```bash
    pytest test/test.py -vv
    ```
The API will return the calculated delivery fee.
This command will initiate the pytest framework, executing each test case in `test.py` and providing a detailed output of each test's result, including which tests passed, failed, and any associated error messages for failures.

## Another way to activate the virtual environment and install the dependencies is as follows:

Create a virtual environment:
```
python -m venv .venv
```

Activate the virtual environment:

* Linux / MacOS:
    ```
    source .venv/bin/activate
    ```
* Windows (CMD):
    ```
    .venv/Scripts/activate.bat
    ```

* Windows (Powershell)
    ```
    .venv/Scripts/Activate.ps1
    ```
Install the dependencies:

```bash
pip install -r requirements.txt
```


## Docker

To run the project in a Docker container, follow these commands:

1. Make sure you are in the root folder of "My assignment"

    ```bash
    docker-compose up --build
    ```
2. To execute `test.py`:

    ```bash
    docker-compose run deliveryfee-api pytest test/test.py -vv
    ```
The API will return the calculated delivery fee.
This command will initiate the pytest framework, executing each test case in `test.py` and providing a detailed output of each test's result, including which tests passed, failed, and any associated error messages for failures.

## Conclusion
This project showcases my skills in backend development, particularly in building scalable APIs with Python and FastAPI. It demonstrates my understanding of RESTful principles and my ability to write clean, efficient, and well-documented code.
