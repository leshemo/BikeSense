# BlueBike Status Website and App
Website to get status of bluebike stations in Boston.

## Tech Stack:
  - Languages:
    - TypeScript
      - HTML, CSS
    - Python
  - Tools:
    - React
    - Express
    - scikit-learn
    - pandas
    - ClaudiaJS
    - AWS Lambda
    - Android


## Workflow:
- Currently, the BlueBike API is queried on the frontend. This should be done on the backend, which as of now does not really exist but should, on AWS Lambda. 
- The python ML portion is its own Lambda function, but there are compatibility issues between the development, done on Windows, and running the Lambda on AWS's linux system.
- The frontend is a simple React website that works locally, but is not yet on AWS Lambda. Progress should be made there.
- Mobile app should just be an extremely simple widget that queries the backend and displays the result on the user's home screen. Hoping for development via Kotlin.
