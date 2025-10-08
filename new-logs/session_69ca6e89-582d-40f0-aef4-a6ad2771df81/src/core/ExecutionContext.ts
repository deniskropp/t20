import { Session } from './Session';
import { Plan, Task, Artifact, File } from '../custom_types';
import { Logger } from '../logger/Logger';
import { ContextItem } from '../agent/Agent'; // Assuming ContextItem is exported from Agent

const logger = Logger.getInstance();

export class ExecutionContext {
  public session: Session;
  public plan: Plan;
  public stepIndex: number;
  public roundNum: number;
  public items: Record<string, ContextItem>; // Stores remembered artifacts

  constructor(session: Session, plan: Plan, stepIndex: number = 0, roundNum: number = 1) {
    this.session = session;
    this.plan = plan;
    this.stepIndex = stepIndex;
    this.roundNum = roundNum;
    this.items = {}; // Initialize items map
    logger.debug(`ExecutionContext initialized for round ${roundNum}, step ${stepIndex + 1}`);
  }

  /**
   * Advances the execution to the next step in the plan.
   */
  public nextStep(): void {
    this.stepIndex++;
    logger.debug(`Moved to next step. Current step index: ${this.stepIndex}`);
  }

  /**
   * Resets the step index to the beginning of the plan.
   * Typically used at the start of a new round.
   */
  public reset(): void {
    this.stepIndex = 0;
    logger.debug('ExecutionContext reset. Step index set to 0.');
  }

  /**
   * Gets the current task based on the step index.
   * @returns The current Task object.
   */
  public currentStep(): Task {
    if (this.stepIndex >= this.plan.tasks.length) {
      throw new Error(`Step index ${this.stepIndex} is out of bounds for plan with ${this.plan.tasks.length} tasks.`);
    }
    return this.plan.tasks[this.stepIndex];
  }

  /**
   * Records an artifact generated during task execution.
   * @param key A unique key for the artifact (e.g., agent name + task ID).
   * @param value The artifact content (can be string, object, etc.).
   * @param remember If true, the artifact is stored in context memory for future steps.
   */
  public async recordArtifact(key: string, value: any, remember: boolean = false): Promise<void> {
    // Generate a unique key for session storage to avoid conflicts across rounds/steps
    const sessionArtifactKey = `${this.roundNum}/${this.stepIndex}_${key}`;
    await this.session.addArtifact(sessionArtifactKey, value);

    if (remember) {
      // Store in context memory if requested
      const currentTask = this.currentStep();
      this.items[sessionArtifactKey] = new ContextItem(sessionArtifactKey, value, currentTask);
      logger.debug(`Artifact '${key}' recorded and remembered in context memory.`);
    }
  }

  /**
   * Records initial artifacts provided at the start of the workflow.
   * These are typically inputs from the user or system.
   * @param key A unique key for the initial artifact.
   * @param value The artifact content.
   */
  public recordInitial(key: string, value: any): void {
    // Use a special task ID 'initial' for initial artifacts
    const initialTask = new Task({
      id: 'initial',
      description: 'Initial files provided by the user',
      role: 'User',
      agent: 'User',
      requires: [],
    });
    this.items[key] = new ContextItem(key, value, initialTask);
    logger.debug(`Initial artifact '${key}' recorded.`);
  }

  /**
   * Retrieves initial files recorded at the start.
   * @returns An array of File objects or null if not found.
   */
  public getInitialFiles(): File[] | null {
    const initialItem = this.items['initial_files']; // Key used in sysmain.ts
    if (initialItem && initialItem.content && Array.isArray(initialItem.content)) {
      // Ensure content is an array of File objects
      return initialItem.content.map((item: any) => {
        // Basic check to ensure it's a File-like object
        if (item && typeof item === 'object' && 'path' in item && 'content' in item) {
          return new File(item);
        }
        logger.warn('Found non-File item in initial files array.');
        return null;
      }).filter((file: File | null) => file !== null) as File[];
    }
    return null;
  }
}
