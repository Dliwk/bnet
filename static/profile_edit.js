$(function () {
    $('form.profile').submit(function () {
        $("#input-fullname").val($("#profile-fullname").text());
        $("#input-about").val($("#profile-about").text());
    });
});
