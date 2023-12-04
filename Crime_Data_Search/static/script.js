$(document).ready(function() {
    $('#filter1, #filter2, #crimeType, #perpetratorAge, #perpetratorSex, #victimAge, #victimSex').select2({
        placeholder: "Select an option",
        allowClear: true,
        closeOnSelect: false
    });

    $('#start-date').change(function() {
        var startDate = $(this).val();
        $('#end-date').attr('min', startDate);
    });

});
