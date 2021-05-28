//--------------------------------------------Comment--------------------------------------------//

var commentModal = document.getElementById("commentModal");
var leaveCommBtn = document.getElementById("add_comment");
var commentSpan = document.getElementById("comment_modal_close");
var header = document.getElementById("comment_modal_header");
var parent = document.getElementById("comment_parent");

leaveCommBtn.onclick = function() {
    commentModal.style.display = "block";
}

commentSpan.onclick = function() {
    commentModal.style.display = "none";
    parent.value = "";
    header.innerText = "Leave the comment";
}

function addReply(parent_id){
    commentModal.style.display = "block";
    parent.value = parent_id
    header.innerText = "Reply to comment";
}

//--------------------------------------------Review--------------------------------------------//

var reviewModal = document.getElementById("reviewModal");
var addReviewBtn = document.getElementById("add_review");
var reviewSpan = document.getElementById("review_modal_close");

addReviewBtn.onclick = function() {
    if(user === 'AnonymousUser') {
        //redirect to login
        console.log("Login")
        window.location.href = login_url;
    }
    else
        reviewModal.style.display = "block";
}

reviewSpan.onclick = function() {
    reviewModal.style.display = "none";
}

//----------------------------------------------------------------------------------------//

window.onclick = function(event) {
    if (event.target == reviewModal) {
        reviewModal.style.display = "none";
    }
    if (event.target == commentModal) {
        parent.value = "";
        commentModal.style.display = "none";
        header.innerText = "Leave the comment";
    }
}