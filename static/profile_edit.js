$(function () {
    $('form.profile').submit(function () {
        $("#input-fullname").val($("#profile-fullname").text());
        $("#input-about").val($("#profile-about").text());
        $("#input-background-image-url").val($("#profile-background-image-url").text());
    });
});
