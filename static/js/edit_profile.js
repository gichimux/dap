$(document).ready(function() {
    // Function to get the CSRF token from the cookie
    function getCSRFToken() {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, 'csrftoken'.length + 1) === 'csrftoken=') {
                    cookieValue = decodeURIComponent(cookie.substring('csrftoken='.length));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Attach an event listener to the file input field
    $('#avatar-input').on('change', function() {
        var input = this;
        var userAvatar = $('#user-avatar');
        var selectedAvatar = $('#selected-avatar');

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
                // Hide the user-avatar and display the selected-avatar
                userAvatar.hide();
                selectedAvatar.attr('src', e.target.result).show();

                // Automatically trigger the upload when a new image is selected
                uploadAvatar(input.files[0]);
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

    // Function to upload the selected image
    function uploadAvatar(file) {
        var formData = new FormData();
        formData.append('avatar', file);

        // Get the CSRF token
        var csrfToken = getCSRFToken();

        if (csrfToken) {
            // Add the CSRF token as a header
            $.ajaxSetup({
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });

            $.ajax({
                type: 'POST',
                url: '/upload_avatar/',  // Replace with your actual URL
                data: formData,
                processData: false,
                contentType: false,
                success: function(data) {
                    // Update the selected-avatar with the uploaded image
                    $('#selected-avatar').attr('src', data.avatar_url).show();

                    // Hide the user-avatar
                    $('#user-avatar').hide();

                    // Close the modal
                    $('#AvatarModal').modal('hide');
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                    // Handle the error as needed
                }
                });
            }
        }



        // edit modal
        
    });
    

    
    // Keep your existing code for other functionality
