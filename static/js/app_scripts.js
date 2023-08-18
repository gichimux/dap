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









