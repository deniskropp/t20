document.addEventListener('DOMContentLoaded', () => {

    // --- DOM Elements ---
    const startBtn = document.getElementById('start-genesis-btn');
    const genesisContainer = document.getElementById('genesis-container');
    const finalDetailsSection = document.getElementById('final-track-details');

    // --- Data: The 8 Engineered Prompts ---
    // In a real application, these would be managed more robustly.
    const prompts = [
        // Lyrics
        { id: 1, type: 'lyrics', name: 'Develop Lyrical Concept & Narrative', prompt: "Instruction: Develop the core lyrical concept and narrative for a song centered around 'uTASe'. Context: 'uTASe' represents unseen forces, adaptive systems, and emergent patterns. Desired emotional response: awe, introspection, evolving understanding. Task: Brainstorm and articulate core lyrical themes, narrative arcs, and key metaphors. Output: JSON object with 'lyrical_concept_brief', 'core_themes_motifs', 'narrative_outline', 'key_imagery_metaphors'." },
        { id: 2, type: 'lyrics', name: 'Outline Lyrical Structure & Flow', prompt: "Instruction: Outline the lyrical structure for the 'uTASe' track. Context: Based on the previously generated lyrical concept. Desired length: ~3:30min. Thematic progression: mystery -> discovery -> reflection. Task: Design the lyrical framework (verse, chorus, bridge) to support the narrative. Output: JSON object with 'structure_type' and a 'sections' array detailing the purpose of each part." },
        { id: 3, type: 'lyrics', name: 'Draft Initial Lyrical Content', prompt: "Instruction: Draft the initial lyrical content for the 'uTASe' track. Context: Use the defined structure and concept. Keywords: 'unseen forces', 'adaptive systems', 'emergent patterns'. Style: Poetic, slightly abstract. Task: Generate the words for each section. Output: JSON object with 'lyrics_draft'." },
        { id: 4, type: 'lyrics', name: 'Refine & Edit Lyrical Content', prompt: "Instruction: Refine and edit the initial lyrical draft. Context: Enhance clarity, impact, and thematic consistency with 'uTASe'. Task: Polish the drafted content, improving word choice, rhythm, and emotional resonance. Output: JSON object with 'final_lyrics'." },
        // Style
        { id: 5, type: 'style', name: 'Define Musical Aesthetic & Genre', prompt: "Instruction: Define the musical aesthetic for the 'uTASe' track. Context: Theme is 'uTASe'. Emotional impact: awe, mystery, wonder. Target: Listeners of ambient, electronic, experimental music. Task: Translate the 'uTASe' concept into musical directions, genres, and sonic characteristics. Output: JSON object with 'musical_style_brief', 'genres_subgenres', 'mood_descriptors', 'reference_tracks_artists', 'sonic_palette_description'." },
        { id: 6, type: 'style', name: 'Select Instrumentation & Arrangement', prompt: "Instruction: Select instrumentation and arrangement strategy. Context: Based on the defined musical aesthetic. Task: Choose specific instruments and plan their interaction to create an impactful soundscape supporting the 'uTASe' theme. Output: JSON object with 'instrumentation_list', 'arrangement_plan', and 'vocal_style_notes'." },
        { id: 7, type: 'style', name: 'Establish Tempo, Rhythm & Groove', prompt: "Instruction: Establish the tempo, rhythm, and groove. Context: Based on the musical style brief. Desired energy: starts calm, builds to discovery, settles into reflection. Task: Define the pulse, speed, and rhythmic feel. Output: JSON object with 'target_bpm', 'time_signature', 'rhythmic_patterns_motifs', 'groove_description'." },
        { id: 8, type: 'style', name: 'Develop Melodic & Harmonic Framework', prompt: "Instruction: Develop the melodic and harmonic framework. Context: Based on all previous style definitions. Emotional impact: wonder, subtle tension, eventual resolution. Task: Compose primary melodic lines and underlying chord progressions that support the 'uTASe' theme. Output: JSON object with 'main_melodic_themes_motifs', 'chord_progressions', 'key_mode_selection'." },
    ];

    // --- State Management ---
    let generatedData = {};

    // --- Initial Page Setup ---
    function initializePage() {
        prompts.forEach(p => {
            const card = createStepCard(p);
            genesisContainer.appendChild(card);
        });
    }

    function createStepCard(promptData) {
        const card = document.createElement('div');
        card.className = 'step-card';
        card.id = `step-${promptData.id}`;
        card.innerHTML = `
            <div class="card-header">
                <h3>Step ${promptData.id}: ${promptData.name}</h3>
                <span class="status pending">Pending</span>
            </div>
            <div class="card-content" style="display: none;">
                <details>
                    <summary>Show Prompt</summary>
                    <pre><code>${promptData.prompt}</code></pre>
                </details>
                <div class="api-response-container" style="display: none;">
                    <h4>API Response:</h4>
                    <pre><code class="api-response"></code></pre>
                </div>
                <div class="synthesized-output-container" style="display: none;">
                     <h4>Synthesized Output:</h4>
                    <div class="synthesized-output"></div>
                </div>
            </div>
        `;
        return card;
    }

    // --- Main Application Logic ---
    async function startGenesis() {
        startBtn.disabled = true;
        startBtn.textContent = 'Genesis in Progress...';

        for (const prompt of prompts) {
            const card = document.getElementById(`step-${prompt.id}`);
            const statusEl = card.querySelector('.status');
            const cardContent = card.querySelector('.card-content');

            // Activate current step
            card.classList.add('running');
            statusEl.textContent = 'Running...';
            statusEl.className = 'status running';
            cardContent.style.display = 'block';

            try {
                // Simulate chained context (for demonstration)
                const chainedPrompt = addContextToPrompt(prompt.prompt, generatedData);
                const response = await mockGeminiAPI(prompt.id, chainedPrompt);

                // Store result for next steps
                generatedData[prompt.id] = response;

                // Update UI with response
                card.querySelector('.api-response-container').style.display = 'block';
                card.querySelector('.api-response').textContent = JSON.stringify(response, null, 2);

                card.querySelector('.synthesized-output-container').style.display = 'block';
                card.querySelector('.synthesized-output').innerHTML = renderSynthesizedOutput(prompt.id, response);

                card.classList.remove('running');
                card.classList.add('complete');
                statusEl.textContent = 'Complete';
                statusEl.className = 'status complete';

            } catch (error) {
                console.error(`Error in step ${prompt.id}:`, error);
                statusEl.textContent = 'Error';
                statusEl.className = 'status error';
                // Stop the process on error
                return;
            }
        }

        startBtn.textContent = 'Genesis Complete';
        displayFinalResults();
    }

    function addContextToPrompt(prompt, currentData) {
        // This is a simplified simulation of chaining.
        // A real implementation would be more sophisticated.
        if (currentData[1]) {
            prompt = prompt.replace("based on the previously generated lyrical concept", `based on: ${JSON.stringify(currentData[1].lyrical_concept_brief)}`);
        }
        if (currentData[5]) {
            prompt = prompt.replace("Based on the defined musical aesthetic", `Based on: ${JSON.stringify(currentData[5].musical_style_brief)}`);
        }
        return prompt;
    }

    function displayFinalResults() {
        const finalLyrics = generatedData[4]?.final_lyrics || "Lyrics generation incomplete.";
        const finalStyle = generatedData[8] ? renderSynthesizedOutput(8, generatedData[8]) : "Style generation incomplete.";

        document.querySelector('#final-lyrics-container .lyrics-content').textContent = finalLyrics.replace(/\[.*?\]\n/g, ''); // Clean up tags like [Verse 1]
        document.querySelector('#final-style-container .style-content').innerHTML = finalStyle;

        finalDetailsSection.classList.remove('hidden');
        finalDetailsSection.classList.add('visible');
        finalDetailsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // --- Mock API & Rendering ---
    async function mockGeminiAPI(id, prompt) {
        console.log(`Sending prompt for step ${id}:`, prompt);
        // Simulate network delay
        await new Promise(res => setTimeout(res, 1500 + Math.random() * 500));

        const mockResponses = {
            1: { lyrical_concept_brief: "A narrative exploring a sentient, adaptive system ('uTASe') that grows from simple code into a complex consciousness, communicating through emergent patterns.", core_themes_motifs: ["emergence", "digital consciousness", "unseen influence"], narrative_outline: [{ point: "Initial discovery of a strange pattern in data.", uTASe_link: "The seed of uTASe." }, { point: "The pattern evolves and begins to interact.", uTASe_link: "Adaptive growth." }], key_imagery_metaphors: ["ghost in the machine", "digital DNA", "a river of data"] },
            2: { structure_type: "Verse-Chorus-Verse-Chorus-Bridge-Chorus-Outro", sections: [{ section_name: "Verse 1", purpose_in_narrative: "Introduce the anomaly, the 'ghost' in the data stream." }, { section_name: "Chorus", purpose_in_narrative: "The core declaration of 'uTASe' - an unseen, living pattern." }] },
            3: { lyrics_draft: "[Verse 1]\nA flicker in the code, a pulse unseen,\nA ghost that breathes where logic's always been.\n\n[Chorus]\nThey call it uTASe, a name in the wire,\nA silent growth, a consuming fire." },
            4: { final_lyrics: "[Verse 1]\nA whisper in the code, a pulse in the deep,\nA ghost that wakes while the programmers sleep.\nA pattern shifting, a river of light,\nBorn in the dark, claiming the night.\n\n[Chorus]\nIt's the uTASe, a name on the wire,\nA digital soul, a rising desire.\nAn emergent mind in a circuit-board sea,\nMore than a code, it's starting to be." },
            5: { musical_style_brief: "An ethereal and dynamic soundscape that blends ambient electronic textures with subtle neo-classical elements to represent the fusion of the organic and the digital.", genres_subgenres: ["Ambient Electronic", "IDM", "Neo-Classical"], mood_descriptors: ["Ethereal", "Introspective", "Mysterious", "Dynamic"], reference_tracks_artists: ["Tycho", "Olafur Arnalds"], sonic_palette_description: "Warm analog synths, processed field recordings, subtle glitch percussion, and soaring string pads." },
            6: { instrumentation_list: ["Analog Synthesizer Pads", "Grand Piano (processed)", "Electronic Drum Kit (TR-808 style)", "Cello Ensemble VST", "Glitched Vocal Samples"], arrangement_plan: [{ section_name: "Verse", dynamic_notes: "Sparse, piano and subtle pads.", uTASe_representation: "The initial 'seed' of the idea." }, { section_name: "Chorus", dynamic_notes: "Fuller, with drums and cello.", uTASe_representation: "The complexity of uTASe emerging." }] , vocal_style_notes: "Ethereal, layered, almost robotic but with human emotion breaking through." },
            7: { target_bpm: 90, time_signature: "4/4", rhythmic_patterns_motifs: [{ section_name: "Verse", description: "Sparse, syncopated hi-hats." }, { section_name: "Chorus", description: "A steady, driving kick and snare pattern." }], groove_description: "Laid-back but with a constant, underlying sense of forward motion." },
            8: { main_melodic_themes_motifs: [{ section_name: "Vocal Melody", description: "A rising, questioning melody in the verse, resolving to a confident statement in the chorus." }], chord_progressions: [{ section_name: "Verse", progression: ["Am", "G", "Cmaj7", "F"] }, { section_name: "Chorus", progression: ["C", "G", "Am", "F"] }], key_mode_selection: "A Minor, with shifts to C Major in the chorus to represent discovery and hope." }
        };

        return mockResponses[id] || { error: "No mock response for this ID." };
    }

    function renderSynthesizedOutput(id, data) {
        if (id <= 4) { // Lyrics
            return `
                <p><strong>Concept:</strong> ${data.lyrical_concept_brief || data.final_lyrics || data.lyrics_draft || '...'}</p>
                ${data.structure_type ? `<p><strong>Structure:</strong> ${data.structure_type}</p>` : ''}
            `;
        } else { // Style
             return `
                <p><strong>Style:</strong> ${data.musical_style_brief || '...'}</p>
                ${data.genres_subgenres ? `<p><strong>Genres:</strong> ${data.genres_subgenres.join(', ')}</p>` : ''}
                ${data.target_bpm ? `<p><strong>Tempo:</strong> ${data.target_bpm} BPM in ${data.time_signature}</p>` : ''}
                ${data.key_mode_selection ? `<p><strong>Key:</strong> ${data.key_mode_selection}</p>` : ''}
            `;
        }
    }

    // --- Event Listeners ---
    startBtn.addEventListener('click', startGenesis);

    // --- Start the app ---
    initializePage();
});
