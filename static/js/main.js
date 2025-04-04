// Summary form handler
document
  .getElementById("summaryForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    // Show loading indicator
    document.getElementById("loading").classList.remove("hidden");
    // Disable submit button
    document.getElementById("submitBtn").disabled = true;
    document
      .getElementById("submitBtn")
      .classList.add("opacity-50", "cursor-not-allowed");

    try {
      const formData = new FormData(this);
      const response = await fetch("/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      // Add new summary to the list
      const summariesList = document.querySelector(".space-y-2");
      const newSummaryHtml = `
            <div class="group flex items-center justify-between p-3 hover:bg-gray-50 rounded transition-colors duration-150">
                <div class="cursor-pointer flex-grow" onclick="loadSummary('${data.video_id}')">
                    <h3 class="font-semibold text-gray-700">${data.title}</h3>
                    <p class="text-sm text-gray-500">Saved ${data.created_at}</p>
                </div>
                <button onclick="deleteSummary('${data.video_id}', this)" 
                        class="opacity-0 group-hover:opacity-100 transition-opacity duration-150 text-red-500 hover:text-red-700 p-2 rounded-full hover:bg-red-50">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                </button>
            </div>
        `;
      summariesList.insertAdjacentHTML("afterbegin", newSummaryHtml);

      // Update the summary content
      const summaryContent = document.getElementById("summaryContent");
      summaryContent.innerHTML = `
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" data-video-id="${
              data.video_id
            }">
                <h2 class="text-xl font-bold text-gray-800 mb-4">${
                  data.title
                }</h2>
                ${
                  data.duration_minutes > 0
                    ? `
                    <div class="mb-4 text-green-600 font-semibold">
                        You just saved ${data.duration_minutes} minutes! 🎉
                    </div>
                `
                    : ""
                }
                <p class="text-gray-600 whitespace-pre-line">${data.summary}</p>
            </div>
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <h3 class="text-xl font-bold text-gray-800 mb-4">Should You Watch? 🤔</h3>
                <div class="prose">
                    ${data.analysis}
                </div>
            </div>
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <h3 class="text-xl font-bold text-gray-800 mb-4">Ask a Question 🤔</h3>
                <form id="questionForm" class="mb-4">
                    <div class="flex gap-4">
                        <input type="text" 
                               id="questionInput" 
                               class="flex-grow shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" 
                               placeholder="Ask a question about the video content...">
                        <button type="submit" 
                                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                            Ask
                        </button>
                    </div>
                </form>
                <div id="questionLoading" class="hidden">
                    <div class="flex items-center justify-center">
                        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                        <span class="ml-2 text-gray-600">Thinking...</span>
                    </div>
                </div>
                <div id="questionAnswer" class="mt-4"></div>
            </div>
        `;

      // Clear the form
      this.reset();
    } catch (error) {
      console.error("Error:", error);
      // Show error message
      const errorDiv = document.createElement("div");
      errorDiv.className =
        "bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative";
      errorDiv.innerHTML = `<span class="block sm:inline">Error processing video: ${error.message}</span>`;
      document.getElementById("summaryContent").prepend(errorDiv);
    } finally {
      // Hide loading indicator and enable submit button
      document.getElementById("loading").classList.add("hidden");
      document.getElementById("submitBtn").disabled = false;
      document
        .getElementById("submitBtn")
        .classList.remove("opacity-50", "cursor-not-allowed");
    }
  });

async function deleteSummary(videoId, button) {
  if (!confirm("Are you sure you want to delete this summary?")) {
    return;
  }

  try {
    const response = await fetch(`/summary/${videoId}`, {
      method: "DELETE",
    });

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    // Remove the summary item from the list
    const summaryItem = button.closest(".group");
    summaryItem.remove();

    // If this was the currently displayed summary, clear the content
    const summaryContent = document.getElementById("summaryContent");
    if (summaryContent.querySelector(`[data-video-id="${videoId}"]`)) {
      summaryContent.innerHTML = "";
    }
  } catch (error) {
    console.error("Error deleting summary:", error);
    alert("Error deleting summary: " + error.message);
  }
}

async function loadSummary(videoId) {
  try {
    const response = await fetch(`/summary/${videoId}`);
    const data = await response.json();

    if (data.error) {
      console.error(data.error);
      return;
    }

    const summaryContent = document.getElementById("summaryContent");
    summaryContent.innerHTML = `
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" data-video-id="${videoId}">
                <h2 class="text-xl font-bold text-gray-800 mb-4">${
                  data.title
                }</h2>
                ${
                  data.duration_minutes > 0
                    ? `
                    <div class="mb-4 text-green-600 font-semibold">
                        You just saved ${data.duration_minutes} minutes! 🎉
                    </div>
                `
                    : ""
                }
                <p class="text-gray-600 whitespace-pre-line">${data.summary}</p>
            </div>
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <h3 class="text-xl font-bold text-gray-800 mb-4">Should You Watch? 🤔</h3>
                <div class="prose">
                    ${data.analysis}
                </div>
            </div>
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <h3 class="text-xl font-bold text-gray-800 mb-4">Ask a Question 🤔</h3>
                <form id="questionForm" class="mb-4">
                    <div class="flex gap-4">
                        <input type="text" 
                               id="questionInput" 
                               class="flex-grow shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" 
                               placeholder="Ask a question about the video content...">
                        <button type="submit" 
                                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                            Ask
                        </button>
                    </div>
                </form>
                <div id="questionLoading" class="hidden">
                    <div class="flex items-center justify-center">
                        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                        <span class="ml-2 text-gray-600">Thinking...</span>
                    </div>
                </div>
                <div id="questionAnswer" class="mt-4"></div>
            </div>
        `;

    // Reattach the question form handler
    document
      .getElementById("questionForm")
      .addEventListener("submit", handleQuestionSubmit);
  } catch (error) {
    console.error("Error loading summary:", error);
  }
}

async function handleQuestionSubmit(e) {
  e.preventDefault();

  const questionInput = document.getElementById("questionInput");
  const question = questionInput.value.trim();
  if (!question) return;

  const loadingDiv = document.getElementById("questionLoading");
  const answerDiv = document.getElementById("questionAnswer");
  const submitButton = this.querySelector('button[type="submit"]');

  // Show loading state
  loadingDiv.classList.remove("hidden");
  answerDiv.innerHTML = "";
  submitButton.disabled = true;
  submitButton.classList.add("opacity-50", "cursor-not-allowed");

  try {
    const videoId = document.querySelector("[data-video-id]")?.dataset.videoId;
    if (!videoId) {
      throw new Error("No video selected");
    }

    const response = await fetch(`/summary/${videoId}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    // Show the answer
    answerDiv.innerHTML = `
            <div class="bg-gray-50 rounded p-4">
                <p class="text-gray-700 whitespace-pre-line">${data.answer}</p>
            </div>
        `;
  } catch (error) {
    console.error("Error:", error);
    answerDiv.innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
                <span class="block sm:inline">Error: ${error.message}</span>
            </div>
        `;
  } finally {
    // Reset form and loading state
    questionInput.value = "";
    loadingDiv.classList.add("hidden");
    submitButton.disabled = false;
    submitButton.classList.remove("opacity-50", "cursor-not-allowed");
  }
}

// Add question form handler
document
  .getElementById("questionForm")
  .addEventListener("submit", handleQuestionSubmit);
