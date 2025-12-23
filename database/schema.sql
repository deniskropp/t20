-- Database Schema for Component Development and Agent Orchestration
-- Designed to support KickLang knowledge graph integration and Aetheria OS operations.

-- Table: Components
-- Represents the system components under development.
CREATE TABLE Components (
    component_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    status VARCHAR(50) DEFAULT 'Defined' NOT NULL, -- e.g., 'Defined', 'Designed', 'Implemented', 'Verified', 'Documented', 'Refined'
    kicklang_definition JSONB, -- Stores KickLang-structured metadata or definitions for the component
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table: Agents
-- Stores information about the AI agents operating within Aetheria OS.
CREATE TABLE Agents (
    agent_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE, -- e.g., 'GPTASe', 'DB Architect'
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table: Roles
-- Defines the distinct roles that agents can assume.
CREATE TABLE Roles (
    role_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE, -- e.g., 'Database Architect', 'Code Investigator'
    purpose TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table: Agent_Prompts
-- Stores system prompts for agents, adhering to the 'team.prompts' structure.
CREATE TABLE Agent_Prompts (
    prompt_id SERIAL PRIMARY KEY,
    agent_id INT NOT NULL REFERENCES Agents(agent_id) ON DELETE CASCADE,
    role_id INT NOT NULL REFERENCES Roles(role_id) ON DELETE CASCADE,
    system_prompt_content TEXT NOT NULL,
    version INT DEFAULT 1 NOT NULL, -- For tracking prompt updates
    is_active BOOLEAN DEFAULT TRUE NOT NULL, -- To manage active prompts for an agent/role combination
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (agent_id, role_id, version) -- Ensures unique prompt versions for an agent-role pair
);

-- Table: Component_Tasks
-- Tracks the execution of Task-Agnostic Steps (TAS) for each component.
CREATE TABLE Component_Tasks (
    component_task_id SERIAL PRIMARY KEY,
    component_id INT NOT NULL REFERENCES Components(component_id) ON DELETE CASCADE,
    task_name VARCHAR(255) NOT NULL, -- Derived from purified TAS (e.g., 'Define Component Scope')
    status VARCHAR(50) DEFAULT 'Pending' NOT NULL, -- e.g., 'Pending', 'In Progress', 'Completed', 'Failed'
    assigned_agent_id INT REFERENCES Agents(agent_id) ON DELETE SET NULL,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table: Artifacts
-- Stores metadata about task-generated outputs, adhering to 'artifact' schema.
CREATE TABLE Artifacts (
    artifact_id SERIAL PRIMARY KEY,
    system_task_id VARCHAR(50) NOT NULL, -- Corresponds to the 'task' field in the artifact schema (e.g., 'T-02')
    generated_by_agent_id INT REFERENCES Agents(agent_id) ON DELETE SET NULL,
    generated_for_component_id INT REFERENCES Components(component_id) ON DELETE SET NULL,
    output_summary TEXT, -- Stores the 'output' text message content from the agent
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table: Artifact_Files
-- Stores details and content of files generated as part of an artifact.
CREATE TABLE Artifact_Files (
    file_id SERIAL PRIMARY KEY,
    artifact_id INT NOT NULL REFERENCES Artifacts(artifact_id) ON DELETE CASCADE,
    path VARCHAR(1024) NOT NULL, -- File path or name (e.g., 'src/main.py')
    content TEXT NOT NULL, -- Full content of the file
    file_type VARCHAR(100), -- e.g., 'text/plain', 'application/json'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_components_name ON Components(name);
CREATE INDEX idx_agents_name ON Agents(name);
CREATE INDEX idx_roles_title ON Roles(title);
CREATE INDEX idx_agent_prompts_agent_role ON Agent_Prompts(agent_id, role_id);
CREATE INDEX idx_component_tasks_component_id ON Component_Tasks(component_id);
CREATE INDEX idx_component_tasks_agent_id ON Component_Tasks(assigned_agent_id);
CREATE INDEX idx_artifacts_system_task_id ON Artifacts(system_task_id);
CREATE INDEX idx_artifacts_agent_id ON Artifacts(generated_by_agent_id);
CREATE INDEX idx_artifact_files_artifact_id ON Artifact_Files(artifact_id);
