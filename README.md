# Voice Anomaly Detection System

A Python-based voice recognition and anomaly detection system that can identify users by their voice patterns and detect potential security threats.

## Features

- Voice-based user authentication
- Real-time voice pattern analysis (In progress)
- Anomaly detection and alerting
- Voice similarity scoring
- MongoDB-based user profile storage
- RESTful API endpoints
- Command-line interface

## Prerequisites

- Python 3.8 or higher
- MongoDB (local or cloud instance)
- Git

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Voice-anomaly
```

### 2. Set Up Virtual Environment

Navigate to the backend directory and create a virtual environment:

```bash
cd Voice-anomaly/backend
python -m venv venv
```

### 3. Activate Virtual Environment

**On Windows:**
```bash
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure MongoDB

Make sure MongoDB is running on your system. The application will automatically connect to `mongodb://localhost:27017/voice_anomaly`.

If you're using a different MongoDB connection, update the connection string in `db/mongo_client.py`.

## Usage

### Starting the Flask Server

1. **Activate the virtual environment** (if not already activated):
   ```bash
   .\venv\Scripts\Activate.ps1  # Windows
   # or
   source venv/bin/activate     # macOS/Linux
   ```

2. **Start the Flask server**:
   ```bash
   python app.py
   ```

The server will start on `http://127.0.0.1:5000` with debug mode enabled.

### Using the Command Line Interface (CLI)

The CLI tool allows you to check voice samples and enroll new users.

#### Basic Usage

```bash
python voice_cli.py <path_to_audio_file>
```

#### Examples

1. **Check if a voice is recognized**:
   ```bash
   python voice_cli.py ..\data\heavy_voice.mp3
   ```

2. **Check with a different voice sample**:
   ```bash
   python voice_cli.py ..\data\normal.mp3
   ```

#### CLI Workflow

1. **Voice Recognition**: The CLI sends the audio file to the server for analysis
2. **Match Found**: If the voice matches a registered user, access is granted
3. **No Match**: If the voice is not recognized, you'll see a warning and options:
   - Add as a new user
   - Cancel the operation

#### CLI Output Examples

**Successful Recognition:**
```
Checking voice sample against database...

Voice recognized! User: mishabharti
Access Granted - Welcome back!
```

**Unrecognized Voice:**
```
Checking voice sample against database...

WARNING: Voice not recognized in database!
This could indicate:
   • A new user trying to access the system
   • A potential security threat (voice impersonation)
   • Audio quality issues or background noise

Would you like to add this as a new user? (y/n): y
Enter the name of the user to register: john_doe

SECURITY NOTICE: Adding new user 'john_doe' to the voice recognition system.
This action will grant access to the system for this voice pattern.
Confirm add user 'john_doe' with this voice sample? (y/n): y

User 'john_doe' successfully enrolled in voice recognition system!
   Voice pattern registered and access granted.
```

### Using the REST API

The system provides several REST endpoints for programmatic access.

#### Base URL
```
http://127.0.0.1:5000
```

#### Available Endpoints

##### 1. Voice Monitoring (Check Voice)

**Endpoint:** `POST /monitor/start`

**Description:** Check if a voice sample matches any registered user

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Form data with key `"audio"` containing the audio file

**Postman Setup:**
1. Create a new POST request to `http://127.0.0.1:5000/monitor/start`
2. Go to the "Body" tab
3. Select "form-data"
4. Add a key named `"audio"` with type "File"
5. Select your audio file
6. Send the request

**Response Examples:**

*Voice Recognized:*
```json
{
  "status": "exists",
  "user": "mishabharti",
  "scores": {
    "voice_similarity": 85.2,
    "behavior_match": 78.5,
    "risk_score": 0.15,
    "risk_level": "LOW",
    "verdict": "Normal"
  }
}
```

*Voice Not Recognized:*
```json
{
  "status": "not_found",
  "message": "Voice not recognized in database"
}
```

##### 2. User Enrollment

**Endpoint:** `POST /user/enroll`

**Description:** Register a new user with voice samples

**Request:**
- Method: `POST`
- Content-Type: `application/json`
- Body: JSON with user_id and audio_paths

**Postman Setup:**
1. Create a new POST request to `http://127.0.0.1:5000/user/enroll`
2. Go to the "Body" tab
3. Select "raw" and choose "JSON"
4. Add the following JSON:
```json
{
  "user_id": "new_user",
  "audio_paths": ["path/to/audio1.mp3", "path/to/audio2.mp3"]
}
```
5. Send the request

**Response:**
```json
{
  "status": "User enrolled",
  "user_id": "new_user"
}
```

##### 3. Get All Users

**Endpoint:** `GET /user/all_users`

**Description:** Retrieve all registered users

**Postman Setup:**
1. Create a new GET request to `http://127.0.0.1:5000/user/all_users`
2. Send the request

**Response:**
```json
[
  {
    "user_id": "mishabharti",
    "embedding": [...],
    "behavior": {
      "pitch_avg": 150.5,
      "tempo_avg": 120.3,
      "mfcc_avg": [...]
    },
    "created_at": "2024-01-15T10:30:00.000Z"
  }
]
```

##### 4. Get Recent Alerts

**Endpoint:** `GET /alerts/recent`

**Description:** Get recent security alerts

**Postman Setup:**
1. Create a new GET request to `http://127.0.0.1:5000/alerts/recent`
2. Send the request

**Response:**
```json
[
  {
    "user_id": "mishabharti",
    "scores": {
      "voice_similarity": 45.2,
      "behavior_match": 30.1,
      "risk_score": 0.75,
      "risk_level": "HIGH",
      "verdict": "Possible impersonation"
    },
    "timestamp": "2024-01-15T10:30:00.000Z",
    "status": "PENDING"
  }
]
```

## Audio File Requirements

- **Format**: MP3, WAV, or other common audio formats
- **Quality**: Clear audio with minimal background noise
- **Duration**: 3-10 seconds recommended
- **Content**: Speech or voice samples (not music)

## System Architecture

```
Voice-anomaly/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── voice_cli.py          # Command-line interface
│   ├── requirements.txt      # Python dependencies
│   ├── core/
│   │   ├── embeddings.py     # Voice embedding extraction
│   │   ├── feature_extraction.py  # Audio feature analysis
│   │   ├── scoring.py        # Similarity scoring algorithms
│   │   └── utils.py          # Utility functions
│   ├── db/
│   │   ├── crud.py           # Database operations
│   │   └── mongo_client.py   # MongoDB connection
│   └── routes/
│       ├── user.py           # User management endpoints
│       ├── voice_monitor.py  # Voice monitoring endpoints
│       └── alerts.py         # Alert management endpoints
└── data/
    ├── heavy_voice.mp3       # Sample audio files
    ├── normal.mp3
    └── ...
```

## Troubleshooting

### Common Issues

1. **Connection Error**: Make sure the Flask server is running
2. **MongoDB Connection**: Ensure MongoDB is running and accessible
3. **Audio Processing**: Check that audio files are valid and readable
4. **Virtual Environment**: Always activate the virtual environment before running commands

### Debug Mode

The Flask server runs in debug mode by default, which provides detailed error messages and automatic reloading when code changes.

### Logs

Check the terminal output for detailed logs and error messages. The system provides verbose logging for debugging purposes.

## Security Considerations

- Voice patterns are stored as mathematical embeddings, not raw audio
- Similarity thresholds can be adjusted for security vs. usability
- All API endpoints should be secured in production
- Consider implementing rate limiting for production use

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
