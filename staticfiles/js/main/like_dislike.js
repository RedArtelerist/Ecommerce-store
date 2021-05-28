function like() {
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();
    console.log(like);

    $.ajax({
        url : "/" + type +"/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            var res = json.result;
            if(res === true){
                like.find("[data-icon='like']").removeClass("default").addClass("liked");
                var dis = dislike.find("[data-icon='dislike']");
                if(dis.hasClass("disliked"))
                    dis.removeClass("disliked").addClass("default");
            }
            else
                like.find("[data-icon='like']").removeClass("liked").addClass("default");

            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
        }
    });

    return false;
}

function dislike() {
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    $.ajax({
        url : "/" + type +"/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            var res = json.result;
            if(res === true){
                dislike.find("[data-icon='dislike']").removeClass("default").addClass("disliked");
                var lik = like.find("[data-icon='like']");
                if(lik.hasClass("liked"))
                    lik.removeClass("liked").addClass("default");
            }
            else
                dislike.find("[data-icon='dislike']").removeClass("disliked").addClass("default");

            dislike.find("[data-count='dislike']").text(json.dislike_count);
            like.find("[data-count='like']").text(json.like_count);
        }
    });

    return false;
}

// Connecting Handlers
$(function() {
    $('[data-action="like"]').click(like);
    $('[data-action="dislike"]').click(dislike);
});