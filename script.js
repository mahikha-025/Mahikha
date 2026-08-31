const MODEL_URL = "https://teachablemachine.withgoogle.com/models/hh8MwC0Iw/";

let recognizer = null;
let listening = false;
let classified = false;

const startButton = document.getElementById("btn-start");
const stopButton = document.getElementById("btn-stop");

const modelStatusText = document.getElementById("model-status-text");
const modelStatusDot = document.getElementById("model-status-dot");

const micStatusText = document.getElementById("mic-status-text");
const micStatusDot = document.getElementById("mic-status-dot");

const predictedClass = document.getElementById("predicted-class");
const confidencePercentage = document.getElementById("confidence-percentage");
const confidenceBar = document.getElementById("confidence-bar");

const probabilitiesContainer =
    document.getElementById("probabilities-container");

const loadingShimmer =
    document.getElementById("model-loading-shimmer");

const errorBanner =
    document.getElementById("error-banner");

const errorMessage =
    document.getElementById("error-message");

const closeErrorButton =
    document.getElementById("btn-close-error");


function showError(message) {
    errorMessage.textContent = message;
    errorBanner.classList.remove("hidden");
}


if (closeErrorButton) {
    closeErrorButton.addEventListener("click", () => {
        errorBanner.classList.add("hidden");
    });
}


async function loadModel() {

    try {

        modelStatusText.textContent = "Loading model...";
        modelStatusDot.className = "dot dot-loading";

        loadingShimmer.style.display = "block";

        const checkpointURL = MODEL_URL + "model.json";
        const metadataURL = MODEL_URL + "metadata.json";

        recognizer = speechCommands.create(
            "BROWSER_FFT",
            undefined,
            checkpointURL,
            metadataURL
        );

        await recognizer.ensureModelLoaded();

        const labels = recognizer.wordLabels();

        console.log("Model loaded successfully!");
        console.log("Classes:", labels);

        modelStatusText.textContent = "Model Ready";
        modelStatusDot.className = "dot dot-success";

        loadingShimmer.style.display = "none";

        startButton.disabled = false;

        displayClasses(labels);

    } catch (error) {

        console.error("MODEL ERROR:", error);

        modelStatusText.textContent = "Model Failed";
        modelStatusDot.className = "dot dot-error";

        loadingShimmer.style.display = "none";

        showError(
            "Model could not be loaded. Open F12 → Console and check the error."
        );

    }
}


function displayClasses(labels) {

    probabilitiesContainer.innerHTML = "";

    labels.forEach((label, index) => {

        const item = document.createElement("div");

        item.className = "probability-item";

        item.innerHTML = `
            <div class="probability-header">
                <span>${label}</span>
                <strong id="prob-${index}">
                    0%
                </strong>
            </div>

            <div class="probability-track">
                <div
                    class="probability-fill"
                    id="bar-${index}"
                    style="width:0%">
                </div>
            </div>
        `;

        probabilitiesContainer.appendChild(item);

    });
}


async function startListening() {

    if (!recognizer || listening) {
        return;
    }

    try {

        listening = true;
        classified = false;

        startButton.disabled = true;
        stopButton.disabled = false;

        predictedClass.textContent = "Listening...";

        confidencePercentage.textContent = "0%";
        confidenceBar.style.width = "0%";

        micStatusText.textContent = "Listening";
        micStatusDot.className = "dot dot-success";

        recognizer.listen(
            result => {

                if (classified) {
                    return;
                }

                const scores = result.scores;
                const labels = recognizer.wordLabels();

                let highestIndex = 0;

                for (let i = 1; i < scores.length; i++) {

                    if (scores[i] > scores[highestIndex]) {
                        highestIndex = i;
                    }

                }

                const bestLabel = labels[highestIndex];
                const confidence = scores[highestIndex];

                const percentage =
                    Math.round(confidence * 100);

                predictedClass.textContent = bestLabel;

                confidencePercentage.textContent =
                    percentage + "%";

                confidenceBar.style.width =
                    percentage + "%";

                updateProbabilities(labels, scores);

                /*
                 * Classify ONE sound and stop.
                 * Only accept the result when confidence is 70% or higher.
                 */
                if (confidence >= 0.70) {

                    classified = true;

                    setTimeout(() => {
                        stopListening();
                    }, 300);

                }

            },

            {
                includeSpectrogram: false,
                probabilityThreshold: 0
            }

        );

    } catch (error) {

        console.error("MICROPHONE ERROR:", error);

        showError(
            "Microphone access failed. Please allow microphone permission."
        );

        stopListening();

    }
}


function updateProbabilities(labels, scores) {

    labels.forEach((label, index) => {

        const percentage =
            Math.round(scores[index] * 100);

        const value =
            document.getElementById(`prob-${index}`);

        const bar =
            document.getElementById(`bar-${index}`);

        if (value) {
            value.textContent =
                percentage + "%";
        }

        if (bar) {
            bar.style.width =
                percentage + "%";
        }

    });
}


function stopListening() {

    if (recognizer && listening) {
        recognizer.stopListening();
    }

    listening = false;

    startButton.disabled = !recognizer;
    stopButton.disabled = true;

    micStatusText.textContent = "Stopped";
    micStatusDot.className = "dot";

}


startButton.addEventListener(
    "click",
    startListening
);


stopButton.addEventListener(
    "click",
    stopListening
);


loadModel();