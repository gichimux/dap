$(document).ready(function () {
    $('.bookmark-button').click(function () {
        var csrftoken = $('[name=csrfmiddlewaretoken]').val(); // Extract CSRF token
        var postID = $(this).siblings('input[name=post_id]').val(); // Extract post_id

        toggleBookmark(postID, csrftoken);
    });
});

function toggleBookmark(postID, csrftoken) {
    $.ajax({
        url: '/api/bookmark-toggle/',  // Update the URL as needed
        method: 'POST',
        headers: { "X-CSRFToken": csrftoken },
        data: { 'post_id': postID },
        success: function (data) {
            console.log('Bookmark toggled successfully');
        },
        error: function (error) {
            console.error('Error toggling bookmark');
        }
    });
}
