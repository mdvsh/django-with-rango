/* For chapter 16 : Intro to jquery
$(document).ready(function() {
    $("#test_btn").click(function(){
        alert("You clicked the button using JQuery!");
    }); 
    $("#test_btn").removeClass('is-primary').addClass('is-success');
        $('p').hover(
        function() {
            $(this).css('color', 'red');
        },
        function() {
            $(this).css('color', 'black');
        });
    
    $('#about-btn').click(function() {
        msgStr = $('#msg').html();
        msgStr = msgStr + " ooo, fancy!";

        $('#msg').html(msgStr);
    })

});
*/