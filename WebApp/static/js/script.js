document.addEventListener('DOMContentLoaded', function () {

  $("#loading-icon").addClass('d-none')
    // Function to toggle the sidebar collapse state based on screen size
    function toggleSidebarCollapse() {
        var sidebarCollapse = document.getElementById('sidebarCollapse');
        var windowWidth = window.innerWidth;

        // If the window width is less than the Bootstrap 'lg' breakpoint (992px), collapse the sidebar
        if (windowWidth < 992) {
            sidebarCollapse.classList.add('collapse');
        } else {
            sidebarCollapse.classList.remove('collapse');
        }
    }

    // Call the function on page load
    toggleSidebarCollapse();

    // Call the function whenever the window is resized
    window.addEventListener('resize', toggleSidebarCollapse);

    HeartHealthMeter(0);
});


function HeartHealthMeter(value=60){
    var data = [
        {
          domain: { x: [0, 1], y: [0, 1] },
          value: value ,
        //   title: { text: "Heart Health Meter" },
          type: "indicator",
          mode: "gauge+number",
          delta: { reference: 90 },
          gauge: { 
              axis: { range: [null, 100]},
              bar: { color: "#fff" },
            steps: [
                { range: [0, 30], color: "#ff6b6b" },
                { range: [30.1, 60], color: "#fffa6b" },
                { range: [60.1, 100], color: "#70ff6b" }
              ],
         }
        }
      ];
      
      var layout = { 
        width: 450, 
        height: 260,
        // margin:{l:0,r:0},
        margin: { t: 5, b: 5, l: 30, r: 30 } 
        // border:"1px solid black"
    };
      Plotly.newPlot('heartHealthMeter', data, layout);
      
}