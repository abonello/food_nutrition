$(document).ready(function(){
    $('.collapsible').collapsible();
    $('select').material_select();
    $('.button-collapse').sideNav();

    $('.panel-collapse').on('show.bs.collapse', function () {
        $(this).siblings('.panel-heading').addClass('active');
    });
    $('.panel-collapse').on('hide.bs.collapse', function () {
        $(this).siblings('.panel-heading').removeClass('active');
    });
});

function flipBox(front, back){
    var front = document.getElementById(front);
    var back = document.getElementById(back);
    var angle_front = rotate_degree(front);
    var angle_back = rotate_degree(back);

    if (angle_front == 0) {
        front.style.transform = "perspective(1000px) rotateY(-180deg)";
        back.style.transform = "perspective(1000px) rotateY(0deg)";
    } else if (angle_front == 180) {
        front.style.transform = "perspective(1000px) rotateY(0deg)";
        back.style.transform = "perspective(1000px) rotateY(180deg)";
    }
}

function rotate_degree(obj) {
    var st = window.getComputedStyle(obj, null);
    var matrix = st.getPropertyValue("transform");
    // 
    if(matrix !== 'none') {
        var values = matrix.split('(')[1].split(')')[0].split(',');
        var a = values[0];
        var b = values[1];
        var angle = Math.round(Math.atan2(b, a) * (180/Math.PI));
    } else { var angle = 0; }
    return (angle < 0) ? angle +=360 : angle;
} 

function toggleChevron(e) {
    $(e.target)
        .prev('.panel-heading')
        .find("i.indicator")
        .toggleClass('glyphicon-chevron-down glyphicon-chevron-up');
}
$('#accordion').on('hidden.bs.collapse', toggleChevron);
$('#accordion').on('shown.bs.collapse', toggleChevron);