document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const dropzoneContent = document.getElementById("dropzone-content");
  const previewContainer = document.getElementById("preview-container");
  const imagePreview = document.getElementById("image-preview");
  const btnChangeImage = document.getElementById("btn-change-image");
  
  const predictionBox = document.getElementById("prediction-box");
  const predictedRoomBadge = document.getElementById("predicted-room-badge");
  const confidenceBars = document.getElementById("confidence-bars");
  
  const styleOptions = document.querySelectorAll(".style-option");
  const btnGenerate = document.getElementById("btn-generate");
  const btnText = btnGenerate.querySelector(".btn-text");
  const btnLoader = btnGenerate.querySelector(".btn-loader");
  
  const resultsSection = document.getElementById("results-section");
  const resultsRoomTag = document.getElementById("results-room-tag");
  const resultsStyleTag = document.getElementById("results-style-tag");
  const galleryGrid = document.getElementById("gallery-grid");
  
  // Modal Elements
  const modalViewer = document.getElementById("modal-viewer");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const modalCloseBackdrop = document.getElementById("modal-close-backdrop");
  const modalTitle = document.getElementById("modal-title");
  const modalSubtitle = document.getElementById("modal-subtitle");
  const modalPrompt = document.getElementById("modal-prompt");
  const baImgBefore = document.getElementById("ba-img-before");
  const baImgAfter = document.getElementById("ba-img-after");
  const baHandle = document.getElementById("ba-handle");
  const baContainer = document.getElementById("ba-container");
  const baAfterDiv = baContainer.querySelector(".ba-after");
  const btnDownloadModal = document.getElementById("btn-download-modal");
  
  // Train Modal Elements
  const modalTrain = document.getElementById("modal-train");
  const btnTrainModal = document.getElementById("btn-train-modal");
  const trainCloseBtn = document.getElementById("train-close-btn");
  const trainCloseBackdrop = document.getElementById("train-close-backdrop");
  const btnTriggerRetrain = document.getElementById("btn-trigger-retrain");
  const trainLog = document.getElementById("train-log");

  // State Variables
  let currentFile = null;
  let currentPrediction = null;
  let selectedStyle = "simple";
  let lastRedesignData = null;

  // --- Drag & Drop Handlers ---
  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  });

  btnChangeImage.addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.click();
  });

  function handleFile(file) {
    if (!file.type.startsWith("image/")) {
      alert("Please upload a valid room image file (JPG, PNG, WEBP).");
      return;
    }

    currentFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
      dropzoneContent.classList.add("hidden");
      previewContainer.classList.remove("hidden");
      
      // Trigger PyTorch Room Prediction & Non-room Validation
      runRoomPrediction(file);
    };
    reader.readAsDataURL(file);
  }

  // --- PyTorch Room Classifier & Non-Room Validation ---
  async function runRoomPrediction(file) {
    predictedRoomBadge.textContent = "Analyzing Image...";
    predictedRoomBadge.className = "predicted-room-badge";
    predictionBox.classList.remove("hidden");
    confidenceBars.innerHTML = `<div class="spinner" style="margin:10px auto;"></div>`;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        body: formData
      });
      const data = await response.json();

      if (data.success) {
        currentPrediction = data.result;
        renderPrediction(data.result);
      } else {
        predictedRoomBadge.textContent = "Prediction Failed";
      }
    } catch (err) {
      console.error("Prediction Error:", err);
      predictedRoomBadge.textContent = "Server Error";
    }
  }

  function renderPrediction(result) {
    if (result.is_room) {
      // Valid Room Detected
      predictedRoomBadge.textContent = `${result.predicted_display} (${result.confidence}%)`;
      predictedRoomBadge.className = "predicted-room-badge room-valid";
      
      btnGenerate.classList.remove("disabled");
      btnGenerate.removeAttribute("disabled");

      // Render Confidence Breakdown Bars
      confidenceBars.innerHTML = `<p class="prediction-hint-msg text-success"><i class="fa-solid fa-circle-check"></i> ${result.message}</p>`;
      const confs = result.confidences;
      
      for (const key in confs) {
        const item = confs[key];
        const itemEl = document.createElement("div");
        itemEl.className = "confidence-item";
        itemEl.innerHTML = `
          <span class="conf-name">${item.name}</span>
          <div class="conf-bar-wrapper">
            <div class="conf-bar-fill" style="width: ${item.confidence}%;"></div>
          </div>
          <span class="conf-val">${item.confidence}%</span>
        `;
        confidenceBars.appendChild(itemEl);
      }
    } else {
      // Non-Room Image Detected
      predictedRoomBadge.textContent = "⚠️ Not a Room Image";
      predictedRoomBadge.className = "predicted-room-badge room-invalid";
      
      btnGenerate.classList.add("disabled");
      btnGenerate.setAttribute("disabled", "true");

      confidenceBars.innerHTML = `
        <div class="non-room-alert">
          <i class="fa-solid fa-triangle-exclamation"></i>
          <div>
            <strong>Non-Room Image Detected</strong>
            <p>${result.message}</p>
          </div>
        </div>
      `;
    }
  }

  // --- Style Selector Handling ---
  styleOptions.forEach((option) => {
    option.addEventListener("click", () => {
      styleOptions.forEach((opt) => opt.classList.remove("active"));
      option.classList.add("active");
      selectedStyle = option.getAttribute("data-style");
    });
  });

  // --- Hugging Face Redesign Generation ---
  btnGenerate.addEventListener("click", async () => {
    if (!currentFile || !currentPrediction || !currentPrediction.is_room) return;

    // Set Loading State
    btnGenerate.classList.add("disabled");
    btnGenerate.setAttribute("disabled", "true");
    btnText.classList.add("hidden");
    btnLoader.classList.remove("hidden");

    resultsSection.classList.add("hidden");

    const formData = new FormData();
    formData.append("file", currentFile);
    formData.append("style", selectedStyle);
    formData.append("room_category", currentPrediction.predicted_category);

    try {
      const response = await fetch("/api/redesign", {
        method: "POST",
        body: formData
      });
      const data = await response.json();

      if (data.success) {
        lastRedesignData = data.redesign;
        renderRedesignGallery(data.redesign);
      } else {
        alert(data.message || "Unable to redesign non-room image.");
      }
    } catch (err) {
      console.error("Redesign generation error:", err);
      alert("Failed to connect to Hugging Face Redesign API.");
    } finally {
      // Restore Button State
      btnGenerate.classList.remove("disabled");
      btnGenerate.removeAttribute("disabled");
      btnText.classList.remove("hidden");
      btnLoader.classList.add("hidden");
    }
  });

  // --- Render 4 Architecture-Preserved Img2Img Redesign Variations Gallery ---
  function renderRedesignGallery(redesignData) {
    resultsRoomTag.textContent = redesignData.room_type;
    resultsStyleTag.textContent = `${redesignData.style_title} Style`;
    galleryGrid.innerHTML = "";

    redesignData.variations.forEach((item) => {
      const card = document.createElement("div");
      card.className = "gallery-card";
      card.innerHTML = `
        <div class="gallery-img-wrapper" data-id="${item.id}">
          <img src="${item.image_data}" alt="${item.title}">
          <div class="card-overlay">
            <span class="view-btn"><i class="fa-solid fa-expand"></i> View Before/After</span>
          </div>
        </div>
        <div class="gallery-card-body">
          <h4 class="gallery-card-title">${item.title}</h4>
          <span class="gallery-card-model"><i class="fa-solid fa-microchip"></i> ${item.model_used}</span>
          <div class="gallery-card-actions">
            <button class="btn-card-action btn-inspect" data-id="${item.id}">
              <i class="fa-solid fa-arrows-split-up-and-left"></i> Compare
            </button>
            <a href="${item.image_data}" download="AI_Interior_${redesignData.room_type}_Var${item.id}.jpg" class="btn-card-action">
              <i class="fa-solid fa-download"></i> Save
            </a>
          </div>
        </div>
      `;
      galleryGrid.appendChild(card);
    });

    resultsSection.classList.remove("hidden");
    resultsSection.scrollIntoView({ behavior: "smooth" });

    document.querySelectorAll(".gallery-img-wrapper, .btn-inspect").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const id = parseInt(btn.getAttribute("data-id"));
        openModalViewer(id);
      });
    });
  }

  // --- Before vs After Modal Slider ---
  function openModalViewer(variationId) {
    if (!lastRedesignData) return;

    const variation = lastRedesignData.variations.find((v) => v.id === variationId);
    if (!variation) return;

    modalTitle.textContent = `${lastRedesignData.room_type} - ${variation.title}`;
    modalSubtitle.textContent = `Style: ${lastRedesignData.style_title} | Engine: ${variation.model_used}`;
    modalPrompt.textContent = variation.prompt;

    baImgBefore.src = imagePreview.src;
    baImgAfter.src = variation.image_data;
    btnDownloadModal.href = variation.image_data;
    btnDownloadModal.download = `AI_Interior_${lastRedesignData.room_type}_Variation_${variationId}.jpg`;

    setSliderPosition(50);
    modalViewer.classList.remove("hidden");
  }

  function setSliderPosition(percentage) {
    const pos = Math.max(0, Math.min(100, percentage));
    baAfterDiv.style.width = `${pos}%`;
    baHandle.style.left = `${pos}%`;
  }

  let isDragging = false;
  baHandle.addEventListener("mousedown", () => (isDragging = true));
  window.addEventListener("mouseup", () => (isDragging = false));

  baContainer.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    const rect = baContainer.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const pct = (x / rect.width) * 100;
    setSliderPosition(pct);
  });

  baContainer.addEventListener("touchmove", (e) => {
    if (e.touches && e.touches[0]) {
      const rect = baContainer.getBoundingClientRect();
      const x = e.touches[0].clientX - rect.left;
      const pct = (x / rect.width) * 100;
      setSliderPosition(pct);
    }
  });

  [modalCloseBtn, modalCloseBackdrop].forEach((el) => {
    el.addEventListener("click", () => modalViewer.classList.add("hidden"));
  });

  [trainCloseBtn, trainCloseBackdrop].forEach((el) => {
    el.addEventListener("click", () => modalTrain.classList.add("hidden"));
  });

  btnTrainModal.addEventListener("click", () => {
    modalTrain.classList.remove("hidden");
  });

  btnTriggerRetrain.addEventListener("click", async () => {
    btnTriggerRetrain.disabled = true;
    trainLog.classList.remove("hidden");
    trainLog.textContent = "Generating dataset & training PyTorch classifier...";

    try {
      const res = await fetch("/api/train", { method: "POST" });
      const data = await res.json();
      if (data.success) {
        trainLog.textContent = "Success! Room classifier model re-trained and updated.";
      } else {
        trainLog.textContent = "Training error: " + data.message;
      }
    } catch (e) {
      trainLog.textContent = "Error triggering model training.";
    } finally {
      btnTriggerRetrain.disabled = false;
    }
  });
});
