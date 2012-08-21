$(document).ready(function() {
    
    $("#months").hide();
    $("#show_months").show();

    $('#show_months').click( function() {
    $("#months").slideToggle();
    });
});
    
