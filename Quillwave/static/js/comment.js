document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".comment-btn");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const postId = this.getAttribute("data-post-id");
            const commentSection = document.getElementById(`comment-section-${postId}`);

            if (commentSection) {
                // Toggle display of the comment form
                commentSection.style.display = 
                    commentSection.style.display === "block" ? "none" : "block";
            }
        });
    });

    // Add event listener for comment form submission
    document.querySelectorAll(".comment-form").forEach(form => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const postId = this.getAttribute("data-post-id");
            const formData = new FormData(this);  // Get form data

            fetch(`/add_comment/${postId}/`, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": document.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    // Append new comment dynamically
                    const commentList = document.getElementById(`comments-list-${postId}`);
                    const newComment = document.createElement("div");
                    newComment.classList.add("comment");
                    newComment.innerHTML = `<strong>${data.user}</strong>: ${data.content}`;
                    commentList.appendChild(newComment);

                    // Update the comment count
                    const commentCount = document.getElementById(`comment-count-${postId}`);
                    commentCount.innerText = parseInt(commentCount.innerText) + 1;

                    // Clear the comment input field
                    this.reset();
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});