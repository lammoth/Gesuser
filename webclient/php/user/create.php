<?php
include_once("../config.php");
?>
<div class="form_section wrap">
	<h3>Datos del usuario</h3>
	<p class="description">Completa los datos referentes a la identificaci&oacute;n del usuario. Todos los datos de esta secci&oacute;n son obligatorios</p>
	<table>
		<tr>
			<td class="left">
				<label for="uid">Nombre de usuario</label>
			</td>
			<td class="right">
				<input type="text" id="uid" name="uid" class="input" required="required" filtered="filtered" />
				<!--<span class="error"></span>-->
			</td>
            <td class="form_error">
                <span class="error"></span>
            </td>
		</tr>
		<tr>
			<td class="left">
				<label for="pwd">Contrase&ntilde;a</label>
			</td>
			<td class="right">
				<input type="password" id="pwd" name="pwd" class="input" required="required" filtered="filtered" />
                <!--<span class="error"></span>-->
			</td>
            <td class="form_error">
                <span class="error"></span>
            </td>
		</tr>
		<tr>
			<td class="left">
				<label for="pwd2">Repite la contrase&ntilde;a</label>
			</td>
			<td class="right">
				<input type="password" id="pwd2" name="pwd2" class="input" required="required" />
				<!--<span class="error"></span>-->
			</td>
            <td class="form_error">
                <span class="error"></span>
            </td>
		</tr>
		<tr>
			<td class="left">
				<label for="gecos">Nombre completo</label>
			</td>
			<td class="right">
				<input type="text" id="gecos" name="gecos" class="input" required="required" />
				<!--<span class="error"></span>-->
			</td>
            <td class="form_error">
                <span class="error"></span>
            </td>
		</tr>
	</table>
</div>
<div class="form_section wrap">
	<h3>Propiedades de la cuenta</h3>
	<p class="description">Completa los datos referentes a las propiedades de la cuenta del usuario.</p>
	<table>
		<tr>
			<td class="left">
				<label for="quota">Cuota</label>
			</td>
			<td class="right">
				<input type="text" id="quota" name="quota" class="input" required="required" integer="integer" />
				<img alt="Cuota" title="Espacio para el usuario en MB" src="http://<?php echo SERVER_NAME.APP_DIR;?>/img/common/info_icon.png" width="16" height="16" class="user_img_quota"/>
			</td>
            <td class="form_error">
                <span class="error"></span>
            </td>
		</tr>
		<tr>
			<td class="left">
				<label for="course">Curso</label>
			</td>
			<td class="right">
				<input type="text" id="course" name="course" class="input" required="required" lessfiltered="lessfiltered" />
				<img alt="Curso" title="Curso del usuario" src="http://<?php echo SERVER_NAME.APP_DIR;?>/img/common/info_icon.png" width="16" height="16" class="user_img_course"/>
				<!--<span class="error"></span>-->
			</td>
            <td class="form_error">
                <span class="error"></span>
            </td>
		</tr>
		<tr>
			<td class="left">
				<label for="profile">Perfil</label>
			</td>
			<td class="right">
				<select id="profile" name="profile">
					<option value="1">Fijo</option>
					<option value="2">M&oacute;vil</option>
				</select>
                <img alt="Perfil" title="Tipo de perfil" src="http://<?php echo SERVER_NAME.APP_DIR;?>/img/common/info_icon.png" width="16" height="16" class="user_img_profile"/>
				<!--<span class="error"></span>-->
			</td>
            <td class="form_error">
                <span class="error"></span>
            </td>
		</tr>
		<tr>
			<td class="left">
				<label for="group">Grupo</label>
			</td>
			<td class="right">
				<select id=group" name="group">
					<option value="1">Alumno</option>
					<option value="2">Gesti&oacute;n</option>
					<option value="3">Profesor</option>
				</select>				
				<!--<span class="error"></span>-->
			</td>
            <td class="form_error">
                <span class="error"></span>
            </td>
		</tr>
	</table>
	<!--<a class="note reset" href="#" onclick="$(GUI.main_frm).reset();return false;">resetear</a>-->
</div>
<a class="user_batch_add" href="#" onclick="$('#user_batch').slideToggle('fast');return false;">Alta masiva de usuarios</a>
<div id="user_batch" style="display: none">
    <div class="user_form_section_batch">
        <h3>Alta masiva de usuarios</h3>
        <p class="description">
            Para realizar altas masivas de usuarios se debe crear un fichero con la siguiente estructura d&oacute;nde cada usuario es una nueva l&iacute;nea:<br /><br />
            <span class="example">nombredeusuario;nombre apellidos;grupo;perfil;curso;cuota<br/><br></span>
            <span class="information"><strong>"grupo"</strong> => <strong>a</strong>: Alumnos, <strong>p</strong>: Profesores, <strong>g</strong>: Gesti&oacute;n. S&oacute;lo debe ponerse una.<br></span>
            <span class="information"><strong>"perfil"</strong> => <strong>1</strong>: Fijo, <strong>2</strong>: M&oacute;vil. S&oacute;lo debe ponerse una de las dos.<br></span>
            <!-- <span class="information"><strong>"curso"</strong> => Debe ir indicado por un campo num&eacute;rico.<br></span> -->
            <span class="information"><strong>"cuota"</strong> => El espacio se debe indicar en <strong>megas</strong>, por ejemplo, 250.<br></span>
        </p>
        <table>
            <tr>
                <td class="left">
                    <label for="user_file_uploader">Fichero</label>
                </td>
                <td class="right">
                    <!--<input type="file" id="fileupload" name="fileupload" />-->
                    <div id="user_file_uploader">
                        <noscript>
                            <p>Please enable JavaScript to use file uploader.</p>
                            <!-- or put a simple form for upload here -->
                        </noscript>
                    </div>
                </td>
                <td class="form_error">
                    <span class="error">
                        <a href="#" id="user_delete_file" class="user_delete_file" style="display:none;" onclick="UserOperations.restablish_user_fileupload();">
                            <img alt="Eliminar" title="Eliminar archivo" src="http://<?php echo SERVER_NAME.APP_DIR;?>/img/common/delete_icon.png" width="16" height="16" />
                        </a>
                    </span>
                </td>
            </tr>
        </table>
        <div id="user_batch_log" style="display:none">
            <p class="user_batch_new">Usuarios creados&nbsp;&nbsp;&nbsp;&nbsp;<span id="user_batch_no_add"></span><a href="#" onclick="$('#user_batch_new_names').slideToggle('fast');return false;">Ver historial</a></p>
            <div id="user_batch_new_names" style="display:none;"></div>
            <p class="user_batch_del">Errores&nbsp;&nbsp;&nbsp;&nbsp;<span id="user_batch_no_error"></span><a href="#" onclick="$('#user_batch_error_names').slideToggle('fast');return false;">Ver historial</a></p>
            <div id="user_batch_error_names" style="display:none;"></div>
        </div>
    </div>
</div>
<div class="form_line wrap"></div>
<div class="form_section wrap">
    <input type="button" onclick="UserOperations.create_user();" value="Crear usuario/s" class="btn" />
</div>