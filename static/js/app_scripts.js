function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  

$(".tab").click(function(){
    $(".tabs-bar").find(".tab-active").removeClass("tab-active");
    $(".content-container").children().hide();
    $(this).addClass("tab-active");
    $(".content-" + this.id).show();
})

$(".form-tab").click(function(){
    $(".form-tabs-bar").find(".form-tab-active").removeClass("form-tab-active");
    $(".form-content-container").children().hide();
    $(this).addClass("form-tab-active");
    $(".form-content-" + this.id).show();
})

$('.file-input').on('change', function() {
    var fileName = $(this).val().split('\\').pop();
    $(this).next('.file-label').html('<span class="icon">📷</span> ' + fileName);
});

$('#id_image').change(function () {
    var fileInput = $(this)[0];
    if (fileInput.files && fileInput.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#thumbnail').attr('src', e.target.result);
            $('.thumbnail-container').show(); // Show the thumbnail container
        };
        reader.readAsDataURL(fileInput.files[0]);
    } else {
        $('.thumbnail-container').hide(); // Hide the thumbnail container
    }
});

$('.clear-image-button').click(function () {
    $('#id_image').val(null); // Clear the selected image
    $('.thumbnail-container').hide();
});


$('.show-more-link').click(function () {
    $(this).hide();
    $(this).siblings('.short-body').hide();
    $(this).siblings('.full-body').show();
    $(this).siblings('.show-less-link').show();

});

$('.show-less-link').click(function () {
    $(this).hide();
    $(this).siblings('.full-body').hide();
    $(this).siblings('.short-body').show();
    $(this).siblings('.show-more-link').show();
});

$('.topic-button').click(function() {
  const topic = $(this).data('topic');
  window.location.href = `/topics/${topic}/`; // Redirect to the topic URL
});

$('.copy-url-button').click(function () {
  const postURL = $(this).data('url');
  
  navigator.clipboard.writeText(postURL)
      .then(() => {
          // Show a notification or alert that URL is copied
          alert('URL copied to clipboard: ' + postURL);
      })
      .catch((error) => {
          console.error('Error copying URL:', error);
      });
});

// Select all comment textareas
var commentTextareas = $('.comment-form textarea');

// Function to adjust textarea height
function adjustTextareaHeight(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
}

// Attach input event listener to all comment textareas
commentTextareas.on('input', function () {
  adjustTextareaHeight(this);
});

// Initialize textarea heights
commentTextareas.each(function () {
  adjustTextareaHeight(this);
});

