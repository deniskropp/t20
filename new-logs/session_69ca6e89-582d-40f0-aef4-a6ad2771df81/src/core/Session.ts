import { Session as SessionBase } from '../core/Session';
import { Agent } from '../agent/Agent';
import { Logger } from '../logger/Logger';
import { Plan, Task, File, Artifact } from '../custom_types';
import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { glob } from 'glob';
import { v4 as uuidv4 } from 'uuid';

const logger = Logger.getInstance();

// Constants for directory and file names
const AGENTS_DIR_NAME = 'agents';
const CONFIG_DIR_NAME = 'config';
const PROMPTS_DIR_NAME = 'prompts';
const RUNTIME_CONFIG_FILENAME = 'runtime.yaml';

export class Session extends SessionBase {
  public agents: Agent[];
  public projectRoot: string;
  public sessionDir: string;
  public sessionId: string;
  public state: string;
  public config: Record<string, any> = {};

  constructor(agents: Agent[], projectRoot: string) {
    super(); // Call base constructor if it exists and needs initialization
    this.sessionId = `session_${uuidv4()}`;
    this.agents = agents;
    this.projectRoot = projectRoot;
    this.sessionDir = path.join(this.projectRoot, 'sessions', this.sessionId);
    this.state = 'initialized';

    // Ensure session directory exists
    fs.mkdirSync(this.sessionDir, { recursive: true });
    logger.info(`Session created: ${this.sessionId} in directory ${this.sessionDir}`);

    // Load configuration during session initialization
    this.config = this._loadConfig(path.join(this.projectRoot, CONFIG_DIR_NAME, RUNTIME_CONFIG_FILENAME));
    const logLevel = this.config.loggingLevel || 'INFO';
    Logger.setup(logLevel); // Setup logging based on config
  }

  /**
   * Adds an artifact to the session.
   * @param name Name of the artifact file.
   * @param content Content of the artifact. Can be string, object, or array.
   */
  public async addArtifact(name: string, content: any): Promise<void> {
    const artifactPath = path.join(this.sessionDir, name);
    try {
      // Ensure directory exists
      await fs.promises.mkdir(path.dirname(artifactPath), { recursive: true });

      let dataToWrite: string;
      if (typeof content === 'string') {
        dataToWrite = content;
      } else {
        // Assume JSON serializable content (object, array, etc.)
        dataToWrite = JSON.stringify(content, null, 2);
      }

      await fs.promises.writeFile(artifactPath, dataToWrite, 'utf-8');
      logger.info(`Artifact '${name}' saved in session ${this.sessionId}.`);
    } catch (error) {
      logger.error(`Error saving artifact '${name}' to ${artifactPath}:`, error);
      // Consider re-throwing or handling the error appropriately
    }
  }

  /**
   * Retrieves an artifact from the session.
   * @param name Name of the artifact file.
   * @returns The content of the artifact, or null if not found or error occurs.
   */
  public async getArtifact(name: string): Promise<any | null> {
    const artifactPath = path.join(this.sessionDir, name);
    try {
      const content = await fs.promises.readFile(artifactPath, 'utf-8');
      // Attempt to parse as JSON if the filename suggests it
      if (name.endsWith('.json')) {
        try {
          return JSON.parse(content);
        } catch (e) {
          logger.warn(`Failed to parse artifact '${name}' as JSON, returning raw content. Error: ${(e as Error).message}`);
          return content; // Return raw content if JSON parsing fails
        }
      }
      return content;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        logger.warn(`Artifact '${name}' not found in session ${this.sessionId}.`);
      } else {
        logger.error(`Error retrieving artifact '${name}' from ${artifactPath}:`, error);
      }
      return null;
    }
  }

  // Helper method to load configuration (can be moved to a dedicated config service)
  private _loadConfig(configPath: string): Record<string, any> {
    logger.info(`Loading configuration from: ${configPath}`);
    try {
      const configFileContent = fs.readFileSync(configPath, 'utf-8');
      const config = yaml.load(configFileContent) as Record<string, any>;
      logger.info('Configuration loaded successfully.');
      return config;
    } catch (error) {
      logger.error(`Error loading configuration from ${configPath}:`, error);
      return {}; // Return empty config if file not found or error occurs
    }
  }

  // Placeholder for other Session methods if needed
}
