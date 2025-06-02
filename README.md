# Auto-Sorpresa de Cumpleaños

This is a simple web application for organizing a surprise birthday party. Users can submit their name, email, and volunteer to help organize. The data is saved to a CSV file.

## Features

- Web form for user input (Name, Email, Volunteer Status)
- Data saved to `leads.csv`
- Basic HTML styling
- Confirmation page after submission
- Docker support for containerization
- Basic Terraform configuration for infrastructure management (example)

## Prerequisites

- Python 3.7+
- Flask (`pip install -r requirements.txt`)
- Docker (for containerized deployment)
- Terraform (for infrastructure management)

## Running the Application

### Directly with Python

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will be available at `http://localhost:5000` (or `http://0.0.0.0:5000`).

### Using Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t birthday-surprise-app .
    ```
2.  **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 birthday-surprise-app
    ```
    The application will be available at `http://localhost:5000`.

## Terraform Configuration

A basic Terraform configuration (`main.tf`) is included as an example. It uses the `local` provider to create an informational file.

1.  **Initialize Terraform:**
    ```bash
    terraform init
    ```
2.  **Apply the configuration:**
    ```bash
    terraform apply -auto-approve
    ```
    This will create a `terraform_info.txt` file in the project directory.

    **Note:** This Terraform configuration is a placeholder. For a real-world deployment, you would replace it with configurations for your chosen cloud provider and resources (e.g., VMs, databases, load balancers).

## Files

-   `app.py`: Main Flask application file.
-   `requirements.txt`: Python dependencies.
-   `templates/`: Directory for HTML templates.
    -   `index.html`: Main landing page.
    -   `success.html`: Confirmation page.
-   `static/`: Directory for static files.
    -   `style.css`: CSS styles.
-   `leads.csv`: File where submitted data is stored.
-   `Dockerfile`: For building the Docker image.
-   `main.tf`: Example Terraform configuration.
