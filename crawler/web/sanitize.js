(function() {

    function load_jq(callback) {
        var script = document.createElement("script")
        script.type = "text/javascript";
        script.src = "https://code.jquery.com/jquery-3.5.1.min.js";
        document.getElementsByTagName("head")[0].appendChild(script);
    }

    function remove_invisible() {
        var $ = window.jQuery;
        $('*').each(function() {
            if ($(this).css('visibility') == 'hidden' || $(this).css('display') == 'none') {
                $(this).remove()
            }
        });
    }

    function try_remove() {
        try {
            remove_invisible()
        } catch (e) {
            setTimeout(try_remove, 100)
        }
    }

    try {
        remove_invisible()
    } catch (e) {
        load_jq()
        setTimeout(try_remove, 100)
    }

})();