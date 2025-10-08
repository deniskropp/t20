import { LLM } from '../llm/LLM';
import { BaseModel } from 'pydantic';

export class MockLLM extends LLM {
  // Mock implementation of generateContent
  public generateContent = jest.fn();

  // Mock implementation of the factory if needed, though usually handled by jest.mock
  public static factory = jest.fn();
}
