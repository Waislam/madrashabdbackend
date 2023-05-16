function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

jQuery(function($){
    $(document).ready(function(){
        $("#id_division").change(function(){
            $.ajax({
                url:"/accounts/district/",
                type:"POST",
                data:{division: $(this).val(),},
                success: function(result) {
                    console.log(result);
                    cols = document.getElementById("id_district");
                    cols.options.length = 0;
                    cols.options.add(new Option("District", "District"));
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });
        });
        $("#id_district").change(function(){
            $.ajax({
                url:"/accounts/thana/",
                type:"POST",
                data:{district: $(this).val(),},
                success: function(result) {
                    console.log(result);
                    cols = document.getElementById("id_thana");
                    cols.options.length = 0;
                    cols.options.add(new Option("Thana", "Thana"));
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });
        });
        $("#id_district").change(function(){
            $.ajax({
                url:"/accounts/post-office/",
                type:"POST",
                data:{district: $(this).val(),},
                success: function(result) {
                    console.log(result);
                    cols = document.getElementById("id_post_office");
                    cols.options.length = 0;
                    cols.options.add(new Option("Post-Office", "Post-Office"));
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });
        });
        $("#id_post_office").change(function(){
            $.ajax({
                url:"/accounts/post-code/",
                type:"POST",
                data:{post_office: $(this).val(),},
                success: function(result) {
                    console.log(result);
                    cols = document.getElementById("id_post_code");
                    cols.options.length = 0;
                    cols.options.add(new Option("Post-Code", "Post-Code"));
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });
        });
    });
});