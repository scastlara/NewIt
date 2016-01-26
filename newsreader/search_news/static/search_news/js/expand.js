// This function makes the divs small - big to change on click
$(document).ready(function(){
    $('.wrapper').on('click', function (e) {
        this.expand = !this.expand;
        $(this).closest('.wrapper').find('.small-news, .big-news').toggleClass('small-news big-news');
    });
});
