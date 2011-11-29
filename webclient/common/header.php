<!DOCTYPE HTML">
<html>
  <head>
    <title>G3</title>
	<meta name="description" content="" />
	<meta name="keywords" content="" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

    <?php
        //Loading all css files
        $css_obj = new CSS_load();
        $css_obj->load_all_css_files();
        
        //Loading all js files
        $javascript_obj = new Javascript_load();
        $javascript_obj->load_all_js_files();
    ?>
  </head>
  <body>