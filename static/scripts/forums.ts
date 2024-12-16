namespace ArticleExercise {
    export const baseURL: string = `http://localhost:5000`;

    // define interfaces to match the API
    export interface Comment {
        id: number;
        articleID: number;
        timestamp: string;
        text: string;
    }
    export interface CommentList {
        requested: string;
        comments: Array<Comment>;
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    loadComments();

    // attach an event listener to the comment button to post comments
    const commentButton = <HTMLButtonElement> document.getElementById("post-button");
    commentButton.addEventListener("click", postComment);

    // attach an event listener to the comment field to submit on enter
    const commentField = <HTMLInputElement> document.getElementById("post-field");
    commentField.addEventListener("keyup", (event) => {
        if (event.code === "Enter") {
            postComment();
        }
    });
});

async function loadComments() {
    // get the article id from the hidden field
    const articleIDField = <HTMLInputElement> document.getElementById("articleID");
    const articleID = articleIDField.value;

    // define the url to fetch comments for this article
    const commentsURL = `${ArticleExercise.baseURL}/api/v1/comments/${articleID}`;
   
    // TODO: fetch all comments for this article and pass them to appendComment in order
    const response = await fetch(commentsURL);
    const commentIndex = <ArticleExercise.CommentList> await validateJSON(response);

    for (const comment of commentIndex.comments) {
        appendComment(comment);
    }
}

async function appendComment(comment: ArticleExercise.Comment) {
    const commentsSection = <HTMLDivElement> document.getElementById("comment-list");
    // TODO: create a new div for this comment and append it to the comments section
    const commentDiv = document.createElement("div");
    commentsSection.appendChild(commentDiv);

    // TODO: fill out the comment div with information from the given comment
    //       set its inner text to comment.text and add "comment" to its CSS classes
    commentDiv.innerText = comment.text;
    commentDiv.classList.add("comment");
}

async function postComment() {
    // get the article id from the hidden field
    const articleIDField = <HTMLInputElement> document.getElementById("articleID");
    const articleID = articleIDField.value;
    // get the contents of the comment field
    const commentField = <HTMLInputElement> document.getElementById("comment-field");
    const commentText = commentField.value;
    // create a comment object to be posted
    const comment = {
        "articleID": articleID,
        "text": commentText
    }
    // clear the text of the comment field before submitting
    commentField.value = "";

    // define the url to add a comment for this article
    const commentPostURL = `${ArticleExercise.baseURL}/api/v1/comments/${articleID}`;

    // create a post request to upload this comment to the server
    const response = await fetch(commentPostURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(comment)
    });

    // validate the JSON of the now inserted comment that comes back
    const serverComment = await validateJSON(response);
    console.log(serverComment);

    // insert this comment directly in the page for user feedback
    appendComment(serverComment);
    commentField.value = "";
}

// /**
//  * Validate a response to ensure the HTTP status code indcates success.
//  * 
//  * @param {Response} response HTTP response to be checked
//  * @returns {object} object encoded by JSON in the response
//  */
// async function validateJSON(response: Response) {
//     if (response.ok) {
//         return response.json();
//     } else {
//         return Promise.reject(response);
//     }
// }