function display_hide(commentId){
    var x = document.getElementById("comment-"+commentId)
    if (x.style.display == "none"){
        x.style.display = "block";
    }else{
        x.style.display = "none";
    }
}