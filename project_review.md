### 0) Executive Summary
SWE-agent is an autonomous programmer system that uses language models to solve software engineering tasks. It provides a command-line interface and API for running AI agents that can navigate codebases, edit files, execute commands, and create pull requests to fix issues. (Python, FastAPI, Docker, React frontend)

### 1) Repository Map
```
sweagent/
├── sweagent/                 # Main source code
│   ├── agent/               # Agent logic and models
│   │   ├── agents.py        # Core agent implementation
│   │   ├── models.py        # Language model interfaces
│   │   └── hooks/           # Agent lifecycle hooks
│   ├── environment/         # Environment management
│   │   ├── swe_env.py       # Main environment class
│   │   └── repo.py          # Repository handling
│   ├── run/                 # Entry points and execution
│   │   ├── run.py           # Main run command
│   │   └── run_batch.py     # Batch processing
│   ├── tools/               # Tool definitions and parsing
│   ├── api/                 # FastAPI web interface
│   └── frontend/            # React frontend
├── config/                  # Configuration files
│   ├── default.yaml         # Default agent configuration
│   ├── function_calling.yaml # Function calling config
│   └── thought_action.yaml  # Thought-action config
├── tests/                   # Test suite
├── docker/                  # Docker configuration
└── docs/                    # Documentation
```

Key configuration files:
- `pyproject.toml` - Project dependencies and metadata
- `Dockerfile` - Container setup with Python, Node.js, Docker CLI
- `config/default.yaml` - Default agent behavior templates

### 2) System Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI/API       │    │   Agent Core     │    │   Environment   │
│                 │    │                  │    │                 │
│ - run.py        │───▶│ - Agent class    │───▶│ - SWEEnv        │
│ - run_batch.py  │    │ - Model config   │    │ - Deployment    │
│ - FastAPI       │    │ - Templates      │    │ - Repository    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Tools         │    │   Hooks          │    │   Frontend      │
│                 │    │                  │    │                 │
│ - Edit tools    │    │ - Agent hooks    │    │ - React app     │
│ - Bash tools    │    │ - Env hooks      │    │ - Web interface │
│ - File tools    │    │ - Lifecycle      │    │ - Real-time UI  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

The system follows a layered architecture:
- **Presentation Layer**: CLI, API, and React frontend
- **Application Layer**: Agent orchestration and model management
- **Domain Layer**: Tools, hooks, and environment abstraction
- **Infrastructure Layer**: Docker deployment and repository handling

### 3) Execution Walkthroughs

**Walkthrough 1: Basic Issue Resolution**
```bash
# User runs:
sweagent run --model_name gpt4 --problem_statement "Fix bug in utils.py"

# Execution flow:
1. sweagent/run/run.py:main() parses arguments
2. Creates AgentConfig from config/default.yaml
3. Initializes SWEEnv with Docker deployment
4. Agent processes problem statement with templates
5. Agent loops: thought → action → observation
6. Uses tools to edit files, run tests, create commits
7. Creates pull request with fixes
```

**Walkthrough 2: Batch Processing**
```bash
# User runs:
sweagent run-batch --config config/batch.yaml --instances instances.json

# Execution flow:
1. sweagent/run/run_batch.py:main() loads batch config
2. Creates multiple agent instances
3. Processes each instance in sequence/parallel
4. Collects results and statistics
5. Generates summary report
```

**Walkthrough 3: API Server**
```bash
# User starts:
sweagent server

# Execution flow:
1. sweagent/api/server.py creates FastAPI app
2. Initializes agent and environment
3. WebSocket connection to React frontend
4. Real-time streaming of agent actions
5. Frontend displays thought-action-observation loop
```

### 4) Key Modules & Functions

**sweagent/agent/agents.py:Agent** (lines 100-500)
- Core agent orchestration logic
- Manages thought-action-observation loop
- Handles model interactions and tool execution
- Implements retry logic and error handling

**sweagent/environment/swe_env.py:SWEEnv** (lines 50-200)
- Environment abstraction layer
- Manages Docker containers and deployments
- Handles repository setup and file operations
- Provides bash command execution

**sweagent/run/run.py:main()** (lines 1-100)
- Main entry point for single agent execution
- Argument parsing and configuration loading
- Agent and environment initialization
- Execution orchestration

**sweagent/tools/tools.py:ToolHandler** (lines 1-150)
- Tool registration and execution
- Action parsing and validation
- Tool-specific logic (edit, bash, file operations)
- Error handling and feedback

**sweagent/agent/models.py:get_model()** (lines 1-50)
- Model factory function
- Supports multiple LLM providers (OpenAI, Anthropic, etc.)
- Handles model configuration and initialization
- Implements model-specific adapters

### 5) Configuration & Environment

**Configuration Files:**
- `config/default.yaml` - Default agent behavior, templates, and settings
- `config/function_calling.yaml` - Function calling specific configuration
- `config/thought_action.yaml` - Thought-action pattern configuration
- `pyproject.toml` - Python dependencies and project metadata

**Environment Variables:**
- `OPENAI_API_KEY` - OpenAI API access
- `ANTHROPIC_API_KEY` - Anthropic API access
- `SWEAGENT_CONFIG_DIR` - Custom config directory
- `DOCKER_HOST` - Docker daemon connection

**Deployment:**
- Docker-based environment isolation
- Python 3.9+ with Node.js for frontend
- Volume mounts for repository access
- Network configuration for external access

**Database:**
- No persistent database (stateless design)
- File-based trajectory storage
- JSON format for results and logs

### 6) Dependency Structure

**Core Dependencies:**
- `pydantic` (v2.x) - Data validation and settings
- `fastapi` - Web API framework
- `typer` - CLI framework
- `jinja2` - Template engine for agent prompts
- `pyyaml` - Configuration file parsing

**Model Dependencies:**
- `openai` - OpenAI API client
- `anthropic` - Anthropic API client
- `litellm` - Multi-provider LLM adapter
- `tenacity` - Retry logic

**Environment Dependencies:**
- `swerex` - Runtime environment abstraction
- `docker` - Container management
- `pexpect` - Process interaction

**Frontend Dependencies:**
- `react` - UI framework
- `socket.io` - Real-time communication
- `monaco-editor` - Code editor component

### 7) Quality & Risk Review

**Strengths:**
- Clean separation of concerns with layered architecture
- Comprehensive configuration system with YAML templates
- Strong error handling and retry mechanisms
- Extensible hook system for customization
- Good test coverage for core functionality

**Potential Risks:**
- Complex Docker setup may fail in restricted environments
- Large language model dependencies can be expensive
- No built-in rate limiting for API calls
- Limited error recovery for network failures
- Potential security issues with arbitrary code execution

**Technical Debt:**
- Some hardcoded paths and assumptions
- Limited documentation for advanced configurations
- No centralized logging system
- Mixed async/sync patterns in places

**Performance Considerations:**
- Docker container startup overhead
- LLM API latency impacts responsiveness
- File I/O operations could be optimized
- Memory usage grows with trajectory length

### 8) Developer Guide

**Prerequisites:**
```bash
# Install Python 3.9+
# Install Docker
# Install Node.js 16+
git clone https://github.com/SWE-agent/SWE-agent.git
cd SWE-agent
pip install -e .
```

**Running Tests:**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_run.py

# Run with coverage
pytest --cov=sweagent
```

**Development Workflow:**
```bash
# Start development server
sweagent server --reload

# Run single agent
sweagent run --model_name human --config config/human.yaml

# Run batch processing
sweagent run-batch --instances examples/instances.json
```

**Debugging Tips:**
- Use `--log_level DEBUG` for verbose logging
- Check Docker container logs with `docker logs`
- Use `--trajectory_file` to save execution traces
- Frontend dev tools show WebSocket messages

### 9) Mental Model & Glossary

**Core Concepts:**
- **Agent**: Autonomous programmer that processes issues and creates fixes
- **Environment**: Isolated runtime (Docker container) for code execution
- **Trajectory**: Sequence of thought-action-observation steps
- **Tools**: Actions the agent can take (edit, bash, file operations)
- **Hooks**: Extension points for customizing behavior

**Key Patterns:**
- **Thought-Action-Observation**: Agent reasoning cycle
- **Template-Based Prompting**: Jinja2 templates for LLM prompts
- **Function Calling**: Structured tool invocation
- **Batch Processing**: Multiple instance execution

**Terminology:**
- **SWE**: Software Engineering
- **LM**: Language Model
- **Deployment**: Runtime environment setup
- **Repository**: Target codebase for modifications
- **Instance**: Single problem-solving session

### 10) Appendix

**Useful Links:**
- [Documentation](https://swe-agent.com/latest/)
- [Discord Community](https://discord.gg/AVEFbBn2rH)
- [GitHub Issues](https://github.com/SWE-agent/SWE-agent/issues)

**Known Limitations:**
- Requires Docker daemon access
- Limited to Python repositories currently
- No built-in authentication for multi-user scenarios
- Frontend requires modern browser with WebSocket support

**Future Improvements:**
- Support for more programming languages
- Enhanced security with sandboxing
- Multi-user collaboration features
- Performance optimizations for large codebases
- Integration with CI/CD pipelines
