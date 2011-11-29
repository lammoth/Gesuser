<?php
	include_once("config.php");

	include '_index.php';
	$gesuser = new Gesuser();
	include APP_ROOT.'/common/header.php';
?>
<div id="content" class="wrap">
	<div id="header">
		<?php if($gesuser->auth) include APP_ROOT.'/common/menu.php';?>
	</div>
	<div id="page_content">
		<div class="left_center_container">
			<div id="left_section">
				<!-- submenú -->
			</div>
			<div id="center_section">
				<div id="header_center_section" class="head_center_section_login">
					<h2 id="section_tit">Bienvenido a g3suser</h2>
				</div>
				<div id="content_center_section">
					<div id="loading">
						<img alt="loading" src="<?php echo APP_DIR;?>/img/common/ajax-loader.gif" />
						<label id="loading-text"></label>
					</div>
					<div id="start">
						<?php
						if(!$gesuser->auth)
							include APP_ROOT.'/php/common/login_form.php';
						/*else
							include APP_ROOT.'/php/common/welcome.php';*/
						?>
					</div>
					<form method="POST" action="" id="main_frm"></form>
				</div>
			</div>
		</div>
		<div id="right_section" style="display: none">
        <!--<div id="right_section">-->
			<h3  ondblclick="$('.console').toggle();">Eventos</h3>
			<div class="events_separator wrap"></div>
			<ul id="events"></ul>
		</div>
		<div class="clear"></div>
	</div>
</div>

<a class="console" href="#" onclick="$('#console').html('')">clear</a>
<div id='console' class="console"></div>
<?php include APP_ROOT.'/common/bottom.php';