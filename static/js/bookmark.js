$('.bookmark-button').click(function () {
    const postID = $(this).data('post-id');
    const button = $(this); // Store the button element for later use
    
    $.ajax({
      url: `/posts/${postID}/toggle_bookmark/`,
      type: 'POST',
      headers: { 'X-CSRFToken': getCookie('csrftoken') }, // Include the CSRF token
      data: {},
      success: function () {
          if (button.find('i').hasClass('fa-bookmark')) {
              button.find('i').removeClass('fa-bookmark').addClass('fa-bookmark-alt');
              button.html('<i class="fa-regular fa-bookmark-alt"></i> Bookmarked');
          } else {
              button.find('i').removeClass('fa-bookmark-alt').addClass('fa-bookmark');
              button.html('<i class="fa-regular fa-bookmark"></i> Bookmark');
          }
      },
      error: function (error) {
        console.error('Error toggling bookmark');
      }
    });
  });
  