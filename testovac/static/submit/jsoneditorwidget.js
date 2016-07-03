$.getJSON(
    "/submit/ajax/get_schema",
    function(data){
        var element = document.getElementById('editor_holder');
        var editor = new JSONEditor(element, {
            schema: data,
            theme: 'bootstrap3'
        });
    }
);
