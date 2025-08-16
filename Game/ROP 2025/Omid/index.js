const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const logsDir = path.join(__dirname, 'logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir);
}

const logFilePath = path.join(logsDir, 'progress-log.json');

// Initialize log file if it doesn't exist
if (!fs.existsSync(logFilePath)) {
  fs.writeFileSync(logFilePath, '[]');
}

app.post('/api/submit-progress', (req, res) => {
  try {
    const progressData = req.body;

    // Validate required fields
    const requiredFields = ['username', 'pcr_completed', 'dna_matches_found', 'mistakes_made', 'time_spent', 'timestamp'];
    const missingFields = requiredFields.filter(field => !(field in progressData));

    if (missingFields.length > 0) {
      return res.status(400).json({
        error: 'Missing required fields',
        missingFields: missingFields
      });
    }

    // Add server timestamp for logging purposes
    const logEntry = {
      ...progressData,
      server_timestamp: Date.now() / 1000,
      logged_at: new Date().toISOString()
    };

    // Log to console
    console.log('Progress submission received:');
    console.log(JSON.stringify(logEntry, null, 2));

    // Read existing log data
    const existingData = JSON.parse(fs.readFileSync(logFilePath, 'utf8'));

    // Append new entry
    existingData.push(logEntry);

    // Write back to file
    fs.writeFileSync(logFilePath, JSON.stringify(existingData, null, 2));

    // Send success response
    res.status(200).json({
      message: 'Progress data logged successfully',
      timestamp: logEntry.server_timestamp
    });

  } catch (error) {
    console.error('Error processing progress submission:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Progress submissions will be logged to: ${logFilePath}`);
});
