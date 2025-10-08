import { BaseModel, model_validator } from 'pydantic';
import { Logger } from '../logger/Logger';

const logger = Logger.getInstance();

// Interface for the LLM generation arguments, providing a structured way to pass parameters
export interface LLMGenerateContentArgs {
  modelName: string;
  contents: string;
  systemInstruction?: string;
  temperature?: number;
  responseMimeType?: 'text/plain' | 'application/json' | 'application/json-schema';
  responseSchema?: typeof BaseModel; // Expecting a Pydantic BaseModel class
}

export abstract class LLM {
  /**
   * Abstract method to be implemented by concrete LLM providers.
   * This method performs the actual call to the LLM API.
   * @param args - The arguments for content generation.
   * @returns A Promise resolving to the LLM's response (can be string, object, or parsed schema instance).
   */
  protected abstract generateContentImpl(args: LLMGenerateContentArgs): Promise<any>;

  /**
   * Public method to generate content using an LLM. Handles common logic like:
   * - Retries with exponential backoff
   * - Response parsing based on mime type and schema
   * @param args - The arguments for content generation.
   * @returns A Promise resolving to the processed LLM response, or null if all retries fail.
   */
  public async generateContent(args: LLMGenerateContentArgs): Promise<any> {
    const { modelName, responseSchema, responseMimeType } = args;
    const maxRetries = 3; // Number of times to retry the LLM call
    let lastError: Error | null = null;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        logger.info(`Calling LLM model '${modelName}' (Attempt ${attempt}/${maxRetries})...`);
        const response = await this.generateContentImpl(args);

        if (!response) {
          throw new Error('LLM returned an empty response.');
        }

        // Process the response based on the requested schema and mime type
        if (responseSchema && responseMimeType === 'application/json') {
          if (typeof response === 'string') {
            try {
              const parsedJson = JSON.parse(response);
              // Validate the parsed JSON against the provided Pydantic schema
              const validatedData = responseSchema.parse(parsedJson);
              logger.debug(`LLM response successfully parsed and validated against schema ${responseSchema.name}.`);
              return validatedData;
            } catch (e) {
              // Catch JSON parsing or Pydantic validation errors
              lastError = new Error(`Failed to parse or validate LLM JSON response with schema ${responseSchema.name}: ${e.message}`);
              logger.error(lastError.message);
              // Do not retry on parsing/validation errors, as the response itself is likely malformed
              throw lastError;
            }
          } else if (response instanceof responseSchema) {
            // If the response is already an instance of the expected schema, return it directly
            logger.debug(`LLM response is already an instance of ${responseSchema.name}.`);
            return response;
          } else {
             // Handle cases where the response is neither a string nor the expected schema type
             lastError = new Error(`LLM response was not a string or expected schema type for JSON request.`);
             logger.error(lastError.message);
             throw lastError;
          }
        } else if (responseSchema && responseMimeType === 'application/json-schema') {
            // Specific handling for JSON schema responses if needed
             if (typeof response === 'string') {
                try {
                    const parsedSchema = JSON.parse(response);
                    // Further validation or processing might be needed here
                    logger.debug('LLM response parsed as JSON Schema.');
                    return parsedSchema;
                } catch (e) {
                     lastError = new Error(`Failed to parse LLM JSON Schema response: ${e.message}`);
                     logger.error(lastError.message);
                     throw lastError;
                }
            }
        }

        // Default handling for text responses or un-schematized JSON
        logger.debug('LLM response processed.');
        return response;

      } catch (error) {
        // Capture the error and prepare for retry or final failure
        lastError = error;
        logger.error(`LLM generation failed (Attempt ${attempt}): ${error.message}`);
        // Implement exponential backoff for retries
        if (attempt < maxRetries) {
          const delay = Math.pow(2, attempt) * 1000; // Delay in ms (1s, 2s, 4s)
          logger.info(`Waiting for ${delay / 1000} seconds before retrying...`);
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }
    }

    // If all retries fail, log the last error and return null
    logger.error(`LLM generation failed after ${maxRetries} attempts. Last error: ${lastError?.message}`);
    return null;
  }

  /**
   * Factory method to create an LLM instance based on a species string.
   * This allows for dynamic instantiation of different LLM providers.
   * @param species - A string identifying the LLM species (e.g., 'gemini:gemini-pro', 'ollama:llama3').
   * @returns An instance of a concrete LLM class.
   */
  static factory(species: string): LLM {
    logger.info(`LLM Factory: Creating LLM instance for species '${species}'`);
    
    // TODO: Replace dummy implementations with actual LLM provider classes
    // Example: Implement OllamaLLM, GeminiLLM, OpenAILLM, MistralLLM classes
    // and instantiate them here based on the 'species' string.

    if (species.startsWith('ollama:')) {
        const modelName = species.split(':')[1];
        // return new OllamaLLM(modelName);
        logger.warn('OllamaLLM not implemented. Returning DummyLLM.');
        return new DummyLLM(modelName);
    }
    if (species.startsWith('gemini:') || species === 'gemini-2.5-flash-lite') {
        const modelName = species.includes(':') ? species.split(':')[1] : species;
        // return new GeminiLLM(modelName);
        logger.warn('GeminiLLM not implemented. Returning DummyLLM.');
        return new DummyLLM(modelName);
    }
     if (species.startsWith('openai:') || species.startsWith('gpt:') || species.startsWith('opi:')) {
        const modelName = species.includes(':') ? species.split(':')[1] : species;
        // return new OpenAILLM(modelName);
         logger.warn('OpenAILLM not implemented. Returning DummyLLM.');
        return new DummyLLM(modelName);
    }
    if (species.startsWith('mistral:')) {
        const modelName = species.split(':')[1];
        // return new MistralLLM(modelName);
         logger.warn('MistralLLM not implemented. Returning DummyLLM.');
        return new DummyLLM(modelName);
    }

    // Fallback to DummyLLM if the species is unknown
    logger.warn(`Unknown LLM species '${species}'. Using DummyLLM as fallback.`);
    return new DummyLLM(species);
  }
}

/**
 * A dummy LLM implementation used as a placeholder.
 * It simulates LLM responses without making actual API calls.
 */
class DummyLLM extends LLM {
  constructor(private modelName: string) {
    super();
    logger.warn(`DummyLLM initialized with model: ${this.modelName}. This is a placeholder.`);
  }

  protected async generateContentImpl(args: LLMGenerateContentArgs): Promise<any> {
    logger.warn(`DummyLLM: generateContentImpl called for model ${this.modelName}. Returning mock response.`);
    
    // Simulate response based on schema if provided
    if (args.responseSchema) {
        try {
            // Create a mock response adhering to the schema
            if (args.responseSchema === AgentOutput) {
                return new AgentOutput({
                    output: `Mock output for ${this.modelName} task: ${args.contents.substring(0, 50)}...`,
                    reasoning: 'This is a mock response from DummyLLM.',
                    artifact: new Artifact({ task: 'mock_task', files: [new File({ path: 'mock_output.txt', content: 'Mock file content.'})]}),
                    team: new Team({ notes: 'Mock team notes.'})
                });
            } else if (args.responseSchema === Plan) {
                 return new Plan({
                    highLevelGoal: 'Mock Goal',
                    reasoning: 'Mock reasoning for plan generation',
                    roles: [{title: 'Mock Role', purpose: 'Mock Purpose'}],
                    tasks: [{id: 'T1', description: 'Mock Task', role: 'Mock Role', agent: 'Mock Agent', requires: []}],
                    team: new Team({ notes: 'Mock team notes.'})
                });
            }
            // Add handlers for other schemas as needed
        } catch (e) {
            logger.error(`Error creating mock response for schema ${args.responseSchema.name}:`, e);
            return `Mock response failed for schema ${args.responseSchema.name}.`;
        }
    }
    
    // Default mock response if no schema is provided or handled
    return `This is a mock response from DummyLLM for model ${this.modelName}.`;
  }
}
