t
// app.js

// Mock user ID for demonstration purposes
const CURRENT_USER_ID = 'user-123';

// --- Zustand Store Setup ---
// (This would typically be in src/store/aiStore.ts)
const { create } = await import('zustand');
const api = (await import('./lib/api')).default; // Assuming api.ts is in lib/

// Define types based on Lyra's contract
const SYSTEM_PROMPT = 'You are a helpful and concise AI assistant named AuraFlow. Provide direct answers.';

const useAIStore = create((set, get) => ({
    // Interaction State
    currentPrompt: '',
    messages: [{ role: 'system', content: SYSTEM_PROMPT }],
    conversationId: null,
    aiResponse: null,
    isLoading: false,
    error: null,

    // History State
    conversations: [],
    historyIsLoading: false,
    historyError: null,

    // Actions
    setPrompt: (prompt) => set({ currentPrompt: prompt }),

    fetchAiResponse: async () => {
        const { currentPrompt, messages, conversationId } = get();
        if (!currentPrompt.trim()) return;

        set({ isLoading: true, error: null });

        const userMessage = { role: 'user', content: currentPrompt };
        const updatedMessages = [...messages, userMessage];

        try {
            const response = await api.post('/generate', {
                user_id: CURRENT_USER_ID,
                conversation_id: conversationId,
                messages: updatedMessages,
                stream: false, // For simplicity initially
            });

            const aiResponseData = response.data;
            set({
                aiResponse: aiResponseData,
                conversationId: aiResponseData.conversation_id,
                messages: [...updatedMessages, { role: 'assistant', content: aiResponseData.output.content, id: aiResponseData.id }],
                isLoading: false,
            });
            set({ currentPrompt: '' }); // Clear prompt after successful response

        } catch (error) {
            console.error('Error fetching AI response:', error);
            set({
                error: { code: error.code || 'FETCH_ERROR', message: error.message || 'Failed to get response from AI.' },
                isLoading: false,
            });
        }
    },

    setError: (error) => set({ error }),
    clearError: () => set({ error: null }),

    addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),

    loadConversationHistory: async (limit = 20, offset = 0) => {
        set({ historyIsLoading: true, historyError: null });
        try {
            const response = await api.get('/history', {
                params: { user_id: CURRENT_USER_ID, limit, offset },
            });
            set({
                conversations: response.data.conversations,
                historyIsLoading: false,
            });
        } catch (error) {
            console.error('Error loading conversation history:', error);
            set({
                historyError: { code: error.code || 'HISTORY_LOAD_ERROR', message: error.message || 'Failed to load history.' },
                historyIsLoading: false,
            });
        }
    },

    loadSpecificConversation: async (conversationId) => {
        set({ isLoading: true, error: null, messages: [{ role: 'system', content: SYSTEM_PROMPT }] });
        try {
            const response = await api.get(`/history/${conversationId}`, {
                params: { user_id: CURRENT_USER_ID },
            });
            const conversationMessages = response.data.messages.filter(msg => msg.role !== 'system');
            set({
                conversationId: response.data.id,
                messages: [{ role: 'system', content: SYSTEM_PROMPT }, ...conversationMessages],
                aiResponse: null,
                currentPrompt: '',
                isLoading: false,
            });
        } catch (error) {
            console.error('Error loading specific conversation:', error);
            set({
                error: { code: error.code || 'CONV_LOAD_ERROR', message: error.message || 'Failed to load conversation.' },
                isLoading: false,
            });
        }
    },

    submitFeedback: async (responseId, feedbackType, comment) => {
        try {
            await api.post('/feedback', {
                user_id: CURRENT_USER_ID,
                response_id: responseId,
                feedback_type: feedbackType,
                comment: comment,
            });
            console.log(`Feedback (${feedbackType}) submitted for response ${responseId}`);
        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    },

    clearInteractionState: () => {
        set({
            currentPrompt: '',
            messages: [{ role: 'system', content: SYSTEM_PROMPT }],
            conversationId: null,
            aiResponse: null,
            isLoading: false,
            error: null,
        });
    }
}));

// --- UI Components ---

// Input Component (Textarea for prompts)
function InputComponent({ label, description, id, ...props }) {
    const { currentPrompt, setPrompt, isLoading } = useAIStore();
    const inputId = id || 'prompt-input';

    return (
        <div className="mb-6">
            {label && <label htmlFor={inputId} className="block mb-2 text-label-input font-medium text-primary-text">{label}</label>}
            {description && <p id={`${inputId}-description`} className="text-body-small text-secondary-text mb-2">{description}</p>}
            <textarea
                id={inputId}
                className="input-field"
                value={currentPrompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="What can I help you create or understand today?"
                aria-describedby={description ? `${inputId}-description` : undefined}
                disabled={isLoading}
                rows="5" // Default rows, can be adjusted
            />
        </div>
    );
}

// Button Component
function ButtonComponent({ children, onClick, disabled, className = '' }) {
    const { isLoading } = useAIStore();
    const buttonClasses = `btn-primary ${className} ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`;
    return (
        <button onClick={onClick} disabled={disabled || isLoading} className={buttonClasses}>
            {children}
        </button>
    );
}

// Response Card Component
function ResponseCardComponent({ children, responseId, onFeedback }) {
    return (
        <div className="response-card">
            <div className="text-body-regular">{children}</div>
            <div className="mt-4 flex items-center">
                <button
                    className="feedback-btn mr-2"
                    onClick={() => onFeedback(responseId, 'like')}
                    aria-label="Like response"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
                        <path d="M11.48 3.496a.75.75 0 00-1.496 0l-1.664 5.006a.75.75 0 01-.604.504L2.97 7.077a.75.75 0 00-.426.75v10.898a.75.75 0 00.75.75h7.773c.457 0 .897.274 1.057.701l1.664 5.006a.75.75 0 001.496 0l1.664-5.006a.75.75 0 01.604-.504h5.07a.75.75 0 00.75-.75V11.25a.75.75 0 00-.75-.75h-4.75a.75.75 0 01-.604-.504l-1.664-5.006a.75.75 0 00-1.057-.701l-1.664 5.006a.75.75 0 01-.604.504H11.48zM14.742 10.006a.75.75 0 01.604.504l1.664 5.006a.75.75 0 00.604.504h4.75v7.5a.75.75 0 00.75.75h.001a.75.75 0 00.75-.75v-7.5c0-.457-.274-.897-.701-1.057l-5.006-1.664a.75.75 0 00-.504-.604H14.742zM6.75 10.006a.75.75 0 011.496 0l-1.664 5.006a.75.75 0 00.604.504h7.773a.75.75 0 01.75.75v7.5a.75.75 0 01-.75.75h-7.773a.75.75 0 01-.604-.504l-1.664-5.006a.75.75 0 00-1.057-.701l-1.664 5.006a.75.75 0 00.75.75h4.75v-7.5a.75.75 0 01.75-.75h.001a.75.75 0 01.75-.75V10.006z" />
                    </svg>
                    Like
                </button>
                <button
                    className="feedback-btn"
                    onClick={() => onFeedback(responseId, 'dislike')}
                    aria-label="Dislike response"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
                        <path d="M11.48 3.496a.75.75 0 00-1.496 0l-1.664 5.006a.75.75 0 01-.604.504L2.97 7.077a.75.75 0 00-.426.75v10.898a.75.75 0 00.75.75h7.773c.457 0 .897.274 1.057.701l1.664 5.006a.75.75 0 001.496 0l1.664-5.006a.75.75 0 01.604-.504h5.07a.75.75 0 00.75-.75V11.25a.75.75 0 00-.75-.75h-4.75a.75.75 0 01-.604-.504l-1.664-5.006a.75.75 0 00-1.057-.701l-1.664 5.006a.75.75 0 01-.604.504H11.48zM14.742 10.006a.75.75 0 01.604.504l1.664 5.006a.75.75 0 00.604.504h4.75v7.5a.75.75 0 00.75.75h.001a.75.75 0 00.75-.75v-7.5c0-.457-.274-.897-.701-1.057l-5.006-1.664a.75.75 0 00-.504-.604H14.742zM6.75 10.006a.75.75 0 011.496 0l-1.664 5.006a.75.75 0 00.604.504h7.773a.75.75 0 01.75.75v7.5a.75.75 0 01-.75.75h-7.773a.75.75 0 01-.604-.504l-1.664-5.006a.75.75 0 00-1.057-.701l-1.664 5.006a.75.75 0 00.75.75h4.75v-7.5a.75.75 0 01.75-.75h.001a.75.75 0 01.75-.75V10.006z" />
                    </svg>
                    Dislike
                </button>
                {/* Add Copy/Download buttons here if needed */}
            </div>
        </div>
    );
}

// Loading Indicator Component
function LoadingIndicatorComponent({ size = 'medium' }) {
    const indicatorClasses = `loading-indicator ${size}`;
    return (
        <div className={indicatorClasses} role="status" aria-label="Loading AI response">
            <span className="sr-only">Loading...</span>
        </div>
    );
}

// Navigation Link Component
function NavigationLink({ children, to, ...props }) {
    // Basic routing simulation for demonstration
    const handleClick = (e) => {
        e.preventDefault();
        renderPage(to);
        // Update active state (simple toggle for demo)
        document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
        e.currentTarget.classList.add('active');
    };

    return (
        <a href={to} onClick={handleClick} className="nav-link" {...props}>
            {children}
        </a>
    );
}

// --- Page Components ---

// Home Page Component
function HomePage() {
    const { currentPrompt, fetchAiResponse, isLoading, error, aiResponse, messages } = useAIStore();

    const handleGenerate = () => {
        fetchAiResponse();
    };

    const handleFeedback = (responseId, feedbackType) => {
        useAIStore.getState().submitFeedback(responseId, feedbackType);
    };

    // Extract the latest assistant message for display
    const latestAssistantMessage = messages.slice().reverse().find(msg => msg.role === 'assistant');

    return (
        <div className="home-page">
            <h2 className="text-heading-2 text-center mb-4">Engage with AuraFlow AI</h2>
            <p className="text-body-large text-secondary-text text-center mb-8">Enter your prompt below to unlock the power of AI.</p>

            <InputComponent
                label="Your Prompt"
                description="Enter your prompt for the AI system here. You can refine your prompts for better results."
                id="prompt-input"
            />

            <div className="flex justify-end mb-8">
                <ButtonComponent onClick={handleGenerate}>
                    Generate Response
                </ButtonComponent>
            </div>

            {isLoading && <div className="flex justify-center my-8"><LoadingIndicatorComponent size="large" /></div>}

            {error && (
                <div className="response-card bg-error-red-100 border border-error-red-400 text-error-red-700 p-4 rounded-lg mb-8">
                    <p className="font-bold">Error:</p>
                    <p>{error.message}</p>
                </div>
            )}

            {latestAssistantMessage && (
                <ResponseCardComponent responseId={latestAssistantMessage.id} onFeedback={handleFeedback}>
                    {latestAssistantMessage.content}
                </ResponseCardComponent>
            )}
        </div>
    );
}

// History Page Component
function HistoryPage() {
    const { conversations, loadConversationHistory, loadSpecificConversation, historyIsLoading, historyError } = useAIStore();

    React.useEffect(() => {
        loadConversationHistory();
    }, [loadConversationHistory]);

    const handleConversationClick = (conversationId) => {
        loadSpecificConversation(conversationId);
        // Navigate back to home page after loading conversation
        renderPage('home');
        document.querySelector('.nav-link[href="#home"]').classList.add('active');
        document.querySelector('.nav-link[href="#history"]').classList.remove('active');
    };

    return (
        <div className="history-page">
            <h2 className="text-heading-1 mb-6">Interaction History</h2>
            {historyIsLoading && <div className="flex justify-center my-8"><LoadingIndicatorComponent size="large" /></div>}
            {historyError && <div className="error-message p-4 bg-red-100 text-red-700 rounded-lg">{historyError.message}</div>}
            {!historyIsLoading && !historyError && conversations.length === 0 && (
                <p>No past interactions found.</p>
            )}
            {!historyIsLoading && !historyError && conversations.length > 0 && (
                <ul className="space-y-4">
                    {conversations.map(conv => (
                        <li
                            key={conv.id}
                            className="response-card p-4 cursor-pointer hover:bg-light-neutral"
                            onClick={() => handleConversationClick(conv.id)}
                        >
                            <h3 className="text-heading-3 mb-2">{conv.title || `Conversation ${conv.id.substring(0, 6)}`}</h3>
                            <p className="text-body-small text-secondary-text mb-2">Last updated: {new Date(conv.last_updated).toLocaleString()}</p>
                            {conv.preview_messages && conv.preview_messages.map((msg, index) => (
                                <p key={index} className="text-body-small truncate">
                                    <strong>{msg.role === 'user' ? 'You' : 'AI'}:</strong> {msg.content_snippet}
                                </p>
                            ))}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

// Settings Page Component (Placeholder)
function SettingsPage() {
    return (
        <div className="settings-page">
            <h2 className="text-heading-1 mb-6">Settings</h2>
            <p className="text-body-regular">User settings and preferences will be managed here.</p>
            {/* Add settings form elements here */}
        </div>
    );
}

// --- Routing and Rendering ---
const appRoot = document.getElementById('app');
let currentPage = 'home'; // Default page

function renderPage(pageName) {
    appRoot.innerHTML = ''; // Clear previous content

    let PageComponent;
    switch (pageName) {
        case 'home':
            PageComponent = HomePage;
            break;
        case 'history':
            PageComponent = HistoryPage;
            break;
        case 'settings':
            PageComponent = SettingsPage;
            break;
        default:
            PageComponent = HomePage;
    }

    const element = document.createElement('div');
    appRoot.appendChild(element);
    // Use ReactDOM.render if using React, or a simpler approach for vanilla JS
    // For this example, we'll simulate rendering by directly manipulating DOM
    // In a real React app, you'd use ReactDOM.createRoot(element).render(<PageComponent />);
    // For this vanilla JS simulation, we'll just inject the component's structure
    element.innerHTML = PageComponent().outerHTML; // Simplified rendering
    currentPage = pageName;
}

// Initial render and navigation setup
function initApp() {
    // Render initial page
    renderPage(currentPage);

    // Setup navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = e.currentTarget.getAttribute('href').substring(1); // Remove '#'
            renderPage(pageName);

            // Update active state
            document.querySelectorAll('.nav-link').forEach(nav => nav.classList.remove('active'));
            e.currentTarget.classList.add('active');
        });
    });

    // Set initial active link
    const initialLink = document.querySelector(`.nav-link[href="#${currentPage}"]`);
    if (initialLink) {
        initialLink.classList.add('active');
    }
}

// Simulate React's useEffect for initial setup
// In a real React app, this would be handled by React's lifecycle methods
// For this vanilla JS simulation, we call initApp directly
initApp();

// --- Mock API Service (lib/api.js) ---
// This part simulates the api.ts file from Kodax's output.
// In a real setup, this would be imported.
// For demonstration, we'll define it here if it's not available.
if (!api) {
    console.warn("API module not found, using mock API service.");
    const mockApi = {
        post: async (url, data) => {
            console.log(`Mock API POST ${url}:`, data);
            await new Promise(resolve => setTimeout(resolve, 500)); // Simulate network delay

            if (url === '/generate') {
                if (!data.messages || data.messages.length === 0) {
                    throw { code: 'INVALID_INPUT', message: 'Messages are required.' };
                }
                const userMessage = data.messages.find(m => m.role === 'user');
                if (!userMessage) {
                     throw { code: 'INVALID_INPUT', message: 'User message is required.' };
                }
                // Simulate a response
                return {
                    data: {
                        id: `res_${Date.now()}`,
                        conversation_id: data.conversation_id || `conv_${Date.now()}`,
                        output: {
                            type: 'text',
                            content: `This is a simulated response to: "${userMessage.content.substring(0, 50)}..."`,
                        },
                        metadata: {
                            model: 'mock-model',
                            prompt_tokens: 10,
                            completion_tokens: 20,
                            total_tokens: 30,
                            timestamp: new Date().toISOString(),
                        }
                    }
                };
            } else if (url === '/feedback') {
                 return { data: { status: 'success', message: 'Feedback received.' } };
            }
            throw { code: 'NOT_FOUND', message: 'Mock API endpoint not found.' };
        },
        get: async (url) => {
            console.log(`Mock API GET ${url}`);
            await new Promise(resolve => setTimeout(resolve, 300)); // Simulate network delay

            if (url === '/history') {
                // Simulate history data
                return {
                    data: {
                        conversations: [
                            { id: 'conv_1', title: 'Quantum Computing Basics', last_updated: new Date(Date.now() - 86400000).toISOString(), preview_messages: [{ role: 'user', content_snippet: 'Explain quantum computing...' }, { role: 'assistant', content_snippet: 'Quantum computing uses...' }] },
                            { id: 'conv_2', title: 'Poem Generation', last_updated: new Date(Date.now() - 172800000).toISOString(), preview_messages: [{ role: 'user', content_snippet: 'Write a poem about...' }, { role: 'assistant', content_snippet: 'In realms of thought...' }] },
                        ],
                        total_count: 2
                    }
                };
            } else if (url.startsWith('/history/')) {
                const conversationId = url.split('/')[2];
                // Simulate specific conversation data
                return {
                    data: {
                        id: conversationId,
                        title: `Conversation ${conversationId.substring(0, 6)}`,
                        messages: [
                            { role: 'system', content: SYSTEM_PROMPT },
                            { role: 'user', content: 'Explain quantum computing in simple terms.', id: 'msg_user_1' },
                            { role: 'assistant', content: 'Quantum computing harnesses quantum-mechanical phenomena like superposition and entanglement to perform computations. Unlike classical computers using bits (0 or 1), quantum computers use qubits, which can be 0, 1, or both simultaneously, enabling them to process vast amounts of information faster for certain problems.', id: 'res_1', timestamp: new Date(Date.now() - 86400000).toISOString() },
                            { role: 'user', content: 'Can you give me a practical example of its application?', id: 'msg_user_2' },
                            { role: 'assistant', content: 'A practical example is in drug discovery and materials science, where simulating molecular interactions is computationally intensive for classical computers but feasible for quantum computers.', id: 'res_2', timestamp: new Date(Date.now() - 86400000).toISOString() }
                        ]
                    }
                };
            }
            throw { code: 'NOT_FOUND', message: 'Mock API endpoint not found.' };
        }
    };
    // Assign mockApi to the global scope or a specific variable if needed
    window.api = mockApi; // Make it globally accessible for the script
}

// --- Placeholder for React Integration ---
// In a real React application, you would use ReactDOM to render the main App component.
// Example:
// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import App from './App'; // Assuming App.tsx contains the main structure and routing
//
// const rootElement = document.getElementById('app');
// if (rootElement) {
//     const root = ReactDOM.createRoot(rootElement);
//     root.render(
//         <React.StrictMode>
//             <App />
//         </React.StrictMode>
//     );
// }

// --- Accessibility Enhancements ---
// Ensure focus management for keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab' && !document.activeElement) {
        // If no element is focused, focus the first focusable element
        const focusableElements = document.querySelectorAll('a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
        }
    }
});
