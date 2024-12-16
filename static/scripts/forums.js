var ArticleExercise;
(function (ArticleExercise) {
    ArticleExercise.baseURL = `http://localhost:5000`;
})(ArticleExercise || (ArticleExercise = {}));
document.addEventListener("DOMContentLoaded", async () => {
    loadComments();
    const commentButton = document.getElementById("post-button");
    commentButton.addEventListener("click", postComment);
    const commentField = document.getElementById("post-field");
    commentField.addEventListener("keyup", (event) => {
        if (event.code === "Enter") {
            postComment();
        }
    });
});
async function loadComments() {
    const articleIDField = document.getElementById("articleID");
    const articleID = articleIDField.value;
    const commentsURL = `${ArticleExercise.baseURL}/api/v1/comments/${articleID}`;
    const response = await fetch(commentsURL);
    const commentIndex = await validateJSON(response);
    for (const comment of commentIndex.comments) {
        appendComment(comment);
    }
}
async function appendComment(comment) {
    const commentsSection = document.getElementById("comment-list");
    const commentDiv = document.createElement("div");
    commentsSection.appendChild(commentDiv);
    commentDiv.innerText = comment.text;
    commentDiv.classList.add("comment");
}
async function postComment() {
    const articleIDField = document.getElementById("articleID");
    const articleID = articleIDField.value;
    const commentField = document.getElementById("comment-field");
    const commentText = commentField.value;
    const comment = {
        "articleID": articleID,
        "text": commentText
    };
    commentField.value = "";
    const commentPostURL = `${ArticleExercise.baseURL}/api/v1/comments/${articleID}`;
    const response = await fetch(commentPostURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(comment)
    });
    const serverComment = await validateJSON(response);
    console.log(serverComment);
    appendComment(serverComment);
    commentField.value = "";
}
