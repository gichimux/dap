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

    // Attach event listeners to the file input fields
    $('#cover-image-input').on('change', function () {
        var input = this;
        var userCover = $('#user-cover');

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                // Hide the current cover image and display the selected cover image
                userCover.hide();
                userCover.attr('src', e.target.result).show();
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

    $('#avatar-modal-input').on('change', function () {
        var input = this;
        var userAvatar = $('#user-avatar');

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                // Hide the current avatar image and display the selected avatar image
                userAvatar.hide();
                userAvatar.attr('src', e.target.result).show();
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

    // Attach an event listener to the cover image input field
    $('#cover-image-input').on('change', function() {
        var input = this;
        var userCover = $('#user-cover');

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
                // Display the selected cover image
                userCover.attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

    // Attach an event listener to the avatar input field
    $('#avatar-modal-input').on('change', function() {
        var input = this;
        var userAvatar = $('#user-avatar');

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
                // Display the selected avatar image
                userAvatar.attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

   

   $('form').on('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData();

        // Append the cover image if it has changed
        var coverInput = $('#cover-image-input')[0];
        if (coverInput.files.length > 0) {
            formData.append('cover_image', coverInput.files[0]);
        }

        // Append the avatar image if it has changed
        var avatarInput = $('#avatar-modal-input')[0];
        if (avatarInput.files.length > 0) {
            formData.append('avatar', avatarInput.files[0]);
        }

        // Append other profile information
        formData.append('name', $('#id_name').val());
        formData.append('location', $('#id_location').val());
        formData.append('website', $('#id_website').val());
        formData.append('bio', $('#id_bio').val());

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
                url: '/update_profile/', // Replace with your actual URL for profile update
                data: formData,
                processData: false,
                contentType: false,
                success: function(data) {
                    // Handle the success response as needed
                    console.log('Profile updated successfully:', data);
                },
                error: function(xhr, status, error) {
                    console.error('Profile update error:', xhr.responseText);
                    // Handle the error as needed
                }
            });
        }
    });

    $('#save-changes-button').on('click', function () {
        // Assuming you have a modal with the id "myModal", close it
        $('#ProfileEditModal').modal('hide');

        // Reload the current page
        setTimeout(function() {
            location.reload();
        }, 1000); 
    });

});
