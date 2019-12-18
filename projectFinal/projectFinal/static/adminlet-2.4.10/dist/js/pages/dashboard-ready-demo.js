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

    // The Calender
    $('#calendar').datepicker();

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
    // donut chart
    /*
    var type2 = "line";
    var data2 = {
        labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        datasets: [
            {
                label: "今年",
                data: [10, 20, 42, 20, 16, 35, 25, 26, 25, 60, 50, 25, 25],
                borderColor: 'rgba(60, 141, 188, 0.5)',
                backgroundColor: 'rgba(60, 141, 188, 0.5)'
            },
            {
                label: "去年同期",
                data: [52, 10, 20, 43, 41, 10, 20, 30, 30, 30, 36, 34, 15],
                borderColor: 'rgba(160, 208, 224, 0.5)',
                backgroundColor: 'rgba(160, 208, 224, 0.5)'
            }
        ]
    };

    var ctx2 = document.getElementById("sales-chart").getContext("2d");
    var chart2 = new Chart(ctx, {
        type: type2,
        data: data2,
        options: {
            maintainAspectRatio: false
        }
    });
    */
    // Donut Chart
    var donut = new Morris.Donut({
        element: 'sales-chart',
        resize: true,
        colors: ['#3c8dbc', '#f56954', '#00a65a'],
        data: [
            { label: '一般商品', value: 12 },
            { label: '服務', value: 30 },
            { label: '課程扣點', value: 20 }
        ],
        hideHover: 'auto'
    });

    // Fix for charts under tabs
    $('.box ul.nav a').on('shown.bs.tab', function () {
        donut.redraw();
    });

});
