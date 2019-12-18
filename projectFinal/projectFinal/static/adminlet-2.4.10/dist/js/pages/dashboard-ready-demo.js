/*
 * Author: Abdullah A Almsaeed
 * Date: 4 Jan 2014
 * Description:
 *      This is a demo file used only for the main dashboard (index.html)
 **/

$(function () {

    'use strict';

    // Make the dashboard widgets sortable Using jquery UI
    $('.connectedSortable').sortable({
        placeholder: 'sort-highlight',
        connectWith: '.connectedSortable',
        handle: '.box-header, .nav-tabs',
        forcePlaceholderSize: true,
        zIndex: 999999
    });
    $('.connectedSortable .box-header, .connectedSortable .nav-tabs-custom').css('cursor', 'move');
    $('#revenue-chart-div, #sales-chart').css('cursor', 'auto');
    /* jQueryKnob */
    $('.knob').knob();



    // Sparkline charts that under map
    var myvalues = [1000, 1200, 920, 927, 931, 1027, 819, 930, 1021];
    $('#sparkline-1').sparkline(myvalues, {
        type: 'line',
        lineColor: '#92c1dc',
        fillColor: '#ebf4f9',
        height: '50',
        width: '80'
    });
    myvalues = [515, 519, 520, 522, 652, 810, 370, 627, 319, 630, 921];
    $('#sparkline-2').sparkline(myvalues, {
        type: 'line',
        lineColor: '#92c1dc',
        fillColor: '#ebf4f9',
        height: '50',
        width: '80'
    });
    myvalues = [15, 19, 20, 22, 33, 27, 31, 27, 19, 30, 21];
    $('#sparkline-3').sparkline(myvalues, {
        type: 'line',
        lineColor: '#92c1dc',
        fillColor: '#ebf4f9',
        height: '50',
        width: '80'
    });



    /* Chart.js */
    //revenue chart
    var type = "line";
    var data = {
        labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        datasets: [
            {
                label: "今年",
                data: [10020, 20000, 42500, 20550, 16050, 35820, 25852, 26985, 25810, 60505, 50225, 25511, 25885],
                borderColor: 'rgba(60, 141, 188, 0.5)',
                backgroundColor: 'rgba(60, 141, 188, 0.5)'
            },
            {
                label: "去年同期",
                data: [5250, 10250, 20660, 43300, 41600, 10050, 20580, 30550, 30000, 30000, 36510, 34000, 15520],
                borderColor: 'rgba(160, 208, 224, 0.5)',
                backgroundColor: 'rgba(160, 208, 224, 0.5)'
            }
        ]
    };

    var ctx = document.getElementById("revenue-chart").getContext("2d");
    var chart = new Chart(ctx, {
        type: type,
        data: data,
        options: {
            maintainAspectRatio: false
        }
    });


    //-------------
    //- PIE CHART -
    //-------------
    // Get context with jQuery - using jQuery's .get() method.
    var pieChartCanvas = $('#pieChart').get(0).getContext('2d')

    console.log('pie')
    var pieData = {
        labels: ['一般商品', '服務銷售', '課程扣點'],
        datasets: [
            {
                data: [5, 4, 2],
                backgroundColor: ["#f56954", "#00a65a", "#f39c12"]
            }
        ]
    }
    var pieOptions = {
        title: {
            display: false,
            text: "PIE",
            fontColor: "indigo",
            fontSize: "24"
        }
    }
    var type = "doughnut"; //pie, doughnut
    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    var pieChart = new Chart(pieChartCanvas, {
        type: type,
        data: pieData,
        options: pieOptions
    });



    var barChartCanvas = $('#barChart').get(0).getContext('2d')
    var type = "bar"; //line, bar, horizontalBar,...

    var today = new Date().getDay();
    var day_list = ['日', '一', '二', '三', '四', '五', '六'];
    if (today != 6) {
        day_list = day_list.slice(today + 1).concat(day_list);
    }
    day_list = day_list.slice(0, 6);
    day_list.push('今日');

    var bar_data = {
        labels: day_list,
        datasets: [
            {
                label: '上周',
                backgroundColor: 'rgba(210, 214, 222, 1)',

                data: [65, 59, 80, 81, 56, 55, 40]
            },
            {
                label: '本周',
                backgroundColor: '#00a65a',

                data: [28, 48, 40, 19, 86, 27, 90]
            }
        ]
    }

    var bar_options = {
        title: {
            display: false,
            text: "小马视频",
            fontColor: "green",
            fontSize: "24"
        }
    };

    var bar_chart = new Chart(barChartCanvas, {
        type: type,
        data: bar_data,
        options: bar_options
    });

    // Fix for charts under tabs
    $('.box ul.nav a').on('shown.bs.tab', function () {
        donut.redraw();
    });

});
