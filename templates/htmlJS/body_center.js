
var body_width = +$("body").css("width")
                           .slice(0,-2)
if (body_width>1280){
    var body_wrapper_width = $(".body_wrapper").css("width").slice(0,-2)

    var offset = 0.5*(body_width - body_wrapper_width)

    $(".body_wrapper").css("position", "absolute")
                      .css("left", offset)

    function overlay_offset_adjust(){
      var overlay_wrapper_width = $(".overlay_wrapper").css("width").slice(0,-2)

      var overlay_offset = 0.5*(body_width - overlay_wrapper_width)

      $(".overlay_wrapper").css("position", "absolute").css("left", overlay_offset)
    }//overlay_offset_adjust
}
