if (!$) { var $ = django.jQuery; }

var submit_receiver_configuration_templates;

function update_config() {
    var selected_template = $("#id_receiver_template").val();
    if (selected_template in submit_receiver_configuration_templates) {
        var template_json = submit_receiver_configuration_templates[selected_template];
        $("#id_configuration").val(JSON.stringify(template_json, null, 2));
    }
}

$(document).ready(function() {
    $.getJSON("/submit/ajax/get_receiver_templates/", function (data) {
        submit_receiver_configuration_templates = data;
        if ($("#id_configuration").val() == "{}") {
            update_config();
        }
    });

    $("#id_receiver_template").change(update_config);
});
