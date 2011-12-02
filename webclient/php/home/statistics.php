<?php
include_once("../config.php");
?>
<script type="text/javascript">
    Highcharts.theme = { colors: ['#4572A7'] };// prevent errors in default theme
    var highchartsOptions = Highcharts.getOptions();
</script>
<script type="text/javascript">
    var chart;
    jQuery(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'disk_space_chart',
                width: '500',
                height: '300',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotBorderColor: null,
                plotShadow: false,
                borderColor: null
            },
            title: {
                text: null,
                style: {
                        color: '#3E576F',
                        fontSize: '12px'
                       }
            },
            legend: {
                borderColor: '#DDDDDD'
            },
            credits: {
                enabled: false
            },
            colors: ['#048DC7',
                     '#249F00'
                    ],
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.point.name +'</b>: '+ this.y +' %';
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true,
                    borderColor: null,
                    shadow: null
                }
            },
            series: [{
                type: 'pie',
                name: 'Disk space',
                data: [
                    ['Usado',   41.0],
                    {
                        name: 'Libre',
                        y: 59.0,
                        sliced: true,
                        selected: true
                    },
                ]
            }]
        });
    });
</script>
<script type="text/javascript">

    var chart;
    jQuery(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'users_groups_chart',
                defaultSeriesType: 'area',
                width: '500',
                height: '300'
            },
            title: {
                text: null
            },
            subtitle: {
                text: null
            },
            legend: {
                borderColor: '#DDDDDD'
            },
            xAxis: {
                categories: ['Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio'],
                tickmarkPlacement: 'on',
                title: {
                    enabled: false
                }
            },
            yAxis: {
                title: {
                    text: 'Usuarios'
                },
                labels: {
                    formatter: function() {
                        return this.value;
                    }
                }
            },
            tooltip: {
                formatter: function() {
                    return ''+
                         this.x +': '+ Highcharts.numberFormat(this.y, 0, ',') +' usuarios';
                }
            },
            plotOptions: {
                area: {
                    stacking: 'normal',
                    lineColor: '#666666',
                    lineWidth: 1,
                    marker: {
                        lineWidth: 1,
                        lineColor: '#666666'
                    }
                }
            },
            series: [{
                name: 'Alumnos',
                data: [10, 57, 93, 158, 201, 262]
            }, {
                name: 'Profesores',
                data: [1, 7, 8, 11, 13, 15]
            }, {
                name: 'Gestion',
                data: [1, 1, 1, 2, 3, 2]
            }]
        });


    });
</script>
<div id="statistics_resume">
    <a href="#" onclick="$('#disk_space_chart').slideToggle('slow');return false;">
        <img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/common/list_entry.png" width="16" height="16" alt="list_entry" />
        <span>Espacio en disco</span>
    </a>
    <div id="disk_space_chart" class="statistic" style="display: none"></div>
    <a href="#" onclick="$('#users_groups_chart').slideToggle('slow');return false;">
        <img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/common/list_entry.png" width="16" height="16" alt="list_entry" />
        <span>Usuarios y grupos</span>
    </a>
    <div id="users_groups_chart" class="statistic" style="display: none"></div>
</div>