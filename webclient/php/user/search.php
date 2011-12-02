<?php
include_once("../config.php");
?>
<div class="form_section wrap">
	<h3>Buscar usuarios</h3>
	<p class="description">Completa los datos referentes a la identificaci&oacute;n del usuario.</p>
	<table>
		<tr class="searching">
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
				<a class="advanced_search" href="#" onclick="$('#advanced_search').slideToggle('fast');return false;">B&uacute;squeda avanzada</a>
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
		<!-- <tr class="searching">
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
		</tr> -->
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
        <tr><td></td></tr>
        <tr>
			<td colspan="4">
                <a class="order_search">Ordenar</a>
			</td>
		</tr>
        <tr><td></td></tr>
        <tr class="searching">
			<td class="left">
				<label for="group">Ordenar por</label>
			</td>
			<td class="right">
				<select name="order" class="value">
					<option value="">Indiferente</option>
					<option value="gecos">Nombre</option>
					<option value="quota">Cuota</option>
					<option value="course">Curso</option>
                    <option value="profile">Perfil</option>
                    <option value="group">Grupo</option>
				</select>
				<input type="hidden" class="name" value="order" />
				<input type="hidden" class="op" value="eq" />
			</td>
		</tr>
    </table>
	<!--<a class="note reset" href="#" onclick="$(GUI.main_frm).reset();return false;">resetear</a>-->
</div>
<div class="form_section wrap">
    <input type="button" onclick="UserOperations.search_users();" value="Buscar" class="btn"/>
</div>

<div class="clear"></div>
<div class="form_line"></div>

<div id="search_results">
	<table id="user_search_list">
        <thead>
            <tr>
                <th><input type="checkbox" id="check_all" name="check_all" class="el_sel" onclick="UserOperations.check_all_items();" disabled /></th>
                <th>Usuario</th>
                <th>Nombre</th>
                <th>Grupo</th>
                <th>Perfil</th>
                <th>Cuota</th>
                <th>Curso</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody></tbody>
	</table>
</div>
<div id="remove_selected_items" style="display:none">
    <table>
        <tr>
            <td>
                <a href="#remove_selected_items" class="check_all" onclick="UserOperations.remove_check_items();"><span>Eliminar selecci&oacute;n</span></a>
            </td>
            <td>
                <img alt="loading" src="<?php echo APP_DIR;?>/img/common/ajax-loader.gif" style="display: none;"/>
            </td>
        </tr>
    </table>
</div>
<div id="del_dialog"></div>
<div id="edit_dialog"></div>