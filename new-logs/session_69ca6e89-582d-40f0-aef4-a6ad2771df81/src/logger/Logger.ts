import winston from 'winston';
import { join } from 'path';
import fs from 'fs';

// Define log levels with priorities
const logLevels = {
  error: 0,
  warn: 1,
  info: 2,
  debug: 3,
};

// Define the format for log messages
const logFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }), // Include stack trace for errors
  winston.format.splat(), // Support for string interpolation like printf
  winston.format.printf(({ level, message, timestamp, ...metadata }) => {
    // Construct the log message string
    let msg = `${timestamp} [${level.toUpperCase()}]: ${message}`;
    // Append any additional metadata (e.g., agent name, task ID)
    if (Object.keys(metadata).length > 0) {
      msg += ` ${JSON.stringify(metadata)}`;
    }
    return msg;
  })
);

// Define a format for JSON line logs (useful for log aggregation)
const jsonLogFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.json() // Output logs as JSON objects on separate lines
);

// Ensure the log directory exists
const logDir = process.env.LOG_DIR || 'logs'; // Use LOG_DIR environment variable or default to 'logs'
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

const logFilePath = join(logDir, 'app.log');
const jsonLogFilePath = join(logDir, 'app.jsonl');

export class Logger {
  private static instance: winston.Logger;

  /**
   * Gets the singleton Winston logger instance.
   * Configures transports for console, file (plain text), and file (JSONL).
   * @returns The configured Winston logger instance.
   */
  public static getInstance(): winston.Logger {
    if (!Logger.instance) {
      Logger.instance = winston.createLogger({
        level: process.env.LOG_LEVEL || 'info', // Set log level from environment or default to 'info'
        levels: logLevels,
        format: logFormat, // Default format for transports unless overridden
        transports: [
          // Console transport: Outputs logs to the console with colorization
          new winston.transports.Console({
            format: winston.format.combine(
              winston.format.colorize({ all: true }), // Apply colors to all levels
              logFormat
            ),
          }),
          // File transport: Logs to 'app.log' in plain text format
          new winston.transports.File({
            filename: logFilePath,
            level: process.env.LOG_LEVEL || 'info',
            format: logFormat,
            maxsize: 1024 * 1024 * 5, // Max log file size: 5MB
            tailable: true, // Allows log rotation
          }),
          // JSONL File transport: Logs to 'app.jsonl' in JSON format
          new winston.transports.File({
            filename: jsonLogFilePath,
            level: process.env.LOG_LEVEL || 'info',
            format: jsonLogFormat,
            maxsize: 1024 * 1024 * 5, // Max log file size: 5MB
            tailable: true,
          }),
        ],
        // Handle uncaught exceptions
        exceptionHandlers: [
          new winston.transports.Console({
             format: winston.format.combine(winston.format.colorize({ all: true }), logFormat)
          }),
          new winston.transports.File({
            filename: logFilePath,
            format: logFormat,
          }),
          new winston.transports.File({
            filename: jsonLogFilePath,
            format: jsonLogFormat,
          }),
        ]
      });

      // Optional: Add a listener for logger errors
      Logger.instance.on('error', (err) => {
        console.error('Winston logger encountered an error:', err);
      });
    }
    return Logger.instance;
  }
}
