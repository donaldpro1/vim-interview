# Notification Service

The Notification Service is a simple Node.js application that simulates sending notifications via email and SMS. It includes features like rate limiting and random error simulation to mimic real-world scenarios.

---

## **Features**

1. **Send Email**: Simulates sending email notifications.
2. **Send SMS**: Simulates sending SMS notifications.
3. **Rate Limiting**: Limits the number of requests per endpoint (configurable via environment variables).
4. **Random Errors**: Introduces a configurable percentage of random server errors to simulate failures.

---

## **Setup**

### **1. Prerequisites**

- [Node.js](https://nodejs.org/) (v16 or later)
- [Docker](https://www.docker.com/) (optional for containerized deployment)

### **2. Install Dependencies**

```bash
npm install
```

---

## **Running the Service**

### **1. Locally**

Start the service:

```bash
npm start
```

The service will run on `http://localhost:5001`.

### **2. With Docker**

#### Build the Docker Image:

```bash
docker build -t notification-service .
```

#### Run the Container:

```bash
docker run -p 5001:5001 -e RATE_LIMIT=2 -e ERROR_RATE=0.2 notification-service
```

The service will now be available on `http://localhost:5001`.

---

## **Environment Variables**

| Variable     | Default Value | Description                                      |
| ------------ | ------------- | ------------------------------------------------ |
| `RATE_LIMIT` | `1`           | Number of requests per second per endpoint.      |
| `ERROR_RATE` | `0.1`         | Fraction of requests that return a random error. |

---

## **Endpoints**

### **1. Send Email**

- **POST** `/send-email`

- **Description**: Simulates sending an email.
- **Request**:

  - **Body**:

    ```json
    {
      "email": "user@example.com",
      "message": "This is a test email message."
    }
    ```

- **Response**:

  - **Success (200 OK)**:

    - **Respnse Body**

      ```json
      {
        "status": "sent",
        "channel": "email",
        "to": "user@example.com",
        "message": "This is a test email message."
      }
      ```

    - **Validation Errors (400 Bad Request)**:

      ```json
      {
        "error": "Email and message are required"
      }
      ```

      ```json
      {
        "error": "Invalid email format"
      }
      ```

      ```json
      {
        "error": "Message length must be between 1 and 500 characters"
      }
      ```

  - **Internal Server Error (500)**:
    - Random Error (10% or configurable chance)
      ```json
      {
        "error": "Random server error occurred."
      }
      ```
  - **Rate Limit Exceeded (429 Too Many Requests)**:

    - **Headers**:

      - X-RateLimit-Limit
      - X-RateLimit-Remaining
      - X-RateLimit-Reset

    - **Body**:

      ```json
      {
        "error": "Too many requests, please try again later."
      }
      ```

---

### 2. Send SMS

- **POST** /send-sms

- **Description**: Simulates the sending of an SMS message.

- **Request**:

  - **Body**:

    ```json
    {
      "telephone": "+1234567890",
      "message": "This is a test SMS message."
    }
    ```

- **Response**:

  - **Success (200 OK)**:

    - **Respnse Body**
      ```json
      {
        "status": "sent",
        "channel": "sms",
        "to": "+1234567890",
        "message": "This is a test SMS message."
      }
      ```

  - **Validation Errors (400 Bad Request)**:

    - Missing `telephone` or `message`:

      ```json
      {
        "error": "Telephone and message are required"
      }
      ```

    - Invalid telephone format:

      ```json
      {
        "error": "Invalid telephone format"
      }
      ```

    - Message length out of bounds (too long or too short):

      ```json
      {
        "error": "Message length must be between 1 and 500 characters"
      }
      ```

  - **Internal Server Error (500)**:

    - Random Error (10% or configurable chance)

      ```json
      {
        "error": "Random server error occurred."
      }
      ```

  - **Rate Limit Exceeded (429 Too Many Requests)**:

    - **Headers**:

      - X-RateLimit-Limit
      - X-RateLimit-Remaining
      - X-RateLimit-Reset

    - **Body**:

      ```json
      {
        "error": "Too many requests, please try again later."
      }
      ```

---

## **Testing**

### **Send Email Example**

```bash
curl -X POST http://localhost:5001/send-email \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "message": "Hello via Email!"}'
```

### **Send SMS Example**

```bash
curl -X POST http://localhost:5001/send-sms \
-H "Content-Type: application/json" \
-d '{"telephone": "+1234567890", "message": "Hello via SMS!"}'
```

### **Rate Limit Test**

Send multiple requests quickly to observe the rate limit:

```bash
curl -X POST http://localhost:5001/send-email \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "message": "Hello!"}'
```

Expected response after exceeding the rate limit:

```json
{
  "error": "Too many requests, please try again later."
}
```

### **Random Error Test**

Repeat requests to observe random errors:

```json
{
  "error": "Random server error occurred."
}
```

---

## **Contributing**

Feel free to submit issues or pull requests for improvements or bug fixes.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```

This README provides a clear description of the Notification Service, its features, configuration options, endpoints, and examples for testing.
```
