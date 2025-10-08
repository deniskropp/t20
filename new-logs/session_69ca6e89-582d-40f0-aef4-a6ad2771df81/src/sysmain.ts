import os from 'os';
import path from 'path';
import fs from 'fs';
import minimist from 'minimist';

import { Logger } from './logger/Logger';
import { System } from './system/System';
import { File } from './custom_types';

const logger = Logger.getInstance();

/**
 * Parses command-line arguments for the runtime system.
 * @returns Parsed arguments object.
 */
function parseCommandLineArguments(): minimist.ParsedArgs {
  const args = minimist(process.argv.slice(2), {
    alias: {
      rounds: ['r'],
      files: ['f'],
      planOnly: ['p'],
      orchestrator: ['o'],
      model: ['m'],
      help: ['h'],
    },
    default: {
      rounds: 1,
      planOnly: false,
      orchestrator: 'Meta-AI', // Default orchestrator name
      model: 'gemini-2.5-flash-latest', // Default LLM model
    },
    string: ['task', 'orchestrator', 'model'],
    boolean: ['planOnly', 'help'],
    unknown: (arg) => {
      // Handle unknown arguments or log a warning
      logger.warn(`Unknown argument ignored: ${arg}`);
      return false; // Indicate that the argument is not recognized
    }
  });

  // Basic validation
  if (args.help) {
    printHelp();
    process.exit(0);
  }
  if (!args.task) {
    console.error("Error: The 'task' argument is required.\n");
    printHelp(); // Show help if task is missing
    process.exit(1);
  }
  if (args.rounds < 1) {
    console.error("Error: Number of rounds must be at least 1.\n");
    process.exit(1);
  }

  return args;
}

/**
 * Prints the help message for the command-line interface.
 */
function printHelp(): void {
  console.log(`
Usage: ts-node src/sysmain.ts <task> [options]
`);
  console.log("Options:");
  console.log("  -p, --plan-only     Generate only the plan without executing tasks.");
  console.log("  -r, --rounds <n>    The number of rounds to execute the workflow (default: 1).");
  console.log("  -f, --files <f1 f2...> List of files to be used in the task (e.g., README.md).");
  console.log("  -o, --orchestrator <name> The name of the orchestrator agent to use (default: Meta-AI).");
  console.log("  -m, --model <name>  Default LLM model to use (e.g., 'gemini-2.5-flash-latest').");
  console.log("  -h, --help          Show this help message.");
  console.log("\nArguments:");
  console.log("  task                The initial task or goal for the orchestrator to perform.");
}

/**
 * Sets up the application's logging configuration.
 * @param logLevel The desired logging level (e.g., 'DEBUG', 'INFO').
 */
function setupApplicationLogging(logLevel: string = 'INFO'): void {
  try {
    Logger.setup(logLevel); // Use the static setup method of the Logger class
    logger.info(`Logging initialized with level: ${logLevel}`);
  } catch (e) {
    console.error(`Error setting up logging: ${(e as Error).message}`);
    // Proceed without logging if setup fails, or exit if logging is critical
  }
}

/**
 * Reads and processes input files specified by command-line arguments.
 * @param filePaths Array of file paths.
 * @returns An array of File objects.
 */
function processInputFiles(filePaths: string[]): File[] {
  const fileObjects: File[] = [];
  if (!filePaths || filePaths.length === 0) {
    return fileObjects;
  }

  for (const filePath of filePaths) {
    try {
      // Resolve to absolute path to avoid issues with relative paths
      const absolutePath = path.resolve(filePath);
      if (!fs.existsSync(absolutePath)) {
        logger.warn(`Input file not found, skipping: ${absolutePath}`);
        continue;
      }
      const content = fs.readFileSync(absolutePath, 'utf-8');
      // Use the relative path from the project root for consistency in artifacts
      const relativePath = path.relative(process.cwd(), absolutePath);
      fileObjects.push(new File({ path: relativePath, content }));
      logger.debug(`Processed input file: ${absolutePath} (stored as: ${relativePath})`);
    } catch (error) {
      logger.error(`Error processing file '${filePath}':`, error);
    }
  }
  return fileObjects;
}

/**
 * Main entry point for the Node.js runtime system.
 */
async function systemMain(): Promise<void> {
  let args: minimist.ParsedArgs;
  try {
    args = parseCommandLineArguments();
  } catch (error) {
    // Error already logged by parseCommandLineArguments or setupApplicationLogging
    process.exit(1);
    return;
  }

  // Determine project root relative to the current working directory
  const projectRoot = path.resolve(process.cwd()); 
  logger.info(`Project root determined as: ${projectRoot}`);

  // 1. Initial logging setup (can be reconfigured later by system config)
  setupApplicationLogging('INFO'); // Start with INFO level

  // 2. Process input files
  const inputFiles = processInputFiles(args.files as string[]);

  try {
    // 3. Instantiate and set up the system
    const system = new System(projectRoot, args.model as string);
    await system.setup(args.orchestrator as string);

    // 4. Re-configure logging based on loaded config if available
    const configuredLogLevel = system.config?.loggingLevel || 'INFO';
    setupApplicationLogging(configuredLogLevel);

    // 5. Start the system's main workflow (plan generation)
    const plan = await system.start(args.task as string, inputFiles);

    // If plan-only mode, exit after generating the plan
    if (args.planOnly) {
      logger.info("Plan-only mode: Workflow execution skipped.");
      return;
    }

    // 6. Run the system's main workflow execution
    await system.run(plan, args.rounds as number, inputFiles);

    logger.info("--- System execution finished successfully ---");

  } catch (error) {
    logger.exception("A critical error occurred during system execution:", error);
    process.exit(1);
  }
}

systemMain();
