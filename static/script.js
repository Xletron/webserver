function playVideo(url) {
  const videoPlayer = document.getElementById("video-player");
  videoPlayer.src = url;
  const videoModal = document.getElementById("video-modal");
  videoModal.style.display = "flex"; // Show the video modal

  // Dynamically position the close button in the top right corner of the video modal
  const closeBtn = document.getElementsByClassName("close-button")[0];
  const modalHeader = document.getElementsByClassName("modal-header")[0];
  closeBtn.style.position = "absolute";
  closeBtn.style.top = "10px";
  closeBtn.style.right = "10px";
  closeBtn.style.margin = "8px";

  // Add event listeners
  closeBtn.addEventListener("click", closeVideo);
  videoModal.addEventListener("click", function(event) {
    if (event.target == videoModal) {
      closeVideo();
    }
  });
}

function closeVideo() {
  var modal = document.getElementById("video-modal");
  var videoPlayer = document.getElementById("video-player");
  modal.style.display = "none";
  videoPlayer.pause();
  videoPlayer.currentTime = 0;
}