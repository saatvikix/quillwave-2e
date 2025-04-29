document.querySelectorAll(".like-btn").forEach(button => {
    button.addEventListener("click", function () {
        const postId = this.getAttribute("data-post-id");
        const likeCount = document.getElementById(`like-count-${postId}`);

        fetch(`/like/${postId}/`, {  // <-- trailing slash added here
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.likes !== undefined) {
                likeCount.innerText = data.likes;
                this.classList.toggle("liked", data.liked);
            }
        })
        .catch(error => console.error("Error:", error));
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie("csrftoken");