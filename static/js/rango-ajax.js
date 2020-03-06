$(document).ready(function() {

    $('#like_button').click(function() {
        var categoryIDvar;
        categoryIDvar = $(this).attr('data-categoryid');

        $.get(
            '/rango/like_category/', {'category_id': categoryIDvar},
            function(data) {
                $('#like_count').html(data);
                $('#like_button').hide();
            })
    });

    $('#search-input').keyup(function() {
        var searchQuery;
        searchQuery = $(this).val();

        $.get(
            '/rango/suggest/', {'suggestion':searchQuery}, 
            function(data) {
                $('#categories-listing').html(data);
            })
    });

    $('.rango_add_page').click(function() {
        var catId = $(this).attr('data-categoryid');
        var title = $(this).attr('data-title');
        var url = $(this).attr('data-url');
        var theButton = $(this)

        $.get('/rango/search_add_page', {'category_id':catId, 'title':title, 'url':url},
            function(data) {
                $('#page-listing').html(data);
                theButton.hide();
            })
    });

});