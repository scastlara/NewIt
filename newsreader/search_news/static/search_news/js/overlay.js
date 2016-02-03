$('.news-overlay').hide();

$('.small-news').click(function(){
    $('.news-overlay').hide(250);
    $(this).next().slideToggle(450);
    return false;
});

$('.close-overlay').click(function(){
    $('.news-overlay').hide(250);
});

$("#sidebar").click(function() {
    $('.news-overlay').hide(250);
});

$(document).keyup(function(e) {
    if(e.keyCode== 27) {
        $('.news-overlay').hide(250);
    }
});
