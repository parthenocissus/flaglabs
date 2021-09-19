$(document).ready(function () {

    let sliderHtml = (key, label, type, data) => {
        return `<div id="slider-group"><div class="slider-div"><input type="range" ` +
            `id="${key}" name="${key}" min="${data.min}" max="${data.max}" ` +
            `value="${data.value}" step="${data.step}" data-input-type="${type}">` +
            `<label for="warm">${label}</label></div></div>`;
    };

    let selectHtml = (key, label) => {
        return `<option value="${key}">${label}</option>`;
    };

    let chosen = $(".chosen");
    let sliderGroup = $('#slider-group');
    let sliderHeader = $('#slider-header');

    for (let key in flagMappings) {
        $("#choose-params").append(selectHtml(key, flagMappings[key]["label"]));
    }

    chosen.chosen({max_selected_options: 5})
        .change(function () {
            sliderGroup.empty();
            let keys = $(this).val();
            let visible = (keys.length > 0) ? "visible" : "hidden";
            sliderHeader.css("visibility", visible);
            keys.forEach(key => {
                let type = flagMappings[key]["type"];
                let label = flagMappings[key]["label"];
                let data = flagMappings[key]["data"];
                sliderGroup.append(sliderHtml(key, label, type, data));
            });
        });

    chosen.bind("chosen:maxselected", () => {
        alert("Max parameters limit reached.");
    });

});