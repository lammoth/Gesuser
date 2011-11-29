<?php
include_once("../config.php");
?>

<ul>
	<li class="section_active">
		<a href="welcome" module="home">
			<img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/common/home_icon.png" width="16" height="16" alt="add_user" />
			<span>Inicio</span>
		</a>
	</li>
	<!--<li><a href="#"><img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/del_icon.png" alt="del_user" name="add" width="16" height="16"/><span>Baja de usuarios</span></a></li>
	<li><a href="#"><img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/edit_icon.png" alt="edit_users" name="add" width="16" height="16"/><span>Editar usuarios</span></a></li>-->
	<li>
		<a href="statistics" module="home">
			<img src="http://<?php echo SERVER_NAME.APP_DIR; ?>/img/common/stat_icon.png" width="16" height="16" alt="search_users" />
			<span>Estad&iacute;sticas</span>
		</a>
	</li>
</ul>