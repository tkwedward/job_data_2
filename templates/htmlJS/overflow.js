function overflow(object){
  var widthArray = []
  d3.selectAll(object)
    .on("mouseover", function(){
      console.log(widthArray);
      let _this = d3.select(this)
      if (!widthArray[0]){
        widthArray[0] = +_this.style("width")
                             .slice(0,-2)
      }

      _this.style("overflow", "visible")
          .style("width", "auto")
      if (!widthArray[1]){
        widthArray[1] = _this.node().getBoundingClientRect()["width"]
      }

      if (widthArray[0]<widthArray[1]){
        _this.style("width", widthArray[1])
             .style("z-index", 300)
      } else {
        _this.style("width", widthArray[0])
      }


      console.log( widthArray);

      // let placholder = originalWidth
      // originalWidth = eWidth
      // eWdith = placholder
    })
    .on("mouseout", function(){
      console.log(widthArray);
      if (widthArray[0]<widthArray[1]){
        d3.select(this)
          .style("width", widthArray[0])
          .style("z-index", 0)
          .style("white-space", "nowrap")
          .style("text-overflow", "ellipsis")
          .style("overflow", "hidden")
      }
      widthArray = []
      //
      console.log( widthArray);
    })

}
