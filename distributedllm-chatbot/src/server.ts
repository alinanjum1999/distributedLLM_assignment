import { spawn } from 'child_process';
import * as path from 'path';

// Define the path to the Python script
const PYTHON_SCRIPT = path.join(__dirname, '..', 'chatbot.py');

// Function to start the Python script using the `panel serve` command
function startPythonScript() {
  const pythonProcess = spawn('panel', ['serve', PYTHON_SCRIPT]);

  // Capture and log the Python script's stdout output
  pythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  // Capture and log the Python script's stderr output
  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  // Log when the Python script exits
  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
  });
}

// Start the Python script when the server starts
startPythonScript();
