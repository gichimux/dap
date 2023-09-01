$(document).ready(function () {
    $('.comment-button').click(function () {
      const postID = $(this).data('post-id');
      const commentForm = $(`.comment-form[data-post-id="${postID}"]`);
      commentForm.toggle();
    });
  
    $('.comment-form').submit(function (e) {
      e.preventDefault();
      const form = $(this);
      const postID = form.data('post-id');
      const comment = form.find('[name="comment"]').val();
      const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // Extract CSRF token
  
      $.ajax({
        url: `/posts/${postID}/add_comment/`,
        method: 'POST',
        headers: { "X-CSRFToken": csrftoken }, // Include CSRF token in headers
        data: { comment: comment },
        success: function (data) {
          console.log('Comment posted successfully');
          form.removeClass('active');
          form.find('[name="comment"]').val('');
          // You might want to update the comment count here
          // Update the comment count in the post feed
            updateCommentCount(postID);
            
            // Increment the comment count displayed in the feed template
            const commentCountElement = $(`#comment-count-${postID}`);
            const currentCommentCount = parseInt(commentCountElement.text());
            commentCountElement.text(currentCommentCount + 1);
        },
        error: function (error) {
          console.error('Error posting comment');
        }
      });
    });
  
    $('.cancel-comment').click(function () {
      const form = $(this).closest('.comment-form');
      form.removeClass('active');
      form.find('[name="comment"]').val('');
    });
    

    ////////////
    $('.detail-comment-form').submit(function (e) {
      e.preventDefault();
      const form = $(this);
      const postID = form.data('post-id');
      const comment = form.find('[name="comment"]').val();
      const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // Extract CSRF token

      $.ajax({
          url: `/posts/${postID}/add_comment/`, // Replace with the actual URL
          method: 'POST',
          headers: { "X-CSRFToken": csrftoken }, // Include CSRF token in headers

          data: { comment: comment },
          success: function (data) {
              console.log('Comment posted successfully');
              // Handle success behavior, e.g., updating comment section
              window.location.reload();
          },
          error: function (error) {
              console.error('Error posting comment');
          }
      });
  });

  });

  // Function to update comment count using AJAX
function updateCommentCount(postID) {
  $.ajax({
      url: `/posts/${postID}/get_comment_count/`, // Update the URL to your view
      method: 'GET',
      success: function (data) {
          const commentCountElement = $(`#comment-count-${postID}`);
          commentCountElement.text(data.comment_count);
      },
      error: function (error) {
          console.error('Error getting comment count');
      }
  });
}
  

