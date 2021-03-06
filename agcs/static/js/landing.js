$(function(){
    $(document).on( 'scroll', function(){
        if ($(window).scrollTop() > 100) {
            $('.scroll-top-wrapper').addClass('show');
        }
        else {
            $('.scroll-top-wrapper').removeClass('show');
        }
    });
    $('.scroll-top-wrapper').on('click', scrollToTop);
});

function scrollToTop() {
    verticalOffset = typeof(verticalOffset) != 'undefined' ? verticalOffset : 0;
    element = $('body');
    offset = element.offset();
    offsetTop = offset.top;
    $('html, body').animate({scrollTop: offsetTop}, 500, 'linear');
}

function initMap() {
    var agcs = new google.maps.LatLng(33.023705,-96.772012);
    var infowindow = new google.maps.InfoWindow({
        content:
          '<div id="content">'+
            '<span style="font-size: 16px;">'+
              '<address>'+
                '1727 Nest Pl.<br>'+
                'Plano, TX 75093<br>'+
                '<a href="tel:+19726569338">(972) 656-9338</a>'+
              '</address>'+
              '<a href="https://maps.google.com?daddr=Alpha+Geek+Computer+Services+1727+Nest+Place+Plano+TX+75093"'+
                 'target="_blank">Get Directions <i class="fa fa-external-link-square"></i>'+
              '</a>'+
            '</span>'+
          '</div>'
    });

    var map = new google.maps.Map(document.getElementById('GoogleMap'), {
        center: agcs,
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl:false,
        streetViewControl:false
    });

    var marker = new google.maps.Marker({
        position:agcs,
        map: map,
        title: 'AGCS'
    });

    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
        map.setZoom(10);
        map.setCenter(marker.getPosition());
    });

    google.maps.event.addListener(map,'center_changed',function() {
        window.setTimeout(function() {
            map.panTo(marker.getPosition());
        },3000);
    });

    infowindow.open(map, marker);
}
