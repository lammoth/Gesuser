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
        <img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/list_entry.png" width="16" height="16" alt="list_entry" />
        <span>Espacio en disco</span>
    </a>
    <div id="disk_space_chart" class="statistic" style="display: none"></div>
    <a href="#" onclick="$('#users_groups_chart').slideToggle('slow');return false;">
        <img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/list_entry.png" width="16" height="16" alt="list_entry" />
        <span>Usuarios y grupos</span>
    </a>
    <div id="users_groups_chart" class="statistic" style="display: none"></div>
</div>
<!--<div class="form_section wrap">
	<h3>Buscar usuarios</h3>
	<p>Completa los datos referentes a la identificaci&oacute;n del usuario.</p>
	<table>
		<tr class="searching    ">
			<td class="left">
				<label for="Buscar">Buscar</label>
			</td>
			<td class="right">
				<input type="text" name="query" id="query" class="input value" />
			</td>
			<td class="left">
				<label for="Por" class="label_right">por</label>
			</td>
			<td class="right">
				<select name="search" id="search" class="name">
					<option value="gecos">Nombre</option>
					<option value="uid">Usuario</option>
				</select>
				<input type="hidden" value="eq" class="op" />
			</td>
		</tr>
		<tr>
			<td colspan="4">
				<a class="advanced_search" href="#" onclick="$('#advanced_search').toggle();return false;">B&uacute;squeda avanzada</a>
			</td>
		</tr>
	</table>
	<table id="advanced_search">
		<tr class="searching">
			<td class="left">
				<label for="quota_op">Cuota</label>
			</td>
			<td class="right">
				<select id="quota_op" name="quota_op" class="op">
					<option value="eq">Igual</option>
					<option value="gt">Mayor</option>
					<option value="ge">Mayor o igual</option>
					<option value="lt">Menor</option>
					<option value="le">Menor o igual</option>
				</select>
			</td>
			<td class="left">
				<label for="quota">que</label>
			</td>
			<td class="right">
				<input type="text" name="quota" class="input value" />
				<input type="hidden" class="name" value="quota" />
			</td>
		</tr>
		<tr class="searching">
			<td class="left">
				<label for="course_op">Curso</label>
			</td>
			<td class="right">
				<select id="course_op" name="course_op" class="op">
					<option value="eq">Igual</option>
					<option value="gt">Mayor</option>
					<option value="ge">Mayor o igual</option>
					<option value="lt">Menor</option>
					<option value="le">Menor o igual</option>
				</select>
			</td>
			<td class="left">
				<label for="course">que</label>
			</td>
			<td class="right">
				<input type="text" name="course" class="input value" />
				<input type="hidden" class="name" value="course" />
			</td>
		</tr>
		<tr class="searching">
			<td class="left">
				<label for="profile">Perfil</label>
			</td>
			<td class="right">
				<select name="profile" class="value">
					<option value="">Indiferente</option>
					<option value="1">Fijo</option>
					<option value="2">M&oacute;vil</option>
				</select>
				<input type="hidden" class="name" value="profile" />
				<input type="hidden" class="op" value="eq" />
			</td>
		</tr>
		<tr class="searching">
			<td class="left">
				<label for="group">Grupo</label>
			</td>
			<td class="right">
				<select name="group" class="value">
					<option value="">Indiferente</option>
					<option value="1">Alumno</option>
					<option value="2">Gesti&oacute;n</option>
					<option value="3">Profesor</option>
				</select>
				<input type="hidden" class="name" value="group" />
				<input type="hidden" class="op" value="eq" />
			</td>
		</tr>
	</table>
	<a class="note reset" href="#" onclick="$(GUI.main_frm).reset();return false;">resetear</a>
	<input type="button" onclick="Common.search_users();" value="Buscar" class="btn"/>
</div>

<div class="clear"></div>
<div class="form_line"></div>

<div id="search_results">
	<table id="users">
		<tr>
			<th>Usuario</th>
			<th>Nombre</th>
			<th>Grupo</th>
			<th>Perfil</th>
			<th>Cuota</th>
			<th>Curso</th>
			<th>Acciones</th>
		</tr>
	</table>
</div>
<div class="form_line"></div>-->