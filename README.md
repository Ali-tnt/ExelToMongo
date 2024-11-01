# Excel to MongoDB FastAPI Project

A FastAPI application that handles Excel file uploads containing phone numbers, stores them in MongoDB, and provides CRUD operations. The project includes Docker support and testing.

## Features

- FastAPI REST API
- MongoDB integration
- Excel file processing
- Docker support
- Unit tests
- Complete CRUD operations
- Performance metrics

## Project Structure

```
excel-to-mongodb/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── routes.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Prerequisites

- Python 3.8+
- Docker and Docker Compose (optional)
- MongoDB

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd excel-to-mongodb
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory:
```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=exelToMongoDB
COLLECTION_NAME=phoneNumbers
```

## Running the Application

### Without Docker

1. Start MongoDB:
```bash
# Make sure MongoDB is running on localhost:27017
```

2. Run the FastAPI application:
```bash
uvicorn app.main:app --reload
```

### With Docker

1. Build and run the containers:
```bash
docker-compose up --build
```

## API Endpoints

### Upload Excel File
- **POST** `/upload-excel/`
  - Upload Excel file with phone numbers
  - Returns processing time and count of records

### CRUD Operations
- **GET** `/phones/` - Get all phone numbers
- **GET** `/phones/{phone_number}` - Get specific phone number
- **PUT** `/phones/{phone_number}` - Update phone number
- **DELETE** `/phones/{phone_number}` - Delete phone number

## Testing

Run tests using pytest:
```bash
pytest
```

## Excel File Format

The Excel file should have a column named "mobile" containing phone numbers. Example:

| mobile      |
|-------------|
| 1234567890  |
| 9876543210  |

## Performance Optimization

The application uses:
- Bulk inserts for better performance
- Async operations with Motor
- Proper indexing on MongoDB
- Chunked processing for large files

## Common Issues and Solutions

1. MongoDB Connection Issues:
   - Verify MongoDB is running
   - Check connection string in .env file
   - Ensure network connectivity

2. Excel File Issues:
   - Verify column name is exactly "mobile"
   - Ensure file is in .xlsx format
   - Check file permissions

3. Performance Issues:
   - Increase chunk size for larger files
   - Verify MongoDB indexes
   - Monitor memory usage

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
