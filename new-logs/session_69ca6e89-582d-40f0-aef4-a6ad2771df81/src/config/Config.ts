import { readFileSync } from 'fs';
import { join } from 'path';
import yaml from 'js-yaml';
import { Logger } from '../logger/Logger';

const logger = Logger.getInstance();

// Interface defining the structure of the configuration object
export interface Config {
  projectRoot?: string;       // Root directory of the project
  agentDir?: string;          // Directory containing agent configurations
  promptDir?: string;         // Directory containing prompt templates
  logDir?: string;            // Directory for log files
  defaultModel?: string;      // Default LLM model to use if not specified
  workflowRounds?: number;    // Default number of workflow rounds
  // Add other configuration properties as needed
}

export class Config {
  /**
   * Loads configuration from a YAML file.
   * @param fileName The name of the configuration file (e.g., 'runtime.yaml').
   * @param basePath The base path to search for the config file (defaults to current working directory).
   * @returns A Promise resolving to the loaded Config object with defaults applied.
   */
  public static async load(fileName: string, basePath: string = process.cwd()): Promise<Config> {
    const configPath = join(basePath, fileName);
    logger.info(`Attempting to load configuration from: ${configPath}`);
    try {
      // Read the file content
      const fileContents = readFileSync(configPath, 'utf-8');
      // Parse the YAML content
      const config = yaml.load(fileContents) as Config;

      // Apply default values if properties are missing
      config.projectRoot = config.projectRoot || basePath;
      config.agentDir = config.agentDir || 'agents';
      config.promptDir = config.promptDir || 'prompts';
      config.logDir = config.logDir || 'logs';
      config.defaultModel = config.defaultModel || 'gemini-2.5-flash-lite';
      config.workflowRounds = config.workflowRounds || 3;

      logger.info('Configuration loaded successfully.');
      return config;
    } catch (error) {
      logger.error(`Failed to load configuration from ${configPath}:`, error);
      // In case of failure, return a default configuration to allow the system to start
      // Alternatively, you might want to throw an error to halt execution
      return {
        projectRoot: basePath,
        agentDir: 'agents',
        promptDir: 'prompts',
        logDir: 'logs',
        defaultModel: 'gemini-2.5-flash-lite',
        workflowRounds: 3,
      };
    }
  }
}
