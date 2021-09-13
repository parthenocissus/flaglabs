$(document).ready(function () {

    let flagSelectAPI = "_get_selected",
        urlSelect = $SCRIPT_ROOT + flagSelectAPI;

    let flags = $("#flags");

    $.getJSON(urlSelect, {vector: 0}, (result) => {
        flags.empty();
        result.forEach((i) => {
            flags.append(i);
        });
    }).done(() => {
        console.log("flags received from backend, baby");
    });

});