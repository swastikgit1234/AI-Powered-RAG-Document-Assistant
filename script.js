const API_URL = "http://127.0.0.1:8000";


async function uploadFile() {

    const fileInput = document.getElementById("fileInput");
    const status = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {

        status.innerText = "Please select a PDF or TXT file.";

        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();

    formData.append("file", file);

    status.innerText = "Uploading and processing document...";

    try {

        const response = await fetch(
            `${API_URL}/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {

            status.innerText =
                data.detail || "Upload failed.";

            return;
        }

        status.innerText =
            `Success! ${data.filename} processed into ${data.chunks} chunks.`;

    } catch (error) {

        status.innerText =
            "Could not connect to the backend.";

        console.error(error);
    }
}


async function askQuestion() {

    const questionInput =
        document.getElementById("question");

    const answerDiv =
        document.getElementById("answer");

    const question =
        questionInput.value.trim();

    if (!question) {

        answerDiv.innerText =
            "Please enter a question.";

        return;
    }

    answerDiv.innerText =
        "Thinking...";

    try {

        const response = await fetch(
            `${API_URL}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {

            answerDiv.innerText =
                data.detail || "Something went wrong.";

            return;
        }

        answerDiv.innerText =
            data.answer;

    } catch (error) {

        answerDiv.innerText =
            "Could not connect to the backend.";

        console.error(error);
    }
}