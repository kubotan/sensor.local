let isBackground = false;
document.addEventListener('webkitvisibilitychange', function(){
  if ( document.webkitHidden ) {
    // 非表示状態になった時の動作
    isBackground = true;
  } else {
    // 表示状態になった時の動作
    isBackground = false;
  }
}, false);

$(document).ready(function(){

  $.cookie.json = true;  // Allow save cookie of json format.

  let columns = [
    '温度(℃)',
    '湿度(%)',
    '気圧(hPa)',
    '二酸化炭素(ppm)',
    '照度(lx)',
    '放射線量(cpm)',
    '放射線量(μSv/h)'
  ];

  let hideColumns = [
    '気圧(hPa)',
    '二酸化炭素(ppm)',
    '照度(lx)',
    '放射線量(cpm)',
    '放射線量(μSv/h)'
  ];

  let diffArray = function (arr1, arr2) {
    var newArr = [];
    for(var a = 0 ; a < arr1.length; a++){
      if(arr2.indexOf(arr1[a]) === -1 ){
        newArr.push(arr1[a]);
      }    
    }
    for(var b = 0; b < arr2.length; b++){
      if(arr1.indexOf(arr2[b]) === -1 ){
         newArr.push(arr2[b]);
         }
    }
    return newArr;
  };

  let saveCookieHiddenColums = function (hidden) {
    $.cookie(
      'hiddenColumns',
      hidden,
      {
        expires: 365,
        domain: 'sensor.local',
        path: '/'
      }
    );
  };

  if($.cookie('hiddenColumns')) {
    hideColumns = $.cookie('hiddenColumns');
  } else {
    saveCookieHiddenColums(hideColumns);
  }

  let chart = c3.generate({
    bindto: '#chart',
    legend: {
      item: {
        onclick: function (d) { 
          chart.toggle(d);
          let shown = chart.data.shown().map(item => item.id);
          let hidden = diffArray(columns, shown);
          saveCookieHiddenColums(hidden);
        }
      }
    },
    spline: config.spline,
    data: {
      type: config.type,
      x: 'x',
      xFormat: '%Y/%m/%d %H:%M:%S',
      hide: hideColumns,
      columns: [],
    },
    zoom: {
      enabled: true
    },
    axis: {
      x: {
        type: 'timeseries',
        localtime: true,
        tick: {
          format: config.tickFormat,
        }
      }
    }
  });

  $(window).resize(function() {
    chart.resize({
      height: $('body').height() * 0.9,
      width: $('body').width() * 0.9
    });
  }).trigger('resize');

  let loadJson = function () {
    if(isBackground) {
      return;
    }

    $.getJSON(
      config.jsonPath + '?ts=' + $.now(),
      function(json){

        let data = {
          columns:[
            ['x'],
          ],
        };

        $.each(columns, function(index, value) {
          data.columns.push([value]);
        });

        $.each(json, function(index, value) {
          for(let i=0;i < data.columns.length;i++){
            if(i in value) {
              data.columns[i].push(value[i]);
            }
          }
        });

        chart.load(data);
      }
    );

  };

  loadJson();
  chart.axis.min({y: 1});

  if (config.intervalRealTime > 0) {
    setInterval(loadJson, config.intervalRealTime * 1000);
  }
});
