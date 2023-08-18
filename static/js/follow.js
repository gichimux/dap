$(document).ready(function() {
    // Function to get CSRF token
    function getCSRFToken() {
        return $("input[name='csrfmiddlewaretoken']").val();
    }

    $('.follow-button').click(function(e) {
        e.preventDefault();
        var profileUsername = $(this).data('profile-username');
        var button = $(this);

        $.ajax({
            url: '/follow/' + profileUsername + '/',
            type: 'post',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: getCSRFToken()  // Include the CSRF token
            },
            success: function(response) {
                if (response.success) {
                    if (response.action === 'follow') {
                        button.text('Unfollow');
                    } else if (response.action === 'unfollow') {
                        button.text('Follow');
                    }
                } else {
                    alert(response.message); // Display an error message if necessary
                }
            }
        });

        $.ajax({
            url: '/unfollow/' + profileUsername + '/',
            type: 'post',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: getCSRFToken()  // Include the CSRF token
            },
            success: function(response) {
                if (response.success) {
                    if (response.action === 'follow') {
                        button.text('Unfollow');
                    } else if (response.action === 'unfollow') {
                        button.text('Follow');
                    }
                } else {
                    alert(response.message); // Display an error message if necessary
                }
            }
        });
        
    });
});