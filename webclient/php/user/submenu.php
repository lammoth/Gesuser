<?php
include_once("../config.php");
?>

<ul>
	<li class="section_active">
		<a href="create" module="user">
			<img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/common/add_icon.png" width="16" height="16" alt="add_user" />
			<span>Alta de usuarios</span>
		</a>
	</li>
	<!--<li><a href="#"><img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/del_icon.png" alt="del_user" name="add" width="16" height="16"/><span>Baja de usuarios</span></a></li>
	<li><a href="#"><img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/edit_icon.png" alt="edit_users" name="add" width="16" height="16"/><span>Editar usuarios</span></a></li>-->
	<li>
		<a href="search" module="user">
			<img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/common/search_icon.png" width="16" height="16" alt="search_users" />
			<span>B&uacute;squeda de usuarios</span>
		</a>
	</li>
</ul>